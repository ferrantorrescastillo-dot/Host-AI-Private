from pathlib import Path


TIPO_FACTURA = "FACTURA"
TIPO_ALBARAN = "ALBARAN"
TIPO_RECETA = "RECETA"
TIPO_FICHA_TECNICA = "FICHA_TECNICA"
TIPO_ESCANDALLO = "ESCANDALLO"
TIPO_MENU = "MENU"
TIPO_DESCONOCIDO = "DESCONOCIDO"


def detectar_tipo_archivo(ruta_archivo):
    ruta = Path(ruta_archivo)
    extension = ruta.suffix.lower()

    if extension in [".xlsx", ".xls"]:
        return "EXCEL"

    if extension == ".pdf":
        return "PDF"

    if extension in [".docx", ".doc"]:
        return "WORD"

    if extension in [".jpg", ".jpeg", ".png", ".webp"]:
        return "IMAGEN"

    if extension in [".txt"]:
        return "TEXTO"

    return "DESCONOCIDO"


def detectar_tipo_contenido(texto):
    texto = texto.lower()

    if "factura" in texto:
        return TIPO_FACTURA

    if "albarán" in texto or "albaran" in texto:
        return TIPO_ALBARAN

    if "ingredientes" in texto and "elaboración" in texto:
        return TIPO_RECETA

    if "escandallo" in texto:
        return TIPO_ESCANDALLO

    if "menú" in texto or "menu" in texto:
        return TIPO_MENU

    return TIPO_DESCONOCIDO


def crear_resultado_ingesta(
    origen,
    tipo_archivo,
    tipo_contenido,
    datos,
    confianza=0.0,
    requiere_revision=True,
):
    return {
        "origen": origen,
        "tipo_archivo": tipo_archivo,
        "tipo_contenido": tipo_contenido,
        "confianza": confianza,
        "requiere_revision": requiere_revision,
        "datos": datos,
    }


def procesar_archivo(ruta_archivo):
    tipo_archivo = detectar_tipo_archivo(ruta_archivo)

    return crear_resultado_ingesta(
        origen=str(ruta_archivo),
        tipo_archivo=tipo_archivo,
        tipo_contenido=TIPO_DESCONOCIDO,
        datos={},
        confianza=0.0,
        requiere_revision=True,
    )


def procesar_texto(texto, origen="texto_manual"):
    tipo_contenido = detectar_tipo_contenido(texto)

    return crear_resultado_ingesta(
        origen=origen,
        tipo_archivo="TEXTO",
        tipo_contenido=tipo_contenido,
        datos={
            "texto_original": texto
        },
        confianza=0.3,
        requiere_revision=True,
    )


def mostrar_resultado_ingesta(resultado):
    print("\n========== RESULTADO DE INGESTA ==========\n")
    print(f"Origen        : {resultado['origen']}")
    print(f"Tipo archivo  : {resultado['tipo_archivo']}")
    print(f"Tipo contenido: {resultado['tipo_contenido']}")
    print(f"Confianza     : {resultado['confianza']}")
    print(f"Revisión      : {resultado['requiere_revision']}")
    print("\nDatos:")
    print(resultado["datos"])
    print()