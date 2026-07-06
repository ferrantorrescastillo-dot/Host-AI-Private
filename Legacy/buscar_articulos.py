from configuracion import HOJA_ARTICULOS
from utilidades import abrir_excel

excel = abrir_excel()
hoja = excel[HOJA_ARTICULOS]

buscar = input("¿Qué quieres buscar? ")

resultados = []

for fila in range(2, hoja.max_row + 1):

    nombre = hoja.cell(row=fila, column=2).value
    precio = hoja.cell(row=fila, column=6).value

    ocultar = False

    for columna in range(1, hoja.max_column + 1):

        valor = hoja.cell(row=fila, column=columna).value

        if valor is not None:
            texto = str(valor).upper()
            texto = texto.replace(".", "")
            texto = texto.replace(" ", "")

            if "MP" in texto or "AP" in texto:
                ocultar = True
                break

    if ocultar:
        continue

    if nombre is not None and buscar.lower() in str(nombre).lower():
        resultados.append((nombre, precio))

if len(resultados) == 0:
    print("No se ha encontrado ningún artículo.")
else:
    print("Artículos encontrados:")
    print("----------------------------")

    numero = 1

    for nombre, precio in resultados:
        print(f"{numero}. {nombre} - {precio} €")
        numero = numero + 1

    print("----------------------------")
    print("Se han encontrado", len(resultados), "artículos.")