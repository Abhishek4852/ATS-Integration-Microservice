class ATSError(Exception):
    """Base exception for ATS related errors."""
    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

class ProviderNotFoundError(ATSError):
    """Raised when an unsupported ATS provider is requested."""
    def __init__(self, provider):
        super().__init__(f"ATS provider '{provider}' is not supported.", status_code=400)

class AuthenticationError(ATSError):
    """Raised when ATS authentication fails."""
    def __init__(self, message="Authentication with ATS failed."):
        super().__init__(message, status_code=401)

class ResourceNotFoundError(ATSError):
    """Raised when a requested resource (job, candidate) is not found in ATS."""
    def __init__(self, message="Resource not found in ATS."):
        super().__init__(message, status_code=404)

class ValidationError(ATSError):
    """Raised when input validation fails."""
    def __init__(self, message="Validation error."):
        super().__init__(message, status_code=400)
