// Add after your existing imports
import { ChevronLeft, ChevronRight } from 'lucide-react';
import { useState, useEffect } from 'react';
import { Plus, Wallet, Pencil, Trash2, Filter, Settings } from 'lucide-react';
import Sidebar from "../components/ui/sidebar";
import { Transaction, NewTransaction } from '../types/Transaction';
import { EditTransactionModal } from '../components/EditTransactionModal';
import { getCategoryIcon } from '../utils/categoryIcons';
import { useTheme } from '../App';

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

export default function Transacoes({ settingsOnClick }: { settingsOnClick?: () => void }) {
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
  const [monthlyTotals, setMonthlyTotals] = useState<{receitas: number, despesas: number, saldo: number}>({
    receitas: 0,
    despesas: 0,
    saldo: 0
  });

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

  const fetchMonthlyTotals = async () => {
    try {
      const response = await fetch(`http://localhost:5000/api/transactions/monthly-totals/${mesSelecionado}`);
      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
      const data = await response.json();
      setMonthlyTotals(data);
    } catch (err) {
      console.error('Error fetching monthly totals:', err);
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

  useEffect(() => {
    fetchMonthlyTotals();
  }, [mesSelecionado]);

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

  return (
  <div className="flex h-screen overflow-hidden bg-gray-100">
    {/* Sidebar */}
    <div className="w-64 bg-white border-r shadow-lg">
      <Sidebar settingsOnClick={settingsOnClick} />
    </div>

    {/* Main content */}
    <div className="flex-1 p-6 overflow-y-auto">
      {/* Top Bar with Month and Add Button */}
      <div className="flex justify-between items-center mb-4">
        <div className="flex-1" /> {/* Spacer */}
        <div className="flex items-center space-x-4 bg-white p-2 rounded-lg shadow-sm">
          <button
            onClick={() => setMesSelecionado(getPreviousMonth(mesSelecionado))}
            className="p-2 hover:bg-gray-100 rounded-full transition-colors"
            title="Mês anterior"
          >
            <ChevronLeft className="w-5 h-5" />
          </button>
          
          <span className="text-xl font-bold min-w-[200px] text-center">
            {formatMonthYear(mesSelecionado)}
          </span>
          
          <button
            onClick={() => setMesSelecionado(getNextMonth(mesSelecionado))}
            className="p-2 hover:bg-gray-100 rounded-full transition-colors"
            title="Próximo mês"
          >
            <ChevronRight className="w-5 h-5" />
          </button>
        </div>
        <div className="flex-1 flex justify-end"> {/* Spacer with button */}
          <button
            onClick={() => setIsNewTransactionOpen(true)}
            className="flex items-center space-x-2 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors shadow-md font-medium"
            title="Nova Transação"
          >
            <Plus className="w-5 h-5" />
            <span>Nova Transação</span>
          </button>
        </div>
      </div>

      {/* Filters and Summary */}
      <div className="grid grid-cols-3 gap-4 mb-4">
        {/* Category Filter */}
        <div className="flex items-center space-x-2 bg-white px-3 py-2 rounded-lg border shadow-sm">
          <Filter className="w-4 h-4 text-gray-500" />
          <span className="text-sm text-gray-600">Categoria:</span>
          <select
            value={categoriaFiltro}
            onChange={(e) => setCategoriaFiltro(e.target.value)}
            className="flex-1 px-2 py-1 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
          >
            <option value="">Todas as categorias</option>
            {categorias.map((categoria) => (
              <option key={categoria} value={categoria}>
                {categoria.charAt(0).toUpperCase() + categoria.slice(1)}
              </option>
            ))}
          </select>
        </div>

        {/* Wallet Filter */}
        <div className="flex items-center space-x-2 bg-white px-3 py-2 rounded-lg border shadow-sm">
          <Wallet className="w-4 h-4 text-gray-500" />
          <span className="text-sm text-gray-600">Carteira:</span>
          <select
            value={carteiraFiltro}
            onChange={(e) => setCarteiraFiltro(e.target.value)}
            className="flex-1 px-2 py-1 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
          >
            <option value="">Todas as carteiras</option>
            {carteiras.map((carteira) => (
              <option key={carteira.nome} value={carteira.nome}>
                {carteira.nome}
              </option>
            ))}
          </select>
        </div>

        {/* Summary */}
        <div className="bg-white p-3 rounded-lg shadow-sm">
          <div className="grid grid-cols-3 gap-2 text-sm">
            <div className="text-center">
              <div className="text-gray-500 text-xs">Receitas</div>
              <div className="text-accent-green">R$ {monthlyTotals.receitas.toFixed(2)}</div>
            </div>
            <div className="text-center">
              <div className="text-gray-500 text-xs">Despesas</div>
              <div className="text-accent-red">R$ {monthlyTotals.despesas.toFixed(2)}</div>
            </div>
            <div className="text-center border-l border-gray-200">
              <div className="text-gray-600 font-medium">Saldo</div>
              <div className={`text-lg font-bold ${monthlyTotals.saldo >= 0 ? 'text-accent-green' : 'text-accent-red'}`}>
                R$ {monthlyTotals.saldo.toFixed(2)}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Transaction Count and Active Filters */}
      <div className="flex items-center space-x-2 mb-4 text-sm text-gray-600">
        <span>Transações: {transacoesFiltradas.length}</span>
        {(categoriaFiltro || carteiraFiltro) && (
          <>
            <span>|</span>
            {categoriaFiltro && (
              <span>Categoria: {categoriaFiltro.charAt(0).toUpperCase() + categoriaFiltro.slice(1)}</span>
            )}
            {carteiraFiltro && (
              <>
                <span>|</span>
                <span>Carteira: {carteiraFiltro}</span>
              </>
            )}
            <button
              onClick={limparFiltros}
              className="ml-2 text-blue-500 hover:text-blue-600"
            >
              Limpar Filtros
            </button>
          </>
        )}
      </div>

      {/* Transaction List */}
      <div className="space-y-2">
        {transacoesFiltradas.map((transaction) => {
          const CategoryIcon = getCategoryIcon(transaction.categoria);

          return (
            <div key={transaction.id} className="bg-white rounded-lg shadow-sm p-3">
              <div className="flex justify-between items-center">
                <div className="flex items-center space-x-3">
                  <div className="flex items-center space-x-2">
                    <Wallet
                      className={`w-4 h-4 ${
                        transaction.receita ? 'text-accent-green' : 'text-accent-red'
                      }`}
                    />
                    <CategoryIcon className="w-4 h-4 text-gray-500" />
                  </div>
                  <div>
                    <div className="font-medium text-sm">{transaction.nome}</div>
                    <div className="flex items-center space-x-2 text-xs text-gray-500">
                      <span>{transaction.categoria}</span>
                      <span>•</span>
                      <span className="text-blue-600">{transaction.carteira}</span>
                      <span>•</span>
                      <span>{formatDate(transaction.data)}</span>
                    </div>
                  </div>
                </div>
                <div className="flex items-center space-x-3">
                  <p
                    className={`font-semibold text-sm ${
                      transaction.receita ? 'text-accent-green' : 'text-accent-red'
                    }`}
                  >
                    R$ {Math.abs(Number(transaction.valor)).toFixed(2)}
                  </p>
                  <div className="flex space-x-1">
                    <button
                      onClick={() => setEditingTransaction(transaction)}
                      className="p-1 hover:bg-gray-100 rounded-full"
                      title="Editar"
                    >
                      <Pencil className="w-4 h-4 text-gray-500" />
                    </button>
                    <button
                      onClick={() => handleDeleteTransaction(transaction.id)}
                      className="p-1 hover:bg-gray-100 hover:text-red-500 rounded-full"
                      title="Excluir"
                    >
                      <Trash2 className="w-4 h-4 text-gray-500 hover:text-red-500" />
                    </button>
                  </div>
                </div>
              </div>
              {(transaction.desc || transaction.repeticao > 0) && (
                <div className="mt-2 pl-7 text-xs text-gray-500">
                  {transaction.desc && (
                    <div className="italic">{transaction.desc}</div>
                  )}
                  {transaction.repeticao > 0 && (
                    <div className="flex items-center space-x-2 mt-1">
                      <span>Recorrente ({transaction.repeticao}x)</span>
                      <span className={`px-2 py-0.5 rounded-full ${
                        transaction.feita 
                          ? 'bg-green-100 text-green-800'
                          : 'bg-yellow-100 text-yellow-800'
                      }`}>
                        {transaction.feita ? 'Feito' : 'Pendente'}
                      </span>
                    </div>
                  )}
                </div>
              )}
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

// Export SettingsModal for use in App.tsx
export function SettingsModal({ onClose }: { onClose: () => void }) {
  const { theme, setTheme } = useTheme();
  const themeOptions = [
    { name: 'Light', value: 'light' },
    { name: 'Dark', value: 'dark' },
    { name: 'Green', value: 'green' },
    { name: 'Blue', value: 'blue' },
    { name: 'Neon', value: 'neon' },
  ];
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-40">
      <div className="bg-white dark:bg-gray-900 rounded-lg shadow-lg p-8 w-full max-w-md relative">
        <button
          className="absolute top-2 right-2 text-gray-400 hover:text-gray-700 dark:hover:text-white"
          onClick={onClose}
        >
          &times;
        </button>
        <h2 className="text-xl font-bold mb-4 text-gray-800 dark:text-white flex items-center gap-2">
          <Settings className="w-5 h-5" /> Configurações
        </h2>
        <div>
          <h3 className="font-semibold mb-2 text-gray-700 dark:text-gray-200">Tema do site</h3>
          <div className="space-y-2">
            {themeOptions.map(opt => (
              <button
                key={opt.value}
                className={`w-full text-left px-4 py-2 rounded transition border ${theme === opt.value ? 'bg-blue-500 text-white font-bold border-blue-500' : 'hover:bg-gray-100 dark:hover:bg-gray-800 border-transparent'}`}
                onClick={() => setTheme(opt.value as any)}
              >
                {opt.name}
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}