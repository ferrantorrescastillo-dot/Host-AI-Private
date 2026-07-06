from database import conectar, asegurar_restaurante_demo


PALABRAS_FONDO = ["fumet", "fondo", "caldo", "demi", "glace", "carrillera", "meloso"]
PALABRAS_CORTA = ["pan", "tabla", "agua", "sorbete"]
PALABRAS_AYUDANTE = ["pelar", "cortar", "limpiar", "lavar", "picar", "mise", "bandeja"]


def estimar_tiempo(nombre):
    texto = (nombre or "").lower()

    if any(p in texto for p in ["demi", "glace", "carrillera", "meloso"]):
        return 240
    if any(p in texto for p in ["fumet", "fondo", "caldo"]):
        return 180
    if any(p in texto for p in ["bechamel", "croqueta"]):
        return 90
    if any(p in texto for p in ["crema", "puré", "parmentier"]):
        return 75
    if any(p in texto for p in ["alioli", "guacamole", "pilpil", "salsa"]):
        return 45
    if any(p in texto for p in PALABRAS_CORTA):
        return 30

    return 60


def recomendar_rol(nombre):
    texto = (nombre or "").lower()

    if any(p in texto for p in PALABRAS_AYUDANTE):
        return "Ayudante"
    if any(p in texto for p in ["finalizar", "emplatar", "pase", "revisar"]):
        return "Jefe de partida"

    return "Cocinero"


def recomendar_prioridad(nombre):
    texto = (nombre or "").lower()

    if any(p in texto for p in PALABRAS_FONDO):
        return "alta"

    return "media"


def mostrar_eventos_disponibles(cursor, restaurante_id):
    cursor.execute("""
        SELECT eventos.id, eventos.nombre, eventos.fecha, eventos.numero_personas, menus.nombre AS menu_nombre
        FROM eventos
        LEFT JOIN menus ON eventos.menu_id = menus.id
        WHERE eventos.restaurante_id = ?
        ORDER BY eventos.fecha
    """, (restaurante_id,))

    eventos = cursor.fetchall()

    if not eventos:
        print("\nNo hay eventos creados.\n")
        return []

    print("\n========== EVENTOS DISPONIBLES ==========")
    for evento in eventos:
        print(f"{evento['id']}. {evento['nombre']}")
        print(f"   Fecha    : {evento['fecha']}")
        print(f"   Personas : {evento['numero_personas']}")
        print(f"   Menú     : {evento['menu_nombre']}")
        print()

    return eventos


def crear_orden_desde_evento(restaurante_id=1):
    restaurante_id = asegurar_restaurante_demo()
    conexion = conectar()
    cursor = conexion.cursor()

    eventos = mostrar_eventos_disponibles(cursor, restaurante_id)
    if not eventos:
        conexion.close()
        return

    opcion = input("Selecciona evento para crear orden de producción: ").strip()

    if not opcion.isdigit():
        print("\nOpción incorrecta.\n")
        conexion.close()
        return

    evento_id = int(opcion)

    cursor.execute("""
        SELECT eventos.id, eventos.nombre, eventos.fecha, eventos.numero_personas,
               eventos.menu_id, menus.nombre AS menu_nombre
        FROM eventos
        LEFT JOIN menus ON eventos.menu_id = menus.id
        WHERE eventos.id = ?
        AND eventos.restaurante_id = ?
    """, (evento_id, restaurante_id))

    evento = cursor.fetchone()

    if evento is None:
        print("\nEvento no encontrado.\n")
        conexion.close()
        return

    cursor.execute("""
        SELECT id
        FROM ordenes_produccion
        WHERE origen_tipo = 'EVENTO'
        AND origen_id = ?
        AND restaurante_id = ?
    """, (evento_id, restaurante_id))

    existente = cursor.fetchone()

    if existente:
        print("\nEste evento ya tiene una orden de producción 2.0 creada.\n")
        conexion.close()
        return

    nombre_orden = f"Orden producción - {evento['nombre']}"

    cursor.execute("""
        INSERT INTO ordenes_produccion
        (restaurante_id, origen_tipo, origen_id, nombre, fecha_objetivo, numero_personas, estado, observaciones)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        restaurante_id,
        "EVENTO",
        evento_id,
        nombre_orden,
        evento["fecha"],
        evento["numero_personas"],
        "borrador",
        f"Generada desde evento con menú: {evento['menu_nombre']}",
    ))

    orden_id = cursor.lastrowid

    cursor.execute("""
        SELECT nombre, cantidad, orden
        FROM platos_menu
        WHERE menu_id = ?
        ORDER BY orden
    """, (evento["menu_id"],))

    platos = cursor.fetchall()
    contador = 0

    for plato in platos:
        cantidad_base = plato["cantidad"]
        if cantidad_base is None:
            cantidad_total = evento["numero_personas"]
        else:
            cantidad_total = cantidad_base * evento["numero_personas"]

        nombre = plato["nombre"]

        cursor.execute("""
            INSERT INTO lineas_orden_produccion
            (orden_id, nombre, tipo, cantidad, unidad, estado, rol_recomendado, prioridad, tiempo_estimado_min, orden, observaciones)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            orden_id,
            nombre,
            "plato_pendiente_desglose",
            cantidad_total,
            "raciones",
            "pendiente",
            recomendar_rol(nombre),
            recomendar_prioridad(nombre),
            estimar_tiempo(nombre),
            plato["orden"],
            "Host AI 2.0: pendiente de convertir este plato en elaboraciones reales.",
        ))
        contador += 1

    conexion.commit()
    conexion.close()

    print("\n✅ Orden de producción 2.0 creada.")
    print(f"Evento : {evento['nombre']}")
    print(f"Menú   : {evento['menu_nombre']}")
    print(f"Líneas : {contador}")
    print("\nSiguiente paso: desglosar platos en elaboraciones.\n")


