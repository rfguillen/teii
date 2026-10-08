# Análisis meteorológico reactivo con Marimo

Notebook interactivo que consulta datos meteorológicos de Murcia y muestra la evolución de la temperatura y la velocidad del viento.

## Funcionamiento

Un selector permite utilizar dos fuentes: un CSV local o la API de Open-Meteo. Cuando se consulta la API, el programa transforma la respuesta JSON en un DataFrame y guarda los datos en `data/clima_murcia.csv` para reutilizarlos en modo local.

La interfaz presenta el estado de la carga, una tabla con las primeras diez filas y un gráfico interactivo de líneas con Plotly. Las celdas se actualizan según las dependencias del notebook.

## Instalación y ejecución

Desde esta carpeta, dentro de un entorno Python:

```bash
python -m pip install marimo pandas requests plotly
python -m marimo edit clima_notebook.py
```

También puedes abrirlo en modo aplicación con:

```bash
python -m marimo run clima_notebook.py
```

Ejecuta los comandos desde esta carpeta para que la ruta `data` corresponda a los archivos del notebook. El modo API requiere conexión a Internet. Si el CSV no está disponible, la interfaz permite consultar la API para crearlo.

## Archivos

`clima_notebook.py` contiene la aplicación reactiva y `data` reúne los datos locales.

[Volver a notebooks](../README.md)
