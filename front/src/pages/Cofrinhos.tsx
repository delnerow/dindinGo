import React from 'react';
import Sidebar from "../components/ui/sidebar";
import { Card, CardContent } from "../components/ui/card";
import { Progress } from "../components/ui/progress";

const metas = [
  {
    nome: "Viagem para Paris",
    icone: "🗼",
    orcamento: 30000.00,
    metaMensal: 5000.00,
    guardado: 15000.00,
  },
  {
    nome: "Fundo para Emergência",
    icone: "🆘",
    orcamento: 10000.00,
    metaMensal: 1000.00,
    guardado: 7200.00,
  },
  {
    nome: "Comprar Carro",
    icone: "🚗",
    orcamento: 40000.00,
    metaMensal: 4000.00,
    guardado: 20000.00,
  },
];

export default function Cofrinhos() {
  return (
    <div className="flex h-screen overflow-hidden bg-gray-100">
      <Sidebar />

      <div className="flex-1 ml-64 p-6 overflow-y-auto space-y-6">
        <h2 className="text-2xl font-bold mb-4">Meus Cofrinhos</h2>

        {metas.map((meta, index) => {
          const progresso = (meta.guardado / meta.orcamento) * 100;

          return (
            <Card key={index} className="w-full">
              <CardContent className="p-6 space-y-4">
                <div className="flex items-center space-x-3">
                  <div className="text-3xl">{meta.icone}</div>
                  <h3 className="text-xl font-semibold">{meta.nome}</h3>
                </div>

                <div className="space-y-1 text-sm">
                  <div className="flex justify-between">
                    <span>Orçamento total:</span>
                    <span className="font-medium text-gray-700">R$ {meta.orcamento.toFixed(2)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Meta mensal:</span>
                    <span className="text-blue-600">R$ {meta.metaMensal.toFixed(2)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Já guardado:</span>
                    <span className="text-green-600">R$ {meta.guardado.toFixed(2)}</span>
                  </div>
                </div>

                {/* Barra de progresso */}
                <div>
                  <Progress value={progresso} />
                  <div className="text-right text-xs text-gray-500 mt-1">
                    {progresso.toFixed(1)}% alcançado
                  </div>
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>
    </div>
  );
}