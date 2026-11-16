# Custom exceptions for Project-J

class ProjectJException(Exception):
    """Base exception for Project-J."""
    def __init__(self, detail: str, code: int = 500):
        self.detail = detail
        self.code = code
        super().__init__(self.detail)


class NotFoundException(ProjectJException):
    """Resource not found exception."""
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(detail, code=404)


class ValidationException(ProjectJException):
    """Validation exception."""
    def __init__(self, detail: str = "Validation error"):
        super().__init__(detail, code=422)


class AuthenticationException(ProjectJException):
    """Authentication exception."""
    def __init__(self, detail: str = "Authentication failed"):
        super().__init__(detail, code=401)


class AuthorizationException(ProjectJException):
    """Authorization exception."""
    def __init__(self, detail: str = "Not authorized"):
        super().__init__(detail, code=403)