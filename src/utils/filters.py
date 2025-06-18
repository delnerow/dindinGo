import datetime


def filtra_transacoes_mes(transacoes, mes, ano):
    result = []
    for t in transacoes:
        data = datetime.datetime.fromisoformat(t.data)
        if data.month == mes and data.year == ano:
            result.append(t)
        elif t.rep>1:
            # Adiciona transações fixas de meses anteriores/próximos
            if (data.year < ano) or (data.year == ano and data.month <= mes):
                result.append(t)
    return result