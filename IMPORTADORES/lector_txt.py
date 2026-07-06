from pathlib import Path


def leer_txt(ruta_archivo):
    ruta = Path(ruta_archivo)
    if not ruta.exists():
        raise FileNotFoundError(f"No existe el archivo: {ruta}")
    return ruta.read_text(encoding="utf-8", errors="ignore")
