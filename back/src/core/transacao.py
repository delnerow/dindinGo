"""
transacao.py
------------
Define as classes abstratas e concretas para transações financeiras: Transaction, Receita e Despesa.
Inclui métodos para serialização e manipulação de valores.
"""
from __future__ import annotations
from abc import ABC
from typing import  Dict, Any


import sys
from pathlib import Path

# Add src directory to Python path
src_path = str(Path(__file__).resolve().parent.parent)
if src_path not in sys.path:
    sys.path.append(src_path)


class Transaction(ABC):
    """
    Classe abstrata que representa uma transação financeira.
    """
    def __init__(self, id: int, nome: str, valor: float, categoria: str, data: str, desc: str, carteira: str,  rep :int =1, done : bool = False):
        self.id = id
        self.nome = nome
        self._valor = abs(valor)
        self.categoria = categoria
        self.data = data
        self.desc = desc
        self.carteira = carteira
        self.rep = rep
        self.done = done

    @property
    def valor(self) -> float:
        """
        Retorna o valor da transação. Negativo para Despesa, positivo para Receita.
        """
        return self._valor if isinstance(self, Receita) else -self._valor

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
            'repeticao': self.rep,
            "feita": self.done,
        }

class Receita(Transaction):
    """Representa uma transação de entrada de dinheiro."""
    def __init__(self, id: int, nome: str, valor: float, categoria: str, data: str, desc: str, carteira: str, rep :int =1, done: bool = False):
        super().__init__(id, nome, valor, categoria, data, desc, carteira, rep, done)

class Despesa(Transaction):
    """Representa uma transação de saída de dinheiro."""
    def __init__(self, id: int, nome: str, valor: float, categoria: str, data: str, desc: str, carteira: str,  rep :int =1, done: bool = False):
        super().__init__(id, nome, valor, categoria, data, desc, carteira, rep, done)