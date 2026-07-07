# Sprint 5.6.3 - Hotfix recurso lista

Corrección del error `unhashable type: list` en la planificación por trabajadores.

Cambios:
- Corrige fases que tenían dependencias pasadas por error como recurso.
- Añade normalización defensiva de recursos para evitar listas como claves de diccionario.
- Mantiene tiempos pasivos reales y checklist final al cierre.
