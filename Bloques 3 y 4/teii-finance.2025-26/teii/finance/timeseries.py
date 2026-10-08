"""
Time Series Finance Client classes.

This module provides the client to retrieve and process
weekly adjusted time series data from the AlphaVantage API.
"""

import datetime as dt
import logging
from typing import Optional, Union, Tuple

import pandas as pd

from teii.finance import FinanceClient, FinanceClientInvalidData
from teii.finance.exception import FinanceClientParamError


class TimeSeriesFinanceClient(FinanceClient):
    """
    Wrapper around the AlphaVantage API for Time Series Weekly Adjusted.

    This class handles the downloading, parsing, and formatting of
    weekly adjusted time series stock data into a Pandas DataFrame.

    Notes
    -----
    Source:
        https://www.alphavantage.co/documentation/ (TIME_SERIES_WEEKLY_ADJUSTED)
    """

    _data_field2name_type = {
        "1. open":                  ("open",     "float"),
        "2. high":                  ("high",     "float"),
        "3. low":                   ("low",      "float"),
        "4. close":                 ("close",    "float"),
        "5. adjusted close":        ("aclose",   "float"),
        "6. volume":                ("volume",   "int"),
        "7. dividend amount":       ("dividend", "float")
    }

    def __init__(self, ticker: str,
                 api_key: Optional[str] = None,
                 logging_level: Union[int, str] = logging.WARNING) -> None:
        """
        TimeSeriesFinanceClient constructor.

        Parameters
        ----------
        ticker : str
            The stock ticker symbol.
        api_key : str, optional
            The AlphaVantage API key. Default is None.
        logging_level : int or str, default logging.WARNING
            The logging level to use.
        """

        super().__init__(ticker, api_key, logging_level)

        # Se usa un logger especifico para que los mensajes aparezcan
        # como teii.finance.timeseries en el fichero example.log
        self._logger = logging.getLogger(__name__)
        self._logger.info("TimeSeriesFinanceClient initiailzed for ticker '%s'", ticker)

        self._build_data_frame()

    def _build_data_frame(self) -> None:
        """
        Build Pandas DataFrame and format data.

        Raises
        ------
        FinanceClientInvalidData
            If the JSON data is invalid, empty, or missing expected fields.
        """

        self._logger.info("Building pandas DataFrame for ticker '%s'", self._ticker)

        try:
            # Si el diccionario está vacío no se puede construir un datafgrame válido
            if not isinstance(self._json_data, dict) or len(self._json_data) == 0:
                raise ValueError("Weekly adjusted time series data not found")

            # Build Panda's data frame
            data_frame = pd.DataFrame.from_dict(self._json_data, orient='index', dtype='float')

            # Se comprueba que la respuesta tiene todos los campos esperados por
            # TIME_SERIES_WEEKLY_ADJUSTED
            missing_fields = [data_field
                              for data_field in self._data_field2name_type
                              if data_field not in data_frame.columns]

            if len(missing_fields) > 0:
                raise ValueError(f"Missing data fields: {missing_fields}")

            # Rename data fields
            data_frame = data_frame.rename(columns={key: name_type[0]
                                                    for key, name_type in self._data_field2name_type.items()})

            # Set data field types
            data_frame = data_frame.astype(dtype={name_type[0]: name_type[1]
                                           for key, name_type in self._data_field2name_type.items()})

            # Set index type
            data_frame.index = data_frame.index.astype("datetime64[ns]")

            # Sort data
            self._data_frame = data_frame.sort_index(ascending=True)

        except Exception as e:
            # logger.exception registra el mensaje junto con la traza de la excepción
            self._logger.exception("Invalidad data while building pandas dataframe")
            raise FinanceClientInvalidData("Invalid time series data") from e
        else:
            self._logger.info("Pandas dataframe built with %d rows", len(self._data_frame))

    def _build_base_query_url_params(self) -> str:
        """
        Return base query URL parameters.

        Returns
        -------
        str
            The formatted query parameters for the API request.

        Notes
        -----
        Parameters are dependent on the query type:
            https://www.alphavantage.co/documentation/
        URL format:
            https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol=TICKER&outputsize=full&apikey=API_KEY&data_type=json
        """
        self._logger.info("Building query URL parametress for ticker '%s'", self._ticker)

        return f"function=TIME_SERIES_WEEKLY_ADJUSTED&symbol={self._ticker}&outputsize=full&apikey={self._api_key}"

    @classmethod
    def _build_query_data_key(cls) -> str:
        """
        Return data query key.

        Returns
        -------
        str
            The dictionary key for the time series data.
        """

        # Como es un metodo de clase no hay self._logger
        # Se obtiene el logger que está asociado al módulo actual
        logging.getLogger(__name__).info("Building query data key for %s", cls.__name__)

        return "Weekly Adjusted Time Series"

    def _validate_query_data(self) -> None:
        """
        Validate query data.

        Raises
        ------
        FinanceClientInvalidData
            If the expected metadata field '2. Symbol' does not match the ticker.
        """

        self._logger.info("Validating metadata for ticker '%s'", self._ticker)
        try:
            assert self._json_metadata["2. Symbol"] == self._ticker
        except Exception as e:
            self._logger.exception("Invalid metadata for ticker '%s'", self._ticker)
            raise FinanceClientInvalidData("Metadata field '2. Symbol' not found") from e
        else:
            self._logger.info(f"Metadata key '2. Symbol' = '{self._ticker}' found")

    def weekly_price(self,
                     from_date: Optional[dt.date] = None,
                     to_date: Optional[dt.date] = None) -> pd.Series:
        """
        Return weekly close price from 'from_date' to 'to_date'.

        Parameters
        ----------
        from_date : datetime.date, optional
            The starting date for the price series.
        to_date : datetime.date, optional
            The ending date for the price series.

        Returns
        -------
        pandas.Series
            A Series containing the weekly adjusted close prices.

        Raises
        ------
        FinanceClientParamError
            If `from_date` is strictly greater than `to_date`.
        """

        self._logger.info("Getting weekly price from %s to %s", from_date, to_date)

        assert self._data_frame is not None

        series = self._data_frame['aclose']

        # Comprueba que from_date <= to_date y genera excepción 'FinanceClientParamError' en caso de error
        if from_date is not None and to_date is not None:
            if from_date > to_date:
                raise FinanceClientParamError("Error: from_date must be <= to_date")

            # FIXME: type hint error
            series = series.loc[from_date:to_date]  # type: ignore

        self._logger.info("WEekly price series returned with %d rows", series.count())

        return series

    def weekly_volume(self,
                      from_date: Optional[dt.date] = None,
                      to_date: Optional[dt.date] = None) -> pd.Series:
        """
        Return weekly volume from 'from_date' to 'to_date'.

        Parameters
        ----------
        from_date : datetime.date, optional
            The starting date for the volume series.
        to_date : datetime.date, optional
            The ending date for the volume series.

        Returns
        -------
        pandas.Series
            A Series containing the weekly trading volumes.

        Raises
        ------
        FinanceClientParamError
            If `from_date` is strictly greater than `to_date`.
        """

        self._logger.info("Getting weekly volume from %s to %s", from_date, to_date)

        assert self._data_frame is not None

        series = self._data_frame['volume']

        # Comprueba que from_date <= to_date y genera excepción 'FinanceClientParamError' en caso de error
        if from_date is not None and to_date is not None:
            if from_date > to_date:
                raise FinanceClientParamError("Error: from_date must be <= to_date")

            # FIXME: type hint error
            series = series.loc[from_date:to_date]  # type: ignore

        self._logger.info("Weekly volume series returned with %d rows", series.count())

        return series

    def yearly_dividends(self,
                         from_year: Optional[int] = None,
                         to_year: Optional[int] = None) -> pd.Series:
        """
        Return yearly accumulated dividends from 'from_year' to 'to_year'.

        Parameters
        ----------
        from_year : int, optional
            The starting year/date for the dividends.
        to_year : int, optional
            The ending year/date for the dividends.

        Returns
        -------
        pandas.Series
            A Series containing the accumulated yearly dividends.

        Raises
        ------
        FinanceClientParamError
            If `from_year` is strictly greater than `to_year`.
        """

        self._logger.info("Getting yearly dividends from %s to %s", from_year, to_year)

        assert self._data_frame is not None

        # Comprueba que from_year <= to_year

        if from_year is not None and to_year is not None:
            if from_year > to_year:

                # from teii.finance.exception import FinanceClientParamError  # type: ignore
                raise FinanceClientParamError("Error: from_year must be <= to_year")  # type: ignore

        # Agrupa por ano y suma los dividendos
        series = self._data_frame['dividend'].groupby(self._data_frame.index.year).sum()

        # Filtra por anos
        if from_year is not None and to_year is not None:
            series = series.loc[from_year:to_year]  # type: ignore
        elif from_year is not None:
            series = series.loc[from_year:]  # type: ignore
        elif to_year is not None:
            series = series.loc[:to_year]  # type: ignore

        self._logger.info("Yearly dividends series returned with %d rows", series.count())

        return series

    def highest_weekly_variation(self,
                                 from_date: Optional[dt.date] = None,
                                 to_date: Optional[dt.date] = None) -> Tuple[dt.date, float, float, float]:
        """
        Return the week with the highest stock price variation.

        Parameters
        ----------
        from_date : datetime.date, optional
            The starting date for the search.
        to_date : datetime.date, optional
            The ending date for the search.

        Returns
        -------
        tuple of (datetime.date, float, float, float)
            A tuple containing:
            - The date of the highest variation.
            - The high price of that week.
            - The low price of that week.
            - The absolute variation (high - low).
        """

        self._logger.info("Getting highest weekly variation from %s to %s", from_date, to_date)

        assert self._data_frame is not None

        data_frame = self._data_frame

        # FIXME: type hint error
        if from_date is not None or to_date is not None:
            data_frame = data_frame.loc[from_date:to_date]  # type: ignore

        weekly_variation = data_frame["high"] - data_frame["low"]

        date = weekly_variation.idxmax()
        high = float(data_frame.loc[date, "high"])
        low = float(data_frame.loc[date, "low"])
        variation = float(weekly_variation.loc[date])

        self._logger.info("Highest weekly variation found on %s: high=%s, low=%s, variation=%s",
                          date.date(), high, low, variation)

        return date.date(), high, low, variation
