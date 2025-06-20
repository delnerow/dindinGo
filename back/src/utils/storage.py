"""
storage.py
----------
Gerencia a persistência dos dados do sistema (transações, carteiras, cofrinhos, pontos) usando o padrão Singleton.
Inclui métodos para carregar, salvar e manipular dados no arquivo JSON.
"""
import json
from typing import List, Optional
import os
import sys
from pathlib import Path

# Add src directory to Python path
src_path = str(Path(__file__).resolve().parent.parent)
if src_path not in sys.path:
    sys.path.append(src_path)

# Importe suas classes do modelo e fábricas
from core.transacao import Transaction
from core.carteira import Carteira, Cofrinho
from factories.carteira_factory import CofrinhoFactory, CorrenteFactory
from factories.transaction_factory import DespesaFactory, ReceitaFactory

from core.sistemaDePontos import SistemaDePontos

class StorageManager:
    """
    Implementação do padrão Singleton para gerenciar a persistência de dados.
    """
    _instance: Optional['StorageManager'] = None
    # Update DATA_FILE to use absolute path from project root
    current_path = Path(__file__).resolve()
    project_root = None
            
            # Navigate up until we find dindinGo folder
    for parent in current_path.parents:
        if parent.name == 'dindinGo':
            project_root = parent
            break
            
    if not project_root:
        raise RuntimeError("Could not find project root (dindinGo folder)")
            
    # Set data file path
    DATA_FILE = project_root / 'data' / 'data.json'
    print(f"Data file path: {DATA_FILE}")
    
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
        self.pontos_manager: SistemaDePontos = SistemaDePontos(pontos=0)
        self.cur_id: int = 0
        
        self._load_data()

    def _load_data(self):
        """Carrega os dados do arquivo JSON para a memória da instância."""
        try:
            print(f"Loading data from: {self.DATA_FILE}")  # Debug log
            
            if not os.path.exists(self.DATA_FILE):
                print(f"Data file not found at: {self.DATA_FILE}")
                default_data = {
                    'idGenerator': 0,
                    'transacoes': [],
                    'carteiras': [],
                    'cofrinhos': [],
                    'pontos': [{
                        'pontos': 0,
                        'meta_lazer': 0,
                        'meta_alimentacao': 0,
                        'meta_casa': 0,
                        'meta_mercado': 0,
                        'meta_servico': 0,
                        'gastos_lazer': 0,
                        'gastos_alimentacao': 0,
                        'gastos_casa': 0,
                        'gastos_mercado': 0,
                        'gastos_servico': 0
                    }]
                }
                with open(self.DATA_FILE, 'w', encoding='utf-8') as file:
                    json.dump(default_data, file, indent=4)
                print(f"Arquivo de dados recriado em: {self.DATA_FILE}")
                # Agora tente recarregar os dados
                self._load_data()

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
                    self.pontos_manager = SistemaDePontos.from_dict(pontos_data[0])
            
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
        """Retorna a lista de cofrinhos cadastrados."""
        return self.cofrinhos

    def get_carteiras(self) -> List[Carteira]:
        """Retorna a lista de carteiras cadastradas."""
        return self.carteiras
        
    def get_all_transactions(self) -> List[Transaction]:
        """Retorna todas as transações cadastradas."""
        return self.transacoes
    
    def get_pontos_manager(self) -> SistemaDePontos:
        """Retorna o gerenciador de pontos do sistema."""
        return self.pontos_manager

    def get_next_id(self) -> int:
        """Gera e retorna um novo ID único."""
        self.cur_id += 1
        return self.cur_id

    def add_transaction(self, transaction: Transaction):
        """Adiciona uma nova transação ao sistema."""
        self.transacoes.append(transaction)

    def add_carteira(self, carteira: Carteira):
        """Adiciona uma nova carteira ao sistema e salva os dados."""
        self.carteiras.append(carteira)
        self.save_data()
        
    def add_cofrinho(self, cofrinho: Cofrinho):
        """Adiciona um novo cofrinho ao sistema e salva os dados."""
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
    def remove_carteira(self, carteira: Carteira) -> bool:
        """
        Remove uma carteira do storage.
        """
        try:
            self.carteiras = [c for c in self.carteiras if c.get_nome() != carteira.get_nome()]
            return True
        except Exception:
            return False