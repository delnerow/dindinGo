// Add after your existing imports
import { ChevronLeft, ChevronRight } from 'lucide-react';
import { useState, useEffect } from 'react';
import { Plus, Wallet, Pencil, Trash2, Filter } from 'lucide-react';
import Sidebar from "../components/ui/sidebar";
import { Transaction, NewTransaction } from '../types/Transaction';
import { EditTransactionModal } from '../components/EditTransactionModal';
import { getCategoryIcon } from '../utils/categoryIcons';

// Add these helper functions after your existing constants
const getNextMonth = (currentMonth: string): string => {
  const [year, month] = currentMonth.split('-').map(Number);
  if (month === 12) {
    return `${year + 1}-01`;
  }
  return `${year}-${String(month + 1).padStart(2, '0')}`;
};

const getPreviousMonth = (currentMonth: string): string => {
  const [year, month] = currentMonth.split('-').map(Number);
  if (month === 1) {
    return `${year - 1}-12`;
  }
  return `${year}-${String(month - 1).padStart(2, '0')}`;
};

interface Carteira {
  nome: string;
  descricao: string;
  saldo: number;
}

// Helper function to format dates
const formatDate = (dateString: string): string => {
  const date = new Date(dateString);
  return date.toLocaleDateString('pt-BR');
};

const formatMonthYear = (monthYear: string): string => {
  const [year, month] = monthYear.split('-');
  const date = new Date(Number(year), Number(month) - 1);
  return date.toLocaleDateString('pt-BR', { month: 'long', year: 'numeric' });
};

