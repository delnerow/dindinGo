"""
exceptionHandlers.py
-------------------
Define exceções customizadas para validação e manipulação de transações e carteiras.
Inclui classes para erros de campo vazio, tipo inválido, valor inválido e agrupamento de erros de validação.
"""
class TransactionError(Exception):
    """Exceção base para erros de transação."""
    pass

class EmptyFieldError(TransactionError):
    """Exceção para campo obrigatório vazio."""
    def __init__(self, field):
        self.message = f"O campo '{field}' não pode estar vazio"
        super().__init__(self.message)

class InvalidTypeError(TransactionError):
    """Exceção para tipo inválido em um campo."""
    def __init__(self, field, expected_type):
        self.message = f"O campo '{field}' deve ser do tipo {expected_type}"
        super().__init__(self.message)

class InvalidValueError(TransactionError):
    """Exceção para valor inválido em um campo."""
    def __init__(self, field, reason):
        self.message = f"Valor inválido para '{field}': {reason}"
        super().__init__(self.message)

class CarteiraNotFoundError(TransactionError):
    """Exceção para carteira não encontrada."""
    def __init__(self):
        self.message = "Carteira não encontrada"
        super().__init__(self.message)
        
class ValidationErrors(Exception):
    """Agrupa múltiplos erros de validação para exibição conjunta."""
    def __init__(self):
        self.errors = []  # Will store TransactionError instances
    
    def add(self, error: TransactionError):
        self.errors.append(error)
    
    def has_errors(self):
        return len(self.errors) > 0
    
    def __str__(self):
        return "\n".join(str(error) for error in self.errors)