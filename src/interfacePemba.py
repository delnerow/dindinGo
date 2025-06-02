import datetime
import os

from carteiraActions import criarCarteira, criarCofrinho
from utils.printers import printCarteiras, printCofrinhos, printTransacoes
from utils.filters import filtra_transacoes_mes
from utils.storage import load_data, save_data
from transActions import criar_transacao, editar_transacao

transacoes, carteiras, cofrinhos = load_data()

mes_atual = datetime.datetime.now().month
ano_atual = datetime.datetime.now().year



while True:
    os.system('cls')
    print(f"Transações feitas em {mes_atual:02d}/{ano_atual}:")
    transacoes_mes = filtra_transacoes_mes(transacoes, mes_atual, ano_atual)
    printTransacoes(transacoes_mes)
    printCarteiras(carteiras)
    printCofrinhos(cofrinhos)
        
    acao = int(input(
        "Oq vc deseja fazer\n"
        "[1] Nova transação\n"
        "[2] Adicionar ao cofrinho\n"
        "[3] Quebrar cofrinho\n"
        "[4] Criar Nova Carteira\n"
        "[5] Criar Novo Cofrinho\n"
        "[6] Mês anterior\n"
        "[7] Próximo mês\n"
        "[8] Editar transação\n"
    ))

    if acao == 6:
        if mes_atual == 1:
            mes_atual = 12
            ano_atual -= 1
        else:
            mes_atual -= 1
        continue
    elif acao == 7:
        if mes_atual == 12:
            mes_atual = 1
            ano_atual += 1
        else:
            mes_atual += 1
        continue

    if acao == 1:
        criar_transacao(transacoes, carteiras)
        os.system('cls')
    elif acao == 2:
        os.system('cls')
        if len(cofrinhos) == 0:
            print("Nenhum cofrinho criado ainda. Crie um primeiro.")
            continue
        if len(carteiras) == 0:
            print("Nenhuma carteira criada ainda. Crie uma primeiro.")
            continue
        if len(cofrinhos) == 1:
            cofrinho = cofrinhos[0]
        else:
            printCofrinhos(cofrinhos)
            cofre_index = int(input("Escolha o cofre para adicionar: "))
            if cofre_index < 0 or cofre_index >= len(cofrinhos):
                print("Cofrinho inválido. Usando o cofre padrão.")
                cofrinho = cofrinhos[0]
            else:
                cofrinho = cofrinhos[cofre_index]
        os.system('cls')
        if len(carteiras) == 1:
            corrente = carteiras[0]
        else:
            print("Carteiras disponíveis:")
            printCarteiras(carteiras)
            carteira= int(input("Qual a carteira da transação?\nDigite o número da carteira: "))
            if carteira < 0 or carteira >= len(carteiras):
                print("Carteira inválida. Usando a carteira corrente como padrão.")
                corrente = carteiras[0]
            else:
                corrente = carteiras[carteira]
        valor = int(input("Qual o valor a adicionar ao cofrinho?"))
        if valor >= corrente.getSaldo():
            print("Valor inválido. Você não tem esse dinheiro")
            continue
        corrente.atualizaCarteira(-valor)
        cofrinho.atualizaCarteira(valor)
    
    elif acao == 3:
        os.system('cls')
        if len(cofrinhos) == 0:
            print("Nenhum cofrinho criado ainda. Crie um primeiro.")
            continue
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
        corrente.atualizaCarteira(valor)
        print("Cofrinho quebrado! Valor adicionado à carteira corrente: ", valor)
    elif acao == 4:
        os.system('cls')
        criarCarteira(carteiras)
        os.system('cls')
    elif acao == 5:
        os.system('cls')
        criarCofrinho(cofrinhos)
        os.system('cls')
    elif acao == 8:
        editar_transacao(transacoes, carteiras)
        os.system('pause')
    save_data(transacoes, carteiras, cofrinhos)