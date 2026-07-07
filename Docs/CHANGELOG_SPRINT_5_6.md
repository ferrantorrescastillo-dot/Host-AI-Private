# Sprint 5.6 - Agenda diaria y reparto por trabajadores

## Objetivo

Mejorar Producción Inteligente para que Host AI empiece a repartir el trabajo por personal disponible.

Hasta Sprint 5.4/5.5 el sistema ya podía ordenar tareas y mostrar horario por restricciones.
En este sprint añadimos una primera capa de jefe de cocina real:

- quién hace cada tarea
- cómo repartir 3 trabajadores
- cómo aprovechar tiempos pasivos
- qué revisar al llegar
- qué riesgos tiene el día
- qué significa producción terminada

## Archivos modificados

- Main.py
- MODULOS/produccion_inteligente.py

## Archivos nuevos

- SERVICIOS/planificador_personal.py
- SERVICIOS/agenda_jefe_cocina.py
- Docs/CHANGELOG_SPRINT_5_6.md

## Opciones nuevas

Dentro de:

16. Producción Inteligente

Aparecen:

7. Planificar teniendo en cuenta 3 trabajadores
8. Agenda diaria del jefe de cocina (Sprint 5.6)

## Cómo probar

1. Ejecutar:

python Main.py

2. Entrar en:

16

3. Probar:

7

4. Después probar:

8

## Commit recomendado

git add .
git commit -m "Sprint 5.6 - Agenda diaria y reparto por trabajadores"
git push
