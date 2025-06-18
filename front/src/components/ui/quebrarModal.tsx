import React, { useState, useEffect } from "react";

export default function QuebrarCofrinhoModal({
  onClose,
  onQuebrado,
  cofrinhoNome,
}: {
  onClose: () => void;
  onQuebrado: () => void;
  cofrinhoNome: string;
}) {
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

  const handleQuebrar = async () => {
    const res = await fetch(`http://localhost:5000/api/cofrinhos/${cofrinhoNome}/quebrar`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        carteira: carteiraNome,
      }),
    });

    const data = await res.json();
    if (data.success) {
      alert(data.message);
      onQuebrado();
    } else {
      setErro(data.message || "Erro ao quebrar o cofrinho.");
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-30 flex items-center justify-center z-50">
      <div className="bg-white p-6 rounded shadow-lg w-96">
        <h3 className="text-xl font-semibold mb-4">Quebrar Cofrinho</h3>

        <label className="block mb-1 text-sm font-medium text-gray-700">
          Escolha a carteira de destino:
        </label>
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
          <button onClick={onClose} className="text-gray-500">
            Cancelar
          </button>
          <button onClick={handleQuebrar} className="bg-red-600 text-white px-4 py-2 rounded">
            Quebrar Cofrinho
          </button>
        </div>
      </div>
    </div>
  );
}