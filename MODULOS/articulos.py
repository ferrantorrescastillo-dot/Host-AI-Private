from datos import cargar_articulos
from ia import entender_usuario, confirmar, detectar_precio, detectar_proveedor
from escandallos import buscar_escandallos_por_articulo


def buscar_articulos_parecidos(nombre):
    df = cargar_articulos()
    resultados = []

    for i, fila in df.iterrows():
        articulo = str(fila.iloc[1]).strip()

        if articulo and articulo.lower() != "nan":
            if nombre.strip().lower() in articulo.lower():
                resultados.append((i, fila))

    return resultados


def mostrar_articulo():
    nombre = input("¿Qué artículo quieres buscar? ")

    resultados = buscar_articulos_parecidos(nombre)

    if not resultados:
        print("\nNo he encontrado artículos parecidos.")
        input("\nPulsa ENTER para volver...")
        return

    print("\nArtículos encontrados:\n")

    for numero, (indice, articulo) in enumerate(resultados, start=1):
        print(f"{numero}. {articulo.iloc[1]}")

    opcion = input("\nElige el número del artículo: ")

    if not opcion.isdigit():
        print("Opción no válida.")
        input("\nPulsa ENTER para volver...")
        return

    opcion = int(opcion)

    if opcion < 1 or opcion > len(resultados):
        print("Número fuera de rango.")
        input("\nPulsa ENTER para volver...")
        return

    _, articulo = resultados[opcion - 1]

    conversar_con_articulo(articulo)


def conversar_con_articulo(articulo):
    nombre = articulo.iloc[1]
    proveedor = articulo.iloc[3]
    precio = articulo.iloc[5]

    while True:
        print("\n========================================")
        print("         FICHA DEL ARTÍCULO")
        print("========================================\n")

        print(f"📦 Artículo : {nombre}")
        print(f"🏢 Proveedor: {proveedor}")
        print(f"💰 Precio   : {precio} €")

        print("\n----------------------------------------")
        print(f"¿Qué quieres hacer con {nombre}?")
        print("Ejemplos:")
        print("- ahora vale 1,80")
        print("- ahora se lo compro a Makro")
        print("- ahora vale 1,80 y se lo compro a Makro")
        print("- en qué recetas aparece")
        print("- ver historial")
        print("- salir")
        print("----------------------------------------")

        orden = input("\nTú: ")
        intencion = entender_usuario(orden)

        if intencion == "SALIR":
            break

        elif intencion == "CAMBIAR_PRECIO":
            nuevo_precio = detectar_precio(orden)

            if nuevo_precio is None:
                nuevo_precio = input("\nHost AI: ¿Cuál es el nuevo precio? ")

            print("\nHost AI ha entendido esto:")
            print("----------------------------------------")
            print(f"Artículo      : {nombre}")
            print(f"Precio actual : {precio} €")
            print(f"Nuevo precio  : {nuevo_precio} €")
            print("----------------------------------------")

            if confirmar("¿Es correcto?"):
                print("\nPerfecto. Cambio preparado.")
                print("De momento NO lo guardaré por seguridad.")
            else:
                print("\nVale, no hago nada.")

            input("\nPulsa ENTER para continuar...")

        elif intencion == "CAMBIAR_PROVEEDOR":
            nuevo_proveedor = detectar_proveedor(orden)

            if nuevo_proveedor is None:
                nuevo_proveedor = input("\nHost AI: ¿Cuál es el nuevo proveedor? ")

            print("\nHost AI ha entendido esto:")
            print("----------------------------------------")
            print(f"Artículo          : {nombre}")
            print(f"Proveedor actual  : {proveedor}")
            print(f"Nuevo proveedor   : {nuevo_proveedor}")
            print("----------------------------------------")

            if confirmar("¿Es correcto?"):
                print("\nPerfecto. Cambio preparado.")
                print("De momento NO lo guardaré por seguridad.")
            else:
                print("\nVale, no hago nada.")

            input("\nPulsa ENTER para continuar...")

        elif intencion == "CAMBIAR_PRECIO_Y_PROVEEDOR":
            nuevo_precio = detectar_precio(orden)
            nuevo_proveedor = detectar_proveedor(orden)

            if nuevo_precio is None:
                nuevo_precio = input("\nHost AI: ¿Cuál es el nuevo precio? ")

            if nuevo_proveedor is None:
                nuevo_proveedor = input("\nHost AI: ¿Cuál es el nuevo proveedor? ")

            print("\nHost AI ha entendido esto:")
            print("----------------------------------------")
            print(f"Artículo          : {nombre}")
            print(f"Precio actual     : {precio} €")
            print(f"Nuevo precio      : {nuevo_precio} €")
            print(f"Proveedor actual  : {proveedor}")
            print(f"Nuevo proveedor   : {nuevo_proveedor}")
            print("----------------------------------------")

            if confirmar("¿Es correcto?"):
                print("\nPerfecto. Cambios preparados.")
                print("De momento NO los guardaré por seguridad.")
            else:
                print("\nVale, no hago nada.")

            input("\nPulsa ENTER para continuar...")

        elif intencion == "VER_HISTORIAL":
            print("\nHost AI:")
            print("He entendido que quieres ver el historial de compras.")
            input("\nPulsa ENTER para continuar...")

        elif intencion == "VER_ESCANDALLOS":
            print("\nHost AI:")
            print(f"Buscando recetas donde se utiliza {nombre}...")

            recetas = buscar_escandallos_por_articulo(nombre)

            if not recetas:
                print("\nNo aparece en ninguna receta.")
            else:
                print("\nEste artículo aparece en:\n")

                for receta in recetas:
                    print("•", receta)

                print(f"\nTotal de recetas: {len(recetas)}")

            input("\nPulsa ENTER para continuar...")

        else:
            print("\nHost AI:")
            print("No he entendido la orden.")
            input("\nPulsa ENTER para continuar...")


def mostrar_todos_los_articulos():
    df = cargar_articulos()

    print("\n=========================================")
    print("           LISTADO DE ARTÍCULOS")
    print("=========================================\n")

    contador = 0

    for _, fila in df.iterrows():
        nombre = str(fila.iloc[1]).strip()

        if nombre and nombre.lower() != "nan":
            contador += 1
            print(f"{contador}. {nombre}")

    print(f"\nTotal de artículos encontrados: {contador}")
    input("\nPulsa ENTER para volver...")