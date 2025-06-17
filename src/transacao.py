from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Dict, Any
import datetime

# ==================================
# 1. Classes do Modelo Principal
# ==================================

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
from sistemaDePontos import SistemaDePontos

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
    def __init__(self, nome: str, descricao: str, saldo: float,
                timer_mes: int, ultimo_mes_update: int, ultimo_ano_update: int,
                movimentacoes: List[int] = []):
        super().__init__(nome, descricao, saldo, movimentacoes)
        self._timer_mes = timer_mes
        self._ultimo_mes_update = ultimo_mes_update
        self._ultimo_ano_update = ultimo_ano_update

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
        transacao.done = True 
        self._saldo += transacao.valor
        self.movimentacoes.append(transacao.id)

    def atualiza_carteira(self, transacao: Transaction):
        """
        Implementa o método abstrato herdado de Carteira.
        """
        self.depositar(transacao)

    def get_timer(self):
        """
        Retorna o timer do cofre, quando pode ser quebrado sem
        penalidade alguma.
        """
        return self._timer_mes
    
    def inicializar(self):
        #verificar se deve atualizar o timer_mes
        hoje = datetime.datetime.now()
        mes_atual = hoje.month
        ano_atual = hoje.year
        if self._ultimo_mes_update == mes_atual and self._ultimo_ano_update == ano_atual:
            # timer está atualizado
            pass
        else:
            if ano_atual == self._ultimo_ano_update:
                # mesmo ano, apenas atualizar o mês
                self._timer_mes -= mes_atual - self._ultimo_mes_update
                self._ultimo_mes_update = mes_atual
            else:
                # ano diferente, corrigir o ano
                while self._ultimo_ano_update != ano_atual:
                    self._ultimo_ano_update += 1
                    self._timer_mes -= 12
                # corrigir o mês
                self._timer_mes -= mes_atual - self._ultimo_mes_update
                self._ultimo_mes_update = mes_atual
        # garantir que o self._timer_mes não fique negativo
        self._timer_mes = 0 if self._timer_mes < 0 else self._timer_mes



    def to_dict(self) -> Dict[str, Any]:
        return {
            'nome': self._nome,
            'desc': self._descricao,
            'saldo': self._saldo,
            "timer_mes": self._timer_mes,
            "ultimo_mes_update": self._ultimo_mes_update,
            "ultimo_ano_update": self._ultimo_ano_update,
            'movimentacoes': self.movimentacoes
        }
    
class Corrente(Carteira):
    """
    Representa uma conta corrente que permite receitas e despesas.
    """
    def __init__(self, nome: str, descricao: str, saldo: float, movimentacoes: List[int] = []):
        super().__init__(nome, descricao, saldo, movimentacoes)

    def atualiza_carteira(self, transacao: Transaction, pontos_manager: SistemaDePontos =None ):
        """Adiciona o valor de uma transação (receita ou despesa) ao saldo e chama o sistema de pontos."""
        if not isinstance(transacao, Transaction):
            raise TypeError("Apenas objetos do tipo Transaction podem ser adicionados à carteira.")
        transacao.done = True 
        self._saldo += transacao.valor
        self.movimentacoes.append(transacao.id)
        pontos_manager.adicionar_despesa(transacao.valor, transacao.categoria)

# ==================================
# 2. Classes de Fábrica (Factories)
# ==================================

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
    def create_transaction(self, id: int, nome: str, valor: float, categoria: str, data: str, desc: str, carteira: str, fixo: bool = False, rep: int = 1, done: bool = False) -> Despesa:
        return Despesa(id, nome, valor, categoria, data, desc, carteira, rep, done)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> Despesa:
        return Despesa(
            d['id'], d['nome'], d['valor'], d['categoria'],
            d['data'], d['desc'], d['carteira'], d['repeticao'],d.get('feita')
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
    def create(self, nome: str, descricao: str, saldo: float,timer_mes, ultimo_mes_update, ultimo_ano_update,
                movimentacoes: List[int] = []) -> Cofrinho:
        return Cofrinho(nome, descricao, saldo, timer_mes, ultimo_mes_update, ultimo_ano_update,movimentacoes)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> Cofrinho:
        return Cofrinho(
            d['nome'], d['desc'], d['saldo'], d['timer_mes'], d['ultimo_mes_update'], d['ultimo_ano_update'], d.get('movimentacoes', [])
        )