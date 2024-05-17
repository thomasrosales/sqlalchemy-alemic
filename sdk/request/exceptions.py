
class SdkError(Exception):
    """Base class for all SDK exceptions."""
    pass


class ApiError(SdkError):
    """Exception raised for errors in the API."""
    def __init__(self, status_code, message):
        super().__init__(f"API Error {status_code}: {message}")
        self.status_code = status_code
        self.message = message


class ValidationError(SdkError):
    """Exception raised for validation errors."""
    def __init__(self, message):
        super().__init__(f"Validation Error: {message}")
        self.message = message
