# Sprint 5.8 - Asistente para completar fichas técnicas

## Objetivo

Mejorar el Sprint 5.7.

Antes Host AI detectaba campos faltantes, pero solo los mostraba.
Ahora Host AI pregunta uno por uno, guarda las respuestas y actualiza la ficha.

## Archivos modificados

- SERVICIOS/fichas_tecnicas.py
- MODULOS/fichas.py

## Cambios principales

### Opción 17 → 4

Crear borrador desde receta pegada y completar preguntas.

Flujo:

1. Pegas una receta.
2. Host AI detecta nombre, ingredientes y pasos.
3. Detecta campos faltantes.
4. Te pregunta si quieres responder ahora.
5. Pregunta uno por uno:
   - raciones
   - peso ración
   - conservación
   - vida útil
   - regeneración
   - alérgenos
   - HACCP
   - controles de calidad
   - maquinaria
6. Guarda la ficha con las respuestas.

### Nueva opción 17 → 6

Completar ficha existente.

Sirve para abrir un borrador ya guardado y seguir rellenándolo.

## Prueba

Entrar en:

17
4

Pegar una receta.

Después probar:

17
2

Y luego:

17
3

con el código generado.
