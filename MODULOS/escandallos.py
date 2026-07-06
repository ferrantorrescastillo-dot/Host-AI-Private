import pandas as pd
from configuracion import ARCHIVO_EXCEL, HOJA_ARTICULOS, HOJA_COMPRAS


def buscar_escandallos_por_articulo(nombre_articulo):

    recetas = []

    excel = pd.ExcelFile(ARCHIVO_EXCEL)

    for hoja in excel.sheet_names:

        if hoja in [HOJA_ARTICULOS, HOJA_COMPRAS]:
            continue

        df = pd.read_excel(
            ARCHIVO_EXCEL,
            sheet_name=hoja,
            header=None
        )

        encontrado = False

        for _, fila in df.iterrows():

            texto = " ".join(
                str(valor)
                for valor in fila
                if str(valor).lower() != "nan"
            )

            if nombre_articulo.lower().replace(".", "") in texto.lower().replace(".", ""):
                encontrado = True
                break

        if encontrado:
            recetas.append(hoja)

    return sorted(recetas)