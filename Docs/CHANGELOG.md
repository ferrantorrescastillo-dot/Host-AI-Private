# CHANGELOG

---

# v0.1.0

## Arquitectura

- Se crea un único punto de entrada (`main.py`).
- Se reorganiza la estructura del proyecto.
- Se centralizan las rutas en `configuracion.py`.

---

## Motor de Cocina

- Carga de artículos.
- Carga de proveedores.
- Carga de hojas de escandallos.
- Funcionamiento en solo lectura.

---

## Motor de Búsqueda

Se crea el primer Motor de Búsqueda oficial.

Características:

- búsqueda por coincidencia exacta
- búsqueda parcial
- búsqueda aproximada
- resultados ordenados por relevancia

Estados soportados:

- UNICO
- MULTIPLE
- APROXIMADO
- NINGUNO

---

## Motor de Conversación

Se mejora la detección de preguntas.

Host AI entiende:

- buscame...
- cuanto cuesta...
- precio...
- quien vende...

---

## Orquestador

Se crea el primer Orquestador del sistema.

Responsabilidad:

- recibir la acción detectada
- decidir qué motor ejecutar
- devolver una respuesta estructurada

El Orquestador no conversa con el usuario.

---

## Contexto Conversacional

Se implementa la primera memoria temporal.

Host AI recuerda:

- último artículo consultado
- última acción realizada

Esto permite responder preguntas como:

- ¿y el proveedor?
- ¿el kg?
- ¿medidas?
- ¿cuánto costaba?

sin repetir el nombre del artículo.

---

## Filosofía consolidada

Host AI deja de crecer mediante funciones aisladas y pasa a construirse mediante motores independientes coordinados por un Orquestador.

La IA interpreta.

Los motores ejecutan.

El asistente conversa.

Cada componente tiene una única responsabilidad.

---

## Próxima versión

Sesión 14

Mejorar la carga de información de los artículos para responder con datos reales sobre:

- unidades
- formatos
- referencias
- precios por unidad
- información técnica del artículo

---

# v0.5.1

- Dashboard Cocina corregido con pausa de lectura.
- Dashboard Rentabilidad corregido con pausa de lectura.
- Añadido módulo de Recetas / Elaboraciones.
- Añadido importador básico de recetas desde Word (.docx).
- Añadida opción 8 en Main.py.

## Sprint 4.5 - Compras / Pedidos

- Añadido módulo `Compras / Pedidos`.
- Detecta productos por debajo del stock mínimo.
- Genera pedidos sugeridos agrupando por proveedor.
- Guarda pedidos y líneas de pedido en SQLite.
- Permite exportar el último pedido a TXT.
- Permite marcar un pedido como enviado.
- Corregida lectura defensiva de unidad en `MODULOS/stock.py`.
