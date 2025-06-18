

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
    def create(self, nome: str, descricao: str, saldo: float,timer_mes, ultimo_mes_update, ultimo_ano_update, meta_valor,
                movimentacoes: List[int] = []) -> Cofrinho:
        return Cofrinho(nome, descricao, saldo, timer_mes, ultimo_mes_update, ultimo_ano_update, meta_valor, movimentacoes)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> Cofrinho:
        return Cofrinho(
            d['nome'], d['desc'], d['saldo'], d['timer_mes'], d['ultimo_mes_update'], d['ultimo_ano_update'], d.get('meta_valor'), d.get('movimentacoes', [])
        )