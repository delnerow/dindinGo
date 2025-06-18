import React from "react";
import { Plus } from "lucide-react";

export default function AddButton({ onClick }: { onClick: () => void }) {
  return (
    <button
      onClick={onClick}
      className="fixed bottom-6 right-6 bg-blue-600 text-white p-4 rounded-full shadow-lg hover:bg-blue-700"
      aria-label="Adicionar carteira"
    >
      <Plus />
    </button>
  );
}