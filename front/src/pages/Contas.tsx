import React from 'react';
import Sidebar from "../components/ui/sidebar";
import { Card, CardContent } from "../components/ui/card";
import { CreditCard } from "lucide-react";
import itauLogo from "../components/bankLogos/itau-logo.png";
import bbLogo from "../components/bankLogos/bb-logo.png";
import nubankLogo from "../components/bankLogos/nubank-logo.png";

const bancos = [
  {
    nome: "Itaú",
    logo: itauLogo,
    contas: [
      { tipo: "Conta Corrente", saldo: 15400.75 },
      { tipo: "Poupança", saldo: 3200.10 },
    ],
    cartoes: [
      { final: "1234", limite: 5000 },
      { final: "9876", limite: 3000 },
    ],
  },
  {
    nome: "Banco do Brasil",
    logo: bbLogo,
    contas: [
      { tipo: "Conta Corrente", saldo: 8700.50 },
    ],
    cartoes: [
      { final: "4567", limite: 4000 },
    ],
  },
  {
    nome: "Nubank",
    logo: nubankLogo,
    contas: [
      { tipo: "Conta Corrente", saldo: 2900.00 },
    ],
    cartoes: [
      { final: "1122", limite: 2500 },
    ],
  },
];

export default function Contas() {
  return (
    <div className="flex h-screen overflow-hidden bg-gray-100">
      <Sidebar />

      <div className="flex-1 ml-64 p-6 space-y-6 overflow-y-auto">
        <h2 className="text-2xl font-bold mb-4">Contas Bancárias</h2>

       {bancos.map((banco, index) => (
          <Card key={index} className="w-full">
            <CardContent className="p-6 space-y-4">
              <div className="flex items-center space-x-3">
                <img src={banco.logo} alt={banco.nome} className="w-10 h-10" />
                <h3 className="text-xl font-semibold">{banco.nome}</h3>
              </div>

              <div>
                <p className="text-sm font-medium text-gray-500 mb-1">Contas:</p>
                {banco.contas.map((conta, i) => (
                  <div key={i} className="flex justify-between text-sm">
                    <span>{conta.tipo}</span>
                    <span className="text-green-600">R$ {conta.saldo.toFixed(2)}</span>
                  </div>
                ))}
              </div>

              <div>
                <p className="text-sm font-medium text-gray-500 mb-1">Cartões:</p>
                {banco.cartoes.map((cartao, i) => (
                  <div key={i} className="flex items-center justify-between text-sm">
                    <div className="flex items-center space-x-1">
                      <CreditCard className="w-4 h-4 text-gray-500" />
                      <span>Final {cartao.final}</span>
                    </div>
                    <span className="text-gray-600">Limite: R$ {cartao.limite.toFixed(2)}</span>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}