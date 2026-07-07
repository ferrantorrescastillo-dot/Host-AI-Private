# Sprint 6.0 - Producción desde fichas técnicas

## Objetivo

Conectar el módulo de fichas técnicas con producción inteligente.

Hasta ahora producción trabajaba con demos o tareas internas.
Desde este sprint Host AI ya puede leer una ficha técnica guardada y convertir sus fases en producción.

## Archivos nuevos

- SERVICIOS/produccion_desde_fichas.py

## Archivos modificados

- MODULOS/produccion_inteligente.py

## Nueva opción

16. Producción Inteligente

9. Generar producción desde ficha técnica

## Cómo probar

Primero asegúrate de tener una ficha:

17
1

Luego:

16
9
carrillera

## Qué hace

- Busca ficha por nombre o código.
- Lee fases de la ficha.
- Convierte fases en tareas de producción.
- Separa tiempo activo y pasivo.
- Muestra maquinaria.
- Muestra dependencias.
- Muestra puntos críticos.
- Muestra controles de calidad.
- Genera un horario simple desde la ficha.

## Importante

Este sprint todavía no conecta la ficha con el planificador completo por trabajadores.
Eso será Sprint 6.1.

Sprint 6.0 deja preparada la conversión:

Ficha técnica
→ fases
→ tareas de producción
→ planificación
