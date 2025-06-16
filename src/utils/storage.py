import json

from transacao import CofrinhoFactory, Corrente, Cofrinho, CorrenteFactory, Despesa, DespesaFactory, Receita, ReceitaFactory
from sistemaDePontos import sistemaDePontos

DATA_FILE = 'data.json'
def load_data():
    try:
        with open('data.json', 'r') as file:
            data = json.load(file)
            curId = data.get('idGenerator', 0)
            transacoes = []
            carteiras = []
            cofrinhos = []
            rFactory = ReceitaFactory()
            dFactory = DespesaFactory()
            corFactory = CorrenteFactory()
            cofFactory = CofrinhoFactory()
            pontos = []
            for t in data['transacoes']:
                if t['receita'] == 1:
                    transacoes.append(rFactory.from_dict(t))
                else:
                    transacoes.append(dFactory.from_dict(t))
            for t in data['carteiras']:
                carteiras.append(corFactory.from_dict(t))
            for t in data['cofrinhos']:
                cofrinhos.append(cofFactory.from_dict(t))
            for t in data['pontos']:
                pontos.append(sistemaDePontos.from_dict(t))
            return transacoes, carteiras, cofrinhos, pontos, curId
    except FileNotFoundError:
        return [], [], [], [] , 0

def save_data(transacoes, carteiras, cofrinhos, pontos, curId):
    data = {
        'idGenerator': curId,  # Placeholder for ID generator
        'transacoes': [t.to_dict() for t in transacoes],
        'carteiras': [t.to_dict() for t in carteiras],
        'cofrinhos': [t.to_dict() for t in cofrinhos],
        'pontos': [t.to_dict() for t in pontos]
    }
    with open('data.json', 'w') as file:
        json.dump(data, file, indent=4)