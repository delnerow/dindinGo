import { useState, useEffect } from 'react';
import { Wallet, Pencil } from 'lucide-react';
import Sidebar from "../components/ui/sidebar";
import { Transaction } from '../types/Transaction';
import { EditTransactionModal } from '../components/EditTransactionModal';
import { getCategoryIcon } from '../utils/categoryIcons';

const meses = [
  { label: "Maio de 2025", value: "2025-05" },
  { label: "Junho de 2025", value: "2025-06" },
];

// Helper function to format dates
const formatDate = (dateString: string): string => {
  return new Date(dateString).toLocaleDateString('pt-BR');
};

export default function Transacoes() {
  const [mesSelecionado, setMesSelecionado] = useState("2025-06");
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [editingTransaction, setEditingTransaction] = useState<Transaction | null>(null);

  useEffect(() => {
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

    fetchTransactions();
  }, []);

  const handleEditTransaction = async (updatedTransaction: Transaction) => {
    try {
      const response = await fetch(`http://localhost:5000/api/transactions/${updatedTransaction.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(updatedTransaction),
      });

      if (!response.ok) throw new Error('Failed to update transaction');

      setTransactions(transactions.map(t => 
        t.id === updatedTransaction.id ? updatedTransaction : t
      ));
      setEditingTransaction(null);
    } catch (err) {
      console.error('Update error:', err);
      alert('Failed to update transaction');
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

      {/* Conteúdo principal */}
      <div className="flex-1 p-6 overflow-y-auto">
        <div className="flex justify-between items-center mb-4">
          <span>Transações: {transacoesFiltradas.length}</span>
          <span className={`font-semibold ${total >= 0 ? 'text-green-500' : 'text-red-500'}`}>
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
                      <Wallet className={`w-5 h-5 ${transaction.receita  ? 'text-green-500' : 'text-red-500'}`} />
                      <CategoryIcon className="w-5 h-5 text-gray-500" />
                    </div>
                    <div>
                      <div className="font-medium">{transaction.nome}</div>
                      <div className="text-sm text-gray-500">{transaction.categoria}</div>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className={`font-semibold ${transaction.receita ? 'text-green-500' : 'text-red-500'}`}>
                      R$ {Math.abs(transaction.valor).toFixed(2)}
                    </p>
                    <p className="text-sm text-gray-500">
                      {formatDate(transaction.data)}
                    </p>
                  </div>
                </div>
                <div className="flex justify-end">
                  <button
                    onClick={() => setEditingTransaction(transaction)}
                    className="p-2 hover:bg-gray-100 rounded-full"
                  >
                    <Pencil className="w-4 h-4 text-gray-500" />
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
      </div>
    </div>
  );
}