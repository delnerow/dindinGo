import { Transaction } from '../types/Transaction';
import { X } from 'lucide-react';

interface EditTransactionModalProps {
  transaction: Transaction;
  isOpen: boolean;
  onClose: () => void;
  onSave: (updatedTransaction: Transaction) => void;
}

export function EditTransactionModal({ transaction, isOpen, onClose, onSave }: EditTransactionModalProps) {
  if (!isOpen) return null;

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    
    const updatedTransaction: Transaction = {
      ...transaction,
      nome: formData.get('nome') as string,
      valor: Number(formData.get('valor')),
      categoria: formData.get('categoria') as string,
      data: formData.get('data') as string,
      desc: formData.get('desc') as string,
      carteira: formData.get('carteira') as string,
      repeticao: formData.get('repeticao') === 'true',
    };

    onSave(updatedTransaction);
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 w-full max-w-md">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-bold">Editar Transação</h2>
          <button onClick={onClose} className="p-2">
            <X className="w-5 h-5" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">Nome</label>
            <input
              type="text"
              name="nome"
              defaultValue={transaction.nome}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">Valor</label>
            <input
              type="number"
              name="valor"
              defaultValue={Math.abs(transaction.valor)}
              step="0.01"
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">Categoria</label>
            <select
              name="categoria"
              defaultValue={transaction.categoria}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            >
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
              defaultValue={transaction.data.split('T')[0]}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">Descrição</label>
            <textarea
              name="desc"
              defaultValue={transaction.desc}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">Recorrente</label>
            <input
              type="checkbox"
              name="repeticao"
              defaultChecked={transaction.repeticao}
              className="mt-1 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
            />
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
              Salvar
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}