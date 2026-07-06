# ROADMAP HOST AI 2.1

## Objetivo
Reconstruir el núcleo de Host AI para que deje de trabajar por platos y empiece a trabajar por elaboraciones, dependencias, fases, producción disponible, ADN de cocina y planificación inteligente.

---

## Principio de trabajo
No se añaden más pantallas sueltas.
Cada sprint debe mejorar el núcleo real del producto.

Regla:

```text
Plato → Elaboraciones → Subelaboraciones → Fases → Producción → Planning
```

---

# FASE 1 — Núcleo gastronómico

## Sprint 1 — Base de datos 2.1

Crear o adaptar tablas para:

- elaboraciones
- elaboracion_versiones
- fases_elaboracion
- dependencias_elaboracion
- platos
- componentes_plato
- ordenes_produccion
- lineas_orden_produccion
- produccion_disponible
- maquinaria
- personal
- roles
- adn_cocina
- reglas_adn
- checklists
- rendimientos
- auditoria

### Resultado esperado
Host AI puede guardar fichas técnicas completas, fases, versiones y dependencias.

---

## Sprint 2 — Ficha Técnica Inteligente

Crear módulo para gestionar elaboraciones con:

- nombre
- versión
- rendimiento base
- unidad
- ingredientes
- fases
- tiempos activos y pasivos
- maquinaria
- conservación
- congelación
- calidad
- coste
- observaciones

### Resultado esperado
Host AI deja de guardar recetas como texto plano y empieza a guardar conocimiento gastronómico estructurado.

---

## Sprint 3 — Motor de Dependencias

Crear relaciones como:

```text
Taco de carrillera
↓
Carrillera prensada
↓
Fondo oscuro
↓
Bresa
```

### Resultado esperado
Host AI detecta elaboraciones compartidas y no duplica producciones.

---

# FASE 2 — Producción inteligente

## Sprint 4 — Órdenes de Producción reales

Una orden de producción ya no genera platos.
Genera elaboraciones agrupadas.

Ejemplo:

```text
MENU BODA 50 pax
↓
Carrillera prensada: 8 kg
Demi-glace: 5 L
Puré patata: 6 kg
Alioli: 2 L
```

### Resultado esperado
Host AI empieza a producir como piensa un jefe de cocina.

---

## Sprint 5 — Producción Disponible 2.0

Controlar stock real de elaboraciones:

- cantidad
- unidad
- lote
- ubicación
- fecha producción
- caducidad
- congelado sí/no
- formato de envasado

### Resultado esperado
Antes de producir, Host AI revisa si ya existe producción disponible.

---

## Sprint 6 — Rendimientos reales

Guardar cada producción real:

- previsto
- producido realmente
- diferencia
- merma
- tiempo real
- observaciones

### Resultado esperado
Host AI aprende que una receta no siempre rinde igual que la teoría.

---

# FASE 3 — Planificación inteligente

## Sprint 7 — Fases de producción

Cada elaboración se divide en fases:

```text
Preparar → Cocinar → Reposar → Abatir → Envasar → Etiquetar → Guardar
```

Cada fase tendrá:

- duración activa
- duración pasiva
- maquinaria
- rol necesario
- prioridad
- dependencia

### Resultado esperado
Host AI puede planificar fases, no solo tareas.

---

## Sprint 8 — Motor de Planificación

Algoritmo de prioridad:

```text
1. Lo que tarda más
2. Lo que necesita reposo
3. Lo que desbloquea otras elaboraciones
4. Lo que ocupa maquinaria crítica
5. Lo perecedero
6. Lo rápido
```

### Resultado esperado
Host AI propone un orden lógico de trabajo.

---

## Sprint 9 — Personal y maquinaria

El planning debe tener en cuenta:

- roles
- habilidades
- disponibilidad
- hornos
- marmitas
- freidoras
- Thermomix
- abatidor
- cámaras

### Resultado esperado
Host AI asigna tareas según roles y recursos disponibles.

---

# FASE 4 — Operación real

## Sprint 10 — Estados de operación

Cada evento/orden tendrá estados:

```text
Planificación
Producción
Mise en place
Servicio
Cierre
Revisado
```

### Resultado esperado
Host AI entiende en qué fase está la cocina.

---

## Sprint 11 — Checklists inteligentes

Crear checklists para:

- producción terminada
- mise en place lista
- servicio preparado
- cierre del evento

### Resultado esperado
No se pasa de fase si faltan puntos críticos.

---

## Sprint 12 — Dashboard Cocina 2.1

Mostrar:

- estado del día
- eventos
- producción pendiente
- producción disponible
- fase actual
- primera tarea recomendada
- alertas
- checklists

### Resultado esperado
Al abrir Host AI, el cocinero sabe qué hacer primero.

---

# FASE 5 — ADN de Cocina

## Sprint 13 — ADN de Cocina

Guardar reglas del restaurante:

- fondos siempre primero
- no cortar aguacate antes de 30 min
- usar producción disponible antes de fabricar
- carrilleras se prensan 24 h
- congelar demi-glace en bolsas de 2 L

### Resultado esperado
Host AI decide respetando la forma de trabajar del restaurante.

---

## Sprint 14 — Auditoría y versiones

Guardar historial de:

- cambios de recetas
- versiones
- costes
- rendimientos
- incidencias
- decisiones importantes

### Resultado esperado
Host AI sabe qué cambió, cuándo y por qué.

---

# FASE 6 — Ingesta inteligente

## Sprint 15 — Importador Word 2.1

Convertir documentos en:

- elaboraciones
- ingredientes
- fases
- rendimientos
- observaciones

### Resultado esperado
Host AI crea fichas técnicas desde recetas reales.

---

## Sprint 16 — Relación ingredientes-artículos

Cuando lea una receta:

```text
500 g cebolla
```

Host AI buscará el artículo cebolla.
Si no existe, preguntará si lo crea.

### Resultado esperado
Las recetas alimentan automáticamente artículos y costes.

---

# FASE 7 — Costes y rentabilidad

## Sprint 17 — Coste de elaboración

Calcular:

- coste materia prima
- coste por lote
- coste por kg/L/ración
- coste por versión

---

## Sprint 18 — Coste de plato

Sumar elaboraciones y artículos directos.

---

## Sprint 19 — Dashboard Rentabilidad 2.1

Mostrar:

- platos más rentables
- platos menos rentables
- productos que han subido
- desviaciones
- recomendaciones

---

# Orden de desarrollo inmediato

El siguiente código que debe construirse es:

```text
Sprint 1: Base de datos 2.1
Sprint 2: Ficha Técnica Inteligente
Sprint 3: Motor de Dependencias
Sprint 4: Orden de Producción real por elaboraciones
```

No se debe seguir ampliando el menú antes de completar estos cuatro sprints.

---

# Criterio de éxito de Host AI 2.1

Host AI 2.1 estará listo cuando pueda hacer esto:

```text
Evento → Menú → Platos → Elaboraciones → Dependencias → Producción agrupada
```

y deje de generar tareas por plato.

Ese será el primer núcleo real del jefe de cocina digital.
