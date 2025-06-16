import datetime
import os

from carteiraActions import criarCarteira, criarCofrinho
from interfaceFacade import GerenciamentoDeCarteiras
from utils.printers import printCarteiras, printCofrinhos, printTransacoes
from utils.filters import filtra_transacoes_mes
from utils.storage import load_data, save_data
from transActions import criar_transacao, editar_transacao


gerenciador = GerenciamentoDeCarteiras()

while True:
    os.system('cls')
    print(f"Transações feitas em {gerenciador.get_mes_atual():02d}/{gerenciador.get_ano_atual()}:")
    transacoes_mes = filtra_transacoes_mes(gerenciador.get_transacoes(), gerenciador.get_mes_atual(), gerenciador.get_ano_atual())
    printTransacoes(transacoes_mes)
    printCarteiras(gerenciador.get_carteiras())
    printCofrinhos(gerenciador.get_cofrinhos())
        
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
        gerenciador.mes_anterior()
    elif acao == 7:
        gerenciador.proximo_mes()
    if acao == 1:
        modo = int(input("Despesa(1) ou Ganho(2)?"))
        nome, valor, categoria, data, desc, carteira, repeticao = criar_transacao(gerenciador.get_carteiras())
        if modo == 1:
            gerenciador.adicionar_despesa(nome, valor, categoria, data, desc, carteira, repeticao)  
        elif modo == 2:
            gerenciador.adicionar_receita(nome, valor, categoria, data, desc, carteira, repeticao)
        os.system('cls')
    elif acao == 2:
        os.system('cls')
        if len(gerenciador.get_cofrinhos()) == 0:
            print("Nenhum cofrinho criado ainda. Crie um primeiro.")
            continue
        if len(gerenciador.get_cofrinhos()) == 0:
            print("Nenhuma carteira criada ainda. Crie uma primeiro.")
            continue
        if len(gerenciador.get_cofrinhos()) == 1:
            cofrinho = gerenciador.get_cofrinhos()[0]
        else:
            printCofrinhos(gerenciador.get_cofrinhos())
            cofre_index = int(input("Escolha o cofre para adicionar: "))
            if cofre_index < 0 or cofre_index >= len(gerenciador.get_cofrinhos()):
                print("Cofrinho inválido. Usando o cofre padrão.")
                cofrinho = gerenciador.get_cofrinhos()[0]
            else:
                cofrinho = gerenciador.get_cofrinhos()[cofre_index]
        os.system('cls')
        if len(gerenciador.get_carteiras()) == 1:
            corrente = gerenciador.get_carteiras()[0]
        else:
            print("Carteiras disponíveis:")
            printCarteiras(gerenciador.get_carteiras())
            carteira= int(input("Qual a carteira da transação?\nDigite o número da carteira: "))
            if carteira < 0 or carteira >= len(gerenciador.get_carteiras()):
                print("Carteira inválida. Usando a carteira corrente como padrão.")
                corrente = gerenciador.get_carteiras()[0]
            else:
                corrente = gerenciador.get_carteiras()[carteira]
        valor = int(input("Qual o valor a adicionar ao cofrinho?"))
        if valor >= corrente.getSaldo():
            print("Valor inválido. Você não tem esse dinheiro")
            continue
        corrente.atualizaCarteira(-valor)
        cofrinho.depositar(valor)
    
    elif acao == 3:
        os.system('cls')
        if len(gerenciador.get_cofrinhos()) == 0:
            print("Nenhum cofrinho criado ainda. Crie um primeiro.")
            continue
        if len(gerenciador.get_cofrinhos()) == 1:
            cofrinho = gerenciador.get_cofrinhos()[0]
        else:
            print("Cofrinhos disponíveis:")
            printCofrinhos(gerenciador.get_cofrinhos())
            cofre_index = int(input("Escolha o cofre para quebrar: "))
            if cofre_index < 0 or cofre_index >= len(gerenciador.get_cofrinhos()):
                print("Cofrinho inválido. Usando o cofre padrão.")
                cofrinho = gerenciador.get_cofrinhos()[0]
            else:
                cofrinho = gerenciador.get_cofrinhos()[cofre_index]
        valor = cofrinho.quebrar()
        corrente.atualizaCarteira(valor)
        print("Cofrinho quebrado! Valor adicionado à carteira corrente: ", valor)
    elif acao == 4:
        os.system('cls')
        criarCarteira(gerenciador.get_carteiras())
        os.system('cls')
    elif acao == 5:
        os.system('cls')
        criarCofrinho(gerenciador.get_cofrinhos())
        os.system('cls')
    elif acao == 8:
        editar_transacao(gerenciador.get_transacoes(), gerenciador.get_carteiras())
        os.system('pause')
    gerenciador.salvar_dados()
