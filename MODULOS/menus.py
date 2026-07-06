from database import conectar


def mostrar_menus():

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id, nombre
        FROM menus
        ORDER BY nombre
    """)

    menus = cursor.fetchall()

    if not menus:
        print("\nNo hay menús importados.")
        conexion.close()
        return

    print("\n========== MENÚS ==========\n")

    for menu in menus:
        print(f"{menu['id']}. {menu['nombre']}")

    opcion = input("\nSelecciona un menú (0 para volver): ")

    if opcion == "0":
        conexion.close()
        return

    try:
        menu_id = int(opcion)
    except:
        print("\nOpción incorrecta.")
        conexion.close()
        return

    cursor.execute("""
        SELECT nombre
        FROM menus
        WHERE id = ?
    """, (menu_id,))

    menu = cursor.fetchone()

    if menu is None:
        print("\nMenú no encontrado.")
        conexion.close()
        return

    print("\n================================")
    print(menu["nombre"])
    print("================================\n")

    cursor.execute("""
        SELECT
            nombre,
            cantidad,
            coste_racion
        FROM platos_menu
        WHERE menu_id = ?
        ORDER BY orden
    """, (menu_id,))

    platos = cursor.fetchall()

    for plato in platos:

        cantidad = plato["cantidad"]
        coste = plato["coste_racion"]

        if cantidad is None:
            cantidad = "-"

        if coste is None:
            coste = "-"

        print(f"• {plato['nombre']}")
        print(f"  Cantidad : {cantidad}")
        print(f"  Coste    : {coste}")
        print()

    conexion.close()