def listar_ordenes(restaurante_id=1):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id, nombre, fecha_objetivo, numero_personas, estado, origen_tipo, origen_id
        FROM ordenes_produccion
        WHERE restaurante_id = ?
        ORDER BY fecha_objetivo
    """, (restaurante_id,))

    ordenes = cursor.fetchall()
    conexion.close()

    print("\n========== ÓRDENES DE PRODUCCIÓN 2.0 ==========")

    if not ordenes:
        print("No hay órdenes creadas.\n")
        return

    for orden in ordenes:
        print(f"{orden['id']}. {orden['nombre']}")
        print(f"   Fecha   : {orden['fecha_objetivo']}")
        print(f"   Personas: {orden['numero_personas']}")
        print(f"   Estado  : {orden['estado']}")
        print()


def seleccionar_orden(restaurante_id=1):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id, nombre, fecha_objetivo, numero_personas, estado
        FROM ordenes_produccion
        WHERE restaurante_id = ?
        ORDER BY fecha_objetivo
    """, (restaurante_id,))

    ordenes = cursor.fetchall()
    conexion.close()

    if not ordenes:
        print("\nNo hay órdenes creadas.\n")
        return None

    print("\n========== SELECCIONAR ORDEN ==========")
    for orden in ordenes:
        print(f"{orden['id']}. {orden['nombre']} - {orden['fecha_objetivo']} - {orden['estado']}")

    opcion = input("\nSelecciona orden (0 para volver): ").strip()

    if opcion == "0":
        return None

    if not opcion.isdigit():
        print("\nOpción incorrecta.\n")
        return None

    return int(opcion)


