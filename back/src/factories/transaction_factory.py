"""
transaction_factory.py
---------------------
Fábricas abstratas e concretas para criação de transações (Receita e Despesa).
Permite instanciar objetos a partir de parâmetros ou dicionários (para persistência).
"""

from abc import ABC, abstractmethod
from typing import Any, Dict

import sys
from pathlib import Path

# Add src directory to Python path
src_path = str(Path(__file__).resolve().parent.parent)
if src_path not in sys.path:
    sys.path.append(src_path)

from core.transacao import Despesa, Receita, Transaction


class TransactionFactory(ABC):
    """
    Classe abstrata para fábricas de transações.
    """
    @abstractmethod
    def create_transaction(self, id: int, nome: str, valor: float, categoria: str, data: str, desc: str, carteira: str,  rep: int, done: bool) -> Transaction:
        """Cria uma transação a partir dos parâmetros fornecidos."""
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, d: Dict[str, Any]) -> Transaction:
        """Cria uma transação a partir de um dicionário (usado na desserialização)."""
        pass

class ReceitaFactory(TransactionFactory):
    """
    Fábrica para criar objetos Receita.
    """
    def create_transaction(self, id: int, nome: str, valor: float, categoria: str, data: str, desc: str, carteira: str,  rep: int = 1, done: bool = False) -> Receita:
        """Cria uma transação do tipo Receita."""
        return Receita(id, nome, valor, categoria, data, desc, carteira, rep, done)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> Receita:
        """Cria uma receita a partir de um dicionário."""
        return Receita(
            d['id'], d['nome'], d['valor'], d['categoria'],
            d['data'], d['desc'], d['carteira'], d['repeticao'],d.get('feita')
        )

class DespesaFactory(TransactionFactory):
    """
    Fábrica para criar objetos Despesa.
    """
    def create_transaction(self, id: int, nome: str, valor: float, categoria: str, data: str, desc: str, carteira: str,  rep: int = 1, done: bool = False) -> Despesa:
        """Cria uma transação do tipo Despesa."""
        return Despesa(id, nome, valor, categoria, data, desc, carteira, rep, done)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> Despesa:
        """Cria uma despesa a partir de um dicionário."""
        return Despesa(
            d['id'], d['nome'], d['valor'], d['categoria'],
            d['data'], d['desc'], d['carteira'], d['repeticao'],d.get('feita')
        )
