import datetime
import os
import time
from utils.printers import print_carteiras, print_cofrinhos, print_transacoes
from utils.filters import filtra_transacoes_mes
from interfaceFacade import GerenciamentoDeCarteiras

# ==============================================================================
# FUNÇÕES AUXILIARES
# ==============================================================================

def get_numeric_input(prompt: str, value_type: type = float) -> float:
    """
    Solicita um input numérico ao usuário de forma segura,
    tratando erros de valor e permitindo vírgulas.
    """
    while True:
        try:
            input_str = input(prompt)
            value = value_type(input_str.replace(',', '.'))
            return value
        except ValueError:
            print("Entrada inválida. Por favor, digite um número.")

def selecionar_item(lista_itens: list, nome_item: str, impressora_func):
    """
    Função genérica para o usuário selecionar um item de uma lista.
    """
    if not lista_itens:
        print(f"Nenhum(a) {nome_item} disponível. Crie um(a) primeiro.")
        time.sleep(2)
        return None

    if len(lista_itens) == 1:
        return lista_itens[0]

    print(f"Selecione um(a) {nome_item}:")
    impressora_func(lista_itens)

    try:
        prompt = f"Digite o número do(a) {nome_item}: "
        idx = int(get_numeric_input(prompt, value_type=int))
        if 0 <= idx < len(lista_itens):
            return lista_itens[idx]
        else:
            print("Seleção inválida. Usando o primeiro item como padrão.")
            return lista_itens[0]
    except (ValueError, IndexError):
        print("Entrada inválida. Usando o primeiro item como padrão.")
        return lista_itens[0]

def selecionar_categoria(gerenciador: GerenciamentoDeCarteiras) -> str:
    """
    Mostra as categorias disponíveis e permite ao usuário selecionar uma.
    """
    categorias = gerenciador.get_categorias_disponiveis()
    print("Selecione uma categoria:")
    for i, cat in enumerate(categorias):
        print(f"[{i+1}] {cat.capitalize()}")

    try:
        prompt = "Digite o número da categoria: "
        idx = int(get_numeric_input(prompt, value_type=int))
        if 1 <= idx <= len(categorias):
            return categorias[idx - 1]
        else:
            print("Seleção inválida. Usando a primeira categoria como padrão.")
            return categorias[0]
    except (ValueError, IndexError):
        print("Entrada inválida. Usando a primeira categoria como padrão.")
        return categorias[0]

# ==============================================================================
# LÓGICA PRINCIPAL DA INTERFACE
# ==============================================================================

gerenciador = GerenciamentoDeCarteiras()

