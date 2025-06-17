from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Dict, Any

# ==================================
# 1. Classes do Modelo Principal
# ==================================

class Transaction(ABC):
    """
    Classe abstrata que representa uma transação financeira.
    """
    def __init__(self, id: int, nome: str, valor: float, categoria: str, data: str, desc: str, carteira: str, fixo: bool = False):
        self.id = id
        self.nome = nome
        self._valor = abs(valor)  # Armazena sempre um valor positivo
        self.categoria = categoria
        self.data = data
        self.desc = desc
        self.carteira = carteira # Nome/ID da carteira associada
        self.fixo = fixo

    @property
    def valor(self) -> float:
        """
        Retorna o valor da transação. Negativo para Despesa, positivo para Receita.
        """
        return self._valor if isinstance(self, Receita) else -self._valor

    def set_carteira(self, carteira: Carteira):
        """
        Define a qual objeto Carteira esta transação pertence.
        """
        if isinstance(carteira, Carteira):
            self.carteira = carteira.getNome()
        else:
            raise TypeError("O argumento 'carteira' deve ser uma instância de Carteira.")

    def to_dict(self) -> Dict[str, Any]:
        """
        Converte o objeto Transaction para um dicionário (serialização).
        """
        return {
            'id': self.id,
            'receita': isinstance(self, Receita),
            'nome': self.nome,
            'valor': self._valor,
            'categoria': self.categoria,
            'data': self.data,
            'desc': self.desc,
            'carteira': self.carteira,
            'repeticao': self.fixo
        }

class Receita(Transaction):
    """Representa uma transação de entrada de dinheiro."""
    def __init__(self, id: int, nome: str, valor: float, categoria: str, data: str, desc: str, carteira: str, repeticao: bool = False):
        super().__init__(id, nome, valor, categoria, data, desc, carteira, repeticao)

class Despesa(Transaction):
    """Representa uma transação de saída de dinheiro."""
    def __init__(self, id: int, nome: str, valor: float, categoria: str, data: str, desc: str, carteira: str, repeticao: bool = False):
        super().__init__(id, nome, valor, categoria, data, desc, carteira, repeticao)


class Carteira(ABC):
    """
    Classe abstrata que representa uma carteira ou conta.
    """
    def __init__(self, nome: str, descricao: str, saldo: float, movimentacoes: List[int] = []):
        self._nome = nome
        self._descricao = descricao
        self._saldo = saldo
        self.movimentacoes = movimentacoes  # Lista para armazenar IDs de transações

    def getSaldo(self) -> float:
        return self._saldo

    def getNome(self) -> str:
        return self._nome

    def getDescricao(self) -> str:
        return self._descricao

    def to_dict(self) -> Dict[str, Any]:
        """
        Converte o objeto Carteira para um dicionário (serialização).
        """
        return {
            'nome': self._nome,
            'desc': self._descricao,
            'saldo': self._saldo,
            'movimentacoes': self.movimentacoes
        }
    
    def ajustar_saldo(self, valor_ajuste: float):
        """
        Ajusta diretamente o saldo da carteira.
        Usado para correções ou edições de transações.
        """
        self._saldo += valor_ajuste

    @abstractmethod
    def atualizaCarteira(self, transacao: Transaction):
        """
        Método abstrato para atualizar a carteira com uma transação completa.
        As subclasses (Corrente, Cofrinho) devem implementar sua própria lógica.
        """
        pass

