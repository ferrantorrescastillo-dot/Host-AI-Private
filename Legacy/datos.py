import pandas as pd
from configuracion import ARCHIVO_EXCEL, HOJA_ARTICULOS


def cargar_articulos():
    return pd.read_excel(ARCHIVO_EXCEL, sheet_name=HOJA_ARTICULOS, header=2)


def guardar_articulos(df):
    with pd.ExcelWriter(
        ARCHIVO_EXCEL,
        engine="openpyxl",
        mode="a",
        if_sheet_exists="replace"
    ) as writer:
        df.to_excel(writer, sheet_name=HOJA_ARTICULOS, index=False)