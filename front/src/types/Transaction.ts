export interface Transaction {
    id: number;
    receita: boolean;  // Changed from tipo_transacao
    nome: string;
    valor: number;
    categoria: string;
    data: string;
    desc: string;
    carteira: string;
    repeticao: boolean;  // Changed from number to boolean
    feita?: boolean;     // Added optional feita field
}

export type NewTransaction = Omit<Transaction, 'id'>;