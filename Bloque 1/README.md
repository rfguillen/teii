# Bloque 1 · Programación lineal con SageMath

Notebook dedicado a resolver problemas de optimización lineal.

## Qué resuelve

El primer ejercicio estudia las intersecciones de las rectas asociadas a las restricciones, comprueba qué vértices son factibles y evalúa en ellos una función objetivo. Incluye las funciones `Redundante` y `Resol1` para tratar las restricciones y seleccionar el mejor vértice de los casos propuestos.

El segundo ejercicio trabaja con una tabla de programación lineal: extracción de columnas y términos independientes, operaciones de pivote y actualización de la tabla hasta obtener una solución con `Simplex`.

## Archivo

[teii-bloque1.ipynb](teii-bloque1.ipynb) contiene el código, los ejemplos y sus salidas guardadas.

## Cómo utilizarlo

1. Abre el notebook en Jupyter con SageMath disponible.
2. Selecciona el kernel **SageMath**. El archivo se guardó con SageMath 10.7.
3. Ejecuta las celdas en orden para definir las funciones auxiliares antes de los ejemplos.
4. Modifica las restricciones o la función objetivo de los ejemplos para estudiar otros casos del mismo formato.

El código utiliza construcciones de SageMath como `var`, `solve`, `QQ`, `block_matrix` y rangos `[a..b]`; necesita ese entorno para ejecutarse correctamente.

## Resultado académico

Calificación: **10/10**.

[Volver a TEII](../README.md)
