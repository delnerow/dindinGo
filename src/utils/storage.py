import json
from typing import List, Optional

# Importe suas classes
from transacao import Transaction, Carteira, Cofrinho, ReceitaFactory, DespesaFactory, CorrenteFactory, CofrinhoFactory
from sistemaDePontos import sistemaDePontos # Certifique-se de que este import está correto

class StorageManager:
    # ... (o __new__ e o início do __init__ continuam iguais) ...
    _instance: Optional['StorageManager'] = None
    DATA_FILE = 'data.json'

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
        # Inicializa o sistema de pontos com um valor padrão
        self.pontos_manager: sistemaDePontos = sistemaDePontos(pontos=0)
        self.curId: int = 0
        
        self._load_data()

    def _load_data(self):
        """Carrega os dados do arquivo JSON para a memória da instância."""
        try:
            with open(self.DATA_FILE, 'r') as file:
                data = json.load(file)
                self.curId = data.get('idGenerator', 0)
                
                # ... (lógica para carregar transacoes, carteiras, cofrinhos continua igual) ...
                for t_data in data.get('transacoes', []):
                    factory = ReceitaFactory if t_data.get('receita') else DespesaFactory
                    self.transacoes.append(factory.from_dict(t_data))
                
                for c_data in data.get('carteiras', []):
                    self.carteiras.append(CorrenteFactory.from_dict(c_data))

                for c_data in data.get('cofrinhos', []):
                    self.cofrinhos.append(CofrinhoFactory.from_dict(c_data))
                
                # --- LÓGICA PARA CARREGAR O SISTEMA DE PONTOS ---
                pontos_data = data.get('pontos')
                if pontos_data:
                    # Assumindo que o sistema de pontos tem um método from_dict
                    self.pontos_manager = sistemaDePontos.from_dict(pontos_data[0])

        except (FileNotFoundError, json.JSONDecodeError):
            print("Arquivo de dados não encontrado ou corrompido. Iniciando com estado limpo.")
            pass

    def save_data(self):
        """Salva o estado atual da memória para o arquivo JSON."""
        data = {
            'idGenerator': self.curId,
            'transacoes': [t.to_dict() for t in self.transacoes],
            'carteiras': [c.to_dict() for c in self.carteiras],
            'cofrinhos': [c.to_dict() for c in self.cofrinhos],
            # --- LÓGICA PARA SALVAR O SISTEMA DE PONTOS ---
            'pontos': [self.pontos_manager.to_dict()] 
        }
        with open(self.DATA_FILE, 'w') as file:
            json.dump(data, file, indent=4)

    # --- MÉTODOS DE ACESSO (GETTERS) ---

    def get_pontos_manager(self) -> sistemaDePontos: # <<< O MÉTODO QUE FALTAVA
        """Retorna o objeto gerenciador de pontos."""
        return self.pontos_manager

    # ... (os outros getters e adders continuam aqui) ...
    def get_cofrinhos(self) -> List[Cofrinho]:
        return self.cofrinhos

    def get_carteiras(self) -> List[Carteira]:
        return self.carteiras
        
    def get_all_transactions(self) -> List[Transaction]:
        return self.transacoes
    
    def get_next_id(self) -> int:
        self.curId += 1
        return self.curId

    def add_transaction(self, transaction: Transaction):
        self.transacoes.append(transaction)

    def add_carteira(self, carteira: Carteira):
        self.carteiras.append(carteira)
        self.save_data()
        
    def add_cofrinho(self, cofrinho: Cofrinho):
        self.cofrinhos.append(cofrinho)
        self.save_data()