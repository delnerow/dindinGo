

from transacao import CofrinhoFactory, Corrente, Cofrinho, CorrenteFactory

rFactory = CorrenteFactory()
fFactory = CofrinhoFactory()
def criarCarteira(carteiras):
        nome = input("Qual o nome da nova carteira?")
        desc = input("Qual a descrição da nova carteira?")
        saldo = int(input("Qual o saldo inicial?"))
        corrente = rFactory.create(nome, desc, saldo)
        carteiras.append(corrente)
        
def criarCofrinho(cofrinhos):
        nome = input("Qual o nome do novo cofrinho?")
        desc = input("Qual a descrição do novo cofrinho?")
        saldo = int(input("Qual o saldo inicial?"))
        cofre = fFactory.create(nome, desc, saldo)
        cofrinhos.append(cofre)