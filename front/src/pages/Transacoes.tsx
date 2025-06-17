import { ChevronLeft } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import Sidebar from "../components/ui/sidebar";

const meses = [
  { label: "Maio de 2025", value: "2025-05" },
  { label: "Junho de 2025", value: "2025-06" },
];

interface Transaction {
  id: number;
  nome: string;
  valor: number;
  categoria: string;
  data: string;
  desc: string;
  carteira: string;
  repeticao: boolean;
}

// Helper function to format dates
const formatDate = (dateString: string): string => {
  const date = new Date(dateString);
  return date.toLocaleDateString('pt-BR');
};

export default function Transacoes() {
  const navigate = useNavigate();
  const [mesSelecionado, setMesSelecionado] = useState("2025-06");
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchTransactions = async () => {
      try {
        setIsLoading(true);
        const response = await fetch('http://localhost:5000/api/transactions');
        if (!response.ok) {
          const errorText = await response.text();
          throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
        }
        const data = await response.json();
        setTransactions(data.transacoes); // Note: accessing 'transacoes' from JSON structure
      } catch (err) {
        console.error('Fetch error:', err);
        setError(err instanceof Error ? err.message : 'Failed to load transactions');
      } finally {
        setIsLoading(false);
      }
    };

    fetchTransactions();
  }, []);

  // Filter transactions by selected month
  const transacoesFiltradas = transactions.filter((t) => {
    const data = new Date(t.data);
    const mesAno = `${data.getFullYear()}-${String(data.getMonth() + 1).padStart(2, "0")}`;
    return mesAno === mesSelecionado;
  });

  const total = transacoesFiltradas.reduce((acc, t) => acc + t.valor, 0);

  if (isLoading) return <div>Carregando...</div>;
  if (error) return <div>Erro: {error}</div>;

return (
  <div className="flex h-screen overflow-hidden bg-gray-100">
    {/* Sidebar */}
    <div className="w-64 bg-white border-r shadow-lg">
      <Sidebar />
    </div>

    {/* Conteúdo principal */}
    <div className="flex-1 p-6 overflow-y-auto">
      <div className="flex items-center space-x-2 mb-4">
        <select
          className="text-xl font-bold bg-transparent"
          value={mesSelecionado}
          onChange={(e) => setMesSelecionado(e.target.value)}
        >
          {meses.map((m) => (
            <option key={m.value} value={m.value}>{m.label}</option>
          ))}
        </select>
      </div>

      <div className="flex justify-between items-center mb-4">
        <span>Transações: {transacoesFiltradas.length}</span>
        <span className={`font-semibold ${total >= 0 ? 'text-green-500' : 'text-red-500'}`}>
          Total: R$ {total.toFixed(2)}
        </span>
      </div>

      <div className="space-y-4">
        {transacoesFiltradas.map((transaction) => (
          <div key={transaction.id} className="bg-white rounded-lg shadow p-4">
            <div className="flex justify-between items-start mb-2">
              <div>
                <div className="font-medium">{transaction.nome}</div>
                <div className="text-sm text-gray-500">{transaction.categoria}</div>
              </div>
              <div className="text-right">
                <p className={`font-semibold ${transaction.valor >= 0 ? 'text-green-500' : 'text-red-500'}`}>
                  R$ {Math.abs(transaction.valor).toFixed(2)}
                </p>
                <p className="text-sm text-gray-500">
                  {formatDate(transaction.data)}
                </p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  </div>
);
}