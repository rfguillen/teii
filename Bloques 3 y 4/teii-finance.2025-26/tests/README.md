# Pruebas

Pruebas con pytest para comprobar el comportamiento de `TimeSeriesFinanceClient`.

## Casos cubiertos por los archivos

- Creación del cliente con clave explícita o mediante variable de entorno.
- Manejo de fallos de conexión, falta de clave y respuestas sin datos válidos.
- Consultas de precios y volumen, con y sin intervalos temporales.
- Rechazo de ciertos intervalos de fechas invertidos.
- Agregación anual de dividendos.
- Cálculo de la semana de mayor variación y comprobación de los tipos de salida.

## Ejecución

Desde la raíz del proyecto `teii-finance.2025-26`, después de instalar las dependencias de desarrollo:

```bash
python -m pytest -v --cov=teii --cov-report=term-missing tests/finance
```

`conftest.py` contiene fixtures de apoyo y `finance/test_timeseriesfinanceclient.py` reúne los casos de prueba. Su presencia describe las comprobaciones incluidas; el resultado se obtiene al ejecutarlas en el entorno correspondiente.

[Volver al proyecto](../README.md)
