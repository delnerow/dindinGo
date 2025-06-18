import React, { useEffect, useState } from "react";
import Sidebar from "../components/ui/sidebar";
import { Card, CardContent } from "../components/ui/card";
import AddButton from "../components/ui/adicionarCarteira";
import CarteiraModal from "../components/ui/carteiraModal";

type Carteira = {
  nome: string;
  desc: string;
  saldo: number;
};

export default function Carteiras() {
  const [carteiras, setCarteiras] = useState<Carteira[]>([]);
  const [showModal, setShowModal] = useState(false);

  useEffect(() => {
    fetch("http://localhost:5000/api/carteiras") 
      .then((res) => res.json())
      .then(setCarteiras);
  }, []);

  return (
    <div className="flex h-screen overflow-hidden bg-gray-100">
      <Sidebar />
      
      <div className="flex-1 ml-64 p-6 space-y-6 overflow-y-auto">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-2xl font-bold">Minhas Carteiras</h2>
          <AddButton onClick={() => setShowModal(true)} />
        </div>
        {carteiras.map((carteira, index) => (
          <Card key={index} className="w-full">
            <CardContent className="p-6 space-y-2">
              <h3 className="text-xl font-semibold">{carteira.nome}</h3>
              <p className="text-sm text-gray-500">{carteira.desc}</p>
              <p className="text-green-600 font-medium">
                Saldo: R$ {carteira.saldo.toFixed(2)}
              </p>
            </CardContent>
          </Card>
        ))}

        {showModal && (
          <CarteiraModal
            onClose={() => setShowModal(false)}
            onCreated={(novaCarteira) => {
              setCarteiras((prev) => [...prev, novaCarteira]);
              setShowModal(false);
            }}
          />
        )}
      </div>
    </div>
  );
}
