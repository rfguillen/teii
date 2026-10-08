# Implementación de teii.finance

El paquete separa la comunicación HTTP y el tratamiento general de respuestas de las operaciones específicas sobre series temporales.

| Módulo | Responsabilidad |
|---|---|
| `finance.py` | Clase abstracta `FinanceClient`: configuración de clave, consultas HTTP, procesamiento de JSON y exportación |
| `timeseries.py` | Clase `TimeSeriesFinanceClient`: construcción del DataFrame y consultas de precios, volumen, dividendos y variación semanal |
| `exception.py` | Excepciones de la biblioteca |
| `__init__.py` | Interfaz de importación del subpaquete |
| `data` | Recursos de datos utilizados por el proyecto y las pruebas |

## Flujo de datos

El constructor obtiene la clave recibida como argumento o desde `TEII_FINANCE_API_KEY`, consulta el servicio y procesa la respuesta. El cliente de series comprueba los campos esperados, transforma los tipos de las columnas y ordena los datos por fecha.

Las operaciones de análisis trabajan después sobre ese DataFrame. El precio semanal se toma del cierre ajustado; la variación semanal se calcula como máximo menos mínimo.

[Instalación y ejemplos](../../README.md)
