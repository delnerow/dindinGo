import { useNavigate } from "react-router-dom";

export default function SidebarItem({ icon, label }: { icon: React.ReactNode; label: string }) {
  const navigate = useNavigate();

  const handleClick = () => {
    switch (label) {
      case "Visão Geral":
        navigate("/");
        break;
      case "Transações":
        navigate("/transacoes");
        break;
      case "Cartões de Crédito":
        navigate("/cartoes");
        break;
      
      default:
        break;
    }
  };

  return (
    <div
      onClick={handleClick}
      className="flex items-center space-x-3 p-2 rounded cursor-pointer hover:bg-gray-200 transition"
    >
      {icon}
      <span>{label}</span>
    </div>
  );
}