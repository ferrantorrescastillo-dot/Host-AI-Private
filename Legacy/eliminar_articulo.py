from configuracion import ARCHIVO_EXCEL, HOJA_ARTICULOS
from utilidades import abrir_excel

excel = abrir_excel()
hoja = excel[HOJA_ARTICULOS]

articulo_buscado = input("¿Qué artículo quieres eliminar? ")

encontrado = False

for fila in range(2, hoja.max_row + 1):

    nombre_articulo = hoja.cell(row=fila, column=2).value

    if nombre_articulo is not None and articulo_buscado.lower() in str(nombre_articulo).lower():

        encontrado = True

        print("Artículo encontrado:", nombre_articulo)

        confirmar = input("¿Seguro que quieres eliminarlo? (S/N): ")

        if confirmar.lower() == "s":

            hoja.delete_rows(fila)

            excel.save(ARCHIVO_EXCEL)

            print("Artículo eliminado correctamente.")

        else:

            print("No se ha eliminado ningún artículo.")

        break

if encontrado == False:
    print("No he encontrado ese artículo.")