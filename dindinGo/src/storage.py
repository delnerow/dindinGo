import json
import os

DATA_FILE = 'data.json'

def save_data(transacoes, corrente, cofrinho):
    data = {
        'transacoes': [transacao.__dict__ for transacao in transacoes],
        'corrente': corrente.__dict__,
        'cofrinho': cofrinho.__dict__
    }
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def load_data():
    if not os.path.exists(DATA_FILE):
        return [], None, None
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
        transacoes = [create_transaction(trans) for trans in data['transacoes']]
        corrente = create_wallet(data['corrente'])
        cofrinho = create_savings(data['cofrinho'])
        return transacoes, corrente, cofrinho

def create_transaction(data):
    if data['tipo'] == 'despesa':
        return Despesa(data['nome'], data['valor'], data['categoria'], data['data'], data['repeticao'])
    elif data['tipo'] == 'receita':
        return Receita(data['nome'], data['valor'], data['categoria'], data['data'], data['repeticao'])

def create_wallet(data):
    return Carteira(data['nome'], data['descricao'], data['saldo'])

def create_savings(data):
    return Cofrinho(data['nome'], data['descricao'], data['saldo'])