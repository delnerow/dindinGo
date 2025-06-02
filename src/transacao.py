

class Carteira():
    def __init__(self,nome,descricao,saldo):
        self._nome=nome
        self._descricao=descricao
        self._saldo=saldo
        
    def atualizaCarteira(self, Transacao):
        if isinstance(Transacao, Transaction):
            if isinstance(Transacao, Despesa):
                valor = -Transacao.valor
            else: # Receita 
                valor = Transacao.valor
            self._saldo=self._saldo+valor
        else: 
             self._saldo=self._saldo+Transacao   
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
    def __init__(self,nome,valor, tipo, data, desc,carteira,modo,fixo=False):
        self.nome = nome
        self.valor = valor 
        self.tipo =tipo
        self.data = data
        self.desc = desc
        self.fixo = fixo
        self.modo=modo
        self.carteira = carteira  
        
    def set_carteira(self, carteira):
        if isinstance(carteira, Carteira):
            self.carteira = carteira
        else:
            raise ValueError("Carteira deve ser uma instância da classe Carteira")
    # Formata para JSON
    def to_dict(self):
        return {
                'nome': self.nome,
                'valor': self.valor,
                'tipo': self.tipo,
                'data': self.data,
                'desc': self.desc,
                'carteira': self.carteira,
                'modo': self.modo,
                'repeticao': self.fixo
        }
    # Cria a partir de um dicionário de Json. rever dps detalhes dese classmethod, mas eh bom pra factory...
    @classmethod
    def from_dict(cls, d):
        return cls(d['nome'], d['valor'], d['tipo'], d['data'], d['desc'],d['carteira'],d['modo'], d['repeticao'])
        
        
        
#honestamente, nn acho que precise de duas subclasses para Receita e Despesa, mas vamos manter por enquanto
class Receita(Transaction):
    def __init__(self,nome,valor, tipo, data,desc, carteira, modo, repeticao):
        super().__init__(nome,valor,tipo,data,desc, carteira,"+", repeticao)     
        
class Despesa(Transaction):
    def __init__(self,nome,valor, tipo, data, desc, carteira,modo, repeticao):
        super().__init__(nome,valor,tipo,data, desc, carteira,"-", repeticao)
