import { useState } from 'react';
import { Transaction } from '../types/Transaction';
import { X } from 'lucide-react';

type NewTransaction = Omit<Transaction, 'id'>;
interface Carteira {
  nome: string;
  descricao: string;
  saldo: number;
}
interface EditTransactionModalProps {
  transaction: Transaction | null;
  isOpen: boolean;
  onClose: () => void;
  onSave: (transaction: Transaction | NewTransaction) => Promise<void>;
  carteiras: Carteira[];
}

export function EditTransactionModal({ transaction, isOpen, onClose, onSave, carteiras }: EditTransactionModalProps) {
  const [isFixo, setIsFixo] = useState(transaction ? transaction.repeticao > 0 : false);
  const [repeticoes, setRepeticoes] = useState(transaction?.repeticao || 1);
  const [isFeita, setIsFeita] = useState(transaction?.feita || false);

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    
    const transactionData: NewTransaction = {
      nome: formData.get('nome') as string,
      valor: Number(formData.get('valor')),
      categoria: formData.get('categoria') as string,
      data: formData.get('data') as string,
      desc: formData.get('desc') as string || '',
      carteira: formData.get('carteira') as string,
      repeticao: isFixo ? repeticoes : 0,
      receita: formData.get('tipo') === 'receita',
      feita: isFixo ? isFeita : false // Only allow feita if transaction is fixed
    };

    if (transaction) {
      onSave({ ...transactionData, id: transaction.id });
    } else {
      onSave(transactionData);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 w-full max-w-md">
        <h2 className="text-xl font-bold mb-4">
          {transaction ? 'Editar Transação' : 'Nova Transação'}
        </h2>
        
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">Tipo</label>
            <select
              name="tipo"
              defaultValue={transaction?.receita ? 'receita' : 'despesa'}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
            >
              <option value="receita">Receita</option>
              <option value="despesa">Despesa</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">Nome</label>
            <input
              type="text"
              name="nome"
              defaultValue={transaction?.nome}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">Valor</label>
            <input
              type="number"
              name="valor"
              step="0.01"
              min="0"
              defaultValue={transaction?.valor}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">Categoria</label>
            <select
              name="categoria"
              defaultValue={transaction?.categoria}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
              required
            >
              <option value="">Selecione uma categoria</option>
              <option value="mercado">Mercado</option>
              <option value="casa">Casa</option>
              <option value="alimentação">Alimentação</option>
              <option value="serviço">Serviço</option>
              <option value="lazer">Lazer</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">Data</label>
            <input
              type="date"
              name="data"
              defaultValue={transaction?.data?.split('T')[0] || new Date().toISOString().split('T')[0]}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">Descrição</label>
            <textarea
              name="desc"
              defaultValue={transaction?.desc}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
              rows={3}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">Carteira</label>
            <select
              name="carteira"
              defaultValue={transaction?.carteira}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
              required
            >
              <option value="">Selecione uma carteira</option>
              {carteiras.map((carteira) => (
                <option key={carteira.nome} value={carteira.nome}>
                  {carteira.nome} (R$ {carteira.saldo.toFixed(2)})
                </option>
              ))}
            </select>
          </div>

          <div className="space-y-2">
            <div className="flex items-center">
              <input
                type="checkbox"
                id="isFixo"
                checked={isFixo}
                onChange={(e) => setIsFixo(e.target.checked)}
                className="rounded border-gray-300 text-blue-600"
              />
              <label htmlFor="isFixo" className="ml-2 text-sm font-medium text-gray-700">
                Transação Recorrente
              </label>
            </div>

            {isFixo && (
              <><div>
                <label className="block text-sm font-medium text-gray-700">
                  Número de Repetições
                </label>
                <input
                  type="number"
                  min="1"
                  value={repeticoes}
                  onChange={(e) => setRepeticoes(Number(e.target.value))}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm" />
              </div><div className="flex items-center mt-4">
                  <input
                    type="checkbox"
                    id="isFeita"
                    checked={isFeita}
                    onChange={(e) => setIsFeita(e.target.checked)}
                    className="rounded border-gray-300 text-green-600" />
                  <label htmlFor="isFeita" className="ml-2 text-sm font-medium text-gray-700">
                    Transação já realizada?
                  </label>
                </div></>

            )}
          </div>

          <div className="flex justify-end space-x-2 mt-6">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 border rounded-md hover:bg-gray-100"
            >
              Cancelar
            </button>
            <button
              type="submit"
              className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600"
            >
              {transaction ? 'Salvar' : 'Criar'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}