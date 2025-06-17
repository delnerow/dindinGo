import datetime

from expectionHandlers import CarteiraNotFoundError, EmptyFieldError, InvalidTypeError, InvalidValueError, TransactionError, ValidationErrors
from utils.filters import filtra_transacoes_mes
from utils.storage import load_data, save_data
from transacao import  CofrinhoFactory, CorrenteFactory, DespesaFactory,  ReceitaFactory

class GerenciamentoDeCarteiras:
    def __init__(self):
        transacoes, carteiras, cofrinhos, pontos, curId = load_data()
        self._curId = curId
        self._transacoes = transacoes
        self._carteiras = carteiras
        self._cofrinhos = cofrinhos
        self._mes_atual = datetime.datetime.now().month
        self._ano_atual = datetime.datetime.now().year
        self._transacoes_mes = self.filtrar_transacoes_mes()
        #vetor com um único sistema de pontos
        #para acessar usar pontos[0] 
        self._pontos = pontos 
        self.receitaFactory = ReceitaFactory()
        self.despesaFactory = DespesaFactory()
        self.correnteFactory = CorrenteFactory()
        self.cofrinhoFactory = CofrinhoFactory()
        self.categorias = ["lazer", "alimentação", "casa", "mercado", "serviço"]

    def adicionar_receita(self, nome, valor, tipo, data, desc,carteira,fixo=False):
        """Adiciona uma receita à lista de transações."""

        try:
            self.validar_transacao(nome, valor, tipo, desc, carteira, fixo)
    
            self._curId = self._curId +1
            trans = self.receitaFactory.create_transaction(self._curId,nome, float(valor), tipo, data, desc, carteira, fixo)
            self._transacoes.append(trans)
            self.atualizar_carteira(trans,carteira)
            self.salvar_dados()
            return True, "Receita adicionada com sucesso"
        except ValidationErrors as e:
            return False, f"\nErros de validação:\n{str(e)}"
      
    def adicionar_despesa(self, nome, valor, tipo, data, desc,carteira,fixo=False):
        """Adiciona uma despesa à lista de transações. e atribuir pontuação, 
        retorna pontos perdidos, gasto e meta da categoria da despesa."""
        
        try:
            self.validar_transacao(nome, valor, tipo, desc, carteira, fixo)
            self._curId = self._curId +1
            despesa = self.despesaFactory.create_transaction(self._curId, nome, float(valor), tipo, data, desc, carteira, fixo)
            self._transacoes.append(despesa)
            pontos_perdidos, gasto, meta = self._pontos[0].adicionar_despesa(despesa.valor, despesa.categoria)
            self.salvar_dados()
            self.atualizar_carteira(despesa,carteira)
            return pontos_perdidos, gasto, meta, True, "Receita adicionada com sucesso"
        
        except ValidationErrors as e:
            return False, f"\nErros de validação:\n{str(e)}"
        
    def adicionar_carteira(self, nome, desc, saldo=0):
        """Adiciona uma nova carteira à lista de carteiras."""
        # Cria a carteira e adiciona à lista de carteiras
        try:
            self.validar_carteira(nome, desc, saldo)
            carteira = self.correnteFactory.create(nome, desc, float(saldo))
            self._carteiras.append(carteira)
            self.salvar_dados()
            return True, "Carteira adicionada com sucesso"
        except ValidationErrors as e:
            return False, f"\nErros de validação:\n{str(e)}"
        
    def adicionar_cofrinho(self, nome, desc, saldo=0):
        """Adiciona um novo cofrinho à lista de cofrinhos."""
        # Cria o cofre e adiciona à lista de cofrinhos
        try:
            self.validar_carteira(nome, desc, saldo)
            cofre = self.cofrinhoFactory.create(nome, desc, float(saldo))
            self._cofrinhos.append(cofre)
            self.salvar_dados()
            return True, "Cofrinho adicionado com sucesso"
        except ValidationErrors as e:
            return False, f"\nErros de validação:\n{str(e)}"
    
    def validar_transacao(self, nome, valor, tipo, desc, carteira, fixo):
        """Valida todos os campos da transação e retorna lista de erros"""
        errors = ValidationErrors()
        # Validar nome
        if not nome or nome.strip() == "":
            errors.add(EmptyFieldError("nome"))
            
        # Validar valor
        if not valor or valor.strip() == "":
            errors.add(EmptyFieldError("valor"))
        try:
            valor = float(valor)
            if valor <= 0:
                errors.add(InvalidValueError("valor", "deve ser maior que zero"))
        except ValueError:
            errors.add(InvalidTypeError("valor", "número"))
        
        # Validar tipo
        if not tipo or tipo.strip() == "":
            errors.add(EmptyFieldError("tipo"))
        elif tipo not in self.categorias:
            errors.add(InvalidValueError("tipo", f"deve ser uma das categorias: {', '.join(self.categorias)}"))
            
        # Validar descrição
        if not desc or desc.strip() == "":
            errors.add(EmptyFieldError("descrição"))
            
        # Validar carteira
        if not carteira:
            errors.add(EmptyFieldError("carteira"))
        elif carteira not in self._carteiras:
            errors.add(InvalidValueError("carteira", "não encontrada"))
        # Validar fixo
        if not isinstance(fixo, bool):
            errors.add(InvalidTypeError("fixo", "booleano"))
        if errors.has_errors():
            raise errors
        return errors
        
    def validar_carteira(self, nome, desc, saldo):
        errors = ValidationErrors()
        # Validar nome
        if not nome or nome.strip() == "":
            errors.add(EmptyFieldError("nome"))
            
        # Validar saldo
        if not saldo or saldo.strip() == "":
            errors.add(EmptyFieldError("valor"))
        try:
            saldo = float(saldo)
            if saldo < 0:
                errors.add(InvalidValueError("saldo", "deve ser positivo ou zero"))
        except ValueError:
            errors.add(InvalidTypeError("saldo", "número"))
         
        # Validar descrição
        if not desc or desc.strip() == "":
            errors.add(EmptyFieldError("descrição"))
        if errors.has_errors():
            raise errors
        return errors
            
    def proximo_mes(self):
        """Avança para o próximo mês."""
        if self._mes_atual == 12:
            self._mes_atual = 1
            self._ano_atual += 1
        else:
            self._mes_atual += 1
        self.filtra_transacoes_mes()

    def mes_anterior(self):
        """Volta para o mês anterior."""
        if self._mes_atual == 1:
            self._mes_atual = 12
            self._ano_atual -= 1
        else:
            self._mes_atual -= 1
        self.filtra_transacoes_mes()

    def get_carteiras(self):
        """Retorna a lista de carteiras."""
        return self._carteiras
    
    def get_cofrinhos(self):
        """Retorna a lista de cofrinhos."""
        return self._cofrinhos
    
    def get_transacoes(self):
        """Retorna todas as transações."""
        return self._transacoes

    def get_transacoes_mes(self):
        """Retorna as transações do mês atual."""
        return self._transacoes_mes
    
    def get_mes_atual(self):
        """Retorna o mês atual."""
        return self._mes_atual
    
    def get_ano_atual(self):
        """Retorna o ano atual."""
        return self._ano_atual
    
    def get_pontos(self):
        """Retorna a pontuação do sistema de pontos."""
        if not self._pontos:
            return 0
        return self._pontos[0].get_pontos()

    def filtrar_transacoes_mes(self):
        """Filtra as transações do mês atual."""
        self._transacoes_mes = filtra_transacoes_mes(self._transacoes, self._mes_atual, self._ano_atual)

    def atualizar_carteira(self, transacao, carteira):
        """Atualiza o saldo da carteira com base na transação."""
        if carteira in self._carteiras:
            carteira.atualizaCarteira(transacao)
        else:
            print("Carteira não encontrada.")
        self.salvar_dados()
    
    def depositar_cofrinho(self, trans, cofre, carteira):
        """Deposita um valor no cofre."""
        if cofre in self._cofrinhos:
            cofre.depositar(trans)
            if carteira in self._carteiras:
                carteira.atualizaCarteira(-trans.valor)
        else:
            print("Cofrinho não encontrado.")
        self.salvar_dados()

    def quebrar_cofrinho(self, cofre, carteira):
        """Quebra o cofre e atualiza a carteira."""
        if cofre in self._cofrinhos:
            valor = cofre.quebrar()
            carteira.atualizaCarteira(valor)
        else:
            print("Cofrinho não encontrado.")
        self.salvar_dados()
    
    def salvar_dados(self):
        """Salva os dados das transações, carteiras e cofrinhos."""
        save_data(self._transacoes, self._carteiras, self._cofrinhos, self._pontos, self._curId)