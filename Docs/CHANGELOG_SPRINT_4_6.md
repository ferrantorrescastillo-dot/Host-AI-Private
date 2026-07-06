# CHANGELOG - Sprint 4.6

**Fecha:** 07/07/2026

## Objetivo

Implementar la primera versión del sistema de compras inteligentes basado en stock mínimo y stock óptimo.

---

## Novedades

### Compras

- Añadida configuración de stock mínimo por artículo.
- Añadida configuración de stock óptimo.
- Posibilidad de generar pedidos según necesidades de stock.
- Nuevo listado de artículos sin stock mínimo configurado.
- Pedido manual de prueba para validar el funcionamiento.

---

### Servicios

Actualizado:

- SERVICIOS/compras_servicio.py

Mejoras:

- Cálculo de cantidades a comprar.
- Preparación para futuras recomendaciones automáticas de compra.

---

### Módulos

Actualizado:

- MODULOS/compras.py

Se añaden nuevos menús para:

- Configurar stock mínimo.
- Configurar stock óptimo.
- Visualizar artículos pendientes de configurar.
- Generar pedidos inteligentes.

---

## Arquitectura

Host AI continúa evolucionando hacia una arquitectura modular.

Estado actual:

- ✔ Importación de documentos
- ✔ Comparación de artículos
- ✔ Historial de precios
- ✔ Stock
- ✔ Costes
- ✔ Compras

Siguiente objetivo:

**Motor de Producción Inteligente**

---

## Próximo Sprint

### Sprint 5.0

Primer desarrollo del Motor de Producción Inteligente.

Objetivos:

- Analizar eventos.
- Analizar producción disponible.
- Detectar dependencias entre elaboraciones.
- Priorizar automáticamente la producción.
- Generar planificación diaria como un jefe de cocina.

---

Autor: Host AI Development
Versión: 2.1 DEV