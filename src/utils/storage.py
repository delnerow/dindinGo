import json
from typing import List, Optional
import os

# Importe suas classes do modelo e fábricas
from transacao import Transaction, Carteira, Cofrinho, ReceitaFactory, DespesaFactory, CorrenteFactory, CofrinhoFactory
from sistemaDePontos import sistemaDePontos

class StorageManager:
    """
    Implementação do padrão Singleton para gerenciar a persistência de dados.
    """
    _instance: Optional['StorageManager'] = None
    # Update DATA_FILE to use absolute path from project root
    DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data.json')

    def __new__(cls) -> 'StorageManager':
        if cls._instance is None:
            cls._instance = super(StorageManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        
        self.transacoes: List[Transaction] = []
        self.carteiras: List[Carteira] = []
        self.cofrinhos: List[Cofrinho] = []
        self.pontos_manager: sistemaDePontos = sistemaDePontos(pontos=0)
        self.cur_id: int = 0
        
        self._load_data()

    def _load_data(self):
        """Carrega os dados do arquivo JSON para a memória da instância."""
        try:
            print(f"Loading data from: {self.DATA_FILE}")  # Debug log
            
            if not os.path.exists(self.DATA_FILE):
                print(f"Data file not found at: {self.DATA_FILE}")
                return False

            with open(self.DATA_FILE, 'r', encoding='utf-8') as file:
                data = json.load(file)
                print(f"Successfully loaded data with {len(data.get('transacoes', []))} transactions")
                self.cur_id = data.get('idGenerator', 0)
                
                for t_data in data.get('transacoes', []):
                    factory = ReceitaFactory if t_data.get('receita') else DespesaFactory
                    self.transacoes.append(factory.from_dict(t_data))
                
                for c_data in data.get('carteiras', []):
                    self.carteiras.append(CorrenteFactory.from_dict(c_data))

                for c_data in data.get('cofrinhos', []):
                    self.cofrinhos.append(CofrinhoFactory.from_dict(c_data))
                
                pontos_data = data.get('pontos')
                if pontos_data:
                    self.pontos_manager = sistemaDePontos.from_dict(pontos_data[0])
            
            #update dos cofrinhos na inicialização do sistema
            for cofre in self.cofrinhos:
                cofre.inicializar()
            
            self.save_data()  # Salva os dados carregados para garantir consistência

        except (FileNotFoundError, json.JSONDecodeError):
            print("Arquivo de dados não encontrado ou corrompido. Iniciando com estado limpo.")
            pass

    def save_data(self):
        """Salva o estado atual da memória para o arquivo JSON."""
        data = {
            'idGenerator': self.cur_id,
            'transacoes': [t.to_dict() for t in self.transacoes],
            'carteiras': [c.to_dict() for c in self.carteiras],
            'cofrinhos': [c.to_dict() for c in self.cofrinhos],
            'pontos': [self.pontos_manager.to_dict()] 
        }
        with open(self.DATA_FILE, 'w') as file:
            json.dump(data, file, indent=4)

    def get_cofrinhos(self) -> List[Cofrinho]:
        return self.cofrinhos

    def get_carteiras(self) -> List[Carteira]:
        return self.carteiras
        
    def get_all_transactions(self) -> List[Transaction]:
        return self.transacoes
    
    def get_pontos_manager(self) -> sistemaDePontos:
        return self.pontos_manager

    def get_next_id(self) -> int:
        """Gera e retorna um novo ID único."""
        self.cur_id += 1
        return self.cur_id

    def add_transaction(self, transaction: Transaction):
        self.transacoes.append(transaction)

    def add_carteira(self, carteira: Carteira):
        self.carteiras.append(carteira)
        self.save_data()
        
    def add_cofrinho(self, cofrinho: Cofrinho):
        self.cofrinhos.append(cofrinho)
        self.save_data()
        
    def remove_transaction(self, transaction_id: int) -> bool:
        """
        Remove uma transação pelo ID.
        
        Args:
            transaction_id: ID of the transaction to remove
            
        Returns:
            bool: True if transaction was removed, False if not found
        """
        original_length = len(self.transacoes)
        self.transacoes = [t for t in self.transacoes if t.id != transaction_id]
        
        if len(self.transacoes) < original_length:
            self.save_data()
            return True
        return False