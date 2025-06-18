# =========================================
# Módulo: gerenciadorCarteiras.py
# Descrição: Implementa a fachada para o gerenciamento de carteiras, cofrinhos e transações.
# =========================================
import datetime


import sys
from pathlib import Path

# src directory pro Python path
src_path = str(Path(__file__).resolve().parent.parent)
if src_path not in sys.path:
    sys.path.append(src_path)


from utils.exceptionHandlers import ValidationErrors, EmptyFieldError, InvalidTypeError, InvalidValueError
from utils.storage import StorageManager
from core.transacao import   Receita,   Transaction
from core.carteira import Carteira, Cofrinho
from factories.carteira_factory import CofrinhoFactory, CorrenteFactory
from factories.transaction_factory import DespesaFactory, ReceitaFactory


class GerenciamentoDeCarteiras:
    """
    Implementação do padrão Facade (a famosa Fachada).
    Oferece uma interface simples para o sistema, orquestrando
    operações entre a interface do usuário, a lógica de negócios e a camada de persistência (JSON).
    """
    def __init__(self):
        # Inicializa o gerenciador com as fábricas e o gerenciador de armazenamento
        self.storage = StorageManager()
        self._mes_atual = datetime.datetime.now().month
        self._ano_atual = datetime.datetime.now().year

        self.receita_factory = ReceitaFactory()
        self.despesa_factory = DespesaFactory()
        self.corrente_factory = CorrenteFactory()
        self.cofrinho_factory = CofrinhoFactory()

        self.categorias = ["lazer", "alimentação", "casa", "mercado", "serviço"]

    def adicionar_receita(self, nome: str, valor: float, tipo: str, data: str, desc: str, carteira: Carteira, fixo: bool = False, rep: int = 1):
        """
        Adiciona uma receita à carteira especificada. Permite receitas recorrentes (rep > 1).
        """
        try:
            self.validar_transacao(nome, str(valor), tipo, carteira)
            
            # Get current date as datetime object
            data_atual = datetime.datetime.fromisoformat(data)
            novo_id = self.storage.get_next_id()
            
            # Create transactions for each repetition
            if(rep>1):
                for i in range(rep):
                    # Calculate date for this repetition
                    data_trans = data_atual.replace(month=((data_atual.month - 1 + i) % 12) + 1)
                    if (data_atual.month + i) > 12:
                        data_trans = data_trans.replace(year=data_atual.year + ((data_atual.month + i - 1) // 12))
                    
                    trans = self.receita_factory.create_transaction(
                        novo_id, 
                        f"{nome} ({i+1}/{rep})" if rep > 1 else nome,
                        valor, 
                        tipo, 
                        data_trans.isoformat(), 
                        desc, 
                        carteira.get_nome(), 
                        fixo,
                        rep
                    )
                    
                    self.storage.add_transaction(trans)
                    novo_id = self.storage.get_next_id()
            else:
                trans = self.receita_factory.create_transaction(novo_id, nome, valor, tipo, data, desc, carteira.get_nome(), fixo, rep )
                self.storage.add_transaction(trans)
                carteira.atualiza_carteira(trans)
            self.storage.save_data()
            return True, f"{'Receita adicionada' if rep == 1 else f'Receitas adicionadas para {rep} meses'} com sucesso."
        except ValidationErrors as e:
            return False, f"\nErros de validação:\n{str(e)}"

    def adicionar_despesa(self, nome: str, valor: float, tipo: str, data: str, desc: str, carteira: Carteira, fixo: bool = False, rep : int = 1):
        """
        Adiciona uma despesa à carteira especificada. Permite despesas recorrentes (rep > 1).
        """
        try:
            self.validar_transacao(nome, str(valor), tipo, carteira)
            # Get current date as datetime object
            data_atual = datetime.datetime.fromisoformat(data)
            novo_id = self.storage.get_next_id()
            # Create transactions for each repetition
            if(rep>1):
                for i in range(rep):
                    # Calculate date for this repetition
                    data_trans = data_atual.replace(month=((data_atual.month - 1 + i) % 12) + 1)
                    if (data_atual.month + i) > 12:
                        data_trans = data_trans.replace(year=data_atual.year + ((data_atual.month + i - 1) // 12))
                    
                    
                    trans = self.despesa_factory.create_transaction(
                        novo_id, 
                        f"{nome} ({i+1}/{rep})" if rep > 1 else nome,
                        valor, 
                        tipo, 
                        data_trans.isoformat(), 
                        desc, 
                        carteira.get_nome(), 
                        fixo,
                        rep
                    )
                    
                    self.storage.add_transaction(trans)
                    novo_id = self.storage.get_next_id()
            else:
                despesa = self.despesa_factory.create_transaction(novo_id, nome, valor, tipo, data, desc, carteira.get_nome(), fixo, rep )
                self.storage.add_transaction(despesa)
                pontos_manager = self.storage.get_pontos_manager()
                carteira.atualiza_carteira(despesa, pontos_manager)

            self.storage.save_data()
            return True, "Despesa adicionada com sucesso."
        except ValidationErrors as e:
            return False, f"\nErros de validação:\n{str(e)}"
            
    def realizar_transacao(self, transacao: Transaction):
        """
        Realiza uma transação que estava pendente, atualizando a carteira correspondente.
        """
        #para transacoes que nao foram pagas quando criadas, como as que se repetem
        carteira = next(c for c in self.storage.get_carteiras() if c.get_nome() == transacao.carteira)
        carteira.atualiza_carteira(transacao)   
    
    def editar_transacao(self, transacao_original: Transaction, novos_dados: dict):
        """
        Edita uma transação existente, atualizando seus dados e ajustando o saldo da carteira se necessário.
        """
        try:
            if transacao_original.categoria != "transferencia":
                carteira_existe = any( c.get_nome() == transacao_original.carteira for c in self.storage.get_carteiras())
                if not carteira_existe:
                    return False, "Erro: Não é possível editar transação de uma carteira deletada."
                    
            carteira_associada = next(c for c in self.storage.get_carteiras() if c.get_nome() == transacao_original.carteira)
            
            valor_antigo_com_sinal = transacao_original.valor
            novo_valor_bruto = float(novos_dados.get('valor', transacao_original._valor))
            
            transacao_original.nome = novos_dados.get('nome', transacao_original.nome)
            transacao_original.categoria = novos_dados.get('categoria', transacao_original.categoria)
            transacao_original._valor = novo_valor_bruto
            
            diferenca_de_saldo = transacao_original.valor - valor_antigo_com_sinal
            
            newDone= novos_dados.get('feita')
            if(transacao_original.done and not newDone):
                print("desficou")
                transacao_original.done = newDone
                carteira_associada.ajustar_saldo(-transacao_original.valor)
            elif (not transacao_original.done and newDone):
                carteira_associada.atualiza_carteira(transacao_original, self.storage.get_pontos_manager())
            elif(transacao_original.done and newDone):
                carteira_associada.ajustar_saldo(diferenca_de_saldo)
            self.storage.save_data()
            
            return True, "Transação atualizada com sucesso!"
    
        except StopIteration:
            return False, "Erro: Carteira associada à transação não foi encontrada."
        except ValueError:
            return False, "Erro de validação: O valor inserido não é um número válido."

    def adicionar_carteira(self, nome: str, desc: str, saldo: float = 0):
        """
        Adiciona uma nova carteira corrente ao sistema.
        """
        try:
            self.validar_carteira(nome, desc, str(saldo))
            carteira = self.corrente_factory.create(nome, desc, saldo)
            self.storage.add_carteira(carteira)
            return True, "Carteira criada com sucesso."
        except ValidationErrors as e:
            return False, f"\nErros de validação:\n{str(e)}"

    def adicionar_cofrinho(self, nome: str, desc: str, timer_mes: int, meta_valor:float, saldo: float = 0):
        """
        Adiciona um novo cofrinho ao sistema.
        """
        try:
            hoje = datetime.datetime.now()
            mes_atual = hoje.month
            ano_atual = hoje.year
            self.validar_carteira(nome, desc, str(saldo))
            cofre = self.cofrinho_factory.create(nome, desc, saldo, timer_mes, mes_atual, ano_atual, meta_valor)
            self.storage.add_cofrinho(cofre)
            return True, "Cofrinho criado com sucesso."
        except ValidationErrors as e:
            return False, f"\nErros de validação:\n{str(e)}"

    def depositar_cofrinho(self, valor: float, cofrinho: Cofrinho, carteira_origem: Carteira):
        """
        Realiza um depósito de uma carteira para um cofrinho.
        """
        if valor <= 0:
            return False, "O valor do depósito deve ser positivo."
        if valor > carteira_origem.get_saldo():
            return False, "Saldo insuficiente na carteira de origem."

        id_saida = self.storage.get_next_id()
        trans_saida = self.despesa_factory.create_transaction(id_saida, f"Depósito para {cofrinho.get_nome()}", valor, "transferencia", datetime.datetime.now().isoformat(), "", carteira_origem.get_nome())
        
        id_entrada = self.storage.get_next_id()
        trans_entrada = self.receita_factory.create_transaction(id_entrada, f"Depósito de {carteira_origem.get_nome()}", valor, "transferencia", datetime.datetime.now().isoformat(), "", cofrinho.get_nome())

        self.storage.add_transaction(trans_saida)
        self.storage.add_transaction(trans_entrada)
        
        carteira_origem.atualiza_carteira(trans_saida)
        cofrinho.depositar(trans_entrada)

        self.storage.save_data()
        return True, f"Valor de R$ {valor:.2f} depositado com sucesso."

    def quebrar_cofrinho(self, cofrinho: Cofrinho, carteira_destino: Carteira):
        """
        Quebra o cofrinho, transferindo o saldo para uma carteira destino e aplicando penalidade se necessário.
        """
        timer = cofrinho.get_timer()
        valor_quebrado = cofrinho.quebrar()
        
        if valor_quebrado > 0:
            id_trans = self.storage.get_next_id()
            trans = self.receita_factory.create_transaction(id_trans, f"Valor do cofre '{cofrinho.get_nome()}'", valor_quebrado, "transferencia", datetime.datetime.now().isoformat(), "Cofre quebrado", carteira_destino.get_nome())
            self.storage.add_transaction(trans)
            carteira_destino.atualiza_carteira(trans)
            # verifica penalidade de pontos
            self.storage.get_pontos_manager().quebrar_cofrinho(timer)
        
        if cofrinho in self.storage.cofrinhos:
            self.storage.cofrinhos.remove(cofrinho)
        self.storage.save_data()
        return valor_quebrado, "Cofrinho quebrado com sucesso!"

    def deletar_transacao(self, transacao: Transaction) -> tuple[bool, str]:
        """
        Deleta uma transação e atualiza o saldo da carteira associada.
        """
        try:
            # Tenta encontrar a carteira associada
            try:
                carteira_associada = next(
                    c for c in self.storage.get_carteiras() 
                    if c.get_nome() == transacao.carteira
                )
                # Se encontrou a carteira, ajusta o saldo
                carteira_associada.ajustar_saldo(-transacao.valor)
            except StopIteration:
                # Carteira não existe mais, continua com a deleção
                pass
            
            # Remove a transação do storage
            self.storage.remove_transaction(transacao.id)
            
            # Se for uma despesa, atualiza o sistema de pontos
            if not isinstance(transacao, Receita):
                pontos_manager = self.storage.get_pontos_manager()
            
            # Salva as alterações
            self.storage.save_data()
            
            return True, "Transação deletada com sucesso!"
            
        except Exception as e:
            return False, f"Erro ao deletar transação: {str(e)}"

    def validar_transacao(self, nome, valor, tipo, carteira):
        """
        Valida os campos de uma transação, lançando exceções em caso de erro.
        """
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
        """
        Valida os campos de uma carteira, lançando exceções em caso de erro.
        """
        errors = ValidationErrors()
        if not nome or not nome.strip(): errors.add(EmptyFieldError("nome"))
        if not desc or not desc.strip(): errors.add(EmptyFieldError("descrição"))
        
        try:
            s = float(saldo)
            if s < 0: errors.add(InvalidValueError("saldo", "não pode ser negativo"))
        except ValueError: errors.add(InvalidTypeError("saldo", "número"))

        if errors.has_errors(): raise errors

    def deletar_carteira(self, carteira: Carteira) -> tuple[bool, str]:
        """
        Deleta uma carteira corrente se ela tiver saldo zero.
        Não deleta as transações associadas, apenas impede novas transações.
        """
        try:
            # Verifica se é uma carteira corrente
            if isinstance(carteira, Cofrinho):
                return False, "Não é possível deletar cofrinhos por este método."
                
            # Verifica se tem saldo zero
            if carteira.get_saldo() != 0:
                return False, f"Não é possível deletar carteira com saldo (atual: R${carteira.get_saldo():.2f})"
                
            # Remove a carteira do storage
            self.storage.remove_carteira(carteira)
        
            # Salva as alterações
            self.storage.save_data()
            
            return True, "Carteira deletada com sucesso!"
            
        except Exception as e:
            return False, f"Erro ao deletar carteira: {str(e)}"

    def get_carteiras(self):
        """Retorna todas as carteiras correntes."""
        return self.storage.get_carteiras()
    def get_cofrinhos(self):
        """Retorna todos os cofrinhos."""
        return self.storage.get_cofrinhos()
    def get_transacoes(self):
        """Retorna todas as transações."""
        return self.storage.get_all_transactions()
    def get_pontos(self):
        """Retorna o gerenciador de pontos."""
        return self.storage.get_pontos_manager()
    def get_metas(self):
        """Retorna as metas do sistema de pontos."""
        return self.storage.get_pontos_manager().get_metas()
    def get_gastos(self):
        """Retorna os gastos do sistema de pontos."""
        return self.storage.get_pontos_manager().get_gastos()
    def get_categorias_disponiveis(self):
        """Retorna as categorias disponíveis para transações."""
        return self.categorias
    def get_mes_atual(self):
        """Retorna o mês atual do sistema."""
        return self._mes_atual
    def get_ano_atual(self):
        """Retorna o ano atual do sistema."""
        return self._ano_atual

    def proximo_mes(self):
        """
        Avança o sistema para o próximo mês.
        """
        if self._mes_atual == 12:
            self._mes_atual = 1
            self._ano_atual += 1
        else:
            self._mes_atual += 1

    def mes_anterior(self):
        """
        Retrocede o sistema para o mês anterior.
        """
        if self._mes_atual == 1:
            self._mes_atual = 12
            self._ano_atual -= 1
        else:
            self._mes_atual -= 1