while True:
    os.system('cls' if os.name == 'nt' else 'clear')

    print(f"Transações feitas em {gerenciador.get_mes_atual():02d}/{gerenciador.get_ano_atual()}:")
    transacoes = gerenciador.get_transacoes()
    
    transacoes_mes = filtra_transacoes_mes(transacoes, gerenciador.get_mes_atual(), gerenciador.get_ano_atual())
    carteiras = gerenciador.get_carteiras()
    cofrinhos = gerenciador.get_cofrinhos()

    print_transacoes(transacoes_mes)
    print_carteiras(carteiras)
    print_cofrinhos(cofrinhos)

    print(f"\n💎 Pontuação atual: {gerenciador.get_pontos()} 💎")

    menu = (
        "\nO que você deseja fazer?\n"
        "[1] Nova transação\n"
        "[2] Depositar no cofrinho\n"
        "[3] Quebrar cofrinho\n"
        "[4] Criar Nova Carteira\n"
        "[5] Criar Novo Cofrinho\n"
        "[6] Mês anterior\n"
        "[7] Próximo mês\n"
        "[8] Editar transação\n"
        "[9] Deletar transação\n"
        "[10] Deletar carteira\n"
        "[0] Sair\n"
        ">>> "
    )
    acao = get_numeric_input(menu, value_type=int)

    if acao == 1: # Nova transação
        carteira = selecionar_item(carteiras, "carteira", print_carteiras)
        if carteira is None:
            continue

        valor = get_numeric_input("Qual o valor, em reais? ")
        modo = get_numeric_input("Despesa(1) ou Ganho(2)? ", int)
        repeticao = input("É uma transação recorrente? (s/n) ").lower() == 's'
        if repeticao:
            print("Quantas vezes essa transação se repete? (digite um número inteiro)")
            rep = get_numeric_input("Número de repetições: ", int)
        else:
            rep = 1
        nome = input("Qual o nome da transação? ")
        desc = input("Qual a descrição? ")
        tipo = selecionar_categoria(gerenciador)
        data = datetime.datetime.now().isoformat()

        if modo == 2:
            result, msg = gerenciador.adicionar_receita(nome, valor, tipo, data, desc, carteira, repeticao, rep)
        elif modo == 1:
            result, msg = gerenciador.adicionar_despesa(nome, valor, tipo, data, desc, carteira, repeticao, rep)
        else:
            result, msg = False, "Modo inválido."

        print(msg)
        time.sleep(3)

    elif acao == 2: # Depositar no cofrinho
        cofrinho = selecionar_item(cofrinhos, "cofrinho", print_cofrinhos)
        if cofrinho is None:
            continue
        
        corrente = selecionar_item(carteiras, "carteira de origem", print_carteiras)
        if corrente is None:
            continue
        
        prompt_valor = f"Saldo disponível na carteira '{corrente.get_nome()}': R$ {corrente.get_saldo():.2f}\nQual o valor a depositar? "
        valor = get_numeric_input(prompt_valor)
        
        result, msg = gerenciador.depositar_cofrinho(valor, cofrinho, corrente)
        print(msg)
        time.sleep(3)

    elif acao == 3: # Quebrar cofrinho
        cofrinho = selecionar_item(cofrinhos, "cofrinho", print_cofrinhos)
        if cofrinho is None:
            continue
        
        corrente = carteiras[0] if carteiras else None
        if corrente is None:
            print("Você precisa de uma carteira para receber o valor do cofrinho.")
            time.sleep(3)
            continue
        
        valor_quebrado, msg = gerenciador.quebrar_cofrinho(cofrinho, corrente)
        if valor_quebrado is not None:
             print(f"Cofrinho quebrado! Valor de R$ {valor_quebrado:.2f} foi adicionado à carteira '{corrente.get_nome()}'.")
        else:
            print(msg)
        time.sleep(4)

    elif acao == 4: # Criar Nova Carteira
        nome = input("Qual o nome da nova carteira? ")
        desc = input("Qual a descrição da nova carteira? ")
        saldo = get_numeric_input("Qual o saldo inicial? ")
        result, msg = gerenciador.adicionar_carteira(nome, desc, saldo)
        print(msg)
        time.sleep(3)

    elif acao == 5: # Criar Novo Cofrinho
        nome = input("Qual o nome do novo cofrinho? ")
        desc = input("Qual a descrição do novo cofrinho? ")
        saldo = get_numeric_input("Qual o saldo inicial? ")
        timer = get_numeric_input("Em quantos meses você quer quebrar o cofre? ", int)
        result, msg = gerenciador.adicionar_cofrinho(nome, desc, timer, saldo)
        print(msg)
        time.sleep(3)

    elif acao == 6:
        gerenciador.mes_anterior()

    elif acao == 7:
        gerenciador.proximo_mes()

    elif acao == 8: # Editar transação
        transacao_para_editar = selecionar_item(transacoes_mes, "transação", print_transacoes)
        if transacao_para_editar is None:
            continue

        print("\nEditando transação. Deixe em branco para manter o valor atual.")

        novo_nome = input(f"Nome [{transacao_para_editar.nome}]: ") or transacao_para_editar.nome
        novo_valor = input(f"Valor [{transacao_para_editar._valor}]: ") or str(transacao_para_editar._valor)

        novos_dados = {'nome': novo_nome, 'valor': novo_valor}

        sucesso, msg = gerenciador.editar_transacao(transacao_para_editar, novos_dados)
        print(msg)
        time.sleep(3)
        
    elif acao == 9: # Deletar transação
        transacao_para_deletar = selecionar_item(transacoes_mes, "transação", print_transacoes)
        if transacao_para_deletar is None:
            continue

        confirmacao = input(f"\nTem certeza que deseja deletar a transação '{transacao_para_deletar.nome}'? (s/n) ")
        if confirmacao.lower() != 's':
            print("Operação cancelada.")
            time.sleep(2)
            continue

        sucesso, msg = gerenciador.deletar_transacao(transacao_para_deletar)
        print(msg)
        time.sleep(3)
        
    elif acao == 10:  # Deletar carteira
        carteira = selecionar_item(carteiras, "carteira", print_carteiras)
        if carteira is None:
            continue

        print(f"\nSaldo atual da carteira: R${carteira.get_saldo():.2f}")
        if carteira.get_saldo() != 0:
            print("Atenção: Só é possível deletar carteiras com saldo zero!")
            time.sleep(3)
            continue

        confirmacao = input(f"\nTem certeza que deseja deletar a carteira '{carteira.get_nome()}'? (s/n) ")
        if confirmacao.lower() != 's':
            print("Operação cancelada.")
            time.sleep(2)
            continue

        sucesso, msg = gerenciador.deletar_carteira(carteira)
        print(msg)
        time.sleep(3)
        
    elif acao == 0:  # Sair (changed from 9 to 0)
        print("Salvando dados... Até a próxima!")
        break
        
    else:
        print("Opção inválida.")
        time.sleep(2)