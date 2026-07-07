# Sprint 6.2 - Motor de planificación por elaboraciones

## Objetivo

Rehacer el motor de planificación por trabajadores.

Problema anterior:
Host AI planificaba tareas sueltas y mezclaba elaboraciones sin lógica de cocina.

Ejemplo incorrecto:
- limpiar carrilleras
- preparar encurtidos
- marcar carrilleras
- revisar cámara
- volver a carrilleras

Nuevo criterio:
Host AI planifica ELABORACIONES.

## Cambios

- Cada elaboración tiene un responsable principal.
- El cocinero que empieza una elaboración intenta acabarla.
- Las elaboraciones se planifican en paralelo.
- Los tiempos pasivos liberan al cocinero pero no saltan fases.
- La siguiente fase no empieza hasta que la anterior termina realmente.
- Se equilibran los tres cocineros hacia 7h30 de trabajo activo.
- Si falta carga productiva, se rellenan huecos con trabajo real:
  - registros
  - cámaras
  - limpieza profunda
  - mise en place de mañana
  - etiquetas y GN
- Los reposos o prensados que cruzan día se imprimen como Día 1 → Día 2 para no confundir horarios.

## Archivo modificado

- SERVICIOS/planificador_personal.py

## Prueba

16
7

## Resultado esperado

Debe salir:
- Cocinero 1: 7h30
- Cocinero 2: 7h30
- Cocinero 3: 7h30
- Bloque separado de cocciones/reposos/enfriados en marcha
