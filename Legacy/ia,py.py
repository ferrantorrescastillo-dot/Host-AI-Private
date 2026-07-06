def entender_usuario(orden):
    orden = orden.strip().lower()

    if orden in ["salir", "volver", "0", "nada"]:
        return "SALIR"

    if "precio" in orden or "subido" in orden or "bajado" in orden:
        return "CAMBIAR_PRECIO"

    if "proveedor" in orden:
        return "CAMBIAR_PROVEEDOR"

    if "historial" in orden or "compras" in orden:
        return "VER_HISTORIAL"

    if "escandallo" in orden or "receta" in orden:
        return "VER_ESCANDALLOS"

    return "NO_ENTENDIDO"


def confirmar(mensaje):
    respuesta = input(mensaje + " (sí/no): ").strip().lower()

    if respuesta in ["si", "sí", "s"]:
        return True
