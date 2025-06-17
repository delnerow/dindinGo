import React from "react";

interface CalendarProps {
  value?: string;
  className?: string;
}

export const Calendar: React.FC<CalendarProps> = ({ value, className }) => {
  // Se não receber value, usar hoje:
  const today = new Date().toISOString().split("T")[0];
  const dateValue = value ?? today;

  return (
    <div className={`p-4 rounded-xl bg-white shadow-md ${className ?? ""}`}>
      <h2 className="text-lg font-semibold mb-2">Calendário</h2>
      <input
        type="date"
        defaultValue={dateValue}
        className="border rounded p-2 w-full"
      />
    </div>
  );
};