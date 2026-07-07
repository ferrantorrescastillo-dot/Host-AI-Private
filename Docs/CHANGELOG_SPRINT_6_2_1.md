# Sprint 6.2.1 - Hotfix jornadas reales por día

## Problema corregido

El Sprint 6.2 sumaba el total activo global por cocinero mezclando Día 1 y Día 2.
Eso confundía el horario.

## Corrección

- Ahora el total activo se calcula por día.
- Día 1 queda completo de 08:00 a 15:30 para cada cocinero.
- Día 2 solo muestra lo que falta para acabar producción real.
- No se rellenan horas del Día 2 artificialmente.
- Los huecos del Día 1 se rellenan con trabajo útil real:
  - cámaras
  - registros
  - mise en place de mañana
  - etiquetas/GN
  - limpieza de producción

## Archivo modificado

- SERVICIOS/planificador_personal.py

## Prueba

16
7
