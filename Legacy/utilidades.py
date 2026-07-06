import openpyxl
from configuracion import ARCHIVO_EXCEL


def abrir_excel():
    excel = openpyxl.load_workbook(ARCHIVO_EXCEL)
    return excel