"""
Finance Client classes.

This module defines the abstract base class for interacting with
the AlphaVantage Finance API.
"""

import json
import logging
import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, Union

import pandas as pd
import requests

from teii.finance import (FinanceClientAPIError, FinanceClientInvalidAPIKey,
                          FinanceClientInvalidData, FinanceClientIOError)


class FinanceClient(ABC):
    """
    Wrapper around the Finance API.

    This abstract base class handles API key validation, logging
    configuration, HTTP requests, and basic data processing.

    Attributes
    ----------
    _ticker : str
        The stock ticker symbol.
    _api_key : str or None
        The API key used for authentication.
    _logger : logging.Logger
        The logger instance for the class.
    _json_metadata : dict
        Metadata extracted from the API response.
    _json_data : dict
        Main data extracted from the API response.
    _data_frame : pandas.DataFrame or None
        Pandas DataFrame containing the processed time series data.
    """

    _FinanceBaseQueryURL = "https://www.alphavantage.co/query?"  # Class variable

    def __init__(self, ticker: str,
                 api_key: Optional[str] = None,
                 logging_level: Union[int, str] = logging.WARNING,
                 logging_file: Optional[str] = None) -> None:
        """
        FinanceClient constructor.

        Parameters
        ----------
        ticker : str
            The stock ticker symbol (e.g., 'NVDA').
        api_key : str, optional
            The AlphaVantage API key. Default is None (uses env variable).
        logging_level : int or str, default logging.WARNING
            The logging level to use.
        logging_file : str, optional
            Path to a file where logs should be saved.

        Raises
        ------
        FinanceClientInvalidAPIKey
            If the API key is not provided and cannot be found in the environment.
        """

        self._ticker: str = ticker
        self._api_key: Optional[str] = api_key

        # Logging configuration
        self._setup_logging(logging_level, logging_file)

        # Finance API key configuration
        self._logger.info("API key configuration")
        if self._api_key is None:
            self._api_key = os.getenv("TEII_FINANCE_API_KEY")
        if self._api_key is None or not isinstance(self._api_key, str):
            raise FinanceClientInvalidAPIKey(f"{self.__class__.__qualname__} operation failed")

        # Query Finance API
        self._logger.info("Finance API access...")
        response = self._query_api()

        # Process query response
        self._logger.info("Finance API query response processing...")
        self._process_query_response(response)

        # Validate query data
        self._logger.info("Finance API query data validation...")
        self._validate_query_data()

        # Panda's Data Frame
        self._data_frame: Optional[pd.DataFrame] = None

    def _setup_logging(self,
                       logging_level: Union[int, str],
                       logging_file: Optional[str]) -> None:
        """
        Set up the logging configuration.

        Parameters
        ----------
        logging_level : int or str
            The logging level.
        logging_file : str, optional
            Path to the log file.
        """
        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(logging_level)

    @classmethod
    def _build_base_query_url(cls) -> str:
        """
        Return base query URL.

        Returns
        -------
        str
            The base URL for the API.

        Notes
        -----
        URL is independent from the query type.
            https://www.alphavantage.co/documentation/
        URL format:
            https://www.alphavantage.co/query?PARAMS
        """

        return cls._FinanceBaseQueryURL

    @abstractmethod
    def _build_base_query_url_params(self) -> str:
        """
        Return base query URL parameters.

        Returns
        -------
        str
            The formatted query parameters.

        Notes
        -----
        Parameters are dependent on the query type:
            https://www.alphavantage.co/documentation/
        URL format:
            https://www.alphavantage.co/query?PARAMS
        """

        pass  # pragma: nocover

    def _query_api(self) -> requests.Response:
        """
        Query API endpoint.

        Returns
        -------
        requests.Response
            The HTTP response object from the API.

        Raises
        ------
        FinanceClientAPIError
            If the API request fails or the status code is not 200.
        """

        try:
            url = self.__class__._build_base_query_url()
            params = self._build_base_query_url_params()
            response = requests.get(f"{url}{params}")
            assert response.status_code == 200
        except Exception as e:
            raise FinanceClientAPIError("Unsuccessful API access") from e
        else:
            self._logger.info("Successful API access "
                              f"[URL: {response.url}, status: {response.status_code}]")
        return response

    @classmethod
    def _build_query_metadata_key(cls) -> str:
        """
        Return metadata query key.

        Returns
        -------
        str
            The dictionary key for metadata ('Meta Data').
        """

        return "Meta Data"

    @classmethod
    @abstractmethod
    def _build_query_data_key(cls) -> str:
        """
        Return data query key.

        Returns
        -------
        str
            The dictionary key for the main data.
        """

        pass  # pragma: nocover

    def _process_query_response(self, response: requests.Response) -> None:
        """
        Preprocess query data.

        Extracts metadata and data fields from the JSON response.

        Parameters
        ----------
        response : requests.Response
            The HTTP response containing the JSON data.

        Raises
        ------
        FinanceClientInvalidData
            If the expected metadata or data keys are missing.
        """

        try:
            json_data_downloaded = response.json()
            self._json_metadata = json_data_downloaded[self._build_query_metadata_key()]
            self._json_data = json_data_downloaded[self._build_query_data_key()]
        except Exception as e:
            self._logger.exception("Error processing query response")
            print(f"Response content: '{response.text}'")
            raise FinanceClientInvalidData("Invalid data") from e
        else:
            self._logger.info("Metadata and data fields found")

        self._logger.info(f"Metadata: '{self._json_metadata}'")
        self._logger.info(f"Data: '{json.dumps(self._json_data)[0:218]}...'")

    @abstractmethod
    def _validate_query_data(self) -> None:
        """
        Validate query data.
        """

        pass  # pragma: nocover

    def to_pandas(self) -> pd.DataFrame:
        """
        Return pandas data frame from json data.

        Returns
        -------
        pandas.DataFrame
            The processed DataFrame.
        """

        assert self._data_frame is not None

        return self._data_frame

    def to_csv(self, path2file: Path) -> Path:
        """
        Write json data into csv file 'path2file'.

        Parameters
        ----------
        path2file : pathlib.Path
            The path where the CSV file will be saved.

        Returns
        -------
        pathlib.Path
            The path of the created CSV file.

        Raises
        ------
        FinanceClientIOError
            If the file cannot be written due to an I/O or permission error.
        """

        assert self._data_frame is not None

        try:
            self._data_frame.to_csv(path2file)
        except (IOError, PermissionError) as e:
            raise FinanceClientIOError(f"Unable to write json data into file '{path2file}'") from e

        return path2file
