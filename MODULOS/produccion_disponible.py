from database import conectar, asegurar_restaurante_demo


def convertir_numero(texto):
    if texto is None:
        return None
    texto = str(texto).strip().replace(",", ".")
    try:
        return float(texto)
    except ValueError:
        return None


def registrar_entrada_produccion(
    nombre,
    cantidad,
    unidad,
    ubicacion="",
    fecha_caducidad="",
    congelado=0,
    observaciones="",
    tarea_produccion_id=None,
    restaurante_id=1,
):
    conexion = conectar()
    cursor = conexion.cursor()

    nombre = str(nombre).strip()
    unidad = str(unidad or "").strip()
    ubicacion = str(ubicacion or "").strip()
    fecha_caducidad = str(fecha_caducidad or "").strip()
    observaciones = str(observaciones or "").strip()
    congelado = 1 if congelado else 0

    if not nombre or cantidad is None:
        conexion.close()
        return None

    cursor.execute("""
        SELECT id, cantidad
        FROM produccion_disponible
        WHERE restaurante_id = ?
        AND LOWER(nombre) = LOWER(?)
        AND COALESCE(unidad, '') = COALESCE(?, '')
        AND COALESCE(ubicacion, '') = COALESCE(?, '')
        AND COALESCE(fecha_caducidad, '') = COALESCE(?, '')
        AND congelado = ?
        LIMIT 1
    """, (
        restaurante_id,
        nombre,
        unidad,
        ubicacion,
        fecha_caducidad,
        congelado,
    ))

    existente = cursor.fetchone()

    if existente:
        produccion_disponible_id = existente["id"]
        nueva_cantidad = (existente["cantidad"] or 0) + cantidad

        cursor.execute("""
            UPDATE produccion_disponible
            SET cantidad = ?,
                observaciones = ?,
                fecha_actualizacion = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (nueva_cantidad, observaciones, produccion_disponible_id))

    else:
        cursor.execute("""
            INSERT INTO produccion_disponible
            (
                restaurante_id,
                nombre,
                cantidad,
                unidad,
                ubicacion,
                fecha_caducidad,
                congelado,
                observaciones
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            restaurante_id,
            nombre,
            cantidad,
            unidad,
            ubicacion,
            fecha_caducidad,
            congelado,
            observaciones,
        ))

        produccion_disponible_id = cursor.lastrowid

    cursor.execute("""
        INSERT INTO movimientos_produccion_disponible
        (
            restaurante_id,
            produccion_disponible_id,
            tarea_produccion_id,
            tipo_movimiento,
            nombre,
            cantidad,
            unidad,
            motivo
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        restaurante_id,
        produccion_disponible_id,
        tarea_produccion_id,
        "ENTRADA",
        nombre,
        cantidad,
        unidad,
        "Producción real registrada",
    ))

    conexion.commit()
    conexion.close()

    return produccion_disponible_id


def registrar_salida_produccion(
    produccion_disponible_id,
    cantidad,
    motivo="Consumo registrado",
    restaurante_id=1,
):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id, nombre, cantidad, unidad
        FROM produccion_disponible
        WHERE id = ?
        AND restaurante_id = ?
    """, (produccion_disponible_id, restaurante_id))

    item = cursor.fetchone()

    if item is None:
        conexion.close()
        print("\nNo he encontrado esa producción disponible.\n")
        return False

    cantidad_actual = item["cantidad"] or 0

    if cantidad is None or cantidad <= 0:
        conexion.close()
        print("\nCantidad no válida.\n")
        return False

    if cantidad > cantidad_actual:
        print("\n⚠️ Estás intentando consumir más de lo que hay registrado.")
        print(f"Disponible: {cantidad_actual} {item['unidad'] or ''}")
        confirmar = input("¿Quieres dejarlo a 0 igualmente? (s/n): ").lower().strip()
        if confirmar != "s":
            conexion.close()
            return False
        cantidad = cantidad_actual

    nueva_cantidad = cantidad_actual - cantidad

    cursor.execute("""
        UPDATE produccion_disponible
        SET cantidad = ?,
            fecha_actualizacion = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (nueva_cantidad, produccion_disponible_id))

    cursor.execute("""
        INSERT INTO movimientos_produccion_disponible
        (
            restaurante_id,
            produccion_disponible_id,
            tipo_movimiento,
            nombre,
            cantidad,
            unidad,
            motivo
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        restaurante_id,
        produccion_disponible_id,
        "SALIDA",
        item["nombre"],
        -abs(cantidad),
        item["unidad"],
        motivo,
    ))

    conexion.commit()
    conexion.close()

    print("\n✅ Consumo registrado.")
    print(f"Queda: {nueva_cantidad} {item['unidad'] or ''}\n")
    return True


