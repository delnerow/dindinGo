import React, { useEffect, useState } from "react";
import Sidebar from "../components/ui/sidebar";
import { Card, CardContent } from "../components/ui/card";
import { Progress } from "../components/ui/progress";
import AddButton from "../components/ui/adicionarCofrinho";
import CofrinhoModal from "../components/ui/cofrinhoModal";

type Cofrinho = {
  nome: string;
  desc: string;
  timer_mes: number; // Tempo em meses
  saldo: number;
  meta: number;
}


export default function Cofrinhos() {
  const [cofrinhos, setCofrinhos] = useState<Cofrinho[]>([]);
  const [showModal, setShowModal] = useState(false);

  useEffect(() => {
    fetch("http://localhost:5000/api/cofrinhos")
      .then((res) => res.json())
      .then(setCofrinhos);
  }, []);

  const handleCreated = (novaCarteira: Cofrinho) => {
    setCofrinhos((prev) => [...prev, novaCarteira]);
    setShowModal(false);
  };

  function handleAdicionarSaldo(index: number) {
    const valor = prompt("Quanto deseja adicionar?");
    const valorNumerico = parseFloat(valor ?? "0");

    if (!isNaN(valorNumerico) && valorNumerico > 0) {
      setCofrinhos((prev) => {
        const atualizados = [...prev];
        atualizados[index].saldo += valorNumerico;
        return atualizados;
      });
    } else {
      alert("Valor inválido.");
    }
  }


  return (
    <div className="flex h-screen overflow-hidden bg-gray-100">
      <Sidebar />

      <div className="flex-1 ml-64 p-6 space-y-6 overflow-y-auto">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-2xl font-bold">Minhas Carteiras</h2>
          <AddButton onClick={() => setShowModal(true)} />
        </div>

        {cofrinhos.map((cofrinho, index) => {
          const progresso = cofrinho?.meta ? (cofrinho.saldo / cofrinho.meta) * 100 : 0;

          return (
            <Card key={index} className="w-full shadow-md border rounded-lg">
              <CardContent className="p-6 space-y-4">
                <div className="flex justify-between items-center">
                  <h3 className="text-xl font-semibold text-blue-700">
                    {cofrinho.nome}
                  </h3>
                  <span className="text-sm text-gray-500">
                    {Math.round(cofrinho.timer_mes ?? 0)} meses restantes
                  </span>
                </div>
                <p className="text-gray-600">{cofrinho.desc}</p>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-700">
                  Meta: <strong>R$ {(cofrinho.meta ?? 0).toFixed(2)}</strong>
                  </span>
                  <span className="text-green-600">
                  Saldo: <strong>R$ {(cofrinho.saldo ?? 0).toFixed(2)}</strong>
                  </span>
                </div>
                <div>
                  <Progress value={progresso} />
                  <div className="text-right text-xs text-gray-500 mt-1">
                    {progresso.toFixed(1)}% alcançado
                  </div>
                </div>

                <div className="flex justify-end space-x-2 mt-4">
                  <button
                    onClick={() => handleAdicionarSaldo(index)}
                    className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition"
                  >
                    Adicionar Saldo
                  </button>

                </div>
              </CardContent>
            </Card>
          );
        })}

        {showModal && (
          <CofrinhoModal
            onClose={() => setShowModal(false)}
            onCreated={handleCreated}
          />
        )}
      </div>
    </div>
  );
}