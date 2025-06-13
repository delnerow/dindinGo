import datetime
import os

from carteiraActions import criarCarteira, criarCofrinho
from utils.printers import printCarteiras, printCofrinhos, printTransacoes
from utils.filters import filtra_transacoes_mes
from utils.storage import load_data, save_data
from transActions import criar_transacao, editar_transacao
from transacao import  Despesa, Receita


class FacadeInterface:
    def __init__(self):
        transacoes, carteiras, cofrinhos = load_data()
        self.transacoes = transacoes
        self.carteiras = carteiras
        self.cofrinhos = cofrinhos
        self.mes_atual = datetime.datetime.now().month
        self.ano_atual = datetime.datetime.now().year

    def proximo_mes(self):
        if self.mes_atual == 1:
            self.mes_atual = 12
            self.ano_atual -= 1
        else:
            mes_atual -= 1

    def mes_anterior(self):
        if mes_atual == 12:
            mes_atual = 1
            ano_atual += 1
        else:
            mes_atual += 1
    
    def adicionar_ao_cofrinho(self):
        os.system('cls')
        if len(self.cofrinhos) == 0:
            print("Nenhum cofrinho criado ainda. Crie um primeiro.")
            return
        if len(self.carteiras) == 0:
            print("Nenhuma carteira criada ainda. Crie uma primeiro.")
            return
        if len(self.cofrinhos) == 1:
            cofrinho = self.cofrinhos[0]
        else:
            printCofrinhos(self.cofrinhos)
            cofre_index = int(input("Escolha o cofre para adicionar: "))
            if cofre_index < 0 or cofre_index >= len(self.cofrinhos):
                print("Cofrinho inválido. Usando o cofre padrão.")
                cofrinho = self.cofrinhos[0]
            else:
                cofrinho = self.cofrinhos[cofre_index]
        os.system('cls')
        if len(self.carteiras) == 1:
            corrente = self.carteiras[0]
        else:
            print("Carteiras disponíveis:")
            printCarteiras(self.carteiras)
            carteira= int(input("Qual a carteira da transação?\nDigite o número da carteira: "))
            if carteira < 0 or carteira >= len(self.carteiras):
                print("Carteira inválida. Usando a carteira corrente como padrão.")
                corrente = self.carteiras[0]
            else:
                corrente = self.carteiras[carteira]
        valor = int(input("Qual o valor a adicionar ao cofrinho?"))
        if valor >= corrente.getSaldo():
            print("Valor inválido. Você não tem esse dinheiro")
            return
        corrente.atualizaCarteira(-valor)
        cofrinho.atualizaCarteira(valor)
        self.save()

    def criar_transacao(self):
        carteiras = self.carteiras
        transacoes = self.transacoes
        if len(carteiras) == 0:
            print("Nenhuma carteira criada ainda. Crie uma primeiro.")
            return
        if len(carteiras) == 1:
            carteira = carteiras[0]
        else:
            printCarteiras(carteiras)
            carteira_idx = int(input("Qual a carteira da transação?\nDigite o número da carteira: "))
            if carteira_idx < 0 or carteira_idx >= len(carteiras):
                print("Carteira inválida. Usando a carteira corrente como padrão.")
                carteira = carteiras[0]
            else:
                carteira = carteiras[carteira_idx]
        valor = int(input("Qual o valor, em reais?"))
        modo = int(input("Despesa(1) ou Ganho(2)?"))
        repeticao = input("É fixo? (s/n)").lower() == 's'
        nome = input("Qual o nome?")
        desc = input("Qual a descrição?")
        tipoIndex = int(input("Qual a categoria\nLazer(1)\nAlimentação(2)\nCasa(3)\nMercado(4)\nServiço(5)?"))
        tipoL = ["lazer", "alimentação", "casa", "mercado", "serviço"]
        tipo = tipoL[tipoIndex - 1] if 1 <= tipoIndex <= 5 else "lazer"
        data = datetime.datetime.now().isoformat()
        if modo == 2:
            trans = Receita(nome, valor, tipo, data, desc, carteira.getNome(),"+", repeticao)
        elif modo == 1:
            trans = Despesa(nome, valor, tipo, data, desc, carteira.getNome(),"-", repeticao)
        else:
            print("Modo inválido.")
            return
        transacoes.append(trans)
        carteira.atualizaCarteira(trans.valor)
        print("Transação criada!")
        save_data(self.transacoes, self.carteiras, self.cofrinhos)


    def editar_transacao(self):
        transacoes = self.transacoes
        carteiras = self.carteiras
        if not transacoes:
            print("Nenhuma transação para editar.")
            return
        printTransacoes(transacoes)
        idx = int(input("Digite o número da transação que deseja editar: "))
        if idx < 0 or idx >= len(transacoes):
            print("Índice inválido.")
            return
        trans = transacoes[idx]
        print("Deixe em branco para manter o valor atual.")
        valor_antigo = trans.valor
        novo_nome = input(f"Nome [{trans.nome}]: ") or trans.nome
        novo_valor = input(f"Valor [{trans.valor}]: ")
        novo_valor = int(novo_valor) if novo_valor else trans.valor
        novo_tipo = input(f"Tipo [{trans.tipo}]: ") or trans.tipo
        nova_data = input(f"Data (YYYY-MM-DD) [{trans.data}]: ") or trans.data
        nova_desc = input(f"Descrição [{trans.desc}]: ") or trans.desc
        novo_modo = input(f"Despesa(-) ou Ganho(+)?)") or trans.modo
        novo_fixo = input(f"Fixo? (s/n) [{'s' if trans.fixo else 'n'}]: ")
        novo_fixo = trans.fixo if novo_fixo == '' else (novo_fixo.lower() == 's')
        trans.nome = novo_nome
        trans.valor = novo_valor
        trans.tipo = novo_tipo
        trans.data = nova_data
        trans.desc = nova_desc
        trans.fixo = novo_fixo
        trans.modo=novo_modo
        if len(carteiras) > 0:
            carteira = carteiras[0]
            if novo_modo == '-':
                diff = (novo_valor - valor_antigo) * -1
            else:
                diff = novo_valor - valor_antigo
            carteira.atualizaCarteira(diff)
        print("Transação atualizada!")

    def quebrar_cofrinho(self):
        cofrinhos = self.cofrinhos
        os.system('cls')
        if len(cofrinhos) == 0:
            print("Nenhum cofrinho criado ainda. Crie um primeiro.")
            return
        if len(cofrinhos) == 1:
            cofrinho = cofrinhos[0]
        else:
            print("Cofrinhos disponíveis:")
            printCofrinhos(cofrinhos)
            cofre_index = int(input("Escolha o cofre para quebrar: "))
            if cofre_index < 0 or cofre_index >= len(cofrinhos):
                print("Cofrinho inválido. Usando o cofre padrão.")
                cofrinho = cofrinhos[0]
            else:
                cofrinho = cofrinhos[cofre_index]
        valor = cofrinho.quebrar()
        self.corrente.atualizaCarteira(valor)
        print("Cofrinho quebrado! Valor adicionado à carteira corrente: ", valor)

    def criar_carteira(self):
        os.system('cls')
        criarCarteira(self.carteiras)
        os.system('cls')        

    def criarCarteira(self):
            nome = input("Qual o nome da nova carteira?")
            desc = input("Qual a descrição da nova carteira?")
            saldo = int(input("Qual o saldo inicial?"))
            corrente = self.Carteira(nome, desc, saldo)
            self.carteiras.append(corrente)
            
    def criarCofrinho(self):
            nome = input("Qual o nome do novo cofrinho?")
            desc = input("Qual a descrição do novo cofrinho?")
            saldo = int(input("Qual o saldo inicial?"))
            cofre = self.Cofrinho(nome, desc, saldo)
            self.cofrinhos.append(cofre)

    def save(self):
        save_data(self.transacoes, self.carteiras, self.cofrinhos)

    