from database import conectar
from produccion_disponible import (
    convertir_numero,
    registrar_entrada_produccion,
    registrar_rendimiento,
)


def generar_produccion_evento(evento_id):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            eventos.id,
            eventos.nombre,
            eventos.numero_personas,
            eventos.restaurante_id,
            menus.id AS menu_id,
            menus.nombre AS menu_nombre
        FROM eventos
        LEFT JOIN menus ON eventos.menu_id = menus.id
        WHERE eventos.id = ?
    """, (evento_id,))

    evento = cursor.fetchone()

    if evento is None:
        print("\nEvento no encontrado.")
        conexion.close()
        return

    cursor.execute("""
        SELECT id
        FROM producciones
        WHERE evento_id = ?
    """, (evento_id,))

    produccion_existente = cursor.fetchone()

    if produccion_existente:
        print("\nEste evento ya tiene producción generada.")
        conexion.close()
        return

    nombre_produccion = f"Producción - {evento['nombre']}"

    cursor.execute("""
        INSERT INTO producciones (evento_id, nombre, estado, observaciones)
        VALUES (?, ?, ?, ?)
    """, (
        evento_id,
        nombre_produccion,
        "pendiente",
        "Producción generada automáticamente desde el menú del evento.",
    ))

    produccion_id = cursor.lastrowid

    cursor.execute("""
        SELECT nombre, cantidad, coste_racion, orden
        FROM platos_menu
        WHERE menu_id = ?
        ORDER BY orden
    """, (evento["menu_id"],))

    platos = cursor.fetchall()

    orden = 1

    for plato in platos:
        cantidad_base = plato["cantidad"]

        if cantidad_base is None:
            cantidad_total = evento["numero_personas"]
        else:
            cantidad_total = cantidad_base * evento["numero_personas"]

        cursor.execute("""
            INSERT INTO tareas_produccion
            (
                produccion_id,
                nombre,
                cantidad,
                unidad,
                estado,
                orden
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            produccion_id,
            plato["nombre"],
            cantidad_total,
            "raciones",
            "pendiente",
            orden,
        ))

        orden += 1

    conexion.commit()
    conexion.close()

    print("\n✅ Producción generada correctamente.")
    print(f"Evento: {evento['nombre']}")
    print(f"Menú  : {evento['menu_nombre']}")
    print(f"Tareas creadas: {len(platos)}\n")


def mostrar_produccion_evento(evento_id):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id, nombre, estado
        FROM producciones
        WHERE evento_id = ?
    """, (evento_id,))

    produccion = cursor.fetchone()

    if produccion is None:
        print("\nEste evento todavía no tiene producción generada.\n")
        conexion.close()
        return

    print("\n========== PRODUCCIÓN ==========")
    print(f"\n{produccion['nombre']}")
    print(f"Estado: {produccion['estado']}\n")

    cursor.execute("""
        SELECT id, nombre, cantidad, unidad, estado, orden
        FROM tareas_produccion
        WHERE produccion_id = ?
        ORDER BY orden
    """, (produccion["id"],))

    tareas = cursor.fetchall()

    if not tareas:
        print("No hay tareas de producción.")
        conexion.close()
        return

    for tarea in tareas:
        check = "✅" if tarea["estado"] == "hecha" else "□"
        print(f"{check} {tarea['orden']}. {tarea['nombre']}")
        print(f"   Previsto: {tarea['cantidad']} {tarea['unidad']}")
        print(f"   Estado  : {tarea['estado']}")
        print()

    conexion.close()


def marcar_tarea_hecha(evento_id):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT eventos.id, eventos.restaurante_id
        FROM eventos
        WHERE eventos.id = ?
    """, (evento_id,))
    evento = cursor.fetchone()

    if evento is None:
        print("\nEvento no encontrado.")
        conexion.close()
        return

    cursor.execute("""
        SELECT id
        FROM producciones
        WHERE evento_id = ?
    """, (evento_id,))

    produccion = cursor.fetchone()

    if produccion is None:
        print("\nEste evento no tiene producción.")
        conexion.close()
        return

    cursor.execute("""
        SELECT id, nombre, cantidad, unidad, estado, orden
        FROM tareas_produccion
        WHERE produccion_id = ?
        ORDER BY orden
    """, (produccion["id"],))

    tareas = cursor.fetchall()

    if not tareas:
        print("\nNo hay tareas.")
        conexion.close()
        return

    print("\n========== TAREAS ==========")
    print("\nElige la tarea que has terminado.\n")

    for tarea in tareas:
        check = "✅" if tarea["estado"] == "hecha" else "□"
        print(f"{tarea['id']}. {check} {tarea['nombre']} - previsto: {tarea['cantidad']} {tarea['unidad']}")

    opcion = input("\n¿Qué tarea quieres marcar como hecha? ")

    if not opcion.isdigit():
        print("\nOpción incorrecta.")
        conexion.close()
        return

    tarea_id = int(opcion)

    cursor.execute("""
        SELECT id, nombre, cantidad, unidad, estado
        FROM tareas_produccion
        WHERE id = ?
    """, (tarea_id,))

    tarea = cursor.fetchone()

    if tarea is None:
        print("\nTarea no encontrada.")
        conexion.close()
        return

    print("\n========== PRODUCCIÓN REAL ==========")
    print(f"Tarea   : {tarea['nombre']}")
    print(f"Previsto: {tarea['cantidad']} {tarea['unidad']}")

    cantidad_real = convertir_numero(input("\n¿Cuánto has producido realmente? "))
    unidad_real = input(f"Unidad [{tarea['unidad']}]: ").strip() or tarea["unidad"]
    ubicacion = input("Ubicación (cámara, congelador, etc.): ").strip()
    fecha_caducidad = input("Fecha caducidad (YYYY-MM-DD, opcional): ").strip()
    congelado_texto = input("¿Está congelado? (s/n): ").lower().strip()
    observaciones = input("Observaciones: ").strip()

    if cantidad_real is None:
        print("\nCantidad no válida.")
        conexion.close()
        return

    cursor.execute("""
        UPDATE tareas_produccion
        SET estado = 'hecha'
        WHERE id = ?
    """, (tarea_id,))

    conexion.commit()
    conexion.close()

    congelado = 1 if congelado_texto == "s" else 0

    registrar_entrada_produccion(
        nombre=tarea["nombre"],
        cantidad=cantidad_real,
        unidad=unidad_real,
        ubicacion=ubicacion,
        fecha_caducidad=fecha_caducidad,
        congelado=congelado,
        observaciones=observaciones,
        tarea_produccion_id=tarea_id,
        restaurante_id=evento["restaurante_id"],
    )

    registrar_rendimiento(
        nombre=tarea["nombre"],
        cantidad_prevista=tarea["cantidad"],
        cantidad_real=cantidad_real,
        unidad=unidad_real,
        tarea_produccion_id=tarea_id,
        evento_id=evento_id,
        restaurante_id=evento["restaurante_id"],
    )

    print("\n✅ Tarea marcada como hecha.")
    print("✅ Producción real añadida a Producción Disponible.")
    print("✅ Rendimiento registrado.\n")
