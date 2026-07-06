from motor import cargar_restaurante
from articulos import mostrar_articulo, mostrar_todos_los_articulos
from asistente import conversar_con_host_ai


motor = cargar_restaurante()


while True:
    print("\n======================================")
    print("           HOST AI v0.1")
    print("======================================")
    print(f"📦 Artículos cargados : {len(motor['articulos'])}")
    print(f"🏢 Proveedores        : {len(motor['proveedores'])}")
    print(f"🍽 Escandallos        : {len(motor['hojas_escandallos'])}")
    print("======================================")

    print("1. Artículos")
    print("2. Stock")
    print("3. Compras")
    print("4. Recetas")
    print("5. Eventos")
    print("6. Asistente IA")
    print("7. Configuración")
    print("0. Salir")

    opcion = input("\n¿Qué quieres hacer? ")

    if opcion == "1":

        while True:
            print("\n========== ARTÍCULOS ==========")
            print("1. Buscar artículo")
            print("2. Añadir artículo (desactivado)")
            print("3. Modificar artículo (desactivado)")
            print("4. Eliminar artículo (desactivado)")
            print("5. Mostrar todos")
            print("0. Volver")

            opcion_articulos = input("\n¿Qué quieres hacer? ")

            if opcion_articulos == "1":
                mostrar_articulo()

            elif opcion_articulos == "5":
                mostrar_todos_los_articulos()

            elif opcion_articulos == "0":
                break

            else:
                print("\n⚠️ Función todavía no disponible.")

    elif opcion == "6":
        conversar_con_host_ai(motor)

    elif opcion == "0":
        print("\nHost AI:")
        print("Hasta luego 👨‍🍳")
        break

    else:
        print("\nHost AI:")
        print("Todavía no sé hacer eso.")