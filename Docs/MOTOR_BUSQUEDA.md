# MOTOR DE BÚSQUEDA

## Objetivo

El Motor de Búsqueda permite encontrar información dentro de Host AI de forma inteligente.

Debe servir para cualquier restaurante, no solo para el Excel actual.

---

## Responsabilidad

Buscar información dentro de la memoria interna del restaurante.

Puede buscar:

* artículos
* proveedores
* recetas
* compras
* stock
* eventos

---

## Lo que NO hace

El Motor de Búsqueda nunca:

* modifica información
* habla con el usuario
* pregunta confirmaciones
* decide acciones
* escribe en Excel
* interpreta conversaciones completas

Solo busca y devuelve resultados estructurados.

---

## Comportamiento esperado

### Caso 1: búsqueda general

Usuario:

"búscame tomate"

Resultado esperado:

El sistema encuentra varios artículos relacionados:

* tomate pera
* tomate cherry
* tomate rama
* tomate triturado

El Motor de Búsqueda devuelve estado MULTIPLE.

El Motor de Conversación preguntará cuál quiere el usuario.

---

### Caso 2: búsqueda clara

Usuario:

"búscame tomate cherry"

Resultado esperado:

El sistema encuentra una coincidencia clara.

El Motor de Búsqueda devuelve estado UNICO.

El sistema puede continuar sin preguntar.

---

### Caso 3: búsqueda aproximada

Usuario:

"búscame tomate pera extra"

Si no existe exactamente "tomate pera extra", pero sí existe "tomate pera", el motor devuelve una coincidencia probable.

Estado: APROXIMADO.

El Motor de Conversación decidirá si confirma con el usuario.

---

### Caso 4: sin resultados

Usuario:

"búscame tomate azul"

Si no existe nada parecido, el motor devuelve estado NINGUNO.

---

## Estados posibles

El Motor de Búsqueda siempre devolverá uno de estos estados:

* UNICO
* MULTIPLE
* APROXIMADO
* NINGUNO

---

## Formato conceptual de respuesta

Una búsqueda no devuelve texto para enseñar al usuario.

Devuelve datos.

Ejemplo:

estado: MULTIPLE
tipo: ARTICULO
consulta: tomate
resultados:

* tomate pera
* tomate cherry
* tomate rama

---

## Regla principal

El Motor de Búsqueda no decide qué hacer.

Solo responde:

"He encontrado esto."

Después, otros motores deciden:

* si preguntar al usuario
* si mostrar una ficha
* si actualizar stock
* si preparar una compra
* si consultar recetas
* si lanzar otra acción

---

## Relación con otros motores

El Motor de Búsqueda será utilizado por:

* Motor de Conversación
* Motor de Acciones
* Motor de Compras
* Motor de Stock
* Motor de Recetas
* Motor de Eventos
* Motor de Automatizaciones

---

## Decisión arquitectónica

Toda búsqueda oficial de Host AI deberá pasar por este motor.

No debe haber búsquedas sueltas dentro de otros módulos.

Esto evita duplicar lógica y permite mejorar la búsqueda una sola vez para todo el sistema.

---

## Estado

Diseño funcional definido.

Siguiente paso:

Crear `CORE/busqueda.py` con la primera versión del motor en solo lectura.
