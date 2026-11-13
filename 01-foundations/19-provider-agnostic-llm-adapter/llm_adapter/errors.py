"""Normalized provider error taxonomy.

Concrete provider adapters translate their SDK/HTTP errors into these types.
The client does not guess retryability from arbitrary exception messages.
"""
class ProviderError(RuntimeError):
    def __init__(self, message: str, *, provider: str, code: str, retryable: bool = False, status_code: int | None = None) -> None:
        if not provider or not code:
            raise ValueError("provider and code are required")
        super().__init__(message)
        self.provider, self.code, self.retryable, self.status_code = provider, code, retryable, status_code


class ProviderUnavailable(ProviderError):
    def __init__(self, message: str, *, provider: str) -> None:
        super().__init__(message, provider=provider, code="unavailable", retryable=True)


class ProviderTimeout(ProviderError):
    def __init__(self, message: str, *, provider: str) -> None:
        super().__init__(message, provider=provider, code="timeout", retryable=True)


class ProviderRateLimited(ProviderError):
    def __init__(self, message: str, *, provider: str, retry_after: float | None = None) -> None:
        if retry_after is not None and (isinstance(retry_after, bool) or not isinstance(retry_after, (int, float)) or retry_after < 0):
            raise ValueError("retry_after must be a non-negative number or None")
        super().__init__(message, provider=provider, code="rate_limited", retryable=True, status_code=429)
        self.retry_after = retry_after


class ProviderAuthenticationError(ProviderError):
    def __init__(self, message: str, *, provider: str) -> None:
        super().__init__(message, provider=provider, code="authentication_failed", status_code=401)


class ProviderInvalidRequest(ProviderError):
    def __init__(self, message: str, *, provider: str) -> None:
        super().__init__(message, provider=provider, code="invalid_request", status_code=400)


class ProviderResponseError(ProviderError):
    def __init__(self, message: str, *, provider: str) -> None:
        super().__init__(message, provider=provider, code="invalid_provider_response")
