import SidebarItem from "./sidebarItem";
import {
  Home,
  DollarSign,
  PiggyBank,
  CreditCard,
  ChartNoAxesCombined,
} from "lucide-react";

export default function Sidebar() {
  return (
    <div className="w-64 bg-white p-6 border-r shadow-lg fixed h-full">
      <div className="flex items-center gap-2 mb-6">
        <h1 className="text-xl font-bold">DinDinGo</h1>
      </div>
      <nav className="space-y-4">
        <SidebarItem icon={<Home size={20} />} label="Visão Geral" />
        <SidebarItem icon={<DollarSign size={20} />} label="Transações" />
        <SidebarItem icon={<CreditCard size={20} />} label="Carteiras" />
        <SidebarItem icon={<PiggyBank size={20} />} label="Cofrinhos" />
        <SidebarItem icon={<ChartNoAxesCombined size={20} />} label="Pontos" />
      </nav>
    </div>
  );
}









