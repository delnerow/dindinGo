import React, { useState, useEffect } from "react";

export default function DepositarModal({
  onClose,
  onDeposited,
  cofrinhoId,
}: {
  onClose: () => void;
  onDeposited: () => void;
  cofrinhoId: number;
}) {
  const [valor, setValor] = useState("");
  const [carteiras, setCarteiras] = useState([]);
  const [carteiraId, setCarteiraId] = useState("");
  const [erro, setErro] = useState("");

  useEffect(() => {
    // Busca as carteiras existentes
    const fetchCarteiras = async () => {
      const res = await fetch("http://localhost:5000/api/carteiras");
      const data = await res.json();
      if (data.success) {
        setCarteiras(data.carteiras);
        if (data.carteiras.length > 0) {
          setCarteiraId(data.carteiras[0].id.toString());
        }
      }
    };

    fetchCarteiras();
  }, []);

  const handleSubmit = async () => {
    const res = await fetch(`http://localhost:5000/api/cofrinhos/${cofrinhoId}/depositar`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        valor: parseFloat(valor),
        carteira_id: parseInt(carteiraId),
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
          value={carteiraId}
          onChange={(e) => setCarteiraId(e.target.value)}
          className="w-full mb-3 p-2 border rounded"
        >
          {carteiras.map((carteira: any) => (
            <option key={carteira.id} value={carteira.id}>
              {carteira.nome} (R${carteira.saldo?.toFixed(2) || "0.00"})
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
