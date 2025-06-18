import React, { useEffect, useState } from "react";
import Sidebar from "../components/ui/sidebar";
import { Card, CardContent } from "../components/ui/card";
import AddWalletButton from "../components/ui/adicionarCarteira";
import CarteiraModal from "../components/ui/carteiraModal";
import { Trash2 } from 'lucide-react';

type Carteira = {
  nome: string;
  desc: string;
  saldo: number;
};

export default function Carteiras({ settingsOnClick }: { settingsOnClick?: () => void }) {
  const [carteiras, setCarteiras] = useState<Carteira[]>([]);
  const [showModal, setShowModal] = useState(false);

  useEffect(() => {
    fetch("http://localhost:5000/api/carteiras") 
      .then((res) => res.json())
      .then(setCarteiras);
  }, []);

  const handleDeleteCarteira = async (nome: string) => {
    if (!window.confirm('Tem certeza que deseja deletar esta carteira?')) return;
    try {
      const response = await fetch(`http://localhost:5000/api/carteiras/${encodeURIComponent(nome)}`, {
        method: 'DELETE',
      });
      const data = await response.json();
      if (!response.ok || !data.success) {
        alert(data.message || 'Erro ao deletar carteira.');
        return;
      }
      setCarteiras((prev) => prev.filter((c) => c.nome !== nome));
    } catch (err) {
      alert('Erro ao deletar carteira.');
    }
  };

  return (
    <div className="flex h-screen overflow-hidden bg-gray-100">
      <Sidebar settingsOnClick={settingsOnClick} />
      
      <div className="flex-1 ml-64 p-6 space-y-6 overflow-y-auto">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-2xl font-bold">Minhas Carteiras</h2>
          <AddWalletButton onClick={() => setShowModal(true)} />
        </div>
        {carteiras.map((carteiras) => (
          <Card key={carteiras.nome} className="w-full flex justify-between items-center">
            <CardContent className="p-6 space-y-2 flex-1">
              <h3 className="text-xl font-semibold">{carteiras.nome}</h3>
              <p className="text-sm text-gray-500">{carteiras.desc}</p>
              <p className="text-green-600 font-medium">
                Saldo: R$ {carteiras.saldo.toFixed(2)}
              </p>
            </CardContent>
            <button
              className="p-2 text-red-500 hover:bg-red-100 rounded-full m-4"
              title="Deletar carteira"
              onClick={() => handleDeleteCarteira(carteiras.nome)}
            >
              <Trash2 className="w-5 h-5" />
            </button>
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
