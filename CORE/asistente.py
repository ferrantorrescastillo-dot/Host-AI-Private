from cerebro import entender_pregunta
from orquestador import ejecutar_accion

from acciones import (
    BUSCAR_ARTICULO,
    CONSULTAR_PRECIO,
    CONSULTAR_PROVEEDOR,
)

from busqueda import (
    ESTADO_UNICO,
    ESTADO_MULTIPLE,
    ESTADO_APROXIMADO,
    ESTADO_NINGUNO,
)


def crear_contexto():
    return {
        "ultimo_articulo": None,
        "ultima_accion": None,
    }


def guardar_articulo_en_contexto(contexto, articulo, accion=None):
    contexto["ultimo_articulo"] = articulo
    contexto["ultima_accion"] = accion


def mostrar_articulo_basico(articulo):
    print(f"Artículo : {articulo.get('nombre', '')}")
    print(f"Proveedor: {articulo.get('proveedor', '')}")
    print(f"Precio   : {articulo.get('precio', '')} €")


def responder_pregunta_contextual(pregunta, contexto):
    texto = pregunta.lower().strip()
    articulo = contexto.get("ultimo_articulo")

    if articulo is None:
        return False

    if "kg" in texto or "kilo" in texto or "unidad" in texto or "medida" in texto or "medidas" in texto:
        print("\nHost AI:")
        print(f"El último artículo era: {articulo.get('nombre', '')}")
        print(f"Precio registrado: {articulo.get('precio', '')} €")
        print("Todavía no tengo cargada la unidad de medida en el motor.\n")
        return True

    if "proveedor" in texto or "quien" in texto or "vende" in texto:
        print("\nHost AI:")
        print(f"El artículo {articulo.get('nombre', '')} lo suministra:")
        print(f"{articulo.get('proveedor', '')}\n")
        return True

    if "precio" in texto or "cuanto" in texto or "cuánto" in texto:
        print("\nHost AI:")
        print(f"El artículo {articulo.get('nombre', '')} cuesta:")
        print(f"{articulo.get('precio', '')} €\n")
        return True

    return False


def elegir_resultado_busqueda(respuesta_busqueda):
    resultados = respuesta_busqueda.get("resultados", [])

    if not resultados:
        return None

    if len(resultados) == 1:
        return resultados[0]["datos"]

    print("\nHe encontrado varios artículos parecidos:\n")

    for numero, resultado in enumerate(resultados, start=1):
        articulo = resultado["datos"]
        print(f"{numero}. {articulo.get('nombre', '')}")

    opcion = input("\n¿Cuál quieres usar? ")

    if not opcion.isdigit():
        return None

    opcion = int(opcion)

    if opcion < 1 or opcion > len(resultados):
        return None

    return resultados[opcion - 1]["datos"]


def responder_busqueda_articulo(datos, contexto):
    estado = datos["estado"]
    resultados = datos["resultados"]

    print("\nHost AI:")

    if estado == ESTADO_NINGUNO:
        print("No he encontrado ningún artículo parecido.\n")
        return

    if estado == ESTADO_UNICO:
        articulo = resultados[0]["datos"]
        guardar_articulo_en_contexto(contexto, articulo, BUSCAR_ARTICULO)

        print("He encontrado este artículo:\n")
        mostrar_articulo_basico(articulo)
        print()
        return

    if estado == ESTADO_APROXIMADO:
        articulo = resultados[0]["datos"]
        guardar_articulo_en_contexto(contexto, articulo, BUSCAR_ARTICULO)

        print("Creo que te refieres a este artículo:\n")
        mostrar_articulo_basico(articulo)
        print()
        return

    if estado == ESTADO_MULTIPLE:
        articulo = elegir_resultado_busqueda(datos)

        print("\nHost AI:")

        if articulo is None:
            print("No he podido identificar claramente cuál quieres.\n")
        else:
            guardar_articulo_en_contexto(contexto, articulo, BUSCAR_ARTICULO)

            print("Has elegido:\n")
            mostrar_articulo_basico(articulo)
            print()


def responder_precio(datos, contexto):
    articulo = elegir_resultado_busqueda(datos)

    print("\nHost AI:")

    if articulo is None:
        print("No he encontrado claramente ese artículo.\n")
    else:
        guardar_articulo_en_contexto(contexto, articulo, CONSULTAR_PRECIO)

        print(f"El artículo {articulo.get('nombre', '')} cuesta:")
        print(f"{articulo.get('precio', '')} €\n")


def responder_proveedor(datos, contexto):
    articulo = elegir_resultado_busqueda(datos)

    print("\nHost AI:")

    if articulo is None:
        print("No he encontrado claramente ese artículo.\n")
    else:
        guardar_articulo_en_contexto(contexto, articulo, CONSULTAR_PROVEEDOR)

        print(f"El artículo {articulo.get('nombre', '')} lo suministra:")
        print(f"{articulo.get('proveedor', '')}\n")


def mostrar_respuesta_orquestador(respuesta, contexto):
    tipo_respuesta = respuesta.get("tipo_respuesta")
    datos = respuesta.get("datos")

    if tipo_respuesta == "BUSQUEDA_ARTICULO":
        responder_busqueda_articulo(datos, contexto)
        return

    if tipo_respuesta == "CONSULTA_PRECIO":
        responder_precio(datos, contexto)
        return

    if tipo_respuesta == "CONSULTA_PROVEEDOR":
        responder_proveedor(datos, contexto)
        return

    print("\nHost AI:")
    print("No he entendido la pregunta.\n")


def conversar_con_host_ai(motor):
    contexto = crear_contexto()

    print("\n======================================")
    print("        ASISTENTE HOST AI")
    print("======================================")
    print("Escribe 'salir' para volver.\n")

    while True:

        pregunta = input("Tú: ")

        if pregunta.lower().strip() == "salir":
            break

        if responder_pregunta_contextual(pregunta, contexto):
            continue

        accion = entender_pregunta(pregunta)

        if accion == "TOTAL_ARTICULOS":

            print("\nHost AI:")
            print(f"Tienes {len(motor['articulos'])} artículos registrados.\n")

        elif accion == "TOTAL_PROVEEDORES":

            print("\nHost AI:")
            print(f"Trabajas con {len(motor['proveedores'])} proveedores.\n")

        elif accion == "LISTAR_PROVEEDORES":

            print("\nHost AI:\n")

            for proveedor in motor["proveedores"]:
                print("-", proveedor)

            print()

        else:
            respuesta = ejecutar_accion(motor, accion, pregunta)
            mostrar_respuesta_orquestador(respuesta, contexto)