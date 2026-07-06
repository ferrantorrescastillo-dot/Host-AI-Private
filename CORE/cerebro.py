from acciones import (
    BUSCAR_ARTICULO,
    CONSULTAR_PRECIO,
    CONSULTAR_PROVEEDOR,
    NO_ENTENDIDO,
)


def entender_pregunta(texto):
    texto = texto.lower().strip()

    if "cuántos artículos" in texto or "cuantos articulos" in texto:
        return "TOTAL_ARTICULOS"

    if "cuántos proveedores" in texto or "cuantos proveedores" in texto:
        return "TOTAL_PROVEEDORES"

    if texto == "proveedores":
        return "LISTAR_PROVEEDORES"

    if texto.startswith("busca ") or texto.startswith("búscame ") or texto.startswith("buscame "):
        return BUSCAR_ARTICULO

    if texto.startswith("precio ") or "cuánto cuesta" in texto or "cuanto cuesta" in texto:
        return CONSULTAR_PRECIO

    if texto.startswith("proveedor ") or "quién vende" in texto or "quien vende" in texto:
        return CONSULTAR_PROVEEDOR

    return NO_ENTENDIDO


def extraer_consulta_busqueda(texto):
    texto = texto.lower().strip()

    palabras_a_quitar = [
        "búscame",
        "buscame",
        "busca",
        "buscar",
        "precio",
        "proveedor",
        "cuánto cuesta",
        "cuanto cuesta",
        "quién vende",
        "quien vende",
        "de",
        "el",
        "la",
        "los",
        "las",
        "un",
        "una",
    ]

    consulta = texto

    for palabra in palabras_a_quitar:
        consulta = consulta.replace(palabra, " ")

    consulta = " ".join(consulta.split())

    return consulta