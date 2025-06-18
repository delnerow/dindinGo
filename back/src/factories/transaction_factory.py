

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
    @abstractmethod
    def create_transaction(self, id: int, nome: str, valor: float, categoria: str, data: str, desc: str, carteira: str,  rep: int, done: bool) -> Transaction:
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, d: Dict[str, Any]) -> Transaction:
        pass

class ReceitaFactory(TransactionFactory):
    def create_transaction(self, id: int, nome: str, valor: float, categoria: str, data: str, desc: str, carteira: str,  rep: int = 1, done: bool = False) -> Receita:
        return Receita(id, nome, valor, categoria, data, desc, carteira, rep, done)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> Receita:
        return Receita(
            d['id'], d['nome'], d['valor'], d['categoria'],
            d['data'], d['desc'], d['carteira'], d['repeticao'],d.get('feita')
        )

class DespesaFactory(TransactionFactory):
    def create_transaction(self, id: int, nome: str, valor: float, categoria: str, data: str, desc: str, carteira: str,  rep: int = 1, done: bool = False) -> Despesa:
        return Despesa(id, nome, valor, categoria, data, desc, carteira, rep, done)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> Despesa:
        return Despesa(
            d['id'], d['nome'], d['valor'], d['categoria'],
            d['data'], d['desc'], d['carteira'], d['repeticao'],d.get('feita')
        )
