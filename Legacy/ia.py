import re


def entender_usuario(orden):
    orden = orden.strip().lower()

    if orden in ["salir", "volver", "0", "nada"]:
        return "SALIR"

    tiene_precio = (
        "precio" in orden
        or "vale" in orden
        or "cuesta" in orden
        or "subido" in orden
        or "bajado" in orden
    )

    tiene_proveedor = (
        "proveedor" in orden
        or "compro a" in orden
        or "se lo compro a" in orden
        or "lo compro a" in orden
    )

    if tiene_precio and tiene_proveedor:
        return "CAMBIAR_PRECIO_Y_PROVEEDOR"

    if tiene_precio:
        return "CAMBIAR_PRECIO"

    if tiene_proveedor:
        return "CAMBIAR_PROVEEDOR"

    if (
        "historial" in orden
        or "compras" in orden
        or "última compra" in orden
        or "ultima compra" in orden
        or "cuando compre" in orden
        or "cuándo compré" in orden
        or "cuando compré" in orden
    ):
        return "VER_HISTORIAL"

    if (
        "escandallo" in orden
        or "receta" in orden
        or "recetas" in orden
        or "donde se utiliza" in orden
        or "dónde se utiliza" in orden
        or "donde uso" in orden
        or "dónde uso" in orden
        or "platos llevan" in orden
        or "platos tiene" in orden
        or "en qué platos" in orden
        or "en que platos" in orden
    ):
        return "VER_ESCANDALLOS"

    return "NO_ENTENDIDO"


def detectar_precio(texto):
    texto = texto.replace(",", ".")
    numeros = re.findall(r"\d+(?:\.\d+)?", texto)

    if numeros:
        return numeros[-1]

    return None


def detectar_proveedor(texto):
    texto = texto.strip()
    texto_lower = texto.lower()

    frases = ["se lo compro a", "lo compro a", "compro a", "proveedor"]

    for frase in frases:
        if frase in texto_lower:
            partes = texto_lower.split(frase)
            if len(partes) > 1:
                proveedor = partes[1].strip()

                for corte in [" y ", ",", ".", ";"]:
                    if corte in proveedor:
                        proveedor = proveedor.split(corte)[0].strip()

                return proveedor.upper()

    return None


def confirmar(mensaje):
    respuesta = input(mensaje + " (sí/no): ").strip().lower()
    return respuesta in ["si", "sí", "s"]