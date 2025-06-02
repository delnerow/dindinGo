import os
import datetime
from utils.printers import printCarteiras, printTransacoes
from transacao import  Despesa, Receita

def criar_transacao(transacoes, carteiras):
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
    
    
    
    
def editar_transacao(transacoes, carteiras):
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