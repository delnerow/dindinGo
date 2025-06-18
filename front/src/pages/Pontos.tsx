import React, { useEffect, useState } from "react";
import Sidebar from "../components/ui/sidebar";
import { Card, CardContent } from "../components/ui/card";
import { CircleCheckBig, Flame, Trophy } from "lucide-react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

interface PontosBrutos {
  pontos: number;
  meta_lazer: number;
  meta_alimentacao: number;
  meta_casa: number;
  meta_mercado: number;
  meta_servico: number;
  gastos_lazer: number;
  gastos_alimentacao: number;
  gastos_casa: number;
  gastos_mercado: number;
  gastos_servico: number;
}

interface PontosData {
  total: number;
  metas: number;
  gastos: number;
}

const Pontos: React.FC = () => {
  const [pontos, setPontos] = useState<PontosData | null>(null);
  const [grafico, setGrafico] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://localhost:5000/api/pontos")
      .then((res) => res.json())
      .then((data) => {
        console.log("Dados recebidos da API:", data.pontos);
        const p: PontosBrutos = data.pontos; // Acessando o primeiro objeto do array

        const total = p.pontos;

        const metas =
          p.meta_lazer +
          p.meta_alimentacao +
          p.meta_casa +
          p.meta_mercado +
          p.meta_servico;

        const gastos =
          p.gastos_lazer +
          p.gastos_alimentacao +
          p.gastos_casa +
          p.gastos_mercado +
          p.gastos_servico;

        setPontos({ total, metas, gastos });

        const graficoData = [
          {
            categoria: "Lazer",
            Meta: p.meta_lazer,
            Gasto: p.gastos_lazer,
          },
          {
            categoria: "Alimentação",
            Meta: p.meta_alimentacao,
            Gasto: p.gastos_alimentacao,
          },
          {
            categoria: "Casa",
            Meta: p.meta_casa,
            Gasto: p.gastos_casa,
          },
          {
            categoria: "Mercado",
            Meta: p.meta_mercado,
            Gasto: p.gastos_mercado,
          },
          {
            categoria: "Serviço",
            Meta: p.meta_servico,
            Gasto: p.gastos_servico,
          },
        ];

        setGrafico(graficoData);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Erro ao carregar pontos:", err);
        setLoading(false);
      });
  }, []);

  return (
    <div className="flex h-screen overflow-hidden bg-gray-100">
      <Sidebar />

      <main className="flex-1 ml-64 p-6 space-y-6 overflow-y-auto">
        <h1 className="text-2xl font-bold">Seus Pontos</h1>

        {loading ? (
          <div>Carregando...</div>
        ) : !pontos ? (
          <div>Erro ao carregar pontos.</div>
        ) : (
          <>
            <Card className="shadow-lg rounded-2xl p-6 bg-gradient-to-r from-green-400 to-green-600 text-white">
              <CardContent className="flex items-center justify-between">
                <div>
                  <p className="text-lg font-semibold">Total de Pontos</p>
                  <p className="text-5xl font-bold">{pontos.total}</p>
                </div>
                <Trophy className="w-16 h-16 opacity-80" />
              </CardContent>
            </Card>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <Card className="p-4 flex items-center justify-between border-l-4 border-green-500">
                <div>
                  <p className="text-sm text-gray-600">Pontos por metas cumpridas</p>
                  <p className="text-xl font-semibold text-green-700">+{pontos.metas}</p>
                </div>
                <CircleCheckBig className="w-8 h-8 text-green-500" />
              </Card>

              <Card className="p-4 flex items-center justify-between border-l-4 border-red-500">
                <div>
                  <p className="text-sm text-gray-600">Perda por gastos impulsivos</p>
                  <p className="text-xl font-semibold text-red-600">-{pontos.gastos}</p>
                </div>
                <Flame className="w-8 h-8 text-red-500" />
              </Card>
            </div>

            <Card className="p-4 mt-4">
              <p className="text-lg font-semibold mb-4">Comparativo de Metas vs Gastos</p>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={grafico} margin={{ top: 20, right: 30, left: 0, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="categoria" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="Meta" fill="#10B981" />
                  <Bar dataKey="Gasto" fill="#EF4444" />
                </BarChart>
              </ResponsiveContainer>
            </Card>
          </>
        )}
      </main>
    </div>
  );
};

export default Pontos;
