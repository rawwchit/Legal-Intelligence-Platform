class AppException(Exception):
    """Base exception for the application."""
    def __init__(self, message: str):
        self.message=message
        super().__init__(message)

class ResourceNotFoundException(AppException):
    """Raised when a requested resource is not found."""
    
class AuthenticationException(AppException):
    """Raised for authentication failures."""

class AIServiceException(AppException):
    """Raised when the AI service is unavailable."""