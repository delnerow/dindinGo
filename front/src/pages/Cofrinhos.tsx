import React, { useEffect, useState } from "react";
import Sidebar from "../components/ui/sidebar";
import { Card, CardContent } from "../components/ui/card";
import { Progress } from "../components/ui/progress";
import AddSafeButton from "../components/ui/adicionarCofrinho";
import DepositButton from "../components/ui/fazerDeposito";
import CofrinhoModal from "../components/ui/cofrinhoModal";
import DepositoModal from "../components/ui/depositarCofrinhoModal";
import BreakSafeButton from "../components/ui/quebrarCofrinho";
import QuebrarCofrinhoModal from "../components/ui/quebrarModal";

type Cofrinho = {
  nome: string;
  desc: string;
  timer_mes: number;
  saldo: number;
  meta_valor: number;
};

export default function Cofrinhos() {
  const [cofrinhos, setCofrinhos] = useState<Cofrinho[]>([]);
  const [showModal, setShowModal] = useState(false);
  const [showDepositoModal, setShowDepositoModal] = useState(false);
  const [cofrinhoSelecionado, setCofrinhoSelecionado] = useState<Cofrinho | null>(null);
  const [showQuebrarModal, setShowQuebrarModal] = useState(false);
  const [cofrinhoParaQuebrar, setCofrinhoParaQuebrar] = useState<string | null>(null);

  useEffect(() => {
    fetch("http://localhost:5000/api/cofrinhos")
      .then((res) => res.json())
      .then(setCofrinhos);
  }, []);

  const handleCreated = (novoCofrinho: Cofrinho) => {
    setCofrinhos((prev) => [...prev, novoCofrinho]);
    setShowModal(false);
  };

  const abrirModalDeposito = (cofrinho: Cofrinho) => {
    setCofrinhoSelecionado(cofrinho);
    setShowDepositoModal(true);
  };

  return (
    <div className="flex h-screen overflow-hidden bg-gray-100">
      <Sidebar />

      <div className="flex-1 ml-64 p-6 space-y-6 overflow-y-auto">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-2xl font-bold">Meus Cofrinhos</h2>
          <AddSafeButton onClick={() => setShowModal(true)} />
        </div>

        {cofrinhos.map((cofrinho) => {
          const progresso = cofrinho.meta_valor ? (cofrinho.saldo / cofrinho.meta_valor) * 100 : 0;
          const podeQuebrar = cofrinho.timer_mes === 0 || progresso >= 100;

          return (
            <Card key={cofrinho.nome} className="w-full shadow-md border rounded-lg">
              <CardContent className="p-6 space-y-4">
                <div className="flex justify-between items-center">
                  <h3 className="text-xl font-semibold text-blue-700">{cofrinho.nome}</h3>
                  <span className="text-sm text-gray-500">
                    {Math.round(cofrinho.timer_mes)} meses restantes
                  </span>
                </div>

                <p className="text-gray-600">{cofrinho.desc}</p>

                <div className="flex justify-between text-sm">
                  <span className="text-gray-700">
                    Meta: <strong>R$ {cofrinho.meta_valor.toFixed(2)}</strong>
                  </span>
                  <span className="text-green-600">
                    Saldo: <strong>R$ {cofrinho.saldo.toFixed(2)}</strong>
                  </span>
                </div>

                <div>
                  <Progress value={progresso} />
                  <div className="text-right text-xs text-gray-500 mt-1">
                    {progresso.toFixed(1)}% alcançado
                  </div>
                </div>

                <div className="flex justify-between items-center mt-4">
                  <div>
                    {podeQuebrar && (
                      <BreakSafeButton
                        onClick={() => {
                          setCofrinhoParaQuebrar(cofrinho.nome);
                          setShowQuebrarModal(true);
                        }}
                      />
                    )}
                  </div>
                  <div>
                    <DepositButton onClick={() => abrirModalDeposito(cofrinho)} />
                  </div>
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

        {showDepositoModal && cofrinhoSelecionado && (
          <DepositoModal
            cofrinhoNome={cofrinhoSelecionado.nome}
            onClose={() => setShowDepositoModal(false)}
            onDeposited={() => {
              fetch("http://localhost:5000/api/cofrinhos")
                .then((res) => res.json())
                .then(setCofrinhos);
              setShowDepositoModal(false);
            }}
          />
        )}

        {showQuebrarModal && cofrinhoParaQuebrar && (
          <QuebrarCofrinhoModal
            cofrinhoNome={cofrinhoParaQuebrar}
            onClose={() => setShowQuebrarModal(false)}
            onQuebrado={() => {
              fetch("http://localhost:5000/api/cofrinhos")
                .then((res) => res.json())
                .then(setCofrinhos);
              setShowQuebrarModal(false);
            }}
          />
        )}
      </div>
    </div>
  );
}
