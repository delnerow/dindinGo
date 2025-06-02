

class Carteira():
    def __init__(self,nome,descricao,saldo):
        self._nome=nome
        self._descricao=descricao
        self._saldo=saldo
        
    def atualizaCarteira(self, valor):
        self._saldo=self._saldo+valor
    def getSaldo(self):
        return self._saldo


class Cofrinho(Carteira):
    def __init__(self,nome,descricao,saldo):
        super().__init__(nome,descricao,saldo) 
            
    def quebrar(self):
        retorno = self._saldo
        self._saldo=0
        return retorno




class Transaction():
    def __init__(self,nome,valor, tipo, data, repeticao):
        self.nome = nome
        self.valor = valor 
        self.tipo =tipo
        self.data = data
        self.repeticao = repeticao
    # Formata para JSON
    def to_dict(self):
        return {
                'nome': self.nome,
                'valor': self.valor,
                'tipo': self.tipo,
                'data': self.data,
                'repeticao': self.repeticao
        }
    # Cria a partir de um dicionário de Json. rever dps detalhes dese classmethod, mas eh bom pra factory...
    @classmethod
    def from_dict(cls, d):
        return cls(d['nome'], d['valor'], d['tipo'], d['data'], d['repeticao'])
        
class Receita(Transaction):
    def __init__(self,nome,valor, tipo, data, repeticao):
        super().__init__(nome,valor,tipo,data,repeticao)     
        
class Despesa(Transaction):
    def __init__(self,nome,valor, tipo, data, repeticao):
        super().__init__(nome,valor,tipo,data,repeticao)
        self.valor = (-1)*valor 
