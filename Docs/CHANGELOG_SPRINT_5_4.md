# Sprint 5.4 - Planificación por restricciones reales

## Objetivo

Mejorar el horario de producción inteligente para que Host AI empiece a planificar como un jefe de cocina, no solo como una lista de tareas.

## Archivos modificados

- `Main.py`
- `MODULOS/produccion_inteligente.py`
- `SERVICIOS/planificador_produccion.py`

## Archivos nuevos

- `SERVICIOS/planificador_restricciones.py`
- `Docs/CHANGELOG_SPRINT_5_4.md`

## Qué añade

- Distingue tiempo activo y tiempo pasivo.
- Detecta tareas largas.
- Detecta tareas con reposo.
- Da más prioridad a tareas que desbloquean otras.
- Encaja tareas rápidas dentro de tiempos muertos.
- Explica el motivo del orden.
- Muestra riesgos de producción.
- Prepara el camino para Sprint 5.5: personal, maquinaria y cuellos de botella.

## Nueva prueba

En Host AI:

```text
16. Producción Inteligente
6. Generar horario por restricciones reales (Sprint 5.4)
```

## Prueba anterior que debe seguir funcionando

```text
16. Producción Inteligente
5. Generar horario de producción inteligente
```

## Commit recomendado

```powershell
cd "C:\Proyectos\Host-AI"
git status
git add .
git commit -m "Sprint 5.4 - Planificación por restricciones"
git push
```
