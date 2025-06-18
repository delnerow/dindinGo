export interface Transaction {
  id: number;
  receita: boolean;
  nome: string;
  valor: number;
  categoria: string;
  data: string;
  desc: string;
  carteira: string;
  repeticao: boolean;
}