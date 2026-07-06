# CHANGELOG - Sprint 5.3

**Fecha:** 07/07/2026

## Objetivo

Añadir la primera versión del planificador horario de producción inteligente.

---

## Archivos nuevos

- `SERVICIOS/planificador_produccion.py`
- `Docs/CHANGELOG_SPRINT_5_3.md`

---

## Archivos modificados completos

- `Main.py`
- `MODULOS/produccion_inteligente.py`

---

## Novedades

### Producción Inteligente

Se añade una nueva opción dentro de `16. Producción Inteligente`:

5. Generar horario de producción inteligente.

El horario estima:

- Hora de inicio y fin.
- Tiempo activo.
- Tiempo pasivo.
- Responsable sugerido.
- Maquinaria probable.
- Motivos de prioridad.
- Avisos de carga de trabajo.

---

## Importante

Este sprint todavía trabaja con reglas culinarias aproximadas basadas en el nombre de la tarea.

En próximos sprints se conectará con fichas técnicas reales para usar:

- Fases de elaboración.
- Tiempos reales.
- Maquinaria real.
- Personal disponible.
- Producción disponible.

---

## Próximo Sprint

### Sprint 5.4

Motor de producción disponible + planificación.

Objetivo:

- Antes de producir, revisar si ya hay producción disponible.
- Recomendar producir solo lo que falta.
- Avisar de caducidades.
- Integrar el stock de elaboraciones en el plan.

Autor: Host AI Development  
Versión: 2.1 DEV
