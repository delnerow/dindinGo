
class sistemaDePontos:
    def __init__(self, pontos, meta_lazer=100, meta_alimentacao=1000, meta_casa=100, meta_mercado=1000, meta_serviço=100,
                 gastos_lazer=0, gastos_alimentacao=0, gastos_casa=0, gastos_mercado=0, gastos_servico=0):
        
        self._pontos = pontos
        self._meta_lazer = meta_lazer
        self._meta_alimentacao = meta_alimentacao
        self._meta_casa = meta_casa
        self._meta_mercado = meta_mercado
        self._meta_servico = meta_serviço

        self._gastos_lazer = gastos_lazer
        self._gastos_alimentacao = gastos_alimentacao
        self._gastos_casa = gastos_casa
        self._gastos_mercado = gastos_mercado
        self._gastos_servico = gastos_servico

    def __adicionar_pontos(self, pontos):
        """Adiciona pontos ao sistema de pontos.
           método privado!!"""
        if pontos < 0:
            raise ValueError("Pontos não podem ser negativos.")
        self._pontos += pontos

    def __remover_pontos(self, pontos):
        """Remove pontos ao sistema de pontos.
           método privado!!"""
        if pontos < 0:
            raise ValueError("Pontos não podem ser negativos.")
        self._pontos -= pontos
        if self._pontos < 0:
            self._pontos = 0

    def __resetar_pontos(self):
        self._pontos = 0

    def get_pontos(self):
        """Retorna a quantidade de pontos acumulados."""
        return self._pontos
    
    def get_metas(self):
        """Retorna um dicionário com as metas de cada categoria."""
        return {
            'meta_lazer': self._meta_lazer,
            'meta_alimentacao': self._meta_alimentacao,
            'meta_casa': self._meta_casa,
            'meta_mercado': self._meta_mercado,
            'meta_servico': self._meta_servico
        }
    
    def get_gastos(self):
        """Retorna um dicionário com os gastos de cada categoria."""
        return {
            'gastos_lazer': self._gastos_lazer,
            'gastos_alimentacao': self._gastos_alimentacao,
            'gastos_casa': self._gastos_casa,
            'gastos_mercado': self._gastos_mercado,
            'gastos_servico': self._gastos_servico
        }
    def adicionar_despesa(self, valor, tipo):
        """Adiciona uma despesa ao sistema de pontos e atualiza os gastos."""
        tipos = {
            'lazer': ('_gastos_lazer', '_meta_lazer'),
            'alimentação': ('_gastos_alimentacao', '_meta_alimentacao'),
            'casa': ('_gastos_casa', '_meta_casa'),
            'mercado': ('_gastos_mercado', '_meta_mercado'),
            'serviço': ('_gastos_servico', '_meta_servico')
        }
        if tipo not in tipos:
            raise ValueError("Tipo de despesa inválido.")

        gasto_attr, meta_attr = tipos[tipo]
        setattr(self, gasto_attr, getattr(self, gasto_attr) + valor)
        meta = getattr(self, meta_attr)
        gasto = getattr(self, gasto_attr)
        pontos_perdidos = (gasto - meta) // 10 if gasto > meta else 0
        if pontos_perdidos > 0:
            self.__remover_pontos(pontos_perdidos)
            
        return pontos_perdidos, gasto, meta

        

    @classmethod
    def from_dict(cls, d):
        return cls(d['pontos'], 
                   d['meta_lazer'], d['meta_alimentacao'], d['meta_casa'], 
                   d['meta_mercado'], d['meta_servico'], 
                   d['gastos_lazer'], d['gastos_alimentacao'], d['gastos_casa'],
                   d['gastos_mercado'], d['gastos_servico'])
    
    def to_dict(self):
        return {
            'pontos': self._pontos,
            'meta_lazer': self._meta_lazer,
            'meta_alimentacao': self._meta_alimentacao,
            'meta_casa': self._meta_casa,
            'meta_mercado': self._meta_mercado,
            'meta_servico': self._meta_servico,
            'gastos_lazer': self._gastos_lazer,
            'gastos_alimentacao': self._gastos_alimentacao,
            'gastos_casa': self._gastos_casa,
            'gastos_mercado': self._gastos_mercado,
            'gastos_servico': self._gastos_servico
        }   