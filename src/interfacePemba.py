import datetime
import os

from storage import load_data, save_data
from transacao import Carteira, Cofrinho, Despesa, Receita



transacoes, carteiras, cofrinhos = load_data()

while True:
    print("Transações feitas:")
    for transacao in transacoes:
        print(f"{transacao.nome} | {transacao.valor} | {transacao.tipo} | {transacao.data} | Fixo? {transacao.fixo} ")
    for carteira in carteiras:
        print(f"Carteira: {carteira.getNome()} | Saldo: {carteira.getSaldo()} | Descrição: {carteira.getDescricao()}")
    print("Cofrinhos disponíveis:")
    for cofrinho in cofrinhos:
        print(f"Cofrinho: {cofrinho._nome} | Saldo: {cofrinho._saldo} | Descrição: {cofrinho._descricao}")
    acao = int(input("Oq vc deseja fazer\n[1] Nova transação\n[2] Adicionar ao cofrinho \n[3] quebrar cofrinho\n[4] Criar Nova Carteira\n[5] Criar Novo Cofrinho\n"))
    
    if acao == 1:
        if len(carteiras) == 0:
            print("Nenhuma carteira criada ainda. Crie uma primeiro.")
            continue
        os.system('cls')
        valor = int(input("Qual o valor, em reais?"))
        os.system('cls')
        modo = int(input("Despesa(1) ou Ganho(2)?"))
        os.system('cls')
        repeticao = input("É fixo? (s/n)").lower() == 's'
        os.system('cls')
        nome = input("Qual o nome?")
        os.system('cls')
        desc = input("Qual a descrição?")
        os.system('cls')
        tipoIndex = int(input("Qual a categoria\nLazer(1)\nAlimentação(2)\nCasa(3)\nMercado(4)\nServiço(5)?"))
        os.system('cls')
        if len(carteiras) == 1:
            corrente = carteiras[0]
        else:
            print("Carteiras disponíveis:")
            for i, carteira in enumerate(carteiras):
                print(f"{i}: {carteira.getNome()} - Saldo: {carteira.getSaldo()} - Descrição: {carteira.getDescricao()}")
            carteira= int(input("Qual a carteira da transação?\nDigite o número da carteira: "))
            if carteira < 0 or carteira >= len(carteiras):
                print("Carteira inválida. Usando a carteira corrente como padrão.")
                corrente = carteiras[0]
            else:
                corrente = carteiras[carteira]
        tipoL = ["lazer", "alimentação", "casa", "mercado", "serviço"]
        if tipoIndex < 1 or tipoIndex > 5:
            print("Categoria inválida. Usando 'lazer' como padrão.")
            tipo = "lazer"
        else:
            tipo = tipoL[tipoIndex - 1]
        data = datetime.datetime.now().isoformat()
        
        if modo == 2:
            trans = Receita(nome, valor, tipo, data,desc, repeticao)
        elif modo == 1:
            trans = Despesa(nome, valor, tipo, data,desc, repeticao)
        
        transacoes.append(trans)
        corrente.atualizaCarteira(trans.valor)
    
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
            print("Cofrinhos disponíveis:")
            for i, cofre in enumerate(cofrinhos):
                print(f"{i}: {cofre._nome} - Saldo: {cofre._saldo} - Descrição: {cofre._descricao}")
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
            for i, carteira in enumerate(carteiras):
                print(f"{i}: {carteira.getNome()} - Saldo: {carteira.getSaldo()} - Descrição: {carteira.getDescricao()}")
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
        if len(cofrinhos) == 0:
            print("Nenhum cofrinho criado ainda. Crie um primeiro.")
            continue
        if len(cofrinhos) == 1:
            cofrinho = cofrinhos[0]
        else:
            print("Cofrinhos disponíveis:")
            for i, cofre in enumerate(cofrinhos):
                print(f"{i}: {cofre._nome} - Saldo: {cofre._saldo} - Descrição: {cofre._descricao}")
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
        nome = input("Qual o nome da nova carteira?")
        desc = input("Qual a descrição da nova carteira?")
        saldo = int(input("Qual o saldo inicial?"))
        corrente = Carteira(nome, desc, saldo)
        carteiras.append(corrente)
    elif acao == 5:
        os.system('cls')
        nome = input("Qual o nome do novo cofrinho?")
        desc = input("Qual a descrição do novo cofrinho?")
        saldo = int(input("Qual o saldo inicial?"))
        cofrinho = Cofrinho(nome, desc, saldo)
        cofrinhos.append(cofrinho)
    save_data(transacoes, carteiras, cofrinhos)