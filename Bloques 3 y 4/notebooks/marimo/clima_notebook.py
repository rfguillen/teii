import marimo

__generated_with = "0.17.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import requests
    import os
    from pathlib import Path

    mo.md(
        """
        # Análisis Meteorológico Reactivo
        Este notebook permite consultar datos climáticos.
        """
    )

    # --- Configuración de la fuente de datos ---
    fuente_data = mo.ui.radio(
        options=["Local", "API (Consulta en tiempo real)"],
        value="Local",
        label="Selecciona la fuente de datos:"
    )
    fuente_data
    return Path, fuente_data, mo, pd, requests


@app.cell
def _(Path, fuente_data, mo, pd, requests):
    # --- Lógica de Obtención de Datos ---
    DATA_DIR = Path("data")
    # Nos aseguramos de que la carpeta data/ exista
    DATA_DIR.mkdir(exist_ok=True)
    FILE_PATH = DATA_DIR / "clima_murcia.csv"

    df_clima = None

    if fuente_data.value == "Local":
        if FILE_PATH.exists():
            df_clima = pd.read_csv(FILE_PATH)
            # Limpiamos el tipo de dato de la fecha
            df_clima["Fecha"] = pd.to_datetime(df_clima["Fecha"])
            mensaje_estado = mo.md("**Datos cargados correctamente desde el archivo local (`data/clima_murcia.csv`).**")
        else:
            mensaje_estado = mo.md("**Error:** El archivo local de Murcia no existe. Por favor, selecciona la opción 'API' arriba para descargarlo por primera vez.")

    else:
        # URL de Open-Meteo para Murcia (Lat: 37.9870, Lon: -1.1300)
        # Pedimos la temperatura y la velocidad del viento por horas
        url = "https://api.open-meteo.com/v1/forecast?latitude=37.9870&longitude=-1.1300&hourly=temperature_2m,wind_speed_10m"
        try:
            response = requests.get(url)
            response.raise_for_status() # Lanza excepción si el código no es 200
            data_json = response.json()

            # Convertimos el JSON a DataFrame
            df_clima = pd.DataFrame(data_json["hourly"])

            df_clima = df_clima.rename(columns={
                "time": "Fecha",
                "temperature_2m": "Temperatura (°C)",
                "wind_speed_10m": "Viento (km/h)"
            })

            df_clima["Fecha"] = pd.to_datetime(df_clima["Fecha"])

            # Lo guardamos en CSV para que la opción 'Local' funcione a partir de ahora
            df_clima.to_csv(FILE_PATH, index=False)
            mensaje_estado = mo.md("**Datos de Murcia descargados de la API y guardados en caché local.**")

        except Exception as e:
            mensaje_estado = mo.md(f"**Error en la API:** {e}")
    return df_clima, mensaje_estado


@app.cell
def _(df_clima, mensaje_estado, mo):
    # --- Visualización del Estado y la Tabla ---
    if df_clima is not None:
        # Si hay datos, mostramos el mensaje y las primeras 10 filas en una tabla interactiva
        salida = mo.vstack([
            mensaje_estado,
            mo.ui.table(df_clima.head(10))
        ])
    else:
        # Si no hay datos (ej. falta el archivo local), solo mostramos el error
        salida = mensaje_estado

    salida
    return


@app.cell
def _(df_clima, mo):
    import plotly.express as px

    # --- Gráfico Interactivo ---
    if df_clima is not None:
        # Gráfico de líneas para temperatura y viento
        fig = px.line(
            df_clima,
            x="Fecha",
            y=["Temperatura (°C)", "Viento (km/h)"],
            title="Evolución del Clima en Murcia (7 días)",
            markers=True # Añade puntos para cada medición
        )
    
        # Ponemos el diseño un poco más limpio
        fig.update_layout(
            legend_title_text='Indicadores meteorológicos',
            xaxis_title="Día y Hora",
            yaxis_title="Valores"
        )
    
        grafico_salida = fig
    else:
        grafico_salida = mo.md("No hay datos para generar el gráfico.")

    grafico_salida
    return


if __name__ == "__main__":
    app.run()
