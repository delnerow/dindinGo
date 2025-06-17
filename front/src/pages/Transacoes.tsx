import { ChevronLeft } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useState } from 'react';
import Sidebar from "../components/ui/sidebar";

const meses = [
  { label: "Maio de 2025", value: "2025-05" },
  { label: "Junho de 2025", value: "2025-06" },
];

const transacoes = [
  { id: 1, categoria: "Comida", tipo: "Carteira", valor: -40.00, data: new Date("2025-06-23") },
  { id: 2, categoria: "Entretenimento", tipo: "Carteira", valor: -16.00, data: new Date("2025-05-28") },
  { id: 3, categoria: "Shoppping", tipo: "Cartão de crédito", valor: -200.00, data: new Date("2025-05-28") },
];

export default function Transacoes() {
  const navigate = useNavigate();
  const [mesSelecionado, setMesSelecionado] = useState("2025-05");

  const transacoesFiltradas = transacoes.filter((t) => {
    const mesAno = `${t.data.getFullYear()}-${String(t.data.getMonth() + 1).padStart(2, "0")}`;
    return mesAno === mesSelecionado;
  });

  const total = transacoesFiltradas.reduce((acc, t) => acc + t.valor, 0);

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

      <ul className="space-y-2">
        {transacoesFiltradas.map((t) => (
          <li key={t.id} className="flex justify-between items-center bg-white p-3 rounded shadow">
            <div>
              <div className="font-medium">{t.categoria}</div>
              <div className="text-sm text-gray-500">{t.tipo}</div>
            </div>
            <div className="text-right">
              <div className={t.valor < 0 ? "text-red-500" : "text-green-500"}>
                R$ {Math.abs(t.valor).toFixed(2)}
              </div>
              <div className="text-sm text-gray-500">
                {t.data.toLocaleDateString("pt-BR")}
              </div>
            </div>
          </li>
        ))}
      </ul>
    </div>
  </div>
);
}