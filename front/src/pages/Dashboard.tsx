import React from 'react';
import logo from './logo.svg';
import '../App.css';
import { Card, CardContent } from "../components/ui/card";
import { Button } from "../components/ui/button";
import Sidebar from "../components/ui/sidebar";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, LineChart, Line } from "recharts";
import { PieChart, Pie, Cell } from "recharts";
import { Calendar } from "../components/ui/calendar";
import { Home, DollarSign, CreditCard, PieChart as PieIcon, Calendar as CalendarIcon, BarChart3 } from "lucide-react";

const data = [
  { name: "30/05", valor: 200 },
  { name: "31/05", valor: 90 },
  { name: "01/06", valor: 150 },
  { name: "02/06", valor: 120 },
  { name: "03/06", valor: 170 },
  { name: "04/06", valor: 80 },
];

const pieData = [
  { name: "Entradas", value: 2904 },
  { name: "Saídas", value: 1234 },
];

const COLORS = ["#22c55e", "#ef4444"];

export default function Dashboard() {
  return (
    <div className="flex h-screen overflow-hidden bg-gray-100">
      {/* Sidebar */}
      <Sidebar />

    

      {/* Main Content */}
      <div className="flex-1 ml-64 p-6 space-y-6 overflow-y-auto">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Card>
            <CardContent className="p-4">
              <p className="text-sm text-gray-500">Balanço</p>
              <p className="text-2xl text-green-600">R$ 27.155,42</p>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="p-4">
              <p className="text-sm text-gray-500">Cartões de Crédito</p>
              <p className="text-2xl text-red-500">-R$ 489,00</p>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="p-4">
              <p className="text-sm text-gray-500">Saldo Final</p>
              <p className="text-2xl text-green-500">R$ 26.857,42</p>
            </CardContent>
          </Card>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Card>
            <CardContent className="p-4">
              <p className="text-sm text-gray-500 mb-2">Este mês</p>
              <ResponsiveContainer width="100%" height={200}>
                <PieChart>
                  <Pie data={pieData} dataKey="value" outerRadius={60} label>
                    {pieData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                </PieChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-4">
              <p className="text-sm text-gray-500 mb-2">Evolução do Saldo</p>
              <ResponsiveContainer width="100%" height={200}>
                <LineChart data={data}>
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Line type="monotone" dataKey="valor" stroke="#3b82f6" strokeWidth={2} />
                </LineChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Card>
            <CardContent className="p-4">
              <p className="text-sm text-gray-500 mb-2">Últimos 7 dias</p>
              <ResponsiveContainer width="100%" height={200}>
                <BarChart data={data}>
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="valor" fill="#10b981" />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="p-4">
              <p className="text-sm text-gray-500 mb-2">Calendário</p>
              <Calendar value={new Date().toISOString().split("T")[0]} className="rounded-md border" />
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}

