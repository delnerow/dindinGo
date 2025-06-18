import React, { useState, useEffect } from "react";

export default function DepositarModal({
  onClose,
  onDeposited,
  cofrinhoNome,
}: {
  onClose: () => void;
  onDeposited: () => void;
  cofrinhoNome: string;
}) {
  const [valor, setValor] = useState("");
  const [carteiras, setCarteiras] = useState([]);
  const [carteiraNome, setCarteiraNome] = useState("");
  const [erro, setErro] = useState("");

useEffect(() => {
  const fetchCarteiras = async () => {
    const res = await fetch("http://localhost:5000/api/carteiras");
    const data = await res.json();
    setCarteiras(data); 
    if (data.length > 0) {
      setCarteiraNome(data[0].nome);
    }
  };

  fetchCarteiras();
}, []);

    const handleSubmit = async () => {
        console.log("cofrinhoNome =>", cofrinhoNome);
        const res = await fetch(`http://localhost:5000/api/cofrinhos/${cofrinhoNome}/depositar`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            valor: parseFloat(valor),
            carteiras: carteiraNome,
        }),
    });

    const data = await res.json();
    if (data.success) {
      onDeposited();
    } else {
      setErro(data.message || "Erro ao depositar.");
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-30 flex items-center justify-center z-50">
      <div className="bg-white p-6 rounded shadow-lg w-96">
        <h3 className="text-xl font-semibold mb-4">Depositar no Cofrinho</h3>

        <label className="block mb-1 text-sm font-medium text-gray-700">Valor:</label>
        <input
          type="number"
          placeholder="Valor"
          value={valor}
          onChange={(e) => setValor(e.target.value)}
          className="w-full mb-3 p-2 border rounded"
        />

        <label className="block mb-1 text-sm font-medium text-gray-700">Carteira de origem:</label>
        <select
          value={carteiraNome}
          onChange={(e) => setCarteiraNome(e.target.value)}
          className="w-full mb-3 p-2 border rounded"
        >
          {carteiras.map((carteiras: any) => (
            <option key={carteiras.nome} value={carteiras.nome}>
              {carteiras.nome} (R${carteiras.saldo?.toFixed(2) || "0.00"})
            </option>
          ))}
        </select>

        {erro && <p className="text-red-500 text-sm">{erro}</p>}

        <div className="flex justify-end space-x-2 mt-4">
          <button onClick={onClose} className="text-gray-500">Cancelar</button>
          <button onClick={handleSubmit} className="bg-green-600 text-white px-4 py-2 rounded">
            Depositar
          </button>
        </div>
      </div>
    </div>
  );
}
