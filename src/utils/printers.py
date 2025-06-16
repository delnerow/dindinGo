

def printCarteiras(carteiras):
    for carteira in carteiras:
        print("-"*30)
        print(f"💼 Carteira: {carteira.getNome()}")
        print(f"💵 Saldo: {carteira.getSaldo()}")
        print(f"📝 Descrição: {carteira.getDescricao()}")
        print("-"*30)
def printCofrinhos(cofrinhos):
    for cofrinho in cofrinhos:
        print("~"*30)
        print(f"🐷 Cofrinho: {cofrinho._nome}")
        print(f"💵 Saldo: {cofrinho._saldo}")
        print(f"📝 Descrição: {cofrinho._descricao}")
        print("~"*30)
        
def printTransacoes(transacoes):
    for transacao in transacoes:
        print("="*30)
        print(f"📝 Nome: {transacao.nome}")
        print(f"💰 Valor: {transacao.valor}")
        print(f"🏷️ Categoria: {transacao.categoria}")
        print(f"📅 Data: {transacao.data}")
        print(f"📝 Descrição: {transacao.desc}")
        print(f"🔁 Fixo? {'Sim' if transacao.fixo else 'Não'}")
        print("="*30)