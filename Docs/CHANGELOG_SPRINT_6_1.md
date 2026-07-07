# Sprint 6.1 - Planificación realista desde fichas

## Objetivo

Corregir el problema detectado en Sprint 6.0:

No se puede deshuesar una carrillera mientras todavía está braseando.

## Cambios

- Una fase no se considera terminada hasta que acaba su tiempo pasivo.
- Las fases posteriores no se desbloquean al empezar una cocción, sino al terminarla.
- Los tiempos pasivos liberan al cocinero, pero bloquean la elaboración.
- Se añaden dependencias secuenciales automáticas si la ficha no las trae.
- Se mantiene la búsqueda por nombre de ficha.

## Archivos modificados

- SERVICIOS/produccion_desde_fichas.py

## Cómo probar

16
9
carrillera

## Resultado esperado

Si la carrillera brasea de 10:20 a 13:20,
deshuesar debe salir después de las 13:20, no antes.

## Próximo sprint

Sprint 6.2:

Escandallos completos conectados con fichas técnicas.
