import React from "react";
import { Plus } from "lucide-react";

export default function AddButton({ onClick }: { onClick: () => void }) {
  return (
    <button
      onClick={onClick}
      className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white font-medium rounded-lg shadow-md hover:bg-blue-700 transition-all"
    >
      <Plus size={18} />
      Novo Cofrinho
    </button>
  );
}