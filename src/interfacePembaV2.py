import datetime
import os

from carteiraActions import criarCarteira, criarCofrinho
from utils.printers import printCarteiras, printCofrinhos, printTransacoes
from utils.filters import filtra_transacoes_mes
from utils.storage import load_data, save_data
from transActions import criar_transacao, editar_transacao
from interfaceFacade import GerenciamentoDeCarteiras

gerenciador = GerenciamentoDeCarteiras()




while True:
    #os.system('cls')
    print(f"Transações feitas em {gerenciador.get_mes_atual():02d}/{gerenciador.get_ano_atual()}:")
        
    transacoes = gerenciador.get_transacoes()
    transacoes_mes = filtra_transacoes_mes(transacoes, gerenciador.get_mes_atual(), gerenciador.get_ano_atual())
    carteiras = gerenciador.get_carteiras()
    cofrinhos = gerenciador.get_cofrinhos()

    printTransacoes(transacoes_mes)
    printCarteiras(carteiras)
    printCofrinhos(cofrinhos)
    
    print("num transações:", len(gerenciador.get_transacoes())) #debug

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

    num_cofrinhos = len(gerenciador.get_cofrinhos())
    num_carteiras = len(gerenciador.get_carteiras())

    if acao == 6:
        gerenciador.mes_anterior()
        continue
    elif acao == 7:
        gerenciador.proximo_mes()
        continue

    if acao == 1: #nova transação, receita ou despesa
        if num_carteiras == 0:
            print("Nenhuma carteira criada ainda. Crie uma primeiro.")
            continue
        if num_carteiras == 1:
            carteira = carteiras[0]
        else:
            printCarteiras(carteiras)
            carteira_idx = int(input("Qual a carteira da transação?\nDigite o número da carteira: "))
            if carteira_idx < 0 or carteira_idx >= num_carteiras:
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
            gerenciador.adicionar_receita(nome, valor, tipo, data, desc, carteira.getNome(), "+", repeticao)
        elif modo == 1:
            gerenciador.adicionar_despesa(nome, valor, tipo, data, desc, carteira.getNome(), "+", repeticao)
        else:
            print("Modo inválido.")
            continue
        print("Transação criada!")


    elif acao == 2:
        os.system('cls')

        if num_cofrinhos == 0:
            print("Nenhum cofrinho criado ainda. Crie um primeiro.")
            continue
        if num_carteiras == 0:
            print("Nenhuma carteira criada ainda. Crie uma primeiro.")
            continue
        if num_cofrinhos == 1:
            cofrinho = cofrinhos[0]
        else:
            printCofrinhos(cofrinhos)
            cofre_index = int(input("Escolha o cofre para adicionar: "))
            if cofre_index < 0 or cofre_index >= num_cofrinhos:
                print("Cofrinho inválido. Usando o cofre padrão.")
                cofrinho = gerenciador.get_cofrinhos[0]
            else:
                cofrinho = cofrinhos[cofre_index]
        os.system('cls')
        if num_carteiras == 1:
            corrente = carteiras[0]
        else:
            print("Carteiras disponíveis:")
            printCarteiras(carteiras)
            carteira= int(input("Qual a carteira da transação?\nDigite o número da carteira: "))
            if carteira < 0 or carteira >= num_carteiras:
                print("Carteira inválida. Usando a carteira corrente como padrão.")
                corrente = carteiras[0]
            else:
                corrente = carteiras[carteira]
        valor = int(input("Qual o valor a adicionar ao cofrinho?"))
        if valor >= corrente.getSaldo():
            print("Valor inválido. Você não tem esse dinheiro")
            continue
        gerenciador.depositar_cofrinho(valor, cofrinho, corrente)
        print("Valor adicionado ao cofrinho com sucesso!:)")

    elif acao == 3:
        os.system('cls')

        if num_cofrinhos == 0:
            print("Nenhum cofrinho criado ainda. Crie um primeiro.")
            continue
        if num_cofrinhos == 1:
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

        corrente = carteiras[0] 
        gerenciador.quebrar_cofrinho(cofrinho, corrente)
        print("Cofrinho quebrado! Valor adicionado à carteira corrente: ", valor)

    elif acao == 4:
        os.system('cls')
        criarCarteira(carteiras)
        os.system('cls')
    elif acao == 5:
        os.system('cls')
        criarCofrinho(cofrinhos)
        os.system('cls')
    # elif acao == 8:
    #     editar_transacao(transacoes, carteiras)
    #     os.system('pause')
    # save_data(transacoes, carteiras, cofrinhos)

