from pathlib import Path


def leer_word(ruta_archivo):
    ruta = Path(ruta_archivo)
    if not ruta.exists():
        raise FileNotFoundError(f"No existe el archivo: {ruta}")

    try:
        from docx import Document
    except ImportError as exc:
        raise RuntimeError("Falta python-docx. Ejecuta: py -m pip install python-docx") from exc

    doc = Document(str(ruta))
    partes = []
    for p in doc.paragraphs:
        texto = p.text.strip()
        if texto:
            partes.append(texto)
    return "\n".join(partes)
