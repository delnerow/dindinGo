

from transacao import Carteira, Cofrinho


def criarCarteira(carteiras):
        nome = input("Qual o nome da nova carteira?")
        desc = input("Qual a descrição da nova carteira?")
        saldo = int(input("Qual o saldo inicial?"))
        corrente = Carteira(nome, desc, saldo)
        carteiras.append(corrente)
        
def criarCofrinho(cofrinhos):
        nome = input("Qual o nome do novo cofrinho?")
        desc = input("Qual a descrição do novo cofrinho?")
        saldo = int(input("Qual o saldo inicial?"))
        cofre = Cofrinho(nome, desc, saldo)
        cofrinhos.append(cofre)