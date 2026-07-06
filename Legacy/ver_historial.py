from configuracion import HOJA_COMPRAS
from utilidades import abrir_excel

excel = abrir_excel()
historial = excel[HOJA_COMPRAS]

articulo_buscado = input("¿De qué artículo quieres ver el historial? ")

encontrados = 0

for fila in range(2, historial.max_row + 1):

    fecha = historial.cell(row=fila, column=1).value
    articulo = historial.cell(row=fila, column=2).value
    proveedor = historial.cell(row=fila, column=3).value
    precio = historial.cell(row=fila, column=4).value
    cantidad = historial.cell(row=fila, column=5).value
    importe = historial.cell(row=fila, column=6).value
    factura = historial.cell(row=fila, column=7).value
    observaciones = historial.cell(row=fila, column=8).value

    if articulo is not None and articulo_buscado.lower() in str(articulo).lower():

        encontrados += 1

        print("----------------------------------------")
        print("Fecha:", fecha)
        print("Artículo:", articulo)
        print("Proveedor:", proveedor)
        print("Precio:", precio)
        print("Cantidad:", cantidad)
        print("Importe:", importe)
        print("Factura:", factura)
        print("Observaciones:", observaciones)

if encontrados == 0:
    print("No se ha encontrado historial de ese artículo.")
else:
    print("----------------------------------------")
    print("Total de registros:", encontrados)