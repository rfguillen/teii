# Bloques 3 y 4 · Desarrollo Python y análisis de datos

Prácticas que combinan programación Python, consumo de APIs HTTP, transformación de datos y visualización.

## Componentes

| Carpeta | Objetivo |
|---|---|
| [teii-finance.2025-26](teii-finance.2025-26/README.md) | Consultar y analizar series financieras con una jerarquía de clientes Python |
| [notebooks](notebooks/README.md) | Practicar Python y Pandas y construir una visualización meteorológica reactiva |

## Cliente financiero

El paquete `teii.finance` obtiene series semanales de Alpha Vantage, valida los datos y los transforma en estructuras de Pandas. Incluye consultas de precios ajustados, volumen, dividendos anuales y la semana con mayor diferencia entre precio máximo y mínimo.

Se acompaña de pruebas con pytest, configuración de Tox, comprobaciones con Flake8 y mypy y documentación para desarrolladores.

## Notebooks

Los ejercicios de Python y Pandas se publican como notebooks Jupyter. El ejemplo de Marimo utiliza datos meteorológicos de Murcia y permite elegir entre un archivo CSV local y una consulta a Open-Meteo.

## Automatización incluida

Las carpetas `.github/workflows` conservan configuraciones de la entrega para pruebas y empaquetado. Están dentro de estas subcarpetas; su presencia no acredita que exista una automatización activa en la raíz de este repositorio.

## Autoría y calificación

**Daniel Fernandez Ayala y Rafael Guillén García**. Se conserva también el material docente de apoyo.

Calificación de los bloques 3 y 4: **8,7/10**.

[Volver a TEII](../README.md)
