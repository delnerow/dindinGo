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

export default function Dashboard() {
  const [carteiras, setCarteiras] = useState<Carteira[]>([]);
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [carteiraSelecionada, setCarteiraSelecionada] = useState<string>("");
  const [periodoSelecionado, setPeriodoSelecionada] = useState<string>("7");
  const [dataInicial, setDataInicial] = useState<string>("");
  const [dataFinal, setDataFinal] = useState<string>("");
  const [isLoading, setIsLoading] = useState(true);

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
        break;
      case "15":
        dataInicio = new Date(hoje.getTime() - 15 * 24 * 60 * 60 * 1000);
        break;
      case "30":
        dataInicio = new Date(hoje.getTime() - 30 * 24 * 60 * 60 * 1000);
        break;
      case "personalizado":
        if (dataInicial && dataFinal) {
          const inicio = new Date(dataInicial);
          const fim = new Date(dataFinal);
          fim.setHours(23, 59, 59, 999); // Define para o final do dia selecionado
          return {
            inicio: inicio,
            fim: fim
          };
        }
        // Fallback para 7 dias se não há datas personalizadas
        dataInicio = new Date(hoje.getTime() - 7 * 24 * 60 * 60 * 1000);
        break;
      default:
        dataInicio = new Date(hoje.getTime() - 7 * 24 * 60 * 60 * 1000);
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
    const transacoesOrdenadas = [...transacoesFiltradas].sort((a, b) => new Date(a.data).getTime() - new Date(b.data).getTime());
    
    if (transacoesOrdenadas.length === 0) {
      // Se não há transações no período, mostra apenas o saldo atual
      if (carteiraAtual) {
        return [{ name: "Saldo Atual", valor: carteiraAtual.saldo }];
      }
      return [{ name: "Sem dados", valor: 0 }];
    }

    // Para calcular a evolução correta, precisamos do saldo antes do período selecionado
    // Vamos calcular o saldo inicial do período
    const todasTransacoesDaCarteira = transactions.filter(t => t.carteira === carteiraSelecionada);
    const transacoesAntesDoPeriodo = todasTransacoesDaCarteira.filter(t => {
      const dataTransacao = new Date(t.data);
      return dataTransacao < inicio;
    });

    // Calcula o saldo antes do período selecionado
    let saldoInicialPeriodo = 0;
    transacoesAntesDoPeriodo.forEach(t => {
      saldoInicialPeriodo += t.receita ? t.valor : -t.valor;
    });

    // Agora calcula a evolução do saldo dentro do período selecionado
    let saldoAtual = saldoInicialPeriodo;
    const dadosEvolucao = [];

    // Adiciona o ponto inicial (saldo no início do período)
    dadosEvolucao.push({
      name: `${inicio.getDate().toString().padStart(2, '0')}/${(inicio.getMonth() + 1).toString().padStart(2, '0')}`,
      valor: saldoAtual
    });

    // Adiciona pontos para cada transação no período
    transacoesOrdenadas.forEach(t => {
      saldoAtual += t.receita ? t.valor : -t.valor;
      const data = new Date(t.data);
      dadosEvolucao.push({
        name: `${data.getDate().toString().padStart(2, '0')}/${(data.getMonth() + 1).toString().padStart(2, '0')}`,
        valor: saldoAtual
      });
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
      <Sidebar />

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
              <input
                type="date"
                id="data-inicial"
                value={dataInicial}
                onChange={(e) => setDataInicial(e.target.value)}
                max={hojeFormatado}
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
            <div>
              <label htmlFor="data-final" className="block text-sm font-medium text-gray-700 mb-2">
                Data Final:
              </label>
              <input
                type="date"
                id="data-final"
                value={dataFinal}
                onChange={(e) => setDataFinal(e.target.value)}
                min={dataInicial}
                max={hojeFormatado}
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
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
            <strong>Período selecionado:</strong> {inicio.toLocaleDateString('pt-BR')} a {fim.toLocaleDateString('pt-BR')} 
            ({transacoesFiltradas.length} transações encontradas)
          </p>
        </div>

        {/* Card do Saldo da Carteira Selecionada */}
        <div className="grid grid-cols-1 md:grid-cols-1 gap-4">
          {carteiraAtual ? (
            <Card>
              <CardContent className="p-6">
                <p className="text-sm text-gray-500 mb-2">{carteiraAtual.nome}</p>
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
          <Card>
            <CardContent className="p-4">
              <p className="text-sm text-gray-500 mb-2">Receitas vs Despesas (Período Selecionado)</p>
              <ResponsiveContainer width="100%" height={200}>
                <PieChart>
                  <Pie data={pieData} dataKey="value" outerRadius={60} label>
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

          <Card>
            <CardContent className="p-4">
              <p className="text-sm text-gray-500 mb-2">Evolução do Saldo (Período Selecionado)</p>
              <ResponsiveContainer width="100%" height={200}>
                <LineChart data={prepararDadosEvolucao()}>
                  <XAxis dataKey="name" />
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
      </div>
    </div>
  );
}
