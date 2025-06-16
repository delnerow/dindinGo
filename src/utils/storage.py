import json

from transacao import CofrinhoFactory, Corrente, Cofrinho, CorrenteFactory, Despesa, DespesaFactory, Receita, ReceitaFactory

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
            for t in data['transacoes']:
                if t['receita'] == 1:
                    transacoes.append(rFactory.from_dict(t))
                else:
                    transacoes.append(dFactory.from_dict(t))
            for t in data['carteiras']:
                carteiras.append(corFactory.from_dict(t))
            for t in data['cofrinhos']:
                cofrinhos.append(cofFactory.from_dict(t))
            return transacoes, carteiras, cofrinhos, curId
    except FileNotFoundError:
        return [], [], [] , 0

def save_data(curId, transacoes, carteiras, cofrinhos):
    data = {
        'idGenerator': curId,  # Placeholder for ID generator
        'transacoes': [t.to_dict() for t in transacoes],
        'carteiras': [t.to_dict() for t in carteiras],
        'cofrinhos': [t.to_dict() for t in cofrinhos]
    }
    with open('data.json', 'w') as file:
        json.dump(data, file, indent=4)