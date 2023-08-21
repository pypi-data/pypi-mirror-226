"""Exceptions used in dabpumps."""


class DConnectError(Exception):
    """General DConnect error occurred."""


class CannotConnectError(DConnectError):
    """Error to indicate we cannot connect."""


class InvalidAuthError(DConnectError):
    """Error to indicate there is invalid auth."""