def ver_detalle_orden(orden_id):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id, nombre, fecha_objetivo, numero_personas, estado, observaciones
        FROM ordenes_produccion
        WHERE id = ?
    """, (orden_id,))

    orden = cursor.fetchone()

    if orden is None:
        print("\nOrden no encontrada.\n")
        conexion.close()
        return

    cursor.execute("""
        SELECT nombre, tipo, cantidad, unidad, estado, rol_recomendado,
               prioridad, tiempo_estimado_min, observaciones
        FROM lineas_orden_produccion
        WHERE orden_id = ?
        ORDER BY prioridad DESC, tiempo_estimado_min DESC, orden
    """, (orden_id,))

    lineas = cursor.fetchall()
    conexion.close()

    print("\n========== DETALLE ORDEN PRODUCCIÓN 2.0 ==========")
    print(orden["nombre"])
    print(f"Fecha   : {orden['fecha_objetivo']}")
    print(f"Personas: {orden['numero_personas']}")
    print(f"Estado  : {orden['estado']}")
    print("--------------------------------------")

    if not lineas:
        print("No hay líneas de producción.")
        return

    total_min = 0
    for linea in lineas:
        total_min += linea["tiempo_estimado_min"] or 0
        print(f"• {linea['nombre']}")
        print(f"  Tipo     : {linea['tipo']}")
        print(f"  Cantidad : {linea['cantidad']} {linea['unidad']}")
        print(f"  Rol      : {linea['rol_recomendado']}")
        print(f"  Prioridad: {linea['prioridad']}")
        print(f"  Tiempo   : {linea['tiempo_estimado_min']} min")
        print(f"  Nota     : {linea['observaciones']}")
        print()

    print(f"Total estimado bruto: {round(total_min / 60, 2)} h")
    print("\nHost AI:")
    print("Esta orden todavía trabaja por platos. La siguiente versión convertirá estos platos en elaboraciones y dependencias reales.\n")


def convertir_orden_a_produccion(orden_id):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id, nombre, origen_tipo, origen_id
        FROM ordenes_produccion
        WHERE id = ?
    """, (orden_id,))

    orden = cursor.fetchone()

    if orden is None:
        print("\nOrden no encontrada.\n")
        conexion.close()
        return

    if orden["origen_tipo"] != "EVENTO":
        print("\nDe momento solo convierto órdenes creadas desde eventos.\n")
        conexion.close()
        return

    evento_id = orden["origen_id"]

    cursor.execute("SELECT id FROM producciones WHERE evento_id = ?", (evento_id,))
    existente = cursor.fetchone()

    if existente:
        print("\nEste evento ya tiene producción clásica creada. No duplico tareas.\n")
        conexion.close()
        return

    cursor.execute("""
        INSERT INTO producciones (evento_id, nombre, estado, observaciones)
        VALUES (?, ?, ?, ?)
    """, (
        evento_id,
        f"Producción - {orden['nombre']}",
        "pendiente",
        "Creada desde Orden de Producción 2.0",
    ))

    produccion_id = cursor.lastrowid

    cursor.execute("""
        SELECT nombre, cantidad, unidad, rol_recomendado, prioridad, tiempo_estimado_min, orden
        FROM lineas_orden_produccion
        WHERE orden_id = ?
        ORDER BY orden
    """, (orden_id,))

    lineas = cursor.fetchall()

    for i, linea in enumerate(lineas, start=1):
        cursor.execute("""
            INSERT INTO tareas_produccion
            (produccion_id, nombre, cantidad, unidad, estado, orden,
             rol_recomendado, prioridad, tiempo_estimado_min)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            produccion_id,
            linea["nombre"],
            linea["cantidad"],
            linea["unidad"],
            "pendiente",
            linea["orden"] or i,
            linea["rol_recomendado"],
            linea["prioridad"],
            linea["tiempo_estimado_min"],
        ))

    cursor.execute("UPDATE ordenes_produccion SET estado = 'convertida' WHERE id = ?", (orden_id,))

    conexion.commit()
    conexion.close()

    print("\n✅ Orden convertida a producción clásica.")
    print("Ahora puedes verla en Eventos → Abrir evento → Ver producción.\n")


def menu_orden_detalle(orden_id):
    while True:
        print("\n========== ORDEN PRODUCCIÓN 2.0 ==========")
        print("1. Ver detalle")
        print("2. Convertir a producción clásica")
        print("0. Volver")

        opcion = input("\n¿Qué quieres hacer? ").strip()

        if opcion == "1":
            ver_detalle_orden(orden_id)
        elif opcion == "2":
            convertir_orden_a_produccion(orden_id)
        elif opcion == "0":
            break
        else:
            print("\n⚠️ Opción no válida.")


def menu_ordenes_produccion(restaurante_id=1):
    while True:
        print("\n========== ÓRDENES DE PRODUCCIÓN 2.0 ==========")
        print("1. Ver órdenes")
        print("2. Crear orden desde evento")
        print("3. Abrir orden")
        print("0. Volver")

        opcion = input("\n¿Qué quieres hacer? ").strip()

        if opcion == "1":
            listar_ordenes(restaurante_id)
        elif opcion == "2":
            crear_orden_desde_evento(restaurante_id)
        elif opcion == "3":
            orden_id = seleccionar_orden(restaurante_id)
            if orden_id is not None:
                menu_orden_detalle(orden_id)
        elif opcion == "0":
            break
        else:
            print("\n⚠️ Opción no válida.")
