import datetime
from expectionHandlers import ValidationErrors, EmptyFieldError, InvalidTypeError, InvalidValueError
from utils.storage import StorageManager
from transacao import CofrinhoFactory, CorrenteFactory, DespesaFactory, ReceitaFactory, Carteira, Cofrinho, Transaction

class GerenciamentoDeCarteiras:
    """
    Implementação do padrão Facade.
    Oferece uma interface simples para o sistema, orquestrando
    operações entre a interface do usuário, a lógica de negócios e a camada de persistência.
    """
    def __init__(self):
        # O Facade agora USA o Singleton de armazenamento em vez de gerenciar o estado.
        self.storage = StorageManager()
        
        # O estado de visualização (mês/ano) permanece no Facade.
        self._mes_atual = datetime.datetime.now().month
        self._ano_atual = datetime.datetime.now().year
        
        # As fábricas são mantidas aqui, pois o Facade as utiliza para criar objetos.
        self.receitaFactory = ReceitaFactory()
        self.despesaFactory = DespesaFactory()
        self.correnteFactory = CorrenteFactory()
        self.cofrinhoFactory = CofrinhoFactory()

        # A lista de categorias é definida aqui e fornecida para a UI.
        self.categorias = ["lazer", "alimentação", "casa", "mercado", "serviço"]

    # --- Métodos de Negócio (Orquestração) ---

    def adicionar_receita(self, nome: str, valor: float, tipo: str, data: str, desc: str, carteira: Carteira, fixo: bool = False):
        try:
            self.validar_transacao(nome, str(valor), tipo, desc, carteira, fixo)
            
            novo_id = self.storage.get_next_id()
            trans = self.receitaFactory.create_transaction(novo_id, nome, valor, tipo, data, desc, carteira.getNome(), fixo)
            
            self.storage.add_transaction(trans)
            carteira.atualizaCarteira(trans)
            
            self.storage.save_data() # Garante que a mudança no saldo da carteira seja salva
            return True, "Receita adicionada com sucesso."
        except ValidationErrors as e:
            return False, f"\nErros de validação:\n{str(e)}"

    def adicionar_despesa(self, nome: str, valor: float, tipo: str, data: str, desc: str, carteira: Carteira, fixo: bool = False):
        try:
            self.validar_transacao(nome, str(valor), tipo, desc, carteira, fixo)
            
            novo_id = self.storage.get_next_id()
            despesa = self.despesaFactory.create_transaction(novo_id, nome, valor, tipo, data, desc, carteira.getNome(), fixo)
            
            self.storage.add_transaction(despesa)
            carteira.atualizaCarteira(despesa)
            
            # Interage com o sistema de pontos, que também é acessado via storage
            pontos_manager = self.storage.get_pontos_manager()
            pontos_manager.adicionar_despesa(despesa.valor, despesa.categoria)

            self.storage.save_data()
            return True, "Despesa adicionada com sucesso."
        except ValidationErrors as e:
            return False, f"\nErros de validação:\n{str(e)}"

    # Em interfaceFacade.py, dentro da classe GerenciamentoDeCarteiras

    def editar_transacao(self, transacao_original: Transaction, novos_dados: dict):
        """
        Edita uma transação existente, ajusta o saldo da carteira e salva.
        'novos_dados' é um dicionário com os campos a serem alterados.
        """
        try:
            # Encontra a carteira associada à transação original
            carteira_associada = next(c for c in self.storage.get_carteiras() if c.getNome() == transacao_original.carteira)
            
            valor_antigo_com_sinal = transacao_original.valor # Guarda o valor com sinal (+/-)
            
            # Valida os novos dados (simplificado para focar na lógica principal)
            novo_valor_bruto = float(novos_dados.get('valor', transacao_original._valor))
            
            # --- Lógica de atualização ---
            
            # 1. Atualiza os atributos do objeto transação
            transacao_original.nome = novos_dados.get('nome', transacao_original.nome)
            transacao_original.categoria = novos_dados.get('categoria', transacao_original.categoria)
            transacao_original._valor = novo_valor_bruto # Atualiza o valor bruto (sempre positivo)
            
            # 2. Calcula a diferença para o ajuste no saldo
            # O novo .valor já terá o sinal correto
            diferenca_de_saldo = transacao_original.valor - valor_antigo_com_sinal
            
            # 3. Usa o novo método para ajustar o saldo da carteira
            carteira_associada.ajustar_saldo(diferenca_de_saldo)
    
            # 4. Salva o estado modificado (tanto da transação quanto da carteira)
            self.storage.save_data()
            
            return True, "Transação atualizada com sucesso!"
    
        except StopIteration:
            return False, "Erro: Carteira associada à transação não foi encontrada."
        except ValueError:
            return False, "Erro de validação: O valor inserido não é um número válido."

    def adicionar_carteira(self, nome: str, desc: str, saldo: float = 0):
        try:
            self.validar_carteira(nome, desc, str(saldo))
            carteira = self.correnteFactory.create(nome, desc, saldo)
            self.storage.add_carteira(carteira)
            return True, "Carteira criada com sucesso."
        except ValidationErrors as e:
            return False, f"\nErros de validação:\n{str(e)}"

    def adicionar_cofrinho(self, nome: str, desc: str, saldo: float = 0):
        try:
            self.validar_carteira(nome, desc, str(saldo))
            cofre = self.cofrinhoFactory.create(nome, desc, saldo)
            self.storage.add_cofrinho(cofre)
            return True, "Cofrinho criado com sucesso."
        except ValidationErrors as e:
            return False, f"\nErros de validação:\n{str(e)}"

    def depositar_cofrinho(self, valor: float, cofrinho: Cofrinho, carteira_origem: Carteira):
        if valor <= 0:
            return False, "O valor do depósito deve ser positivo."
        if valor > carteira_origem.getSaldo():
            return False, "Saldo insuficiente na carteira de origem."

        # Cria duas transações para rastreamento: uma despesa na carteira e uma receita no cofre
        id_saida = self.storage.get_next_id()
        trans_saida = self.despesaFactory.create_transaction(id_saida, f"Depósito para {cofrinho.getNome()}", valor, "transferencia", datetime.datetime.now().isoformat(), "", carteira_origem.getNome())
        
        id_entrada = self.storage.get_next_id()
        trans_entrada = self.receitaFactory.create_transaction(id_entrada, f"Depósito de {carteira_origem.getNome()}", valor, "transferencia", datetime.datetime.now().isoformat(), "", cofrinho.getNome())

        # Adiciona as transações ao histórico geral
        self.storage.add_transaction(trans_saida)
        self.storage.add_transaction(trans_entrada)
        
        # Atualiza os saldos
        carteira_origem.atualizaCarteira(trans_saida)
        cofrinho.depositar(trans_entrada)

        self.storage.save_data()
        return True, f"Valor de R$ {valor:.2f} depositado com sucesso."

    def quebrar_cofrinho(self, cofrinho: Cofrinho, carteira_destino: Carteira):
        valor_quebrado = cofrinho.quebrar()
        
        if valor_quebrado > 0:
            # Cria uma transação para registrar a entrada do valor na carteira
            id_trans = self.storage.get_next_id()
            trans = self.receitaFactory.create_transaction(id_trans, f"Valor do cofre '{cofrinho.getNome()}'", valor_quebrado, "transferencia", datetime.datetime.now().isoformat(), "Cofre quebrado", carteira_destino.getNome())
            self.storage.add_transaction(trans)
            carteira_destino.atualizaCarteira(trans)
        
        self.storage.save_data()
        return valor_quebrado, "Cofrinho quebrado com sucesso!"

    # --- Métodos de Validação ---

    def validar_transacao(self, nome, valor, tipo, desc, carteira, fixo):
        errors = ValidationErrors()
        if not nome or not nome.strip(): errors.add(EmptyFieldError("nome"))
        
        try:
            val = float(valor)
            if val <= 0: errors.add(InvalidValueError("valor", "deve ser maior que zero"))
        except ValueError: errors.add(InvalidTypeError("valor", "número"))

        if tipo not in self.categorias: errors.add(InvalidValueError("tipo", f"inválida"))
        if not carteira or not isinstance(carteira, Carteira): errors.add(InvalidTypeError("carteira", "inválida"))
        
        if errors.has_errors(): raise errors

    def validar_carteira(self, nome, desc, saldo):
        errors = ValidationErrors()
        if not nome or not nome.strip(): errors.add(EmptyFieldError("nome"))
        if not desc or not desc.strip(): errors.add(EmptyFieldError("descrição"))
        
        try:
            s = float(saldo)
            if s < 0: errors.add(InvalidValueError("saldo", "não pode ser negativo"))
        except ValueError: errors.add(InvalidTypeError("saldo", "número"))

        if errors.has_errors(): raise errors

    # --- Getters (Fornecem dados para a UI) ---

    def get_carteiras(self): return self.storage.get_carteiras()
    def get_cofrinhos(self): return self.storage.get_cofrinhos()
    def get_transacoes(self): return self.storage.get_all_transactions()
    def get_pontos(self): return self.storage.get_pontos_manager().get_pontos()
    def get_categorias_disponiveis(self): return self.categorias
    def get_mes_atual(self): return self._mes_atual
    def get_ano_atual(self): return self._ano_atual

    # --- Métodos de Controle de Visualização ---

    def proximo_mes(self):
        if self._mes_atual == 12:
            self._mes_atual = 1
            self._ano_atual += 1
        else:
            self._mes_atual += 1

    def mes_anterior(self):
        if self._mes_atual == 1:
            self._mes_atual = 12
            self._ano_atual -= 1
        else:
            self._mes_atual -= 1