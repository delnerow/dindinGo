import React from "react";
import { cn } from "../../lib/utils";

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {}

export const Button: React.FC<ButtonProps> = ({ className, ...props }) => {
  return (
    <button
      className={cn(
        "px-4 py-2 rounded-xl bg-blue-600 text-white hover:bg-blue-700 transition",
        className
      )}
      {...props}
    />
  );
};