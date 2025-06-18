import { useState, useEffect } from 'react';
import { Transaction } from '../types/Transaction';

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
  
  // Função para formatar a data para o input date
  const formatDateForInput = (dateString: string): string => {
    if (!dateString) return new Date().toISOString().split('T')[0];
    
    // Se a data já está no formato YYYY-MM-DD, retorna como está
    if (dateString.match(/^\d{4}-\d{2}-\d{2}$/)) {
      return dateString;
    }
    
    // Se tem timestamp, extrai apenas a data
    if (dateString.includes('T')) {
      return dateString.split('T')[0];
    }
    
    // Se é apenas uma data, tenta converter
    try {
      const date = new Date(dateString);
      return date.toISOString().split('T')[0];
    } catch {
      return new Date().toISOString().split('T')[0];
    }
  };

  const [formData, setFormData] = useState({
    nome: transaction?.nome || '',
    valor: transaction?.valor || 0,
    categoria: transaction?.categoria || '',
    data: formatDateForInput(transaction?.data || ''),
    desc: transaction?.desc || '',
    carteira: transaction?.carteira || '',
    tipo: transaction?.receita ? 'receita' : 'despesa'
  });

  // Atualiza o formData quando a transação muda
  useEffect(() => {
    if (transaction) {
      setFormData({
        nome: transaction.nome,
        valor: transaction.valor,
        categoria: transaction.categoria,
        data: formatDateForInput(transaction.data),
        desc: transaction.desc,
        carteira: transaction.carteira,
        tipo: transaction.receita ? 'receita' : 'despesa'
      });
      setIsFixo(transaction.repeticao > 0);
      setRepeticoes(transaction.repeticao || 1);
      setIsFeita(transaction.feita || false);
    } else {
      setFormData({
        nome: '',
        valor: 0,
        categoria: '',
        data: new Date().toISOString().split('T')[0],
        desc: '',
        carteira: '',
        tipo: 'despesa'
      });
      setIsFixo(false);
      setRepeticoes(1);
      setIsFeita(false);
    }
  }, [transaction]);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    
    const transactionData: NewTransaction = {
      nome: formData.nome,
      valor: Number(formData.valor),
      categoria: formData.categoria,
      data: formData.data,
      desc: formData.desc,
      carteira: formData.carteira,
      repeticao: isFixo ? repeticoes : 0,
      receita: formData.tipo === 'receita',
      feita: isFixo ? isFeita : false
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
              value={formData.tipo}
              onChange={handleInputChange}
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
              value={formData.nome}
              onChange={handleInputChange}
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
              value={formData.valor}
              onChange={handleInputChange}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">Categoria</label>
            <select
              name="categoria"
              value={formData.categoria}
              onChange={handleInputChange}
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
              value={formData.data}
              onChange={handleInputChange}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">Descrição</label>
            <textarea
              name="desc"
              value={formData.desc}
              onChange={handleInputChange}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
              rows={3}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">Carteira</label>
            <select
              name="carteira"
              value={formData.carteira}
              onChange={handleInputChange}
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