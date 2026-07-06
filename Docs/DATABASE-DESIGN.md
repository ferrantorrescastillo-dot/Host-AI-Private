# DATABASE DESIGN - HOST AI

# Filosofía

La base de datos no representa tablas.

Representa un restaurante vivo.

Host AI no trabaja sobre Excel.

Host AI trabaja sobre un modelo completo del restaurante.

El Excel únicamente será un sistema de importación y exportación.

---

# Arquitectura

Se utilizarán dos niveles de información.

## Nivel 1

Datos del restaurante.

Información objetiva.

Ejemplos:

- artículos
- proveedores
- compras
- recetas
- stock
- ventas
- eventos

---

## Nivel 2

Conocimiento del restaurante.

Información aprendida.

Ejemplos:

- hábitos
- preferencias
- planificación habitual
- recomendaciones
- patrones
- decisiones anteriores

Este conocimiento será generado por Host AI con el tiempo.

---

# Entidades principales

## Restaurante

Todo pertenece a un restaurante.

Campos principales:

- nombre
- dirección
- configuración
- idioma
- moneda
- impuestos
- horarios

---

## Usuario

Representa cualquier persona que utilice Host AI.

Ejemplos:

- jefe de cocina
- cocinero
- gerente
- administrador

---

## Artículo

Representa cualquier producto utilizado por el restaurante.

Ejemplos:

- tomate
- arroz
- sal
- aceite

Información principal:

- nombre
- familia
- unidad
- ubicación
- stock mínimo
- proveedor principal
- activo

El precio NO pertenece realmente al artículo.

El precio pertenece a la relación artículo-proveedor.

---

## Proveedor

Información comercial.

Puede suministrar múltiples artículos.

---

## Artículo-Proveedor

Tabla intermedia.

Permite:

- varios proveedores
- varios formatos
- varios precios
- histórico de compras

---

## Compra

Representa una factura o pedido recibido.

Incluye:

- proveedor
- fecha
- importe
- líneas

---

## Línea de compra

Cada producto comprado.

Incluye:

- artículo
- cantidad
- precio
- formato

---

## Stock

Host AI NO almacenará únicamente el stock actual.

Guardará movimientos.

Ejemplos:

Entrada.

Salida.

Merma.

Inventario.

Ajuste.

Esto permitirá reconstruir cualquier inventario.

---

## Receta

Representa una elaboración.

Incluye:

- nombre
- categoría
- elaboración
- alérgenos

---

## Ingrediente de receta

Une recetas con artículos.

Permite recalcular automáticamente costes.

---

## Evento

Representa cualquier servicio futuro.

Ejemplos:

- boda
- catering
- comunión
- restaurante

Estados:

Pendiente.

Confirmado.

Planificación.

Producción.

Servicio.

Finalizado.

Revisado.

---

## Producción

Representa elaboraciones programadas.

Ejemplos:

- hacer fumet
- confitar pato
- preparar croquetas

---

## Tareas

Todo trabajo pendiente.

Puede generarse automáticamente.

---

## Alertas

Avisos inteligentes.

Ejemplos:

- falta stock
- producto caro
- proveedor retrasado
- evento próximo

---

# Relaciones

Un restaurante tiene:

muchos usuarios

muchos artículos

muchos proveedores

muchas recetas

muchos eventos

muchas compras

---

Un artículo puede tener:

varios proveedores

varias recetas

muchos movimientos de stock

muchas compras

---

Una receta puede contener:

muchos artículos

---

Un evento genera:

compras

producción

tareas

alertas

---

# Filosofía de crecimiento

La base de datos debe poder funcionar para:

1 restaurante

10 restaurantes

1000 restaurantes

sin cambiar la arquitectura.

---

# Tecnologías

Desarrollo:

SQLite

Producción:

PostgreSQL

---

# Principio fundamental

La base de datos almacena hechos.

Host AI interpreta esos hechos.

Nunca al revés.