def registrar_rendimiento(
    nombre,
    cantidad_prevista,
    cantidad_real,
    unidad,
    tarea_produccion_id=None,
    evento_id=None,
    restaurante_id=1,
):
    conexion = conectar()
    cursor = conexion.cursor()

    diferencia = None
    porcentaje = None

    if cantidad_prevista is not None and cantidad_real is not None:
        diferencia = cantidad_real - cantidad_prevista
        if cantidad_prevista != 0:
            porcentaje = (diferencia / cantidad_prevista) * 100

    cursor.execute("""
        INSERT INTO rendimientos_elaboracion
        (
            restaurante_id,
            nombre,
            cantidad_prevista,
            cantidad_real,
            unidad,
            diferencia,
            porcentaje_diferencia,
            tarea_produccion_id,
            evento_id
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        restaurante_id,
        nombre,
        cantidad_prevista,
        cantidad_real,
        unidad,
        diferencia,
        porcentaje,
        tarea_produccion_id,
        evento_id,
    ))

    conexion.commit()
    conexion.close()


def obtener_produccion_disponible(restaurante_id=1):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            id,
            nombre,
            cantidad,
            unidad,
            ubicacion,
            fecha_caducidad,
            congelado,
            observaciones
        FROM produccion_disponible
        WHERE restaurante_id = ?
        AND cantidad != 0
        ORDER BY nombre, fecha_caducidad
    """, (restaurante_id,))

    filas = cursor.fetchall()
    conexion.close()
    return filas


def mostrar_produccion_disponible(restaurante_id=1):
    filas = obtener_produccion_disponible(restaurante_id)

    print("\n========== PRODUCCIÓN DISPONIBLE ==========")

    if not filas:
        print("\nNo hay producción disponible registrada.\n")
        input("Pulsa ENTER para volver...")
        return

    print()
    for fila in filas:
        congelado = "Sí" if fila["congelado"] else "No"
        caducidad = fila["fecha_caducidad"] or "-"
        ubicacion = fila["ubicacion"] or "-"

        print(f"{fila['id']}. {fila['nombre']}")
        print(f"   Cantidad : {fila['cantidad']} {fila['unidad'] or ''}")
        print(f"   Ubicación: {ubicacion}")
        print(f"   Caduca   : {caducidad}")
        print(f"   Congelado: {congelado}")
        print()

    input("Pulsa ENTER para volver...")


def consumir_produccion_disponible(restaurante_id=1):
    filas = obtener_produccion_disponible(restaurante_id)

    print("\n========== CONSUMIR PRODUCCIÓN DISPONIBLE ==========")

    if not filas:
        print("\nNo hay producción disponible registrada.\n")
        input("Pulsa ENTER para volver...")
        return

    print()
    for fila in filas:
        print(f"{fila['id']}. {fila['nombre']} - {fila['cantidad']} {fila['unidad'] or ''}")
        print(f"   Ubicación: {fila['ubicacion'] or '-'} · Caduca: {fila['fecha_caducidad'] or '-'}")

    opcion = input("\n¿Qué producción has usado? (0 para volver): ").strip()

    if opcion == "0":
        return

    if not opcion.isdigit():
        print("\nOpción incorrecta.\n")
        return

    produccion_id = int(opcion)
    cantidad = convertir_numero(input("Cantidad usada: "))
    motivo = input("Motivo / evento / servicio: ").strip() or "Consumo registrado"

    registrar_salida_produccion(
        produccion_disponible_id=produccion_id,
        cantidad=cantidad,
        motivo=motivo,
        restaurante_id=restaurante_id,
    )


def mostrar_rendimientos(restaurante_id=1):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            nombre,
            COUNT(*) AS veces,
            AVG(cantidad_prevista) AS prevista_media,
            AVG(cantidad_real) AS real_media,
            AVG(porcentaje_diferencia) AS diferencia_media,
            unidad
        FROM rendimientos_elaboracion
        WHERE restaurante_id = ?
        GROUP BY nombre, unidad
        ORDER BY nombre
    """, (restaurante_id,))

    filas = cursor.fetchall()
    conexion.close()

    print("\n========== RENDIMIENTOS ==========")

    if not filas:
        print("\nTodavía no hay rendimientos registrados.\n")
        input("Pulsa ENTER para volver...")
        return

    print()
    for fila in filas:
        diferencia = fila["diferencia_media"]
        if diferencia is None:
            diferencia_texto = "-"
        else:
            diferencia_texto = f"{round(diferencia, 2)} %"

        print(f"• {fila['nombre']}")
        print(f"  Veces registrada : {fila['veces']}")
        print(f"  Previsto medio   : {round(fila['prevista_media'] or 0, 2)} {fila['unidad'] or ''}")
        print(f"  Real medio       : {round(fila['real_media'] or 0, 2)} {fila['unidad'] or ''}")
        print(f"  Diferencia media : {diferencia_texto}")
        print()

    input("Pulsa ENTER para volver...")


def menu_produccion_disponible(restaurante_id=1):
    while True:
        print("\n========== PRODUCCIÓN DISPONIBLE ==========")
        print("1. Ver producción disponible")
        print("2. Registrar consumo")
        print("3. Ver rendimientos")
        print("0. Volver")

        opcion = input("\n¿Qué quieres hacer? ")

        if opcion == "1":
            mostrar_produccion_disponible(restaurante_id)
        elif opcion == "2":
            consumir_produccion_disponible(restaurante_id)
        elif opcion == "3":
            mostrar_rendimientos(restaurante_id)
        elif opcion == "0":
            break
        else:
            print("\n⚠️ Opción no válida.")
