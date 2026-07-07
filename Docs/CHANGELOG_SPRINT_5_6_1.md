# Sprint 5.6.1 - Hotfix planificación completa por trabajadores

## Objetivo
Corregir el Sprint 5.6 para que la planificación no sea una demo corta de 2 elaboraciones, sino una producción completa repartida entre 3 cocineros durante jornadas de 8 horas.

## Cambios
- Se añade planificación completa por trabajadores.
- Se reparten tareas entre 3 cocineros.
- Se respeta jornada máxima de 8 h por día.
- Si no cabe todo, se continúa automáticamente al día siguiente.
- Se corrige el fallo lógico de tiempos: no se puede abatir un fondo antes de terminar sus 3 horas de cocción.
- Se añaden dependencias explícitas entre fases.
- Se mantiene la agenda diaria del jefe de cocina.

## Archivos modificados
- Main.py
- MODULOS/produccion_inteligente.py
- SERVICIOS/planificador_personal.py
- SERVICIOS/agenda_jefe_cocina.py
- Docs/CHANGELOG_SPRINT_5_6_1.md

## Prueba
Desde Host AI:

16. Producción Inteligente
7. Repartir producción completa entre trabajadores (8 h / día)

Y también:

16. Producción Inteligente
8. Agenda diaria del jefe de cocina
