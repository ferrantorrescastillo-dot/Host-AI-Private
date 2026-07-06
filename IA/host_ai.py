import subprocess

while True:

    print("")
    print("=====================================")
    print("              HOST AI")
    print("   Asistente Inteligente Hostelería")
    print("=====================================")
    print("1. Buscar artículos")
    print("2. Añadir artículo")
    print("3. Modificar artículo")
    print("4. Eliminar artículo")
    print("5. Ver historial de compras")
    print("0. Salir")

    opcion = input("Selecciona una opción: ")

    if opcion == "1":
        subprocess.run(["python", "buscar_articulos.py"])
        input("\nPulsa ENTER para volver al menú...")

    elif opcion == "2":
        subprocess.run(["python", "añadir_articulo.py"])
        input("\nPulsa ENTER para volver al menú...")

    elif opcion == "3":
        subprocess.run(["python", "actualizar_precios.py"])
        input("\nPulsa ENTER para volver al menú...")

    elif opcion == "4":
        subprocess.run(["python", "eliminar_articulo.py"])
        input("\nPulsa ENTER para volver al menú...")

    elif opcion == "5":
        subprocess.run(["python", "ver_historial.py"])
        input("\nPulsa ENTER para volver al menú...")

    elif opcion == "0":
        print("\n¡Hasta pronto!")
        break

    else:
        print("\nOpción no válida.")
        input("Pulsa ENTER para continuar...")
        