""" Unit tests for teii.finance.timeseries module """


import datetime as dt

import pytest
import requests

import pandas as pd

from pandas.testing import assert_series_equal


from teii.finance import FinanceClientInvalidAPIKey, TimeSeriesFinanceClient, FinanceClientAPIError, FinanceClientInvalidData
from teii.finance.exception import FinanceClientParamError
from importlib import resources
import pandas as pd


def test_constructor_success(api_key_str,
                             mocked_requests):
    # Comprueba que el constructor funciona cuando se le pasa la API key
    TimeSeriesFinanceClient("NVDA", api_key_str)

def test_constructor_env(monkeypatch, mocked_requests):
    # Aquí se simula la API key como variable de entorno
    # El constructor se ejecuta sin recibir api_key_str como parámetro
    monkeypatch.setenv("TEII_FINANCE_API_KEY", "nokey")
    TimeSeriesFinanceClient("NVDA")

def test_constructor_unsuccessful_request(api_key_str, monkeypatch):
    # Se sustituye request.get por una función que siempre falla
    # Se quiere comprobar que el cliente transforma el error de conexión
    # en la excepción "FinanceClientAPIError"
    def mocked_get(_url):
        raise requests.exceptions.ConnectionError("Connection error")
    monkeypatch.setattr("teii.finance.finance.requests.get", mocked_get)
    with pytest.raises(FinanceClientAPIError):
        TimeSeriesFinanceClient("NVDA", api_key_str)

def test_constructor_failure_invalid_api_key():
    # Como no hay API key ni variable de entorno el constructor tiene que lanzar error
    with pytest.raises(FinanceClientInvalidAPIKey):
        TimeSeriesFinanceClient("NVDA")

def test_constructor_invalid_data(api_key_str, mocked_requests):
    # El ticker NODATA usa un JSON con metadatos válidos pero sin datos semanales
    # Por tanto el constructor tiene que fallar al intentar construir el dataframe
    with pytest.raises(FinanceClientInvalidData):
        TimeSeriesFinanceClient("NODATA", api_key_str)

def test_weekly_price_invalid_dates(api_key_str,
                                    mocked_requests):
    fc = TimeSeriesFinanceClient("NVDA", api_key_str)
    
    from_invalido = dt.date(2026, 12, 31)
    to_invalido = dt.date(2025, 1, 1)
    
    with pytest.raises(FinanceClientParamError):
        fc.weekly_price(from_invalido, to_invalido)


def test_weekly_price_no_dates(api_key_str,
                               mocked_requests,
                               pandas_series_NVDA_prices):
    fc = TimeSeriesFinanceClient("NVDA", api_key_str)

    ps = fc.weekly_price()

    assert ps.count() == 1378   # 1999-11-12 to 2026-04-02 (1378 business weeks)

    assert ps.count() == pandas_series_NVDA_prices.count()

    assert_series_equal(ps, pandas_series_NVDA_prices)


def test_weekly_price_dates(api_key_str,
                            mocked_requests,
                            pandas_series_NVDA_prices_filtered):
    fc = TimeSeriesFinanceClient("NVDA", api_key_str)

    ps = fc.weekly_price(dt.date(year=2025, month=4, day=1),
                         dt.date(year=2026, month=3, day=31))

    assert ps.count() == 52    # 2025-04-01 to 2026-03-31 (52 business weeks)

    assert ps.count() == pandas_series_NVDA_prices_filtered.count()

    assert_series_equal(ps, pandas_series_NVDA_prices_filtered)


def test_weekly_volume_invalid_dates(api_key_str,
                                     mocked_requests):
    fc = TimeSeriesFinanceClient("NVDA", api_key_str)

    from_invalido = dt.date(2026, 12, 31)
    to_invalido = dt.date(2025, 1, 1)

    with pytest.raises(FinanceClientParamError):
        fc.weekly_volume(from_invalido, to_invalido)

def test_weekly_volume_no_dates(api_key_str,
                                mocked_requests):
    fc = TimeSeriesFinanceClient("NVDA", api_key_str)

    ps = fc.weekly_volume()

    csv_resource = resources.files("teii.finance.data").joinpath("TIME_SERIES_WEEKLY_ADJUSTED.NVDA.volume.unfiltered.csv")
    pandas_series_NVDA_volumen = pd.read_csv(csv_resource, index_col=0, parse_dates=True).squeeze()

    assert ps.count() == pandas_series_NVDA_volumen.count()
    assert_series_equal(ps, pandas_series_NVDA_volumen)


def test_weekly_volume_dates(api_key_str,
                             mocked_requests):
    fc = TimeSeriesFinanceClient("NVDA", api_key_str)

    ps = fc.weekly_volume(dt.date(year=2025, month=4, day=1),
                         dt.date(year=2026, month=3, day=31))
    
    csv_resource = resources.files("teii.finance.data").joinpath("TIME_SERIES_WEEKLY_ADJUSTED.NVDA.volume.filtered.csv")
    pandas_series_NVDA_volume_filtered = pd.read_csv(csv_resource, index_col=0, parse_dates=True).squeeze()

    assert ps.count() == pandas_series_NVDA_volume_filtered.count()
    assert_series_equal(ps, pandas_series_NVDA_volume_filtered)

def test_yearly_dividends_no_dates(api_key_str,
                                   mocked_requests,
                                   pandas_series_IBM_dividends):
    fc = TimeSeriesFinanceClient("IBM", api_key_str)
    
    ps = fc.yearly_dividends()

    assert ps.count() == 28   # 1999 to 2026 (28 anos)

    assert ps.count() == pandas_series_IBM_dividends.count()

    assert_series_equal(ps, pandas_series_IBM_dividends)


def test_yearly_dividends_dates(api_key_str,
                                mocked_requests,
                                pandas_series_IBM_dividends_filtered):
    fc = TimeSeriesFinanceClient("IBM", api_key_str)

    ps = fc.yearly_dividends(from_year=2024, to_year=2026)

    assert ps.count() == 3    # 2024 to 2026 (3 anos)

    assert ps.count() == pandas_series_IBM_dividends_filtered.count()

    assert_series_equal(ps, pandas_series_IBM_dividends_filtered)  

def test_highest_weekly_variation_no_dates(api_key_str, 
                                           mocked_requests):
    fc = TimeSeriesFinanceClient("NVDA", api_key_str)

    date, high, low, variation = fc.highest_weekly_variation()

    assert isinstance(date, dt.date)
    assert isinstance(high, float)
    assert isinstance(low, float)
    assert isinstance(variation, float)

    assert date == dt.date(year=2021, month=7, day=23) # es la fecha con mas variacion
    assert high == pytest.approx(761.68)
    assert low == pytest.approx(181.64)
    assert variation == pytest.approx(580.04)

def test_highest_weekly_variation_dates(api_key_str,
                                        mocked_requests):
    fc = TimeSeriesFinanceClient("NVDA", api_key_str)

    date, high, low, variation = fc.highest_weekly_variation(
        from_date=dt.date(year=2025, month=4, day=1),
        to_date=dt.date(year=2026, month=3, day=31)
    )

    assert isinstance(date, dt.date)
    assert isinstance(high, float)
    assert isinstance(low, float)
    assert isinstance(variation, float)

    assert date == dt.date(year=2025, month=11, day=7) # es la fecha donde la diferencia es mayor
    assert high == pytest.approx(211.335)
    assert low == pytest.approx(178.91)
    assert variation == pytest.approx(32.425)

