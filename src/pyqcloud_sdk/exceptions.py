# -*- coding: utf-8 -*-


class QcloudWrapperError(Exception):
    """Base exception class for all qcloud-sdk-python-wrapper errors."""

    pass


class ConfigError(QcloudWrapperError):
    """Raised for errors related to client configuration."""

    pass


class AuthenticationError(ConfigError):
    """Raised for authentication-related errors."""

    pass


class ServiceDiscoveryError(QcloudWrapperError):
    """Raised for errors during service discovery."""

    pass


class ServiceNotFoundError(ServiceDiscoveryError):
    """Raised when the requested Tencent Cloud service is not found."""

    pass


class ServiceDefinitionError(ServiceDiscoveryError):
    """Raised when there are errors in the service definition."""

    pass


class APIError(QcloudWrapperError):
    """Base exception class for Tencent Cloud API call errors."""

    pass


class ClientError(APIError):
    """Raised for client-side errors during API calls."""

    pass


class ServerError(APIError):
    """Raised for errors originating from the Tencent Cloud server."""

    def __init__(self, message, request_id=None):
        super().__init__(message)
        self._request_id = request_id

    @property
    def request_id(self):
        """str: The request ID returned by the Tencent Cloud API (if available)."""
        return self._request_id


class LoggingError(QcloudWrapperError):
    """Raised for errors related to logging."""

    pass
