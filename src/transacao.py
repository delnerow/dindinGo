from abc import ABC, abstractmethod

class CarteiraFactory(ABC):  
    @abstractmethod
    def create(self, nome, desc, saldo, movimentacoes=[]):
        pass

    @abstractmethod
    def from_dict(cls, d):
        pass

class CorrenteFactory(CarteiraFactory):
    def create(self,nome,descricao,saldo,transacoes=[]):
        return Corrente(nome, descricao, saldo, transacoes)        

    def from_dict(self, d):
        return Corrente(
            d['nome'], 
            d['desc'], 
            d['saldo'], 
            d.get('movimentacoes', [])
        )
        
class CofrinhoFactory(CarteiraFactory):
    def create(self,nome,descricao,saldo,depositos=[]):
        return Cofrinho(nome, descricao, saldo, depositos)
    
    def from_dict(self, d):
        return Cofrinho(
            d['nome'], 
            d['desc'], 
            d['saldo'], 
            d.get('movimentacoes', [])
        )


class Carteira(ABC):
    def __init__(self,nome,descricao,saldo, movimentacoes=[]):
        self._nome=nome
        self._descricao=descricao
        self._saldo=saldo   
        self.movimentacoes = movimentacoes  # Lista para armazenar transações
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
                'movimentacoes': [id for id in self.movimentacoes]
        }  

class Cofrinho(Carteira):
    def __init__(self,nome,descricao,saldo,movimentacoes=[]):
        super().__init__(nome,descricao,saldo,movimentacoes) 
            
    def quebrar(self):
        retorno = self._saldo
        self._saldo=0
        return retorno
    
    def depositar(self, Transacao):
        if isinstance(Transacao, Transaction):
            if isinstance(Transacao, Despesa):
                #não pode haver despesas em cofrinhos!!!
                print("erro: não é possível adicionar despesas a um cofrinho")
            else: # Receita 
                valor = Transacao.valor
                self._saldo=self._saldo+valor
                self.movimentacoes.append(Transacao.id)
        else: 
             self._saldo=self._saldo+Transacao   

class Corrente(Carteira):
    def __init__(self,nome,descricao,saldo,movimentacoes=[]):
        super().__init__(nome,descricao,saldo,movimentacoes) 
            
    def atualizaCarteira(self, Transacao):
        if isinstance(Transacao, Transaction):
            valor = Transacao.valor
            self._saldo=self._saldo+valor
            self.movimentacoes.append(Transacao.id)  # Adiciona a transação à lista
        else: 
             self._saldo=self._saldo+Transacao


# Abstract Factory
class TransactionFactory(ABC):
    @abstractmethod
    def create_transaction(self, id, nome, valor,categoria, data, desc, carteira, repeticao):
        pass

    @abstractmethod
    def from_dict(self, d):
        pass

# Concrete Factories
class ReceitaFactory(TransactionFactory):
    def create_transaction(self, id,nome, valor,categoria, data, desc, carteira, repeticao=False):
        return Receita(id, nome, valor,categoria, data, desc, carteira, repeticao)

    def from_dict(self, d):
        return Receita(
            d['id'],
            d['nome'], 
            d['valor'], 
            d['categoria'], 
            d['data'], 
            d['desc'],
            d['carteira'],
            d.get('repeticao', False)
        )

class DespesaFactory(TransactionFactory):
    def create_transaction(self, id,nome, valor,categoria, data, desc, carteira, repeticao=False):
        return Despesa(id,nome, valor,categoria, data, desc, carteira, repeticao)

    def from_dict(self, d):
        return Despesa(
            d['id'],
            d['nome'], 
            d['valor'], 
            d['categoria'], 
            d['data'], 
            d['desc'],
            d['carteira'],
            d.get('repeticao', False)
        )

class Transaction(ABC):
    def __init__(self,id, nome,valor,categoria, data, desc,carteira,fixo=False):
        self.nome = nome
        self._valor = abs(valor) 
        self.categoria =categoria
        self.data = data
        self.desc = desc
        self.fixo = fixo
        self.id = id
        self.carteira = carteira  
        
    @property
    def valor(self):
        return self._valor if isinstance(self,Receita) else -self._valor
    
    def set_carteira(self, carteira):
        if isinstance(carteira, Corrente):
            self.carteira = carteira
        else:
            raise ValueError("Carteira deve ser uma instância da classe Carteira.")
    # Formata para JSON
    def to_dict(self):
        return {
                'id': self.id,
                'receita': isinstance(self, Receita),
                'nome': self.nome,
                'valor': self._valor,
                'categoria': self.categoria,
                'data': self.data,
                'desc': self.desc,
                'carteira': self.carteira,
                'repeticao': self.fixo
        }
        
        
#honestamente, nn acho que precise de duas subclasses para Receita e Despesa, mas vamos manter por enquanto
class Receita(Transaction):
    def __init__(self,id, nome,valor,categoria, data,desc, carteira, repeticao):
        super().__init__(id, nome,valor,categoria,data,desc, carteira, repeticao)     
        
class Despesa(Transaction):
    def __init__(self,id, nome,valor,categoria, data, desc, carteira,repeticao):
        super().__init__(id, nome,valor,categoria,data, desc, carteira, repeticao)

