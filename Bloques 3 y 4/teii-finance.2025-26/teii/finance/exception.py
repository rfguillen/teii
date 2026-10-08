"""
Exception classes.

This module contains the custom exception hierarchy used by the
finance package to handle API, data, and input errors.
"""


class FinanceClientError(Exception):
    """
    FinanceClient exception base class.

    Notes
    -----
    Based on the Transformer Pattern:
    https://www.loggly.com/blog/exceptional-logging-of-exceptions-in-python/
    """

    pass


class FinanceClientInvalidAPIKey(FinanceClientError):
    """
    Invalid finance API Key.
    """

    pass


class FinanceClientAPIError(FinanceClientError):
    """
    Finance API access failure.
    """

    pass


class FinanceClientInvalidData(FinanceClientError):
    """
    Finance API returned incomplete or malformed data.
    """

    pass


class FinanceClientIOError(FinanceClientError):
    """
    Error reading or writing data file.
    """

    pass


class FinanceClientParamError(FinanceClientError):  # Creada en Ejercicio PRICE
    """
    Invalid parameters passed to a method.
    """

    pass
