"""
carteira_factory.py
-------------------
Fábricas abstratas e concretas para criação de carteiras (Corrente e Cofrinho).
Permite instanciar objetos a partir de parâmetros ou dicionários (para persistência).
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List
import sys
from pathlib import Path

# Add src directory to Python path
src_path = str(Path(__file__).resolve().parent.parent)
if src_path not in sys.path:
    sys.path.append(src_path)
from core.carteira import Carteira, Cofrinho, Corrente


class CarteiraFactory(ABC):
    """
    Classe abstrata para fábricas de carteiras.
    """
    @abstractmethod
    def create(self, nome: str, descricao: str, saldo: float, movimentacoes: List[int]) -> Carteira:
        """Cria uma carteira a partir dos parâmetros fornecidos."""
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, d: Dict[str, Any]) -> Carteira:
        """Cria uma carteira a partir de um dicionário (usado na desserialização)."""
        pass

class CorrenteFactory(CarteiraFactory):
    """
    Fábrica para criar objetos Corrente.
    """
    def create(self, nome: str, descricao: str, saldo: float, movimentacoes: List[int] = []) -> Corrente:
        """Cria uma carteira corrente."""
        return Corrente(nome, descricao, saldo, movimentacoes)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> Corrente:
        """Cria uma carteira corrente a partir de um dicionário."""
        return Corrente(
            d['nome'], d['desc'], d['saldo'], d.get('movimentacoes', [])
        )

class CofrinhoFactory(CarteiraFactory):
    """
    Fábrica para criar objetos Cofrinho.
    """
    def create(self, nome: str, descricao: str, saldo: float,timer_mes, ultimo_mes_update, ultimo_ano_update, meta_valor,
                movimentacoes: List[int] = []) -> Cofrinho:
        """Cria um cofrinho com os parâmetros fornecidos."""
        return Cofrinho(nome, descricao, saldo, timer_mes, ultimo_mes_update, ultimo_ano_update, meta_valor, movimentacoes)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> Cofrinho:
        """Cria um cofrinho a partir de um dicionário."""
        return Cofrinho(
            d['nome'], d['desc'], d['saldo'], d['timer_mes'], d['ultimo_mes_update'], d['ultimo_ano_update'], d.get('meta_valor'), d.get('movimentacoes', [])
        )