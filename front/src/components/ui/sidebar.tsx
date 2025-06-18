import SidebarItem from "./sidebarItem";
import {
  Home,
  DollarSign,
  PiggyBank,
  CreditCard,
  BarChart3,
  Calendar as CalendarIcon,
  RotateCcw as RotateIcon,
} from "lucide-react";

export default function Sidebar() {
  return (
    <div className="w-64 bg-white p-6 border-r shadow-lg fixed h-full">
      <h1 className="text-xl font-bold mb-6">Orçamento Fácil</h1>
      <nav className="space-y-4">
        <SidebarItem icon={<Home size={20} />} label="Visão Geral" />
        <SidebarItem icon={<DollarSign size={20} />} label="Transações" />
        <SidebarItem icon={<CreditCard size={20} />} label="Carteiras" />
        <SidebarItem icon={<PiggyBank size={20} />} label="Cofrinhos" />
        <SidebarItem icon={<RotateIcon size={20} />} label="Gastos Recorrentes" />
        <SidebarItem icon={<BarChart3 size={20} />} label="Gastos Mensais" />
        <SidebarItem icon={<CalendarIcon size={20} />} label="Calendário" />
      </nav>
    </div>
  );
}









