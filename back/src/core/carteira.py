"""
carteira.py
-----------
Define as classes abstratas e concretas para carteiras do sistema: Carteira, Corrente e Cofrinho.
Inclui métodos para manipulação de saldo, movimentações e integração com o sistema de pontos.
"""

from abc import ABC, abstractmethod
import datetime
from typing import Any, Dict, List
import sys
from pathlib import Path

# Add src directory to Python path
src_path = str(Path(__file__).resolve().parent.parent)
if src_path not in sys.path:
    sys.path.append(src_path)

from core.sistemaDePontos import SistemaDePontos

from core.transacao import  Transaction
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
        """Retorna o saldo atual da carteira."""
        return self._saldo

    def get_nome(self) -> str:
        """Retorna o nome da carteira."""
        return self._nome

    def get_descricao(self) -> str:
        """Retorna a descrição da carteira."""
        return self._descricao

    def to_dict(self) -> Dict[str, Any]:
        """Converte a carteira para um dicionário (serialização)."""
        return {
            'nome': self._nome,
            'desc': self._descricao,
            'saldo': self._saldo,
            'movimentacoes': self.movimentacoes
        }
    
    def ajustar_saldo(self, valor_ajuste: float):
        """Ajusta o saldo da carteira pelo valor fornecido."""
        self._saldo = self._saldo + valor_ajuste

    @abstractmethod
    def atualiza_carteira(self, transacao: Transaction):
        """
        Método abstrato para atualizar a carteira com uma transação completa.
        """
        pass
from core.transacao import  Despesa
class Cofrinho(Carteira):
    """
    Representa uma conta poupança simples (Cofrinho).
    """
    def __init__(self, nome: str, descricao: str, saldo: float,
                timer_mes: int, ultimo_mes_update: int, ultimo_ano_update: int, meta_valor: float,
                movimentacoes: List[int] = []):
        super().__init__(nome, descricao, saldo, movimentacoes)
        self._timer_mes = timer_mes
        self._ultimo_mes_update = ultimo_mes_update
        self._ultimo_ano_update = ultimo_ano_update
        self.meta_valor = meta_valor  # Valor alvo para o cofre

    def quebrar(self) -> float:
        """Quebra o cofrinho, zerando o saldo e limpando as movimentações."""
        retorno = self._saldo
        self._saldo = 0
        self.movimentacoes.clear()
        return retorno

    def depositar(self, transacao: Transaction):
        """Deposita uma transação do tipo Receita no cofrinho."""
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
        """
        Atualiza o timer do cofrinho de acordo com o mês e ano atuais.
        """
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
        """Converte o cofrinho para um dicionário (serialização)."""
        return {
            'nome': self._nome,
            'desc': self._descricao,
            'saldo': self._saldo,
            "timer_mes": self._timer_mes,
            "ultimo_mes_update": self._ultimo_mes_update,
            "ultimo_ano_update": self._ultimo_ano_update,
            'meta_valor': self.meta_valor,
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
        print("Add!")
        if pontos_manager is not None:
            pontos_manager.adicionar_despesa(transacao.valor, transacao.categoria)

        
