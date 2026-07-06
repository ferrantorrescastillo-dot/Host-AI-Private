from pathlib import Path


def leer_pdf(ruta_archivo):
    ruta = Path(ruta_archivo)
    if not ruta.exists():
        raise FileNotFoundError(f"No existe el archivo: {ruta}")

    textos = []

    try:
        import pdfplumber
        with pdfplumber.open(str(ruta)) as pdf:
            for pagina in pdf.pages:
                texto = pagina.extract_text() or ""
                if texto.strip():
                    textos.append(texto)
    except Exception:
        textos = []

    if not textos:
        try:
            from PyPDF2 import PdfReader
            reader = PdfReader(str(ruta))
            for pagina in reader.pages:
                texto = pagina.extract_text() or ""
                if texto.strip():
                    textos.append(texto)
        except Exception as exc:
            raise RuntimeError(
                "No he podido leer el PDF. Instala pdfplumber y PyPDF2: "
                "py -m pip install pdfplumber PyPDF2"
            ) from exc

    return "\n".join(textos)
