"""
Finance subpackage that retrieves finance data from AlphaVantage.

Classes
-------
FinanceClient
    Abstract base class for financial API clients.
TimeSeriesFinanceClient
    Client to retrieve and process weekly adjusted time series data.

Exceptions
----------
FinanceClientAPIError
    Exception raised when there is an API communication error.
FinanceClientInvalidAPIKey
    Exception raised when the provided API key is invalid.
FinanceClientInvalidData
    Exception raised when the API returns invalid or unexpected data.
FinanceClientIOError
    Exception raised when there is an I/O error processing files.
"""

from .exception import (FinanceClientAPIError, FinanceClientInvalidAPIKey,
                        FinanceClientInvalidData, FinanceClientIOError)
from .finance import FinanceClient
from .timeseries import TimeSeriesFinanceClient

__all__ = ('FinanceClientInvalidAPIKey',
           'FinanceClientAPIError',
           'FinanceClientInvalidData',
           'FinanceClientIOError',
           'FinanceClient',
           'TimeSeriesFinanceClient')
