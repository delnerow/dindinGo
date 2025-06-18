import { 
  ShoppingBag, 
  Home, 
  Coffee, 
  Wrench,
  Palmtree,
  LucideIcon
} from 'lucide-react';

export const getCategoryIcon = (category: string): LucideIcon => {
  const icons: { [key: string]: LucideIcon } = {
    'mercado': ShoppingBag,
    'casa': Home,
    'alimentação': Coffee,
    'serviço': Wrench,
    'lazer': Palmtree,
  };

  return icons[category.toLowerCase()] || ShoppingBag;
};