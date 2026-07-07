# Sprint 5.7 - Fichas Técnicas Host AI v1.0

## Objetivo

Crear el primer núcleo de fichas técnicas para Host AI.

La ficha técnica deja de ser una receta bonita y pasa a ser la base de conocimiento para:

- producción
- planificación
- compras
- stock
- costes
- calidad
- formación
- IA futura

## Archivos nuevos

- MODELOS/ficha_tecnica.py
- SERVICIOS/fichas_tecnicas.py
- MODULOS/fichas.py
- DATOS/fichas_tecnicas/
- Docs/CHANGELOG_SPRINT_5_7.md

## Archivos modificados

- Main.py

## Menú nuevo

17. Fichas Técnicas Host AI

Opciones:

1. Crear ficha demo completa: Carrillera melosa
2. Listar fichas guardadas
3. Ver ficha como cocinero
4. Crear borrador desde receta pegada
5. Explicar estructura Ficha Técnica Host AI v1.0

## Qué se puede probar

Primero:

17
1

Esto crea la ficha completa de carrillera.

Después:

17
2

Lista fichas.

Después:

17
3

Código:

ELAB-CAR-001

Después:

17
4

Pegar una receta incompleta y comprobar que Host AI detecta campos faltantes y pregunta qué falta.

## Próximo paso recomendado

Sprint 5.8:

- Guardar respuestas del usuario para completar una ficha.
- Editar campos concretos.
- Convertir ficha técnica en fases de producción reales.
- Conectar fichas técnicas con planificación.
