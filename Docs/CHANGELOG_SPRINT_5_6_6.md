# Sprint 5.6.6 - Dueño de elaboración y carga equilibrada

## Cambios

- Añadida regla de dueño de elaboración:
  - quien empieza una elaboración intenta continuarla hasta terminarla.
  - reduce cambios raros entre cocineros.
- Carrilleras, Fondo oscuro y Croquetas intentan mantenerse en el mismo cocinero.
- Añadidas tareas flexibles para rellenar huecos:
  - mise en place de mañana
  - revisión de cámaras
  - salsa fría / mise en place de servicio
- Se imprime total activo por cocinero y día.
- Se mantiene salida agrupada por Cocinero 1, Cocinero 2 y Cocinero 3.
- Los tiempos pasivos siguen separados y no bloquean al trabajador.

## Archivo modificado

- SERVICIOS/planificador_personal.py

## Prueba

16. Producción Inteligente
7. Planificación por trabajadores
