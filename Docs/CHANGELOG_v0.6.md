# HOST AI v0.6

## Objetivo

Crear el primer flujo real de producción disponible.

La producción ya no se marca solo como hecha. Ahora Host AI pregunta cuánto se ha producido realmente y lo guarda como stock de elaboraciones / producción disponible.

---

## Cambios principales

### Producción disponible

Nueva capacidad:

- Registrar producción real.
- Guardar cantidad, unidad, ubicación, caducidad y congelación.
- Ver producción disponible desde el menú principal.
- Ver producción disponible dentro de un evento.

Ejemplo:

- Bechamel: 17.5 kg
- Fumet: 38 L
- Croquetas: 120 uds

---

### Rendimientos

Nueva capacidad:

- Comparar cantidad prevista vs cantidad real.
- Guardar histórico de rendimientos.
- Ver desviación media por elaboración / producción.

Ejemplo:

- Previsto: 40 L fumet
- Real: 36 L fumet
- Desviación: -10 %

---

### Dashboard Cocina

Ahora muestra:

- Próximos eventos.
- Producción pendiente.
- Producción disponible.

---

### Dashboard Rentabilidad

Ahora empieza a mostrar rendimientos reales cuando existan datos.

---

### Importador de recetas

Mejorado para detectar títulos de elaboraciones usando la regla definida por Ferran:

- Títulos en MAYÚSCULAS = nueva elaboración.
- Texto normal = contenido de la elaboración anterior.

---

## Archivos modificados

- Main.py
- CORE/database.py
- CORE/importador_recetas.py
- MODULOS/produccion.py
- MODULOS/produccion_disponible.py
- MODULOS/eventos.py
- MODULOS/dashboard.py

---

## Cómo probar

1. Ejecutar Main.py.
2. Entrar en Eventos.
3. Abrir un evento.
4. Generar producción si no existe.
5. Marcar una tarea como hecha.
6. Introducir cantidad real, unidad, ubicación y caducidad.
7. Entrar en Producción Disponible.
8. Comprobar que aparece la producción registrada.
