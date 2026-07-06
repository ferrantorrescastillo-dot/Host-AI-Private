# Host AI 2.1 Sprint 4.3

## Objetivo

Añadir entrada de mercancía y stock de artículos a partir de documentos importados.

## Cambios principales

- Nueva opción `13. Stock / Mercancía`.
- Nueva opción dentro de importadores: registrar entrada de mercancía desde documento.
- Nuevas tablas:
  - `entradas_mercancia`
  - `lineas_entrada_mercancia`
  - `movimientos_stock`
  - `incidencias_recepcion`
- Nuevas columnas en `articulos`:
  - `stock_actual`
  - `unidad_stock`
- Nuevo servicio `stock_servicio.py`.
- Nuevo servicio `entradas_mercancia.py`.
- Nuevo módulo `stock.py`.

## Flujo recomendado de prueba

1. Importar documento.
2. Vista previa / comparar con artículos.
3. Aplicar cambios del documento.
4. Registrar entrada de mercancía desde documento.
5. Entrar en `13. Stock / Mercancía`.
6. Ver stock y movimientos.

## Nota

Este sprint suma stock automáticamente usando las cantidades detectadas en el documento.
La revisión fina de faltantes, productos dañados o cantidades distintas se hará en el siguiente sprint.
