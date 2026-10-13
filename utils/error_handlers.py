"""
Custom exceptions and error handling wrappers.
"""

class StudioBaseException(Exception):
    """Base exception for GenAI Video Intelligence Studio."""
    def __init__(self, message: str, details: str = ""):
        super().__init__(message)
        self.message = message
        self.details = details

class OllamaConnectionError(StudioBaseException):
    """Raised when Ollama server is unreachable or model is missing."""
    pass

class MediaProcessingError(StudioBaseException):
    """Raised when FFmpeg/FFprobe operations fail."""
    pass

class YouTubeAPIError(StudioBaseException):
    """Raised when YouTube Data API or metadata extraction fails."""
    pass

class ValidationError(StudioBaseException):
    """Raised when input validation fails."""
    pass

def format_error_for_ui(e: Exception) -> str:
    """Format an exception into a clean, actionable UI message."""
    if isinstance(e, OllamaConnectionError):
        return f"⚠️ **Ollama Error**: {e.message}\n\n*Diagnostics*: {e.details or 'Check if `ollama serve` is running and `ollama list` contains llama3.2.'}"
    elif isinstance(e, YouTubeAPIError):
        return f"⚠️ **YouTube Error**: {e.message}\n\n*Note*: {e.details or 'Ensure the URL is public and valid.'}"
    elif isinstance(e, MediaProcessingError):
        return f"⚠️ **Media Processing Error**: {e.message}\n\n*Details*: {e.details}"
    elif isinstance(e, ValidationError):
        return f"⚠️ **Validation Error**: {e.message}"
    return f"⚠️ **Unexpected Error**: {str(e)}"
