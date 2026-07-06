# CHANGELOG v0.8 - Planificación / Personal

## Objetivo

Empezar a repartir la producción como lo haría un jefe de cocina: por roles, responsabilidades y personal disponible.

---

## Añadido

- Nuevo módulo `MODULOS/planificacion.py`.
- Nueva opción principal: `10. Planificación / Personal`.
- Roles base de cocina:
  - Ayudante
  - Cocinero
  - Jefe de partida
  - Jefe de cocina
- Registro de personal de cocina.
- Asignación automática de tareas pendientes por rol.
- Asignación automática de persona recomendada.
- Estimación básica de tiempo por tarea.
- Prioridad básica por tarea.
- Planning de producción agrupado por persona.

---

## Base de datos

Nuevas tablas:

- `roles_cocina`
- `personal_cocina`
- `planificaciones_dia`

Nuevos campos en `tareas_produccion`:

- `rol_recomendado`
- `persona_asignada`
- `tiempo_estimado_min`
- `prioridad`

---

## Dashboard

El Dashboard Cocina ahora muestra si las tareas ya tienen asignación de persona/rol.

---

## Filosofía

Host AI no reparte tareas directamente a personas sin criterio.

Primero piensa en roles:

- Ayudante: tareas básicas, cortes, limpieza, apoyo.
- Cocinero: producción, fuegos, elaboraciones.
- Jefe de partida: tareas finales y supervisión.
- Jefe de cocina: organización, control y decisiones.

Después asigna a las personas disponibles.
