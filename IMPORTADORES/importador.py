from pathlib import Path
from .lector_pdf import leer_pdf
from .lector_word import leer_word
from .lector_txt import leer_txt
from .parser_documento import parsear_documento
from .guardar_documento import guardar_documento_importado


def leer_archivo(ruta_archivo):
    ruta = Path(ruta_archivo)
    extension = ruta.suffix.lower()

    if extension == ".pdf":
        return leer_pdf(ruta)
    if extension in [".docx", ".doc"]:
        return leer_word(ruta)
    if extension in [".txt"]:
        return leer_txt(ruta)

    raise ValueError(f"Tipo de archivo no soportado todavía: {extension}")


def importar_documento_desde_archivo(ruta_archivo, restaurante_id=1, guardar=True):
    texto = leer_archivo(ruta_archivo)
    documento = parsear_documento(texto, ruta_archivo)
    documento_id = None
    if guardar:
        documento_id = guardar_documento_importado(documento, restaurante_id)
    return documento_id, documento
