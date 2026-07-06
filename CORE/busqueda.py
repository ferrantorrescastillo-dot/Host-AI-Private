from difflib import SequenceMatcher


ESTADO_UNICO = "UNICO"
ESTADO_MULTIPLE = "MULTIPLE"
ESTADO_APROXIMADO = "APROXIMADO"
ESTADO_NINGUNO = "NINGUNO"


def normalizar_texto(texto):
    """
    Limpia un texto para poder compararlo mejor.
    """
    if texto is None:
        return ""

    return str(texto).lower().strip()


def calcular_similitud(texto_1, texto_2):
    """
    Calcula cuánto se parecen dos textos.
    Devuelve un número entre 0 y 1.
    """
    texto_1 = normalizar_texto(texto_1)
    texto_2 = normalizar_texto(texto_2)

    if not texto_1 or not texto_2:
        return 0

    return SequenceMatcher(None, texto_1, texto_2).ratio()


def buscar_articulos(motor, consulta):
    """
    Busca artículos dentro del motor principal de Host AI.

    No habla con el usuario.
    No pregunta nada.
    No modifica datos.
    No escribe en Excel.

    Solo devuelve un resultado estructurado.
    """

    consulta_normalizada = normalizar_texto(consulta)
    articulos = motor.get("articulos", [])

    resultados = []

    for articulo in articulos:
        nombre = articulo.get("nombre", "")
        nombre_normalizado = normalizar_texto(nombre)

        if not nombre_normalizado:
            continue

        puntuacion = 0

        # Coincidencia fuerte:
        # ejemplo: consulta "tomate cherry" y artículo "tomate cherry"
        if consulta_normalizada == nombre_normalizado:
            puntuacion = 100

        # Coincidencia contenida:
        # ejemplo: consulta "tomate" y artículo "tomate pera"
        elif consulta_normalizada in nombre_normalizado:
            puntuacion = 80

        # Coincidencia inversa:
        # ejemplo: consulta larga que contiene el nombre del artículo
        elif nombre_normalizado in consulta_normalizada:
            puntuacion = 75

        # Coincidencia aproximada:
        # ejemplo: "tomate pera extra" parecido a "tomate pera"
        else:
            similitud = calcular_similitud(consulta_normalizada, nombre_normalizado)

            if similitud >= 0.60:
                puntuacion = int(similitud * 70)

        if puntuacion > 0:
            resultados.append({
                "tipo": "ARTICULO",
                "puntuacion": puntuacion,
                "datos": articulo
            })

    resultados = sorted(
        resultados,
        key=lambda resultado: resultado["puntuacion"],
        reverse=True
    )

    return construir_respuesta_busqueda(
        tipo="ARTICULO",
        consulta=consulta,
        resultados=resultados
    )


def construir_respuesta_busqueda(tipo, consulta, resultados):
    """
    Construye una respuesta estándar para cualquier búsqueda futura.
    """

    if not resultados:
        estado = ESTADO_NINGUNO

    elif len(resultados) == 1:
        if resultados[0]["puntuacion"] >= 80:
            estado = ESTADO_UNICO
        else:
            estado = ESTADO_APROXIMADO

    else:
        mejor = resultados[0]
        segundo = resultados[1]

        diferencia = mejor["puntuacion"] - segundo["puntuacion"]

        if mejor["puntuacion"] >= 90 and diferencia >= 20:
            estado = ESTADO_UNICO
        elif mejor["puntuacion"] >= 60 and diferencia >= 25:
            estado = ESTADO_APROXIMADO
        else:
            estado = ESTADO_MULTIPLE

    return {
        "estado": estado,
        "tipo": tipo,
        "consulta": consulta,
        "resultados": resultados
    }


def obtener_mejor_resultado(respuesta_busqueda):
    """
    Devuelve el mejor resultado cuando existe.
    """

    resultados = respuesta_busqueda.get("resultados", [])

    if not resultados:
        return None

    return resultados[0]


def mostrar_respuesta_busqueda(respuesta_busqueda):
    """
    Función temporal para probar el motor desde consola.

    Más adelante esta responsabilidad pasará al Motor de Conversación.
    """

    estado = respuesta_busqueda["estado"]
    resultados = respuesta_busqueda["resultados"]

    if estado == ESTADO_NINGUNO:
        print("\nNo he encontrado ningún resultado parecido.\n")
        return

    if estado == ESTADO_UNICO:
        articulo = resultados[0]["datos"]

        print("\nHe encontrado este artículo:\n")
        print(f"Artículo : {articulo.get('nombre', '')}")
        print(f"Proveedor: {articulo.get('proveedor', '')}")
        print(f"Precio   : {articulo.get('precio', '')} €\n")
        return

    if estado == ESTADO_APROXIMADO:
        articulo = resultados[0]["datos"]

        print("\nCreo que te refieres a este artículo:\n")
        print(f"Artículo : {articulo.get('nombre', '')}")
        print(f"Proveedor: {articulo.get('proveedor', '')}")
        print(f"Precio   : {articulo.get('precio', '')} €\n")
        return

    if estado == ESTADO_MULTIPLE:
        print("\nHe encontrado varios artículos parecidos:\n")

        for numero, resultado in enumerate(resultados, start=1):
            articulo = resultado["datos"]
            print(f"{numero}. {articulo.get('nombre', '')}")

        print()