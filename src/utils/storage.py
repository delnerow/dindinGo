import json

from transacao import Carteira, Cofrinho, Despesa, Receita

DATA_FILE = 'data.json'
def load_data():
    try:
        with open('data.json', 'r') as file:
            data = json.load(file)
            transacoes = []
            carteiras = []
            cofrinhos = []
            for t in data['transacoes']:
                if t['tipo'] == 'receita':
                    transacoes.append(Receita.from_dict(t))
                else:
                    transacoes.append(Despesa.from_dict(t))
            for t in data['carteiras']:
                carteiras.append(Carteira.from_dict(t))
            for t in data['cofrinhos']:
                cofrinhos.append(Cofrinho.from_dict(t))
            return transacoes, carteiras, cofrinhos
    except FileNotFoundError:
        return [], [], []

def save_data(transacoes, carteiras, cofrinhos):
    data = {
        'transacoes': [t.to_dict() for t in transacoes],
        'carteiras': [t.to_dict() for t in carteiras],
        'cofrinhos': [t.to_dict() for t in cofrinhos]
    }
    with open('data.json', 'w') as file:
        json.dump(data, file, indent=4)