from database import conectar, asegurar_restaurante_demo

from produccion import (
    generar_produccion_evento,
    mostrar_produccion_evento,
    marcar_tarea_hecha,
)

from produccion_disponible import (
    mostrar_produccion_disponible,
    mostrar_rendimientos,
)


def mostrar_eventos():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            eventos.id,
            eventos.nombre,
            eventos.fecha,
            eventos.numero_personas,
            eventos.estado,
            menus.nombre AS menu_nombre
        FROM eventos
        LEFT JOIN menus ON eventos.menu_id = menus.id
        ORDER BY eventos.fecha
    """)

    eventos = cursor.fetchall()

    print("\n========== EVENTOS ==========")

    if not eventos:
        print("\nNo hay eventos creados todavía.\n")
        conexion.close()
        input("Pulsa ENTER para volver...")
        return

    print()
    for evento in eventos:
        print(f"{evento['id']}. {evento['nombre']}")
        print(f"   Fecha    : {evento['fecha']}")
        print(f"   Personas : {evento['numero_personas']}")
        print(f"   Menú     : {evento['menu_nombre']}")
        print(f"   Estado   : {evento['estado']}")
        print()

    conexion.close()
    input("Pulsa ENTER para volver...")


def seleccionar_menu(cursor):
    cursor.execute("""
        SELECT id, nombre
        FROM menus
        WHERE activo = 1
        ORDER BY nombre
    """)

    menus = cursor.fetchall()

    if not menus:
        print("\nNo hay menús importados.")
        return None

    print("\n========== MENÚS DISPONIBLES ==========")
    print()

    for menu in menus:
        print(f"{menu['id']}. {menu['nombre']}")

    opcion = input("\nSelecciona el menú del evento: ")

    if not opcion.isdigit():
        print("\nOpción incorrecta.")
        return None

    menu_id = int(opcion)

    for menu in menus:
        if menu["id"] == menu_id:
            return menu_id

    print("\nMenú no encontrado.")
    return None


def crear_evento():
    restaurante_id = asegurar_restaurante_demo()

    conexion = conectar()
    cursor = conexion.cursor()

    print("\n========== CREAR EVENTO ==========")
    print()

    nombre = input("Nombre del evento: ").strip()
    fecha = input("Fecha del evento (YYYY-MM-DD): ").strip()
    personas = input("Número de personas: ").strip()

    if not nombre:
        print("\nEl evento necesita un nombre.")
        conexion.close()
        return

    if not personas.isdigit():
        print("\nEl número de personas no es válido.")
        conexion.close()
        return

    numero_personas = int(personas)

    menu_id = seleccionar_menu(cursor)

    if menu_id is None:
        conexion.close()
        return

    observaciones = input("\nObservaciones: ").strip()

    cursor.execute("""
        INSERT INTO eventos
        (
            restaurante_id,
            menu_id,
            nombre,
            fecha,
            numero_personas,
            estado,
            observaciones
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        restaurante_id,
        menu_id,
        nombre,
        fecha,
        numero_personas,
        "pendiente",
        observaciones,
    ))

    conexion.commit()
    conexion.close()

    print("\n✅ Evento creado correctamente.\n")


def seleccionar_evento():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            eventos.id,
            eventos.nombre,
            eventos.fecha,
            eventos.numero_personas,
            menus.nombre AS menu_nombre
        FROM eventos
        LEFT JOIN menus ON eventos.menu_id = menus.id
        ORDER BY eventos.fecha
    """)

    eventos = cursor.fetchall()

    if not eventos:
        print("\nNo hay eventos creados.")
        conexion.close()
        return None

    print("\n========== SELECCIONAR EVENTO ==========")
    print()

    for evento in eventos:
        print(f"{evento['id']}. {evento['nombre']}")
        print(f"   Fecha    : {evento['fecha']}")
        print(f"   Personas : {evento['numero_personas']}")
        print(f"   Menú     : {evento['menu_nombre']}")
        print()

    opcion = input("\nSelecciona un evento (0 para volver): ")

    conexion.close()

    if opcion == "0":
        return None

    if not opcion.isdigit():
        print("\nOpción incorrecta.")
        return None

    return int(opcion)


def menu_evento_detalle(evento_id):
    while True:
        print("\n========== EVENTO ==========")
        print("1. Ver producción")
        print("2. Generar producción")
        print("3. Marcar tarea como hecha")
        print("4. Ver producción disponible")
        print("5. Ver rendimientos")
        print("0. Volver")

        opcion = input("\n¿Qué quieres hacer? ")

        if opcion == "1":
            mostrar_produccion_evento(evento_id)
        elif opcion == "2":
            generar_produccion_evento(evento_id)
        elif opcion == "3":
            marcar_tarea_hecha(evento_id)
        elif opcion == "4":
            mostrar_produccion_disponible()
        elif opcion == "5":
            mostrar_rendimientos()
        elif opcion == "0":
            break
        else:
            print("\n⚠️ Opción no válida.")


def menu_eventos():
    while True:
        print("\n========== EVENTOS ==========")
        print("1. Ver eventos")
        print("2. Crear evento")
        print("3. Abrir evento")
        print("0. Volver")

        opcion = input("\n¿Qué quieres hacer? ")

        if opcion == "1":
            mostrar_eventos()
        elif opcion == "2":
            crear_evento()
        elif opcion == "3":
            evento_id = seleccionar_evento()
            if evento_id is not None:
                menu_evento_detalle(evento_id)
        elif opcion == "0":
            break
        else:
            print("\n⚠️ Opción no válida.")
