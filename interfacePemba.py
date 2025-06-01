

from transacao import Carteira, Cofrinho, Despesa, Receita
import datetime
import os

transacoes =[]
corrente=Carteira("Carteira Corrente","Carteira para transações do dia a dia",0)
cofrinho=Cofrinho("Cofrinho","Cofrinho para poupança",0)
while True:
    print("Transações feitas:")
    for transacao in transacoes:
        print(f"{transacao.nome} - {transacao.valor} - {transacao.tipo} - {transacao.data} - {transacao.repeticao} vezes por ano")
    print("Carteira Corrente: ", corrente.getSaldo())
    print("Cofrinho: ", cofrinho._saldo)
    # Interface Pemba - Gerenciamento de Transações Financeiras
    acao = int(input("Oq vc deseja fazer\n [1] Nova transação\n[2] Adicionar ao cofrinho \n[3] quebrar cofrinho"))
    if acao==1:
        os.system('cls')
        valor = int(input("qual o valor?"))
        os.system('cls')
        tipo = int(input("despesa(1) ou ganho(2)?"))
        os.system('cls')
        nome = input("Qual o nome?")
        os.system('cls')
        repeticao = input("Quantas vezes se repete por ano?")
        desc= "lorem ipsum"
        data = datetime.datetime.now()
        if(tipo==2):
            trans=Receita(nome,valor,"lazer",data,repeticao)
        elif(tipo==1):
            trans=Despesa(nome,valor,"lazer",data,repeticao)
        transacoes.append(trans)
        corrente.atualizaCarteira(trans.valor)
    if acao==2:
        os.system('cls')
        valor = int(input("Qual o valor a adicionar ao cofrinho?"))
        if(valor>=corrente.getSaldo()):
            print("Valor inválido.ce nao tem esse dinheiro")
            continues
        corrente.atualizaCarteira(-valor)
        cofrinho.atualizaCarteira(valor)
    if acao==3:
        valor = cofrinho.quebrar()
        corrente.atualizaCarteira(valor)
        print("Cofrinho quebrado! Valor adicionado à carteira corrente: ", valor)