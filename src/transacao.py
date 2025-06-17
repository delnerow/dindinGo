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
        self._valor = abs(valor)
        self.categoria = categoria
        self.data = data
        self.desc = desc
        self.carteira = carteira
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
            self.carteira = carteira.get_nome()
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
        self.movimentacoes = movimentacoes

    def get_saldo(self) -> float:
        return self._saldo

    def get_nome(self) -> str:
        return self._nome

    def get_descricao(self) -> str:
        return self._descricao

    def to_dict(self) -> Dict[str, Any]:
        return {
            'nome': self._nome,
            'desc': self._descricao,
            'saldo': self._saldo,
            'movimentacoes': self.movimentacoes
        }
    
    def ajustar_saldo(self, valor_ajuste: float):
        self._saldo += valor_ajuste

    @abstractmethod
    def atualiza_carteira(self, transacao: Transaction):
        """
        Método abstrato para atualizar a carteira com uma transação completa.
        """
        pass

class Cofrinho(Carteira):
    """
    Representa uma conta poupança simples (Cofrinho).
    """
    def __init__(self, nome: str, descricao: str, saldo: float, movimentacoes: List[int] = []):
        super().__init__(nome, descricao, saldo, movimentacoes)

    def quebrar(self) -> float:
        retorno = self._saldo
        self._saldo = 0
        self.movimentacoes.clear()
        return retorno

    def depositar(self, transacao: Transaction):
        if not isinstance(transacao, Transaction):
            raise TypeError("Apenas objetos do tipo Transaction podem ser depositados.")
        
        if isinstance(transacao, Despesa):
            print(f"ERRO: Não é possível adicionar uma Despesa ('{transacao.nome}') a um Cofrinho.")
            return

        self._saldo += transacao.valor
        self.movimentacoes.append(transacao.id)

    def atualiza_carteira(self, transacao: Transaction):
        """
        Implementa o método abstrato herdado de Carteira.
        """
        self.depositar(transacao)

class Corrente(Carteira):
    """
    Representa uma conta corrente que permite receitas e despesas.
    """
    def __init__(self, nome: str, descricao: str, saldo: float, movimentacoes: List[int] = []):
        super().__init__(nome, descricao, saldo, movimentacoes)

    def atualiza_carteira(self, transacao: Transaction):
        """Adiciona o valor de uma transação (receita ou despesa) ao saldo."""
        if not isinstance(transacao, Transaction):
            raise TypeError("Apenas objetos do tipo Transaction podem ser adicionados à carteira.")

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