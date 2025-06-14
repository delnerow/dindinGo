

class sistemaDePontos:
    def __init__(self, pontos):
        self._pontos = pontos

    def adicionar_pontos(self, pontos):
        if pontos < 0:
            raise ValueError("Pontos não podem ser negativos.")
        self._pontos += pontos

    def remover_pontos(self, pontos):
        if pontos < 0:
            raise ValueError("Pontos não podem ser negativos.")
        self._pontos -= pontos
        if self._pontos < 0:
            self._pontos = 0

    def get_pontos(self):
        return self.pontos

    def resetar_pontos(self):
        self._pontos = 0

    def getPontos(self):
        return self._pontos
    
    @classmethod
    def from_dict(cls, d):
        return cls(d['pontos'])
    