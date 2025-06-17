class TransactionError(Exception):
    """Base exception for transaction errors"""
    pass

class EmptyFieldError(TransactionError):
    """Raised when a required field is empty"""
    def __init__(self, field):
        self.message = f"O campo '{field}' não pode estar vazio"
        super().__init__(self.message)

class InvalidTypeError(TransactionError):
    """Raised when a field has invalid type"""
    def __init__(self, field, expected_type):
        self.message = f"O campo '{field}' deve ser do tipo {expected_type}"
        super().__init__(self.message)

class InvalidValueError(TransactionError):
    """Raised when a value is invalid"""
    def __init__(self, field, reason):
        self.message = f"Valor inválido para '{field}': {reason}"
        super().__init__(self.message)

class CarteiraNotFoundError(TransactionError):
    """Raised when carteira is not found"""
    def __init__(self):
        self.message = "Carteira não encontrada"
        super().__init__(self.message)
        
class ValidationErrors(Exception):
    def __init__(self):
        self.errors = []  # Will store TransactionError instances
    
    def add(self, error: TransactionError):
        self.errors.append(error)
    
    def has_errors(self):
        return len(self.errors) > 0
    
    def __str__(self):
        return "\n".join(str(error) for error in self.errors)