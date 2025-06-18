import { useNavigate } from "react-router-dom";

export default function SidebarItem({ icon, label, onClick }: { icon: React.ReactNode; label: string; onClick?: () => void }) {
  const navigate = useNavigate();

  const handleClick = () => {
    if (onClick) {
      onClick();
      return;
    }
    switch (label) {
      case "Visão Geral":
        navigate("/");
        break;
      case "Transações":
        navigate("/transacoes");
        break;
      case "Carteiras":
        navigate("/carteiras");
        break;
      case "Cofrinhos":
        navigate("/cofrinhos");
        break;
      case "Pontos":
        navigate("/pontos");
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