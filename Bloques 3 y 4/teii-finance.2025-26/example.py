""" Ejemplo de uso del paquete teii. """


import logging

import matplotlib.pyplot as plt

import teii.finance as tf

import datetime as dt


def setup_logging(example_logging_level, finance_logging_level):
    """ Crea y configura logger. """

    # Ahora se configura manualmente el fichero, el formato y los loggers
    file_handler = logging.FileHandler("example.log", mode="w", encoding="utf-8")

    # Se deja el handler en DEBUG ara que no bloquee mensajes
    # El filtrado real lo hace cada logger mediante setLevel()
    file_handler.setLevel(logging.DEBUG)

    # Formato de cada log: fecha - nombre del logger - nivel - mensaje
    file_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))

    # Logger propio de example.py
    logger = logging.getLogger(__name__)

    # Limpiar handlers previos para evitar mensajes duplicados
    logger.handlers.clear()

    # Nivel minimo de mensajes que emitira example.py
    logger.setLevel(example_logging_level)

    # Añadir el handler que escribe en example.log
    logger.addHandler(file_handler)

    # Evitar que los mensajes de example.py se propaguen
    logger.propagate = False

    # Logger base para el paquete teii.finance, los loggers de teii.finance.finance y
    # teii.finance.timeseries pertenecen a esta jerarquia, por eso se configura el logger padre "teii.finance"
    finance_logger = logging.getLogger("teii.finance")

    # Limpiar handlers para evitar duplicados
    finance_logger.handlers.clear()

    # Nivel mínimo de mensajes que emitirá el paquete teii.finance
    finance_logger.setLevel(finance_logging_level)

    # Tambien escribira en example.log usando el mismo handler
    finance_logger.addHandler(file_handler)

    # Evitar propagacion
    finance_logger.propagate = False

    logger.info("Loggers configurados explícitamente: example.py=%s, teii.finance=%s",
                logging.getLevelName(example_logging_level),
                logging.getLevelName(finance_logging_level)
    )

    return logger

def plot(pandas_series, ticker, logger):
    """ Dibuja una gráfica a partir de la serie de Pandas. """

    logger.info("Dibujando gráfica...")

    pandas_series.plot(xlabel='Fecha', ylabel='Precio en USD', title=f"Evolución del Precio de {ticker}")
    plt.show()  # ¡Necesario para que se muestre la gráfica en una ventana!


def main():
    """ Muestra como usar teii-finance. """

    logger = setup_logging(logging.DEBUG, logging.INFO)

    logger.info("Inicio")

    # Define ticker y API key
    ticker = 'IBM'
    my_alpha_vantage_api_key = 'OLEJDK01J91MJZ6R'     # Sólo funcionará con IBM (para demos)
                                                      # Obtenida API key real de https://www.alphavantage.co/support/#api-key
                                                      # (No más de 1 llamada por segundo
                                                      # 5 llamadas por minuto y 25 llamadas por día),

    # Crea cliente
    try:
        tf_client = tf.TimeSeriesFinanceClient(ticker,
                                               my_alpha_vantage_api_key,
                                               logging_level=logging.INFO)
    # Captura y muestra todas las excepciones
    except Exception as e:
        logger.error(f"{e}", exc_info=False)
    # Usa el cliente
    else:
        
        #   Filtra los datos para mostrar únicamente el año 2026
        from_date = dt.date(2026, 1, 1)
        to_date = dt.date(2026, 12, 31)
        # Genera una serie de Pandas con precio de cierre semanal
        pd_series = tf_client.weekly_price(from_date, to_date)

        logger.info(pd_series)

        # Dibuja una gráfica a partir de la serie de Pandas
        plot(pd_series, ticker, logger)
    finally:
        logger.info("Fin")


if __name__ == "__main__":
    main()