export default function Transacoes() {
  const [carteiras, setCarteiras] = useState<Carteira[]>([]);
  const [isNewTransactionOpen, setIsNewTransactionOpen] = useState(false);
  const [mesSelecionado, setMesSelecionado] = useState("2025-06");
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [editingTransaction, setEditingTransaction] = useState<Transaction | null>(null);
  const [categorias, setCategorias] = useState<string[]>([]);
  const [categoriaFiltro, setCategoriaFiltro] = useState<string>("");
  const [carteiraFiltro, setCarteiraFiltro] = useState<string>("");

  // Função para limpar todos os filtros
  const limparFiltros = () => {
    setCategoriaFiltro("");
    setCarteiraFiltro("");
  };

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

  // Add function to fetch categorias
  const fetchCategorias = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/categorias');
      if (!response.ok) throw new Error('Failed to fetch categorias');
      const data = await response.json();
      setCategorias(data);
    } catch (err) {
      console.error('Error fetching categorias:', err);
    }
  };

  useEffect(() => {
    fetchTransactions();
    fetchCarteiras();
    fetchCategorias();
  }, []);

  const handleEditTransaction = async (transaction: Transaction | NewTransaction) => {
  try {
    if ('id' in transaction) {
      console.log('Updating transaction:', transaction); // Debug log
      const response = await fetch(`http://localhost:5000/api/transactions/${transaction.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ...transaction,
          feita: Boolean(transaction.feita) // Ensure boolean value
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to update transaction');
      }

      // Refresh transactions to get updated data
      await fetchTransactions();
      setEditingTransaction(null);
    }
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
    const filtroMes = mesAno === mesSelecionado;
    
    // Filtro por categoria
    const filtroCategoria = categoriaFiltro === "" || t.categoria === categoriaFiltro;
    
    // Filtro por carteira
    const filtroCarteira = carteiraFiltro === "" || t.carteira === carteiraFiltro;
    
    return filtroMes && filtroCategoria && filtroCarteira;
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
          <div className="flex items-center space-x-4">
  <button
    onClick={() => setMesSelecionado(getPreviousMonth(mesSelecionado))}
    className="p-2 hover:bg-gray-200 rounded-full transition-colors"
    title="Mês anterior"
  >
    <ChevronLeft className="w-5 h-5" />
  </button>
  
  <span className="text-xl font-bold">
    {formatMonthYear(mesSelecionado)}
  </span>
  
  <button
    onClick={() => setMesSelecionado(getNextMonth(mesSelecionado))}
    className="p-2 hover:bg-gray-200 rounded-full transition-colors"
    title="Próximo mês"
  >
    <ChevronRight className="w-5 h-5" />
  </button>
</div>
        </div>

        <div className="flex items-center space-x-4">
          {/* Filtro por categoria */}
          <div className="flex items-center space-x-2 bg-gray-50 px-3 py-2 rounded-lg border">
            <Filter className="w-4 h-4 text-gray-500" />
            <span className="text-sm text-gray-600">Categoria:</span>
            <select
              value={categoriaFiltro}
              onChange={(e) => setCategoriaFiltro(e.target.value)}
              className="px-3 py-1 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
            >
              <option value="">Todas as categorias</option>
              {categorias.map((categoria) => (
                <option key={categoria} value={categoria}>
                  {categoria.charAt(0).toUpperCase() + categoria.slice(1)}
                </option>
              ))}
            </select>
          </div>

          {/* Filtro por carteira */}
          <div className="flex items-center space-x-2 bg-gray-50 px-3 py-2 rounded-lg border">
            <Wallet className="w-4 h-4 text-gray-500" />
            <span className="text-sm text-gray-600">Carteira:</span>
            <select
              value={carteiraFiltro}
              onChange={(e) => setCarteiraFiltro(e.target.value)}
              className="px-3 py-1 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
            >
              <option value="">Todas as carteiras</option>
              {carteiras.map((carteira) => (
                <option key={carteira.nome} value={carteira.nome}>
                  {carteira.nome}
                </option>
              ))}
            </select>
          </div>

          {/* Botão para limpar filtros */}
          {(categoriaFiltro || carteiraFiltro) && (
            <button
              onClick={limparFiltros}
              className="flex items-center space-x-2 px-3 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors text-sm"
              title="Limpar todos os filtros"
            >
              <span>Limpar Filtros</span>
            </button>
          )}

          <button
            onClick={() => setIsNewTransactionOpen(true)}
            className="flex items-center space-x-2 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
          >
            <Plus className="w-5 h-5" />
            <span>Nova Transação</span>
          </button>
        </div>
      </div>

      <div className="flex justify-between items-center mb-4">
        <div className="flex items-center space-x-4">
          <span>Transações: {transacoesFiltradas.length}</span>
          <div className="flex items-center space-x-2">
            <span className="text-sm text-gray-600">|</span>
            <span className="text-sm text-gray-600">
              {categoriaFiltro ? `Categoria: ${categoriaFiltro.charAt(0).toUpperCase() + categoriaFiltro.slice(1)}` : 'Sem filtro de categoria'}
            </span>
            {(categoriaFiltro || carteiraFiltro) && (
              <>
                <span className="text-sm text-gray-600">|</span>
                <span className="text-sm text-gray-600">
                  {carteiraFiltro ? `Carteira: ${carteiraFiltro}` : 'Sem filtro de carteira'}
                </span>
              </>
            )}
          </div>
        </div>
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
        <div className="flex items-center space-x-2">
          <span className="text-sm text-gray-500">
            {transaction.categoria}
          </span>
          <span className="text-sm text-gray-400">•</span>
          <span className="text-sm font-medium text-blue-600">
            {transaction.carteira}
          </span>
        </div>
        {transaction.desc && (
              <div className="text-sm text-gray-400 mt-1 italic">
                {transaction.desc}
              </div>
            )}
            {transaction.repeticao > 0 && (
          <div className="flex items-center mt-1 space-x-2">
            <span className="text-xs text-gray-500">
              Recorrente ({transaction.repeticao}x)
            </span>
            <span className={`text-xs px-2 py-0.5 rounded-full ${
              transaction.feita 
                ? 'bg-green-100 text-green-800'
                : 'bg-yellow-100 text-yellow-800'
            }`}>
              {transaction.feita ? 'Feito' : 'Pendente'}
            </span>
          </div>
        )}
 

                  </div>
                </div>
                <div className="text-right">
                  <p
                    className={`font-semibold ${
                      transaction.receita ? 'text-green-500' : 'text-red-500'
                    }`}
                  >
                    R$ {Math.abs(Number(transaction.valor)).toFixed(2)}
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
          carteiras={carteiras}  // Add carteiras prop
        />
      )}

      {/* New Transaction Modal */}
      {isNewTransactionOpen && (
        <EditTransactionModal
          transaction={null}
          isOpen={isNewTransactionOpen}
          onClose={() => setIsNewTransactionOpen(false)}
          onSave={handleAddTransaction}
          carteiras={carteiras}  // Add carteiras prop
        />
      )}
    </div>
  </div>
);
}