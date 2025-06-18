
def print_carteiras(carteiras):
    """Imprime uma lista de objetos Carteira no console."""
    for carteira in carteiras:
        print("-" * 30)
        print(f"💼 Carteira: {carteira.get_nome()}")
        print(f"💵 Saldo: R$ {carteira.get_saldo():.2f}")
        print(f"📝 Descrição: {carteira.get_descricao()}")
        print("-" * 30)

def print_cofrinhos(cofrinhos):
    """Imprime uma lista de objetos Cofrinho no console."""
    for cofrinho in cofrinhos:
        print("~" * 30)
        print(f"🐷 Cofrinho: {cofrinho.get_nome()}")
        print(f"💵 Saldo: R$ {cofrinho.get_saldo():.2f}")
        print(f"📝 Descrição: {cofrinho.get_descricao()}")
        print("~" * 30)
        
def print_transacoes(transacoes):
    """Imprime uma lista de objetos Transaction no console."""
    if not transacoes:
        print("Nenhuma transação para exibir neste período.")
        return
        
    for transacao in transacoes:
        print("=" * 30)
        print(f"📝 Nome: {transacao.nome}")
        # O .valor já tem o sinal correto
        print(f"💰 Valor: R$ {transacao.valor:.2f}")
        print(f"🏷️ Categoria: {transacao.categoria.capitalize()}")
        print(f"📅 Data: {transacao.data}")
        print(f"📝 Descrição: {transacao.desc}")
        print(f"🔁 Fixo? {'Sim' if transacao.rep>1 else 'Não'}")
        print("=" * 30)