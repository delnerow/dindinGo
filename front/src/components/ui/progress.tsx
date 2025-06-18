import React from "react";
import { cn } from "../../lib/utils";

interface Progress extends React.HTMLAttributes<HTMLDivElement> {
    value: number;
}

export function Progress({ value }: { value: number }) {
  const clampedValue = Math.min(value, 100);

  return (
    <div className="w-full bg-gray-200 h-3 rounded">
      <div
        className="bg-green-500 h-3 rounded transition-all duration-300"
        style={{ width: `${clampedValue}%` }}
      />
    </div>
  );
}