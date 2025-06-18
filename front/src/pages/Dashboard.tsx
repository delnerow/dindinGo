import React, { useEffect, useState } from "react";
import logo from "./logo.svg";
import "../App.css";
import { Card, CardContent } from "../components/ui/card";
import Sidebar from "../components/ui/sidebar";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  LineChart,
  Line,
} from "recharts";
import { PieChart, Pie, Cell } from "recharts";
import { Calendar } from "../components/ui/calendar";
import {
  Home,
  DollarSign,
  CreditCard,
  PieChart as PieIcon,
  Calendar as CalendarIcon,
  BarChart3,
} from "lucide-react";

type Carteira = {
  nome: string;
  descricao: string;
  saldo: number;
};

type Transaction = {
  id: number;
  receita: boolean;
  nome: string;
  valor: number;
  categoria: string;
  data: string;
  desc: string;
  carteira: string;
  repeticao: boolean;
};

const COLORS = ["#22c55e", "#ef4444"];

export default function Dashboard({ settingsOnClick }: { settingsOnClick?: () => void }) {
  const [carteiras, setCarteiras] = useState<Carteira[]>([]);
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [carteiraSelecionada, setCarteiraSelecionada] = useState<string>("");
  const [periodoSelecionado, setPeriodoSelecionada] = useState<string>("7");
  const [dataInicial, setDataInicial] = useState<string>("");
  const [dataFinal, setDataFinal] = useState<string>("");
  const [isLoading, setIsLoading] = useState(true);
  const [fullScreenChart, setFullScreenChart] = useState<null | 'pie' | 'line'>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Buscar carteiras
        const carteirasResponse = await fetch('http://localhost:5000/api/carteiras');
        if (!carteirasResponse.ok) throw new Error('Failed to fetch carteiras');
        const carteirasData = await carteirasResponse.json();
        setCarteiras(carteirasData);
        
        // Seleciona a primeira carteira por padrão se existir
        if (carteirasData.length > 0) {
          setCarteiraSelecionada(carteirasData[0].nome);
        }

        // Buscar transações
        const transactionsResponse = await fetch('http://localhost:5000/api/transactions');
        if (!transactionsResponse.ok) throw new Error('Failed to fetch transactions');
        const transactionsData = await transactionsResponse.json();
        setTransactions(transactionsData);
      } catch (err) {
        console.error('Error fetching data:', err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, []);

  // Encontra a carteira selecionada
  const carteiraAtual = carteiras.find(c => c.nome === carteiraSelecionada);

  // Calcula as datas baseadas no período selecionado
  const calcularDatas = () => {
    const hoje = new Date();
    hoje.setHours(23, 59, 59, 999); // Define para o final do dia de hoje
    let dataInicio: Date;
    
    switch (periodoSelecionado) {
      case "7":
        dataInicio = new Date(hoje.getTime() - 7 * 24 * 60 * 60 * 1000);
        dataInicio.setHours(0, 0, 0, 0); // Define para o início do dia
        break;
      case "15":
        dataInicio = new Date(hoje.getTime() - 15 * 24 * 60 * 60 * 1000);
        dataInicio.setHours(0, 0, 0, 0); // Define para o início do dia
        break;
      case "30":
        dataInicio = new Date(hoje.getTime() - 30 * 24 * 60 * 60 * 1000);
        dataInicio.setHours(0, 0, 0, 0); // Define para o início do dia
        break;
      case "personalizado":
        if (dataInicial && dataFinal) {
          const inicio = new Date(dataInicial);
          const fim = new Date(dataFinal);
          inicio.setHours(0, 0, 0, 0); // Define para o início do dia inicial
          fim.setHours(23, 59, 59, 999); // Define para o final do dia final
          return {
            inicio: inicio,
            fim: fim
          };
        }
        // Fallback para 7 dias se não há datas personalizadas
        dataInicio = new Date(hoje.getTime() - 7 * 24 * 60 * 60 * 1000);
        dataInicio.setHours(0, 0, 0, 0); // Define para o início do dia
        break;
      default:
        dataInicio = new Date(hoje.getTime() - 7 * 24 * 60 * 60 * 1000);
        dataInicio.setHours(0, 0, 0, 0); // Define para o início do dia
    }
    
    return {
      inicio: dataInicio,
      fim: hoje
    };
  };

  const { inicio, fim } = calcularDatas();

  // Filtra transações pela carteira selecionada e período
  const transacoesFiltradas = transactions.filter(t => {
    if (t.carteira !== carteiraSelecionada) return false;
    
    const dataTransacao = new Date(t.data);
    return dataTransacao >= inicio && dataTransacao <= fim;
  });

  // Calcula dados para o gráfico de pizza (receitas vs despesas) - APENAS do período selecionado
  const receitas = transacoesFiltradas.filter(t => t.receita).reduce((sum, t) => sum + t.valor, 0);
  const despesas = transacoesFiltradas.filter(t => !t.receita).reduce((sum, t) => sum + t.valor, 0);
  
  const pieData = [
    { name: "Receitas", value: receitas },
    { name: "Despesas", value: despesas },
  ];

  // Prepara dados para o gráfico de linha (evolução do saldo) - APENAS do período selecionado
const prepararDadosEvolucao = () => {
  const transacoesOrdenadas = [...transacoesFiltradas].sort(
    (a, b) => new Date(a.data).getTime() - new Date(b.data).getTime()
  );

  // Return early case with current saldo if no transactions
  if (transacoesOrdenadas.length === 0) {
    if (carteiraAtual) {
      const hoje = new Date().toLocaleDateString('pt-BR');
      return [{ name: hoje, valor: carteiraAtual.saldo }];
    }
    return [{ name: "Sem dados", valor: 0 }];
  }

  // Calculate initial balance before selected period
  const todasTransacoesDaCarteira = transactions.filter(t => t.carteira === carteiraSelecionada);
  const transacoesAntesDoPeriodo = todasTransacoesDaCarteira.filter(t => {
    const dataTransacao = new Date(t.data);
    return dataTransacao < inicio;
  });
  
  let saldoInicialPeriodo = 0;
  transacoesAntesDoPeriodo.forEach(t => {
    saldoInicialPeriodo += t.receita ? t.valor : -t.valor;
  });

  // Add current balance from carteira
  if (carteiraAtual) {
    saldoInicialPeriodo = carteiraAtual.saldo - transacoesFiltradas.reduce((acc, t) => 
      acc + (t.receita ? t.valor : -t.valor), 0
    );
  }

  // Group transactions by day and calculate running balance
  let saldoAtual = saldoInicialPeriodo;
  const saldoPorDia: { [dia: string]: number } = {};
  
  // Add initial balance to first day if there are transactions
  if (transacoesOrdenadas.length > 0) {
    const primeiraDia = new Date(transacoesOrdenadas[0].data)
      .toLocaleDateString('pt-BR');
    saldoPorDia[primeiraDia] = saldoInicialPeriodo;
  }

  // Calculate running balance for each day
  transacoesOrdenadas.forEach(t => {
    saldoAtual += t.receita ? t.valor : -t.valor;
    const dia = new Date(t.data).toLocaleDateString('pt-BR');
    saldoPorDia[dia] = saldoAtual;
  });

  // Add current day with final balance if not already included
  const hoje = new Date().toLocaleDateString('pt-BR');
  if (!saldoPorDia[hoje] && carteiraAtual) {
    saldoPorDia[hoje] = carteiraAtual.saldo;
  }

  // Convert to array and sort by date
  const dadosEvolucao = Object.entries(saldoPorDia)
    .map(([dia, valor]) => ({ name: dia, valor }))
    .sort((a, b) => {
      const [diaA, mesA, anoA] = a.name.split('/').map(Number);
      const [diaB, mesB, anoB] = b.name.split('/').map(Number);
      return new Date(anoA, mesA - 1, diaA).getTime() - 
             new Date(anoB, mesB - 1, diaB).getTime();
    });

  return dadosEvolucao;
};

  // Valida se o período personalizado não excede 45 dias
  const validarPeriodoPersonalizado = () => {
    if (periodoSelecionado === "personalizado" && dataInicial && dataFinal) {
      const inicio = new Date(dataInicial);
      const fim = new Date(dataFinal);
      const diffTime = Math.abs(fim.getTime() - inicio.getTime());
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
      return diffDays <= 45;
    }
    return true;
  };

  // Obtém a data de hoje no formato YYYY-MM-DD para limitar a data final
  const hojeFormatado = new Date().toISOString().split('T')[0];

  // Função para formatar data no formato brasileiro
  const formatarDataBrasileira = (data: Date | string) => {
    if (typeof data === 'string') {
      // Espera formato YYYY-MM-DD
      const [ano, mes, dia] = data.split('-');
      if (ano && mes && dia) return `${dia}/${mes}/${ano}`;
      return data;
    }
    return data.toLocaleDateString('pt-BR');
  };

  // Componente de Modal para tela cheia
  const FullScreenModal = ({ children, onClose }: { children: React.ReactNode, onClose: () => void }) => (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-70" onClick={onClose}>
      <div className="bg-white rounded-lg shadow-lg p-6 max-w-5xl w-full h-[90vh] flex flex-col justify-center" onClick={e => e.stopPropagation()}>
        <button className="self-end mb-2 text-gray-500 hover:text-gray-800" onClick={onClose}>&#10005;</button>
        <div className="flex-1 flex items-center justify-center">{children}</div>
      </div>
    </div>
  );

  if (isLoading) {
    return (
      <div className="flex h-screen overflow-hidden bg-gray-100">
        <Sidebar />
        <div className="flex-1 ml-64 p-6 flex items-center justify-center">
          <p>Carregando...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex h-screen overflow-hidden bg-gray-100">
      {/* Sidebar */}
      <Sidebar settingsOnClick={settingsOnClick} />

      {/* Main Content */}
      <div className="flex-1 ml-64 p-6 space-y-6 overflow-y-auto">
        {/* Seletor de Carteira e Período */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
          {/* Seletor de Carteira */}
          <div>
            <label htmlFor="carteira-select" className="block text-sm font-medium text-gray-700 mb-2">
              Selecione uma Carteira:
            </label>
            <select
              id="carteira-select"
              value={carteiraSelecionada}
              onChange={(e) => setCarteiraSelecionada(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="">Selecione uma carteira</option>
              {carteiras.map((carteira, index) => (
                <option key={index} value={carteira.nome}>
                  {carteira.nome}
                </option>
              ))}
            </select>
          </div>

          {/* Seletor de Período */}
          <div>
            <label htmlFor="periodo-select" className="block text-sm font-medium text-gray-700 mb-2">
              Período:
            </label>
            <select
              id="periodo-select"
              value={periodoSelecionado}
              onChange={(e) => setPeriodoSelecionada(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="7">Últimos 7 dias</option>
              <option value="15">Últimos 15 dias</option>
              <option value="30">Últimos 30 dias</option>
              <option value="personalizado">Personalizado</option>
            </select>
          </div>
        </div>

        {/* Datas Personalizadas */}
        {periodoSelecionado === "personalizado" && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            <div>
              <label htmlFor="data-inicial" className="block text-sm font-medium text-gray-700 mb-2">
                Data Inicial:
              </label>
              <div className="relative">
                <input
                  type="date"
                  id="data-inicial"
                  value={dataInicial}
                  onChange={(e) => setDataInicial(e.target.value)}
                  max={hojeFormatado}
                  className="w-full px-3 py-2 pr-10 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
                <div className="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
                  <CalendarIcon className="h-5 w-5 text-gray-400" />
                </div>
              </div>
            </div>
            <div>
              <label htmlFor="data-final" className="block text-sm font-medium text-gray-700 mb-2">
                Data Final:
              </label>
              <div className="relative">
                <input
                  type="date"
                  id="data-final"
                  value={dataFinal}
                  onChange={(e) => setDataFinal(e.target.value)}
                  min={dataInicial}
                  max={hojeFormatado}
                  className="w-full px-3 py-2 pr-10 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
                <div className="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
                  <CalendarIcon className="h-5 w-5 text-gray-400" />
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Aviso de período inválido */}
        {periodoSelecionado === "personalizado" && !validarPeriodoPersonalizado() && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
            <p className="text-sm">O período selecionado não pode exceder 45 dias.</p>
          </div>
        )}

        {/* Informações do período selecionado */}
        <div className="bg-blue-50 border border-blue-200 text-blue-700 px-4 py-3 rounded mb-6">
          <p className="text-sm">
            <strong>Período selecionado:</strong> {periodoSelecionado === "personalizado" && dataInicial && dataFinal
              ? `${formatarDataBrasileira(dataInicial)} a ${formatarDataBrasileira(dataFinal)}`
              : `${formatarDataBrasileira(inicio)} a ${formatarDataBrasileira(fim)} `}
            ({transacoesFiltradas.length} transações encontradas)
          </p>
        </div>

        {/* Card do Saldo da Carteira Selecionada */}
        <div className="grid grid-cols-1 md:grid-cols-1 gap-4">
          {carteiraAtual ? (
            <Card>
              <CardContent className="p-6">
                <p className="text-sm text-gray-500 mb-2">Saldo: {carteiraAtual.nome}</p>
                <p className="text-3xl font-bold text-green-600 mb-2">
                  R$ {carteiraAtual.saldo.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                </p>
                <p className="text-sm text-gray-400">{carteiraAtual.descricao}</p>
              </CardContent>
            </Card>
          ) : (
            <Card>
              <CardContent className="p-6">
                <p className="text-gray-500 text-center">Selecione uma carteira para ver o saldo</p>
              </CardContent>
            </Card>
          )}
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Gráfico de Pizza */}
          <Card onClick={() => setFullScreenChart('pie')} className="cursor-pointer hover:shadow-2xl transition-shadow">
            <CardContent className="p-4">
              <p className="text-sm text-gray-500 font-bold mb-4">Receitas vs Despesas (Período Selecionado)</p>
              <ResponsiveContainer width="100%" height={200}>
                <PieChart>
                  <Pie 
                    data={pieData} 
                    dataKey="value" 
                    outerRadius={60} 
                    label={({ name, value }) => `${name}: R$ ${Number(value).toLocaleString('pt-BR', { minimumFractionDigits: 2 })}`}
                  >
                    {pieData.map((entry, index) => (
                      <Cell
                        key={`cell-${index}`}
                        fill={COLORS[index % COLORS.length]}
                      />
                    ))}
                  </Pie>
                  <Tooltip formatter={(value) => `R$ ${Number(value).toLocaleString('pt-BR', { minimumFractionDigits: 2 })}`} />
                </PieChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>

          {/* Gráfico de Linha */}
          <Card onClick={() => setFullScreenChart('line')} className="cursor-pointer hover:shadow-2xl transition-shadow">
            <CardContent className="p-4">
              <p className="text-sm text-gray-500 font-bold mb-10">Evolução do Saldo (Período Selecionado)</p>
              <ResponsiveContainer width="100%" height={200}>
                <LineChart 
                  data={prepararDadosEvolucao()}
                  margin={{ top: 5, right: 20, left: 20, bottom: 5 }}
                >
                  <XAxis dataKey="name" tickFormatter={(str) => str.slice(0, 5)} />
                  <YAxis />
                  <Tooltip formatter={(value) => `R$ ${Number(value).toLocaleString('pt-BR', { minimumFractionDigits: 2 })}`} />
                  <Line
                    type="monotone"
                    dataKey="valor"
                    stroke="#3b82f6"
                    strokeWidth={2}
                  />
                </LineChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </div>

        {/* Modal de Tela Cheia para os Gráficos */}
        {fullScreenChart === 'pie' && (
          <FullScreenModal onClose={() => setFullScreenChart(null)}>
            <div className="w-full h-full flex flex-col items-center justify-center">
              <p className="text-lg text-gray-700 font-bold mb-4">Receitas vs Despesas (Período Selecionado)</p>
              <ResponsiveContainer width="90%" height={500}>
                <PieChart>
                  <Pie 
                    data={pieData} 
                    dataKey="value" 
                    outerRadius={200} 
                    label={({ name, value }) => `${name}: R$ ${Number(value).toLocaleString('pt-BR', { minimumFractionDigits: 2 })}`}
                  >
                    {pieData.map((entry, index) => (
                      <Cell
                        key={`cell-full-${index}`}
                        fill={COLORS[index % COLORS.length]}
                      />
                    ))}
                  </Pie>
                  <Tooltip formatter={(value) => `R$ ${Number(value).toLocaleString('pt-BR', { minimumFractionDigits: 2 })}`} />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </FullScreenModal>
        )}
        {fullScreenChart === 'line' && (
          <FullScreenModal onClose={() => setFullScreenChart(null)}>
            <div className="w-full h-full flex flex-col items-center justify-center">
              <p className="text-lg text-gray-700 font-bold mb-4">Evolução do Saldo (Período Selecionado)</p>
              <ResponsiveContainer width="90%" height={500}>
                <LineChart 
                  data={prepararDadosEvolucao()}
                  margin={{ top: 5, right: 20, left: 40, bottom: 5 }}
                >
                  <XAxis dataKey="name" tickFormatter={(str) => str.slice(0, 5)} />
                  <YAxis />
                  <Tooltip formatter={(value) => `R$ ${Number(value).toLocaleString('pt-BR', { minimumFractionDigits: 2 })}`} />
                  <Line
                    type="monotone"
                    dataKey="valor"
                    stroke="#3b82f6"
                    strokeWidth={2}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </FullScreenModal>
        )}
      </div>
    </div>
  );
}
