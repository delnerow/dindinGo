import React, { useState } from "react";

export default function CarteiraModal({
  onClose,
  onCreated,
}: {
  onClose: () => void;
  onCreated: (carteira: any) => void;
}) {
  const [nome, setNome] = useState("");
  const [desc, setDesc] = useState("");
  const [saldo, setSaldo] = useState("0.00");
  const [erro, setErro] = useState("");

  const handleSubmit = async () => {
    const res = await fetch("http://localhost:5000/api/carteiras", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ nome, desc, saldo: parseFloat(saldo) }),
    });

    const data = await res.json();
    if (data.success) {
      onCreated(data.carteira); 
    } else {
      setErro(data.message);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-30 flex items-center justify-center z-50">
      <div className="bg-white p-6 rounded shadow-lg w-96">
        <h3 className="text-xl font-semibold mb-4">Nova Carteira</h3>
        <input
          type="text"
          placeholder="Nome"
          value={nome}
          onChange={(e) => setNome(e.target.value)}
          className="w-full mb-2 p-2 border rounded"
        />
        <input
          type="text"
          placeholder="Descrição"
          value={desc}
          onChange={(e) => setDesc(e.target.value)}
          className="w-full mb-2 p-2 border rounded"
        />
        <input
          type="number"
          placeholder="Saldo inicial"
          value={saldo}
          onChange={(e) => setSaldo(e.target.value)}
          className="w-full mb-2 p-2 border rounded"
        />

        {erro && <p className="text-red-500 text-sm">{erro}</p>}

        <div className="flex justify-end space-x-2 mt-4">
          <button onClick={onClose} className="text-gray-500">Cancelar</button>
          <button onClick={handleSubmit} className="bg-blue-600 text-white px-4 py-2 rounded">
            Criar
          </button>
        </div>
      </div>
    </div>
  );
}
