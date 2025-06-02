import datetime
import os
import json

from transacao import Carteira, Cofrinho, Despesa, Receita


# carregando dados, supondo só uma conta
def load_data():
    try:
        with open('data.json', 'r') as file:
            data = json.load(file)
            transacoes = []
            for t in data['transacoes']:
                if t['tipo'] == 'receita':
                    transacoes.append(Receita.from_dict(t))
                else:
                    transacoes.append(Despesa.from_dict(t))
            corrente = Carteira("Carteira Corrente", "Carteira para transações do dia a dia", data['corrente'])
            cofrinho = Cofrinho("Cofrinho", "Cofrinho para poupança", data['cofrinho'])
            return transacoes, corrente, cofrinho
    except FileNotFoundError:
        return [], Carteira("Carteira Corrente", "Carteira para transações do dia a dia", 0), Cofrinho("Cofrinho", "Cofrinho para poupança", 0)

def save_data(transacoes, corrente, cofrinho):
    data = {
        'transacoes': [t.to_dict() for t in transacoes],
        'corrente': corrente._saldo,
        'cofrinho': cofrinho._saldo
    }
    with open('data.json', 'w') as file:
        json.dump(data, file, indent=4)

transacoes, corrente, cofrinho = load_data()

while True:
    print("Transações feitas:")
    for transacao in transacoes:
        print(f"{transacao.nome} - {transacao.valor} - {transacao.tipo} - {transacao.data} - {transacao.repeticao} vezes por ano")
    print("Carteira Corrente: ", corrente.getSaldo())
    print("Cofrinho: ", cofrinho._saldo)
    acao = int(input("Oq vc deseja fazer\n [1] Nova transação\n[2] Adicionar ao cofrinho \n[3] quebrar cofrinho"))
    
    if acao == 1:
        os.system('cls')
        valor = int(input("qual o valor?"))
        os.system('cls')
        tipo = int(input("despesa(1) ou ganho(2)?"))
        os.system('cls')
        nome = input("Qual o nome?")
        os.system('cls')
        repeticao = input("Quantas vezes se repete por ano?")
        desc = "lorem ipsum"
        data = datetime.datetime.now().isoformat()
        
        if tipo == 2:
            trans = Receita(nome, valor, "lazer", data, repeticao)
        elif tipo == 1:
            trans = Despesa(nome, valor, "lazer", data, repeticao)
        
        transacoes.append(trans)
        corrente.atualizaCarteira(trans.valor)
    
    elif acao == 2:
        os.system('cls')
        valor = int(input("Qual o valor a adicionar ao cofrinho?"))
        if valor >= corrente.getSaldo():
            print("Valor inválido. Você não tem esse dinheiro")
            continue
        corrente.atualizaCarteira(-valor)
        cofrinho.atualizaCarteira(valor)
    
    elif acao == 3:
        valor = cofrinho.quebrar()
        corrente.atualizaCarteira(valor)
        print("Cofrinho quebrado! Valor adicionado à carteira corrente: ", valor)
    
    save_data(transacoes, corrente, cofrinho)