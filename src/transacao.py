

class Carteira():
    def __init__(self,nome,descricao,saldo):
        self._nome=nome
        self._descricao=descricao
        self._saldo=saldo
        
    def atualizaCarteira(self, valor):
        self._saldo=self._saldo+valor
    def getSaldo(self):
        return self._saldo
    def getNome(self):
        return self._nome
    def getDescricao(self): 
        return self._descricao
    # Formata para JSON
    def to_dict(self):
        return {
                'nome': self._nome,
                'desc': self._descricao,
                'saldo': self._saldo,
        }
    # Cria a partir de um dicionário de Json. rever dps detalhes dese classmethod, mas eh bom pra factory...
    @classmethod
    def from_dict(cls, d):
        return cls(d['nome'], d['desc'], d['saldo'])


class Cofrinho(Carteira):
    def __init__(self,nome,descricao,saldo):
        super().__init__(nome,descricao,saldo) 
            
    def quebrar(self):
        retorno = self._saldo
        self._saldo=0
        return retorno




class Transaction():
    def __init__(self,nome,valor, tipo, data, desc,fixo=False):
        self.nome = nome
        self.valor = valor 
        self.tipo =tipo
        self.data = data
        self.desc = desc
        self.fixo = fixo
    # Formata para JSON
    def to_dict(self):
        return {
                'nome': self.nome,
                'valor': self.valor,
                'tipo': self.tipo,
                'data': self.data,
                'desc': self.desc,
                'repeticao': self.fixo
        }
    # Cria a partir de um dicionário de Json. rever dps detalhes dese classmethod, mas eh bom pra factory...
    @classmethod
    def from_dict(cls, d):
        return cls(d['nome'], d['valor'], d['tipo'], d['data'], d['desc'], d['repeticao'])
        
class Receita(Transaction):
    def __init__(self,nome,valor, tipo, data,desc, repeticao):
        super().__init__(nome,valor,tipo,data,desc,repeticao)     
        
class Despesa(Transaction):
    def __init__(self,nome,valor, tipo, data, desc, repeticao):
        super().__init__(nome,(-1)*valor,tipo,data, desc,repeticao)
