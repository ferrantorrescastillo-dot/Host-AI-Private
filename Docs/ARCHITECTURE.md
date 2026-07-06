# HOST AI - ARQUITECTURA OFICIAL

Versión: 1.0

Este documento define la arquitectura oficial de Host AI.

Cualquier nueva funcionalidad deberá respetar estas reglas.

---

# FILOSOFÍA

Host AI NO es un programa.

Host AI es una plataforma formada por motores independientes.

Cada motor tiene una única responsabilidad.

La IA nunca contendrá la lógica del negocio.

La IA únicamente comprenderá al usuario y decidirá qué motor utilizar.

---

# ARQUITECTURA GENERAL

                 Usuario
                     │
                     ▼
              Motor Conversación
                     │
                     ▼
               Motor Acciones
                     │
                     ▼
               Motor Cocina
                     │
      ┌──────────────┼──────────────┐
      │              │              │
      ▼              ▼              ▼
 Motor Búsqueda  Motor Compras  Motor Stock
      │              │              │
      └──────────────┼──────────────┘
                     ▼
               Motor Recetas
                     │
                     ▼
            Motor Automatizaciones
                     │
                     ▼
               Motor Eventos

Todos los motores podrán consultar el Motor de Cocina.

Ningún motor accederá directamente al Excel.

---

# MOTOR DE COCINA

Responsabilidad

Ser la memoria del restaurante.

Conocer:

- artículos
- proveedores
- recetas
- compras
- stock
- eventos
- clientes (futuro)

No habla.

No pregunta.

No interpreta.

Solo conoce información.

---

# MOTOR DE BÚSQUEDA

Responsabilidad

Buscar información.

Debe poder buscar:

- artículos
- proveedores
- recetas
- compras
- stock
- eventos

Nunca modificará información.

---

# MOTOR DE CONVERSACIÓN

Responsabilidad

Interpretar el lenguaje natural.

Convertir frases del usuario en intenciones.

Ejemplo

"¿Quién vende tomate?"

↓

BUSCAR_PROVEEDOR

Nunca realizará búsquedas.

Nunca modificará información.

---

# MOTOR DE ACCIONES

Responsabilidad

Ejecutar acciones.

Ejemplos

Actualizar precio.

Crear pedido.

Modificar proveedor.

Actualizar stock.

No interpreta preguntas.

---

# MOTOR DE AUTOMATIZACIONES

Responsabilidad

Detectar situaciones automáticamente.

Ejemplos

Cambios en Excel.

Subidas de precio.

Productos sin comprar.

Stock bajo.

Recetas afectadas.

---

# MOTOR DE RECETAS

Responsabilidad

Gestionar recetas.

Ingredientes.

Costes.

Versiones.

Escandallos.

---

# MOTOR DE COMPRAS

Responsabilidad

Compras.

Pedidos.

Facturas.

Historial.

---

# MOTOR DE STOCK

Responsabilidad

Existencias.

Entradas.

Salidas.

Inventarios.

---

# MOTOR DE EVENTOS

Responsabilidad

Bodas.

Caterings.

Producción.

Personal.

Calendario.

---

# IA

La IA nunca contendrá reglas del negocio.

Solo hará tres cosas:

1. Comprender al usuario.

2. Elegir qué motor utilizar.

3. Responder utilizando la información recibida.

Toda la inteligencia del restaurante estará en los motores.

No en la IA.

---

# FUENTES DE DATOS

Host AI deberá aceptar datos desde:

- Excel
- Bases de datos externas
- APIs
- CSV
- Facturas
- Albaranes
- Entrada manual

Todas las fuentes terminarán en el Motor de Cocina.

---

# PRINCIPIOS DE DESARROLLO

Cada motor debe poder utilizarse desde cualquier parte del sistema.

Cada motor debe tener una única responsabilidad.

Ningún motor debe duplicar lógica de otro.

La documentación se actualizará antes de modificar la arquitectura.

Toda funcionalidad nueva deberá indicar a qué motor pertenece.

---

# OBJETIVO FINAL

Construir una plataforma preparada para gestionar cualquier restaurante o catering, independientemente de su tamaño o de la herramienta que utilice actualmente.