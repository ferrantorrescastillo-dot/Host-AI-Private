# DECISIONES

## 05/07/2026

### Excel

DECISIÓN

Excel seguirá siendo la herramienta de edición principal.

MOTIVO

Los cocineros ya trabajan con Excel.

No queremos obligarlos a cambiar.

Host AI leerá automáticamente los cambios.

---

### Arquitectura

DECISIÓN

Host AI trabajará sobre una memoria interna.

No leerá continuamente el Excel.

MOTIVO

Mayor velocidad.

Permite IA.

Permite automatizaciones.

Permite conectar otros sistemas además de Excel.

---

### Filosofía

Host AI no será un ERP.

Debe comportarse como un segundo de cocina.

Debe preguntar.

Debe observar.

Debe avisar.

Debe ayudar.

No limitarse a ejecutar órdenes.

---

### Desarrollo

Siempre entregar archivos completos.

Nunca fragmentos.

Probar después de cada cambio.

No modificar código sin conocer el estado actual del archivo.
---

## 05/07/2026

### Arquitectura de entrada de datos

DECISIÓN

Host AI no dependerá de una única fuente de datos.

Todo restaurante podrá utilizar Host AI independientemente de cómo gestione actualmente su información.

Host AI deberá soportar tres escenarios:

### Escenario 1

El restaurante trabaja con Excel.

Host AI leerá y sincronizará automáticamente los cambios del Excel.

No será necesario cambiar la forma de trabajar del cliente.

---

### Escenario 2

El restaurante ya utiliza otro software o una base de datos.

Host AI deberá poder importar o conectarse a esos datos.

Una vez importados, trabajará exactamente igual que con Excel.

---

### Escenario 3

El restaurante no tiene ningún sistema organizado.

Host AI permitirá crear toda la estructura desde cero:

- artículos
- proveedores
- recetas
- compras
- stock
- eventos

Esta función se desarrollará en una fase posterior.

---

### Regla principal

Independientemente del origen de los datos, toda la información terminará siempre en el Motor de Cocina de Host AI.

El Motor de Cocina será la única fuente de información utilizada por la IA.

La IA nunca dependerá directamente de un Excel, una API o una base de datos externa.

---

### Motivo

Esto permite que Host AI sea compatible con cualquier restaurante o catering.

Solo cambia la forma de importar los datos.

El funcionamiento interno del programa será siempre el mismo.

Esto hace que el proyecto sea escalable, mantenible y preparado para crecer durante muchos años.
---

## 05/07/2026

# Arquitectura del proyecto

DECISIÓN

Host AI se desarrollará por motores independientes.

No se desarrollará por pantallas ni por menús.

Arquitectura prevista:

- Motor de Cocina
- Motor de Búsqueda
- Motor de Conversación
- Motor de Acciones
- Motor de Automatizaciones
- Motor de Compras
- Motor de Stock
- Motor de Recetas
- Motor de Eventos
- Motor de Proveedores

La IA utilizará todos estos motores.

Nunca contendrá la lógica del negocio.

---

# Principio de responsabilidad única

Cada motor tendrá una única responsabilidad.

Ejemplo:

Motor de Búsqueda

Responsabilidad:
Buscar información.

No modificará datos.

No hablará con el usuario.

No tomará decisiones.

---

Motor de Cocina

Responsabilidad:

Conocer todo el restaurante.

Será la memoria interna de Host AI.

Nunca hablará con el usuario.

Nunca interpretará preguntas.

---

# Desarrollo

Antes de programar un motor se escribirá primero su especificación técnica.

Después se programará.

Después se probará.

Después se documentará.

Solo entonces se integrará con el resto del sistema.

---

# Objetivo

Construir una arquitectura preparada para miles de restaurantes sin necesidad de rehacer el proyecto.