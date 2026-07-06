# PROJECT STATE - HOST AI

## Estado actual
Proyecto: Host AI  
Objetivo: asistente tipo segundo de cocina para hostelería.

Host AI no es un ERP.  
Debe pensar, preguntar, anticiparse y ayudar al cocinero.

## Ruta del proyecto
C:\Users\ferra\OneDrive\Documentos\Curso Python

## Arquitectura actual
- main.py oficial en la raíz del proyecto
- CORE/
  - motor.py
  - cerebro.py
  - asistente.py
  - busqueda.py
  - acciones.py
  - orquestador.py
  - configuracion.py
- MODULOS/
- EXCEL/
- Docs/
- Legacy/ como copia antigua, no tocar

## Excel actual
EXCEL/Escandallos Boronat_ACTUALIZADO.xlsx

## Hojas configuradas
- Listado de Artículos
- Historial de Compras

## Funciones que ya funcionan
- Menú principal.
- Carga del Excel desde ruta centralizada.
- Motor de Cocina básico en solo lectura.
- Motor de Búsqueda básico.
- Orquestador básico.
- Asistente IA conectado al Orquestador.
- Buscar artículos por lenguaje natural:
  - buscame tomate
  - buscame tomate cherry
- Consultar precio:
  - precio cherry
  - cuanto cuesta tomate cherry
- Consultar proveedor:
  - quien vende tomate cherry
- Resolver varios resultados preguntando al usuario.
- Contexto temporal de conversación:
  - recuerda el último artículo consultado
  - responde preguntas cortas como “medidas?” o “quién lo vende?”

## Reglas de trabajo
- No escribir sobre el Excel principal sin copia.
- Pasar archivos completos para copiar y pegar.
- Si no se sabe cómo está un archivo, pedirlo antes.
- Cambios pequeños y probar después.
- No tocar Legacy salvo revisión explícita.
- Cada sesión debe tener un objetivo único.
- La IA no contiene lógica de negocio; la lógica vive en los motores.

## Siguiente paso
Sesión 14: mejorar datos de artículos.

Objetivo:
Cargar más información real desde el Excel para que Host AI pueda responder mejor sobre:
- unidad de medida
- formato
- precio por kg/unidad
- proveedor
- datos del artículo

## Frase para continuar en un chat nuevo
Seguimos con Host AI. Lee PROJECT_STATE.md y continúa con la Sesión 14: mejorar datos de artículos.