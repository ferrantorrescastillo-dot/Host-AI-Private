# HOST AI MASTER ARCHITECTURE v1.0

## 1. Visión

Host AI no es un ERP, ni un recetario, ni un chatbot conectado a Excel.

Host AI es un sistema operativo inteligente para cocinas profesionales.

Su objetivo es que un jefe de cocina pueda convertir el conocimiento real de su restaurante en un sistema vivo que planifica, calcula, pregunta, recomienda, aprende y ayuda a ejecutar el día a día.

La IA no contiene la lógica del negocio. La IA conversa, interpreta y propone. La lógica vive en motores independientes.

---

## 2. Principio central

Host AI debe pensar como un jefe de cocina.

Eso significa que no empieza por compras ni por tablas. Empieza por objetivos reales:

- Tengo una boda.
- Tengo un servicio.
- Tengo una producción pendiente.
- Tengo una elaboración que caduca.
- Tengo que ahorrar coste.
- Tengo que organizar el día.

A partir de ese objetivo, Host AI debe desplegar automáticamente el árbol gastronómico:

```text
Objetivo
↓
Evento / Servicio
↓
Menú
↓
Platos
↓
Elaboraciones
↓
Subelaboraciones
↓
Ingredientes
↓
Stock
↓
Compras
↓
Producción
↓
Planning
↓
Servicio
↓
Cierre
```

---

## 3. Arquitectura general

Host AI se divide en capas.

```text
INTERFAZ
- Dashboard Cocina
- Dashboard Rentabilidad
- Eventos
- Producción
- Compras
- IA conversacional

ORQUESTADOR
- Recibe intención del usuario
- Decide qué motores activar
- Coordina acciones
- Pide confirmación cuando hace falta

MOTORES
- Motor Gastronómico
- Motor Dependencias
- Motor Producción
- Motor Planificación
- Motor Producción Disponible
- Motor Costes
- Motor Compras
- Motor Stock
- Motor Aprendizaje
- Motor Ingesta
- Motor ADN Cocina
- Motor Servicio

DATOS
- Base de datos relacional
- Documentos importados
- Historial
- Auditoría
```

Regla: las pantallas nunca contienen lógica importante. Solo muestran información y llaman al Core.

---

## 4. Entidades principales

### 4.1 Restaurante

Representa una empresa o unidad operativa.

Campos principales:

- id
- nombre
- dirección
- teléfono
- email
- moneda
- idioma
- configuración fiscal
- horarios
- estado

Todo pertenece a un restaurante.

---

### 4.2 Artículo

Materia prima o producto comprado.

Ejemplos:

- Tomate cherry
- Harina
- Nata
- Huesos
- Cebolla

Campos:

- id
- restaurante_id
- nombre
- nombre_normalizado
- familia
- subfamilia
- unidad_base
- alérgenos
- ubicación
- stock_minimo
- stock_actual calculado por movimientos
- activo

El precio no pertenece directamente al artículo. El precio pertenece a la relación artículo-proveedor y al historial de compras.

---

### 4.3 Proveedor

Empresa que suministra productos.

Campos:

- id
- restaurante_id
- nombre
- teléfono
- email
- persona_contacto
- días_reparto
- pedido_mínimo
- observaciones
- activo

---

### 4.4 Artículo-Proveedor

Relación entre artículos y proveedores.

Permite varios proveedores para el mismo artículo.

Campos:

- articulo_id
- proveedor_id
- precio_actual
- unidad_precio
- formato_compra
- código_proveedor
- es_principal
- fecha_ultimo_precio

---

## 5. Ficha Técnica Inteligente

La ficha técnica es una de las piezas centrales del sistema.

No sirve solo para cocinar. Sirve para que cualquier cocinero consiga el mismo resultado, aunque nunca haya hecho esa elaboración.

### 5.1 Identificación

- nombre
- código interno
- familia
- tipo: salsa, fondo, guarnición, base, postre, frío, caliente...
- responsable
- versión
- estado: borrador, validada, en producción, retirada
- fecha creación
- fecha revisión

### 5.2 Objetivo final

Define qué resultado buscamos.

Ejemplo:

> Demi-glace brillante, color oscuro, textura napante y sabor intenso.

Campos:

- descripción del resultado
- sabor ideal
- textura ideal
- color ideal
- uso principal
- estándar visual

### 5.3 Rendimiento

Todas las elaboraciones tienen rendimiento fijo para estandarizar.

Campos:

- cantidad_base
- unidad_base
- raciones_equivalentes
- lote_mínimo
- lote_máximo
- múltiplo_recomendado
- merma_teórica
- rendimiento_real_medio

Ejemplo:

```text
Fumet
Receta base: 20 L
Evento necesita: 60 L
Multiplicador: x3
```

### 5.4 Ingredientes

Cada ingrediente debe enlazar con artículos reales si existen.

Campos:

- artículo_id
- nombre detectado
- cantidad
- unidad
- merma
- coste unitario
- coste total
- proveedor habitual
- ingrediente crítico sí/no

Si Host AI no encuentra el artículo, pregunta:

> No encuentro “parmesano 36 meses”. ¿Quieres enlazarlo con Parmigiano Reggiano o crear artículo nuevo?

### 5.5 Dependencias

Una elaboración puede depender de otra.

Ejemplo:

```text
Demi-glace
↓
Fondo oscuro
↓
Bresa
```

Campos:

- elaboración_origen
- elaboración_dependencia
- cantidad necesaria
- unidad
- obligatoria sí/no

### 5.6 Fases de producción

La receta se divide en fases.

Fases posibles:

- planificación
- descongelado
- preparación
- pesado
- mise en place
- preelaboración
- marcado
- cocción
- reducción
- triturado
- colado
- rectificación
- enfriado
- abatido
- reposo
- prensado
- moldeado
- porcionado
- envasado
- etiquetado
- almacenamiento
- registro

Cada fase tiene:

- nombre
- descripción
- tiempo_activo
- tiempo_pasivo
- maquinaria
- utensilios
- personal recomendado
- temperatura
- punto crítico
- resultado esperado
- fase bloqueante sí/no

Ejemplo:

```text
Carrillera prensada
1. Marcar
2. Estofar
3. Desmigar
4. Prensar 24 h
5. Porcionar
6. Reducir salsa
7. Envasar
8. Etiquetar
9. Guardar
```

### 5.7 Maquinaria

Campos:

- maquinaria imprescindible
- maquinaria opcional
- capacidad necesaria
- cuello de botella sí/no

Ejemplo:

```text
Imprescindible: marmita
Opcional: Thermomix
```

### 5.8 Conservación

Campos:

- conservación en frío
- congelable sí/no
- vida útil en frío
- vida útil congelado
- formato de envasado
- ubicación recomendada
- regeneración

Regla: no se considera terminada una elaboración si no está etiquetada, registrada y almacenada.

### 5.9 Calidad

Controles antes de aceptar la elaboración:

- peso final
- volumen final
- textura
- sabor
- olor
- color
- temperatura
- consistencia
- control visual
- pH si procede
- errores frecuentes

### 5.10 Coste

Campos:

- coste materia prima
- coste mano de obra
- coste energía
- coste envase
- coste total
- coste por unidad
- coste por ración

### 5.11 Aprendizaje

Host AI aprende con producciones reales.

Campos calculados:

- rendimiento real medio
- tiempo real medio
- merma real media
- incidencias frecuentes
- recomendaciones futuras

Ejemplo:

> La demi-glace suele rendir 18,7 L aunque la receta diga 20 L.

---

## 6. Control de versiones

Las fichas técnicas tendrán versiones.

Regla:

```text
Cambio pequeño → actualizar versión actual
Cambio grande → nueva versión
```

Ejemplo:

```text
Demi-glace v1.0
Demi-glace v1.1
Demi-glace v2.0
```

Esto permite saber:

- qué versión se usó en cada evento
- cuánto costaba
- qué rendimiento daba
- qué técnica tenía
- cuándo cambió
- por qué cambió

---

## 7. Platos

Un plato no es una elaboración.

Un plato es montaje/composición.

```text
Elaboraciones
↓
Mise en place
↓
Montaje
↓
Plato terminado
```

Ejemplo:

```text
Taco de carrillera
- tortilla
- carrillera prensada
- salsa
- cebolla encurtida
- brotes
- montaje final
```

Una elaboración puede pertenecer a muchos platos.

Si dos platos usan la misma elaboración, Host AI debe agrupar producción.

Controles de calidad del plato terminado:

- temperatura
- peso
- sabor
- textura
- olor
- vista
- decoración
- limpieza del plato
- emoción / recuerdo

---

## 8. Menús

Un menú agrupa platos.

Campos:

- nombre
- tipo
- precio venta
- coste estimado
- food cost
- margen
- platos
- orden de servicio
- alérgenos

---

## 9. Eventos

Un evento genera necesidades de producción.

Campos:

- nombre
- fecha
- número_personas
- menú
- estado
- observaciones
- cliente
- restricciones
- alérgenos especiales

Estados:

```text
Planificación
Producción
Mise en place
Servicio
Cierre
Revisado
```

---

## 10. Órdenes de Producción

La orden de producción es el centro operativo.

Puede venir de:

- evento
- servicio diario
- reposición de stock
- menú semanal
- producción para congelar

Flujo:

```text
Objetivo
↓
Orden de producción
↓
Elaboraciones necesarias
↓
Producción disponible
↓
Faltante real
↓
Fases
↓
Planning
↓
Ejecución
↓
Registro
```

---

## 11. Producción Disponible

Stock real de elaboraciones ya producidas.

Ejemplos:

- 8 L fumet
- 12 kg bechamel
- 40 croquetas boleadas
- 6 kg demi-glace

Campos:

- elaboración_id
- versión_id
- cantidad
- unidad
- lote
- fecha_producción
- caducidad
- congelado sí/no
- ubicación
- formato
- estado

Cuando una tarea se marca como hecha, Host AI pregunta:

- cuánto se produjo realmente
- unidad
- caducidad
- ubicación
- congelado sí/no

---

## 12. Rendimientos

Cada producción real actualiza rendimiento.

Campos:

- elaboración_version_id
- cantidad_prevista
- cantidad_real
- diferencia
- tiempo_previsto
- tiempo_real
- merma
- observación

Con el tiempo Host AI aprende.

Ejemplo:

```text
Fumet
Previsto: 20 L
Real medio: 18,6 L
Recomendación: aumentar agua o ajustar receta base.
```

---

## 13. Maquinaria

Host AI debe conocer recursos.

Campos:

- nombre
- tipo
- capacidad
- cantidad
- disponible sí/no
- ubicación
- cuello_botella sí/no

Ejemplos:

- horno
- marmita
- freidora
- abatidor
- Thermomix
- Roner
- brasa
- plancha

Regla: un buen jefe nunca espera una máquina. Si una está ocupada, adelanta otra elaboración.

---

## 14. Personal y roles

Host AI reparte tareas por roles, no por personas al principio.

Roles:

- ayudante
- cocinero
- jefe de partida
- jefe de cocina

Ayudante:

- pelar
- cortar
- limpiar
- pesar
- preparar mise en place

Cocinero:

- elaboraciones
- fondos
- carnes
- pescados
- salsas
- emplatado

Jefe de partida:

- coordina partida
- controla calidad
- ejecuta elaboraciones complejas

Jefe de cocina:

- supervisa
- reorganiza
- decide
- controla coste/calidad/tiempo

---

## 15. ADN de Cocina

Cada restaurante tendrá reglas propias.

No son recetas. Son forma de trabajar.

Ejemplos:

- Fondos siempre primero.
- No cortar aguacate con más de 30 min.
- Toda elaboración caliente pasa por abatidor.
- Carrilleras se prensan 24 h.
- Demi-glace en bolsas de 2 L.
- Usar producción disponible antes de producir nuevo.
- No iniciar receta si falta ingrediente crítico.
- La maquinaria se limpia antes de cambiar producción.

Cuando Host AI tenga dudas, consulta el ADN de Cocina.

---

## 16. Motor de Dependencias

Responsabilidad:

- recorrer platos
- encontrar elaboraciones
- encontrar subelaboraciones
- agrupar iguales
- calcular total necesario

Ejemplo:

```text
Plato A necesita demi-glace 2 L
Plato B necesita demi-glace 3 L
Plato C necesita demi-glace 1 L
↓
Producción total demi-glace: 6 L
```

---

## 17. Motor de Producción

Responsabilidad:

- generar orden de producción
- usar producción disponible primero
- calcular faltante
- escalar receta base
- generar fases
- registrar producción real

Regla:

```text
Necesidad - Producción disponible = Producción a fabricar
```

---

## 18. Motor de Planificación

Prioridades:

1. Lo que tarda más.
2. Lo que necesita reposo.
3. Lo que desbloquea otras elaboraciones.
4. Lo que ocupa maquinaria crítica.
5. Lo perecedero.
6. Lo rápido.

Debe distinguir:

- tiempo activo
- tiempo pasivo
- maquinaria ocupada
- personal ocupado
- fase bloqueante

Ejemplo:

```text
08:00 Tostar huesos y espinas juntos.
08:20 Mientras el horno trabaja, cortar bresa.
09:00 Arrancar fumet y fondo oscuro.
09:10 Mientras hierven, preparar bechamel.
```