class Cofrinho(Carteira):
    """
    Representa uma conta poupança simples (Cofrinho).
    Não pode ter despesas diretas, apenas depósitos (Receitas).
    """
    def __init__(self, nome: str, descricao: str, saldo: float, movimentacoes: List[int] = []):
        super().__init__(nome, descricao, saldo, movimentacoes)

    def quebrar(self) -> float:
        """Zera o saldo do cofrinho e retorna o valor que havia nele."""
        retorno = self._saldo
        self._saldo = 0
        self.movimentacoes.clear() # Limpa o histórico ao quebrar
        return retorno

    def depositar(self, transacao: Transaction):
        """Adiciona uma transação a este cofrinho."""
        if not isinstance(transacao, Transaction):
            raise TypeError("Apenas objetos do tipo Transaction podem ser depositados.")
        
        if isinstance(transacao, Despesa):
            print(f"ERRO: Não é possível adicionar uma Despesa ('{transacao.nome}') a um Cofrinho.")
            return

        # O valor da transação já é positivo para Receita
        self._saldo += transacao.valor
        self.movimentacoes.append(transacao.id)

    def atualizaCarteira(self, transacao: Transaction):
        """
        Implementa o método abstrato herdado de Carteira.
        Para um Cofrinho, a lógica é a mesma de um depósito.
        """
        # Reutiliza a lógica já existente no método depositar
        self.depositar(transacao)

class Corrente(Carteira):
    """
    Representa uma conta corrente que permite receitas e despesas.
    """
    def __init__(self, nome: str, descricao: str, saldo: float, movimentacoes: List[int] = []):
        super().__init__(nome, descricao, saldo, movimentacoes)

    def atualizaCarteira(self, transacao: Transaction):
        """Adiciona uma transação (receita ou despesa) à conta corrente."""
        if not isinstance(transacao, Transaction):
            raise TypeError("Apenas objetos do tipo Transaction podem ser adicionados à carteira.")

        # O método .valor já retorna o valor com o sinal correto (+/-)
        self._saldo += transacao.valor
        self.movimentacoes.append(transacao.id)

# ==================================
# 2. Classes de Fábrica (Factories)
# ==================================

class TransactionFactory(ABC):
    @abstractmethod
    def create_transaction(self, id: int, nome: str, valor: float, categoria: str, data: str, desc: str, carteira: str, repeticao: bool) -> Transaction:
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, d: Dict[str, Any]) -> Transaction:
        pass

class ReceitaFactory(TransactionFactory):
    def create_transaction(self, id: int, nome: str, valor: float, categoria: str, data: str, desc: str, carteira: str, repeticao: bool = False) -> Receita:
        return Receita(id, nome, valor, categoria, data, desc, carteira, repeticao)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> Receita:
        return Receita(
            d['id'], d['nome'], d['valor'], d['categoria'],
            d['data'], d['desc'], d['carteira'], d.get('repeticao', False)
        )

class DespesaFactory(TransactionFactory):
    def create_transaction(self, id: int, nome: str, valor: float, categoria: str, data: str, desc: str, carteira: str, repeticao: bool = False) -> Despesa:
        return Despesa(id, nome, valor, categoria, data, desc, carteira, repeticao)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> Despesa:
        return Despesa(
            d['id'], d['nome'], d['valor'], d['categoria'],
            d['data'], d['desc'], d['carteira'], d.get('repeticao', False)
        )

class CarteiraFactory(ABC):
    @abstractmethod
    def create(self, nome: str, descricao: str, saldo: float, movimentacoes: List[int]) -> Carteira:
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, d: Dict[str, Any]) -> Carteira:
        pass

class CorrenteFactory(CarteiraFactory):
    def create(self, nome: str, descricao: str, saldo: float, movimentacoes: List[int] = []) -> Corrente:
        return Corrente(nome, descricao, saldo, movimentacoes)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> Corrente:
        return Corrente(
            d['nome'], d['desc'], d['saldo'], d.get('movimentacoes', [])
        )

class CofrinhoFactory(CarteiraFactory):
    def create(self, nome: str, descricao: str, saldo: float, movimentacoes: List[int] = []) -> Cofrinho:
        return Cofrinho(nome, descricao, saldo, movimentacoes)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> Cofrinho:
        return Cofrinho(
            d['nome'], d['desc'], d['saldo'], d.get('movimentacoes', [])
        )