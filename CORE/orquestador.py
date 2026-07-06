from acciones import (
    BUSCAR_ARTICULO,
    CONSULTAR_PRECIO,
    CONSULTAR_PROVEEDOR,
    NO_ENTENDIDO,
)

from cerebro import extraer_consulta_busqueda
from busqueda import buscar_articulos


def ejecutar_accion(motor, accion, texto_usuario):
    consulta = extraer_consulta_busqueda(texto_usuario)

    if accion == BUSCAR_ARTICULO:
        return {
            "tipo_respuesta": "BUSQUEDA_ARTICULO",
            "datos": buscar_articulos(motor, consulta),
        }

    if accion == CONSULTAR_PRECIO:
        return {
            "tipo_respuesta": "CONSULTA_PRECIO",
            "datos": buscar_articulos(motor, consulta),
        }

    if accion == CONSULTAR_PROVEEDOR:
        return {
            "tipo_respuesta": "CONSULTA_PROVEEDOR",
            "datos": buscar_articulos(motor, consulta),
        }

    return {
        "tipo_respuesta": NO_ENTENDIDO,
        "datos": None,
    }