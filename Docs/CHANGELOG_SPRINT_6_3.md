# Sprint 6.3 - Motor económico: escandallos, stock y compras

## Decisiones cerradas

### 1. Producciones intermedias

Las elaboraciones intermedias también existen como stock.

Ejemplo:

- Produces 30 litros de fondo oscuro.
- En stock aparece Fondo oscuro: 30 L.
- Luego una receta consume 2 L, otra consume 4 L, etc.

Esto es lo correcto porque refleja la cocina real.

---

### 2. Compras y unidades convertibles

Se trabaja con unidad base y unidad de compra.

Ejemplo:

- Cebolla unidad base: kg.
- Unidad de compra: caja.
- 1 caja = 25 kg.

Así puedes registrar:

- entra 25 kg
- o entra 1 caja

Y Host AI lo convierte.

---

### 3. Mermas

El stock guarda lo real comprado.

Ejemplo:

- Compras 10 kg de cebolla.
- Stock: 10 kg.

La merma se aplica en el escandallo.

Ejemplo:

- escandallo usa 1,2 kg cebolla
- merma 12%
- cantidad neta estimada: 1,056 kg

Esto permite diferenciar compra real y rendimiento real.

---

### 4. Histórico de precios

Cada vez que entra una compra con precio nuevo, se guarda:

- fecha
- artículo
- precio anterior
- precio nuevo
- proveedor
- unidad

Así en un año se podrá ver cuánto ha subido el aceite, la carne, verduras, etc.

---

### 5. Producción por lotes

Cada producción genera lote:

- lote
- fecha producción
- fecha caducidad
- responsable
- cantidad producida
- escandallo origen

Ejemplo:

LOTE-20260707-001  
Carrillera melosa prensada  
20 raciones  
Responsable: Ferran  
Caducidad: +5 días

---

## Archivos creados

- SERVICIOS/motor_economico.py
- Docs/CHANGELOG_SPRINT_6_3.md

## Prueba

Desde PowerShell:

python SERVICIOS\motor_economico.py

## Qué prueba

- Crear artículos demo
- Registrar compras
- Convertir caja/botella a kg/L
- Calcular coste de escandallo
- Descontar stock al producir
- Generar lote de producción
- Generar pedido automático
- Guardar histórico de precios

## Próximo sprint

Sprint 6.4:

Conectar motor económico con el menú de Host AI.

Opciones recomendadas:

13. Stock / Mercancía
14. Costes / Rentabilidad
15. Compras / Pedidos

O crear un menú nuevo:

18. Motor económico
