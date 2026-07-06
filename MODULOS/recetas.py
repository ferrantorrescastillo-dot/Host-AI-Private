from database import conectar
from importador_recetas import importar_recetas_desde_word


def listar_elaboraciones():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id, nombre
        FROM elaboraciones
        WHERE activo = 1
        ORDER BY nombre
    """)

    elaboraciones = cursor.fetchall()

    print("\n========== ELABORACIONES ==========\n")

    if not elaboraciones:
        print("No hay elaboraciones guardadas.\n")
        conexion.close()
        input("Pulsa ENTER para volver...")
        return

    for elaboracion in elaboraciones:
        print(f"{elaboracion['id']}. {elaboracion['nombre']}")

    opcion = input("\nSelecciona una elaboración (0 para volver): ")

    if opcion == "0":
        conexion.close()
        return

    if not opcion.isdigit():
        print("\nOpción incorrecta.")
        conexion.close()
        return

    elaboracion_id = int(opcion)

    cursor.execute("""
        SELECT nombre, elaboracion
        FROM elaboraciones
        WHERE id = ?
    """, (elaboracion_id,))

    elaboracion = cursor.fetchone()
    conexion.close()

    if elaboracion is None:
        print("\nElaboración no encontrada.\n")
        return

    print("\n======================================")
    print(elaboracion["nombre"])
    print("======================================\n")
    print(elaboracion["elaboracion"] or "Sin proceso registrado.")
    print()

    input("Pulsa ENTER para volver...")


def contar_elaboraciones():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM elaboraciones
        WHERE activo = 1
    """)

    resultado = cursor.fetchone()
    conexion.close()

    return resultado["total"] if resultado else 0


def menu_recetas():
    while True:
        print("\n========== RECETAS / ELABORACIONES ==========")
        print(f"Elaboraciones guardadas: {contar_elaboraciones()}")
        print("---------------------------------------------")
        print("1. Ver elaboraciones")
        print("2. Importar recetas desde Word")
        print("0. Volver")

        opcion = input("\n¿Qué quieres hacer? ")

        if opcion == "1":
            listar_elaboraciones()

        elif opcion == "2":
            importar_recetas_desde_word()

        elif opcion == "0":
            break

        else:
            print("\n⚠️ Opción no válida.")
