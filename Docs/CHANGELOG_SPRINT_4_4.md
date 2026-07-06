# CHANGELOG - Host AI 2.1 Sprint 4.4

## Nuevo

- Módulo `MODULOS/costes.py`.
- Servicio `SERVICIOS/costes_servicio.py`.
- Nueva opción de menú: `14. Costes / Rentabilidad`.

## Funciones añadidas

- Ver coste estimado de menús.
- Ver coste estimado de eventos.
- Ver últimos precios importados desde documentos.
- Detectar cambios de precio comparando historial.
- Ver productos más caros detectados en documentos.
- Recalcular `coste_total` y `food_cost` de menús.

## Corrección

- Stock: la consulta vuelve a incluir `unidad` para evitar errores al mostrar stock.

## Nota

Este sprint todavía calcula costes a nivel básico usando datos existentes de menús y documentos. El siguiente paso será bajar el cálculo hasta ingredientes reales y escandallos vivos.