---

## 19. Servicio

El servicio no empieza cuando termina la producción.

Estados:

```text
Producción terminada
↓
Mise en place
↓
Servicio
↓
Cierre
```

Antes de servicio debe estar listo:

- postres
- fríos
- salsas
- purés
- cremas
- carnes porcionadas
- pescados preparados
- platos contados
- pinzas y cucharas
- brotes
- alérgenos separados
- temperaturas correctas

---

## 20. Checklists inteligentes

No se pasa de fase sin checklist.

Ejemplo antes de servicio:

- producción terminada
- fríos montados
- salsas regeneradas
- purés calientes
- platos contados
- pinzas preparadas
- alérgenos revisados
- temperaturas correctas

Cuando todo está marcado:

```text
Estado: LISTO PARA SERVICIO
```

---

## 21. Motor de Ingesta

Host AI acepta conocimiento desde:

- Excel
- Word
- PDF
- foto
- texto
- voz
- correo
- WhatsApp
- internet

Flujo:

```text
Entrada
↓
Detectar tipo
↓
Extraer datos
↓
Normalizar
↓
Detectar dudas
↓
Usuario confirma
↓
Guardar
```

Regla: la IA puede proponer, pero el usuario confirma.

---

## 22. Importador de recetas

Debe poder convertir documentos en fichas técnicas.

Regla inicial para documentos de Ferran:

- títulos en MAYÚSCULAS = nueva elaboración
- texto normal = contenido de la elaboración
- ingredientes primero
- proceso después

A futuro, Host AI debe aprender el patrón de cada restaurante.

---

## 23. Motor de Costes y Rentabilidad

Objetivo:

> Saber dónde se gana dinero, dónde se pierde y qué hacer para mejorar.

Debe calcular:

- coste teórico
- coste real
- desviación
- margen
- food cost
- plato rentable
- plato problemático
- productos que suben
- recomendaciones

Ejemplo:

> El salmón ha subido un 18 %. El plato pierde 1,42 € por ración. Opciones: subir precio, cambiar proveedor o reducir cantidad.

---

## 24. Dashboard Cocina

Pregunta que responde:

> ¿Qué tengo que hacer ahora?

Debe mostrar:

- eventos de hoy
- producción pendiente
- producción disponible
- tareas urgentes
- mise en place
- alérgenos
- pedidos urgentes
- avisos
- próxima tarea recomendada

---

## 25. Dashboard Rentabilidad

Pregunta que responde:

> ¿Dónde gano y dónde pierdo dinero?

Debe mostrar:

- beneficio estimado
- facturación
- coste real
- food cost
- platos más rentables
- platos con pérdidas
- productos que suben
- recomendaciones económicas

---

## 26. Auditoría

Todo cambio importante se registra.

Campos:

- usuario
- fecha
- entidad
- acción
- antes
- después
- motivo

Acciones auditables:

- cambiar receta
- cambiar precio
- cambiar proveedor
- cerrar evento
- modificar stock
- confirmar compra

---

## 27. Principios no negociables

1. Nunca introducir dos veces la misma información.
2. La IA propone, el usuario confirma.
3. Todo se aprende.
4. Pensar como jefe de cocina.
5. Usar producción disponible antes de producir.
6. No pasar de fase sin checklist.
7. Toda producción real alimenta rendimientos.
8. Todo cambio importante queda auditado.

---

## 28. Roadmap técnico

### Host AI 2.1

- Motor Gastronómico.
- Ficha Técnica Inteligente.
- Dependencias.
- Fases.
- Producción agrupada.
- ADN Cocina básico.

### Host AI 2.2

- Importador inteligente de recetas.
- Relación automática ingredientes-artículos.
- Dudas de importación.

### Host AI 2.3

- Planificador por fases.
- Maquinaria.
- Personal.
- Tiempos activos/pasivos.

### Host AI 2.4

- Compras inteligentes.
- Stock de artículos.
- Faltantes.
- Proveedores.

### Host AI 2.5

- Rentabilidad real.
- Coste teórico vs real.
- TPV futuro.

---

## 29. Conclusión

Host AI debe dejar de ser un programa que guarda datos.

Debe convertirse en un sistema que entiende la cocina.

La diferencia no estará en tener IA.

La diferencia estará en que Host AI conoce:

- el producto
- la técnica
- la producción
- el tiempo
- la maquinaria
- el personal
- las dependencias
- el coste
- el ADN de cada cocina

Ese es el núcleo sobre el que se construirá todo el producto.
