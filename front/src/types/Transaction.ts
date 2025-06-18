export interface Transaction {
    id: number;
    nome: string;
    valor: number;
    categoria: string;
    data: string;
    desc: string;
    carteira: string;
    repeticao: number;  // number of repetitions (0 if not repeated)
    receita: boolean;
    feita: boolean;
}

export type NewTransaction = Omit<Transaction, 'id'>;