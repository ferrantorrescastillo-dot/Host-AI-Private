from pathlib import Path

# Carpeta raíz del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Excel principal
ARCHIVO_EXCEL = BASE_DIR / "EXCEL" / "Escandallos Boronat_ACTUALIZADO.xlsx"

# Hojas
HOJA_ARTICULOS = "Listado de Artículos"
HOJA_COMPRAS = "Historial de Compras"