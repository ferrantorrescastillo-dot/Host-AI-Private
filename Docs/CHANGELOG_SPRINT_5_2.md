# CHANGELOG - Sprint 5.2

**Fecha:** 07/07/2026

## Objetivo

Añadir la segunda capa del Motor de Producción Inteligente: dependencias básicas, producciones agrupables y plan de producción razonado.

---

## Archivos nuevos

- `SERVICIOS/dependencias.py`
- `SERVICIOS/motor_produccion.py`

---

## Archivos modificados completos

- `Main.py`
- `MODULOS/produccion_inteligente.py`

---

## Archivos incluidos para asegurar compatibilidad

- `SERVICIOS/prioridades.py`

---

## Novedades

### Producción Inteligente

Nueva opción del menú principal:

- `16. Producción Inteligente`

Dentro incluye:

1. Ver siguiente acción recomendada.
2. Ver prioridades de producción.
3. Ver dependencias / producciones agrupables.
4. Generar plan de producción inteligente.

---

## Motor de Dependencias

Host AI empieza a detectar producciones comunes o agrupables como:

- Demi-glace / salsas madre.
- Fumet / caldo de pescado.
- Fondo oscuro.
- Bechamel.
- Puré / parmentier.
- Alioli.
- Mise en place fría.

Todavía es una detección aproximada basada en nombres, pero prepara el camino para el árbol real de elaboraciones.

---

## Motor de Producción

El nuevo motor combina:

- Prioridad culinaria.
- Fecha del evento.
- Cantidad.
- Tipo de elaboración.
- Posibles dependencias comunes.
- Explicación de motivos.

Devuelve un plan razonado en vez de una simple lista de tareas.

---

## Próximo paso

Sprint 5.3:

- Conectar producción disponible.
- Restar lo que ya está producido antes de recomendar fabricar de nuevo.
- Empezar a preparar la producción por elaboraciones reales, no por platos.

