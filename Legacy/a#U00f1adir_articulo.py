from configuracion import ARCHIVO_EXCEL, HOJA_ARTICULOS
from utilidades import abrir_excel

excel = abrir_excel()
hoja = excel[HOJA_ARTICULOS]

print("=== AÑADIR NUEVO ARTÍCULO ===")

nombre = input("Nombre: ")
grupo = input("Grupo: ")
proveedor_mp = input("Proveedor / MP: ")
caracteristicas = input("Características: ")
precio = input("Precio: ")
formato = input("Formato: ")
unidad = input("Unidad: ")
referencia = input("Referencia: ")
marca = input("Marca: ")
notas = input("Notas: ")

nueva_fila = 2

while hoja.cell(row=nueva_fila, column=2).value is not None:
    nueva_fila = nueva_fila + 1

hoja.cell(row=nueva_fila, column=2).value = nombre
hoja.cell(row=nueva_fila, column=3).value = grupo
hoja.cell(row=nueva_fila, column=4).value = proveedor_mp
hoja.cell(row=nueva_fila, column=5).value = caracteristicas
hoja.cell(row=nueva_fila, column=6).value = float(precio.replace(",", "."))
hoja.cell(row=nueva_fila, column=7).value = formato
hoja.cell(row=nueva_fila, column=8).value = unidad
hoja.cell(row=nueva_fila, column=9).value = referencia
hoja.cell(row=nueva_fila, column=10).value = marca
hoja.cell(row=nueva_fila, column=11).value = notas

excel.save(ARCHIVO_EXCEL)

print("Artículo añadido correctamente.")