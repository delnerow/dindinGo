import { useState, useEffect } from 'react';
import { Plus, Wallet, Pencil, Trash2 } from 'lucide-react';
import Sidebar from "../components/ui/sidebar";
import { Transaction, NewTransaction } from '../types/Transaction';
import { EditTransactionModal } from '../components/EditTransactionModal';
import { getCategoryIcon } from '../utils/categoryIcons';


interface Carteira {
  nome: string;
  descricao: string;
  saldo: number;
}

const meses = [
  { label: "Maio de 2025", value: "2025-05" },
  { label: "Junho de 2025", value: "2025-06" },
];

// Helper function to format dates
const formatDate = (dateString: string): string => {
  const date = new Date(dateString);
  return date.toLocaleDateString('pt-BR');
};

export default function Transacoes() {
  const [carteiras, setCarteiras] = useState<Carteira[]>([]);
  const [isNewTransactionOpen, setIsNewTransactionOpen] = useState(false);
  const [mesSelecionado, setMesSelecionado] = useState("2025-06");
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [editingTransaction, setEditingTransaction] = useState<Transaction | null>(null);

  const fetchTransactions = async () => {
    try {
      setIsLoading(true);
      const response = await fetch('http://localhost:5000/api/transactions');
      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
      const data = await response.json();
      setTransactions(data);
    } catch (err) {
      console.error('Fetch error:', err);
      setError(err instanceof Error ? err.message : 'Failed to load transactions');
    } finally {
      setIsLoading(false);
    }
  };
 // Add function to fetch carteiras
  const fetchCarteiras = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/carteiras');
      if (!response.ok) throw new Error('Failed to fetch carteiras');
      const data = await response.json();
      setCarteiras(data);
    } catch (err) {
      console.error('Error fetching carteiras:', err);
    }
  };

  useEffect(() => {
    fetchTransactions();
    fetchCarteiras();
  }, []);

  const handleEditTransaction = async (transaction: Transaction | NewTransaction) => {
  try {
    // Type guard to check if this is an existing transaction
    if ('id' in transaction) {
      const response = await fetch(`http://localhost:5000/api/transactions/${transaction.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(transaction),
      });

      if (!response.ok) throw new Error('Failed to update transaction');

      setTransactions(transactions.map(t => 
        t.id === transaction.id ? transaction : t
      ));
    }
    setEditingTransaction(null);
  } catch (err) {
    console.error('Update error:', err);
    alert('Failed to update transaction');
  }
};

const handleAddTransaction = async (newTransaction: Omit<Transaction, 'id'>) => {
  try {
    const response = await fetch('http://localhost:5000/api/transactions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(newTransaction),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || 'Failed to create transaction');
    }

    await fetchTransactions();
    setIsNewTransactionOpen(false);
  } catch (err) {
    console.error('Create error:', err);
    alert(err instanceof Error ? err.message : 'Failed to create transaction');
  }
};

  const handleDeleteTransaction = async (transactionId: number) => {
    // Replace window.confirm with a safer check
    const userConfirmed = window.confirm('Tem certeza que deseja excluir esta transação?');
    if (!userConfirmed) {
      return;
    }

    try {
      const response = await fetch(
        `http://localhost:5000/api/transactions/${transactionId}`,
        {
          method: 'DELETE',
        }
      );

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to delete transaction');
      }

      // Refresh transactions after deletion
      await fetchTransactions();
      
    } catch (err) {
      console.error('Delete error:', err);
      alert(err instanceof Error ? err.message : 'Failed to delete transaction');
    }
  };

  if (isLoading) return <div>Carregando...</div>;
  if (error) return <div>Erro: {error}</div>;

  const transacoesFiltradas = transactions.filter((t) => {
    const data = new Date(t.data);
    const mesAno = `${data.getFullYear()}-${String(data.getMonth() + 1).padStart(2, "0")}`;
    return mesAno === mesSelecionado;
  });






  
  const total = transacoesFiltradas.reduce((acc, t) => acc + t.valor*(t.receita? 1:-1), 0);

  return (
  <div className="flex h-screen overflow-hidden bg-gray-100">
    {/* Sidebar */}
    <div className="w-64 bg-white border-r shadow-lg">
      <Sidebar />
    </div>

    {/* Main content */}
    <div className="flex-1 p-6 overflow-y-auto">
      <div className="flex justify-between items-center mb-4">
        <div className="flex items-center space-x-2">
          <select
            className="text-xl font-bold bg-transparent"
            value={mesSelecionado}
            onChange={(e) => setMesSelecionado(e.target.value)}
          >
            {meses.map((m) => (
              <option key={m.value} value={m.value}>
                {m.label}
              </option>
            ))}
          </select>
        </div>

        <button
          onClick={() => setIsNewTransactionOpen(true)}
          className="flex items-center space-x-2 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
        >
          <Plus className="w-5 h-5" />
          <span>Nova Transação</span>
        </button>
      </div>

      <div className="flex justify-between items-center mb-4">
        <span>Transações: {transacoesFiltradas.length}</span>
        <span
          className={`font-semibold ${
            total >= 0 ? 'text-green-500' : 'text-red-500'
          }`}
        >
          Total: R$ {total.toFixed(2)}
        </span>
      </div>

      <div className="space-y-4">
        {transacoesFiltradas.map((transaction) => {
          const CategoryIcon = getCategoryIcon(transaction.categoria);

          return (
            <div key={transaction.id} className="bg-white rounded-lg shadow p-4">
              <div className="flex justify-between items-start mb-2">
                <div className="flex items-start space-x-3">
                  <div className="flex flex-col items-center space-y-2">
                    <Wallet
                      className={`w-5 h-5 ${
                        transaction.receita ? 'text-green-500' : 'text-red-500'
                      }`}
                    />
                    <CategoryIcon className="w-5 h-5 text-gray-500" />
                  </div>
                  <div>
                    <div className="font-medium">{transaction.nome}</div>
                    <div className="text-sm text-gray-500">
                      {transaction.categoria}
                    </div>
                  </div>
                </div>
                <div className="text-right">
                  <p
                    className={`font-semibold ${
                      transaction.receita ? 'text-green-500' : 'text-red-500'
                    }`}
                  >
                    R$ {Math.abs(transaction.valor).toFixed(2)}
                  </p>
                  <p className="text-sm text-gray-500">
                    {formatDate(transaction.data)}
                  </p>
                </div>
              </div>
              <div className="flex justify-end space-x-2">
                <button
                  onClick={() => setEditingTransaction(transaction)}
                  className="p-2 hover:bg-gray-100 rounded-full"
                  title="Editar"
                >
                  <Pencil className="w-4 h-4 text-gray-500" />
                </button>
                <button
                  onClick={() => handleDeleteTransaction(transaction.id)}
                  className="p-2 hover:bg-gray-100 hover:text-red-500 rounded-full"
                  title="Excluir"
                >
                  <Trash2 className="w-4 h-4 text-gray-500 hover:text-red-500" />
                </button>
              </div>
            </div>
          );
        })}
      </div>

      {/* Edit Transaction Modal */}
      {editingTransaction && (
        <EditTransactionModal
          transaction={editingTransaction}
          isOpen={!!editingTransaction}
          onClose={() => setEditingTransaction(null)}
          onSave={handleEditTransaction}
        />
      )}

      {/* New Transaction Modal */}
      {isNewTransactionOpen && (
        <EditTransactionModal
          transaction={null}
          isOpen={isNewTransactionOpen}
          onClose={() => setIsNewTransactionOpen(false)}
          onSave={handleAddTransaction}  // Use the handleAddTransaction function
        />
      )}
    </div>
  </div>
);
}