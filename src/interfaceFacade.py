import datetime
import os

from carteiraActions import criarCarteira, criarCofrinho
from utils.printers import printCarteiras, printCofrinhos, printTransacoes
from utils.filters import filtra_transacoes_mes
from utils.storage import load_data, save_data
from transActions import criar_transacao, editar_transacao
from transacao import  Despesa, Receita

class GerenciamentoDeCarteiras:
    def __init__(self):
        transacoes, carteiras, cofrinhos, pontos = load_data()
        self._transacoes = transacoes
        self._carteiras = carteiras
        self._cofrinhos = cofrinhos
        self._mes_atual = datetime.datetime.now().month
        self._ano_atual = datetime.datetime.now().year
        self._transacoes_mes = self.filtrar_transacoes_mes()
        #vetor com um único sistema de pontos
        #para acessar usar pontos[0] 
        self._pontos = pontos 

    def adicionar_receita(self,nome,valor, tipo, data, desc,carteira,modo,fixo=False):
        """Adiciona uma receita à lista de transações."""

        #verifica erro
        if self.erro_add_transacao(nome, valor, tipo, data, desc, carteira, modo, fixo):
            return
        
        # Cria a receita e adiciona à lista de transações
        print("tamanho transacoes:", len(self._transacoes)) #debug

        trans = Receita(nome, valor, tipo, data, desc, carteira, modo, fixo)
        
        print("tamanho transacoes apos criar receita:", len(self._transacoes)) #debug

        self._transacoes.append(trans)
        # Atualiza a carteira associada
        self.atualizar_carteira(valor, carteira)
        # Salva os dados
        self.salvar_dados()

        
    def adicionar_despesa(self,nome,valor, tipo, data, desc,carteira,modo,fixo=False):
        """Adiciona uma despesa à lista de transações. e atribuir pontuação, 
        retorna pontos perdidos, gasto e meta da categoria da despesa."""
        
        #verifica erro
        if self.erro_add_transacao(nome, valor, tipo, data, desc, carteira, modo, fixo):
            return
        
        # Cria a receita e adiciona à lista de transações
        despesa = Despesa(nome, valor, tipo, data, desc, carteira, modo, fixo)
        self._transacoes.append(despesa)
        #atribui pontuação
        pontos_perdidos, gasto, meta = self._pontos[0].adicionar_despesa(despesa.valor, despesa.tipo)
        self.salvar_dados()
        return pontos_perdidos, gasto, meta
        

    def erro_add_transacao(self,nome,valor, tipo, data, desc,carteira,modo,fixo=False):
        return
        #não funciona ainda... :/
        try:
            if carteira not in self._carteiras:
                raise ValueError("Carteira não encontrada.")
        except ValueError as erro:
            print(f"Erro: {erro}")
            return True
        return False
    
    def proximo_mes(self):
        """Avança para o próximo mês."""
        if self._mes_atual == 12:
            self._mes_atual = 1
            self._ano_atual += 1
        else:
            self._mes_atual += 1
        self.filtra_transacoes_mes()

    def mes_anterior(self):
        """Volta para o mês anterior."""
        if self._mes_atual == 1:
            self._mes_atual = 12
            self._ano_atual -= 1
        else:
            self._mes_atual -= 1
        self.filtra_transacoes_mes()

    def get_carteiras(self):
        """Retorna a lista de carteiras."""
        return self._carteiras
    
    def get_cofrinhos(self):
        """Retorna a lista de cofrinhos."""
        return self._cofrinhos
    
    def get_transacoes(self):
        """Retorna todas as transações."""
        return self._transacoes

    def get_transacoes_mes(self):
        """Retorna as transações do mês atual."""
        return self._transacoes_mes
    
    def get_mes_atual(self):
        """Retorna o mês atual."""
        return self._mes_atual
    
    def get_ano_atual(self):
        """Retorna o ano atual."""
        return self._ano_atual
    
    def get_pontos(self):
        """Retorna a pontuação do sistema de pontos."""
        return self._pontos[0].get_pontos()

    def filtrar_transacoes_mes(self):
        """Filtra as transações do mês atual."""
        self._transacoes_mes = filtra_transacoes_mes(self._transacoes, self._mes_atual, self._ano_atual)

    def atualizar_carteira(self, valor, carteira):
        """Atualiza o saldo da carteira com base no valor da transação."""
        if carteira in self._carteiras:
            carteira.atualizaCarteira(valor)
        else:
            print("Carteira não encontrada.")
        self.salvar_dados()
    
    def depositar_cofrinho(self, valor, cofre, carteira):
        """Deposita um valor no cofre."""
        if cofre in self._cofrinhos:
            cofre.depositar(valor)
            carteira.atualizaCarteira(-valor)
        else:
            print("Cofrinho não encontrado.")
        self.salvar_dados()

    def quebrar_cofrinho(self, cofre, carteira):
        """Quebra o cofre e atualiza a carteira."""
        if cofre in self._cofrinhos:
            valor = cofre.quebrar()
            carteira.atualizaCarteira(valor)
        else:
            print("Cofrinho não encontrado.")
        self.salvar_dados()
    
    def salvar_dados(self):
        """Salva os dados das transações, carteiras e cofrinhos."""
        save_data(self._transacoes, self._carteiras, self._cofrinhos, self._pontos)