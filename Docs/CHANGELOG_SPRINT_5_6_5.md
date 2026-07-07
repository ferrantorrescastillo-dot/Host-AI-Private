# Sprint 5.6.5 - Planificador personal real

## Cambios

- Rehecho el planificador por trabajadores.
- La salida vuelve a mostrarse agrupada por Cocinero 1, Cocinero 2 y Cocinero 3.
- Los tiempos pasivos no bloquean al cocinero.
- Las cocciones, enfriados y reposos aparecen en un bloque separado.
- Se respetan dependencias reales:
  - no colar fondo antes de terminar cocción
  - no abatir antes de colar
  - no prensar carrillera antes de cocinar/deshuesar
  - no formar croquetas antes de enfriar bechamel
- Si algo no cabe en una jornada de 8 horas, pasa al día siguiente.

## Archivo modificado

- SERVICIOS/planificador_personal.py

## Prueba

Entrar en:

16. Producción Inteligente
7. Planificación por trabajadores
