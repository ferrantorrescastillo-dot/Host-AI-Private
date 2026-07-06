from datetime import datetime
from configuracion import ARCHIVO_EXCEL, HOJA_ARTICULOS, HOJA_COMPRAS
from utilidades import abrir_excel

excel = abrir_excel()
hoja = excel[HOJA_ARTICULOS]
historial = excel[HOJA_COMPRAS]

articulo_buscado = input("¿Qué artículo quieres buscar? ")

encontrado = False

for fila in range(1, hoja.max_row + 1):
    nombre_articulo = hoja.cell(row=fila, column=2).value

    if nombre_articulo is not None and articulo_buscado.lower() in str(nombre_articulo).lower():
        encontrado = True

        precio_actual = hoja.cell(row=fila, column=6).value
        proveedor_mp = hoja.cell(row=fila, column=4).value

        print("Artículo encontrado:", nombre_articulo)
        print("Precio actual:", precio_actual)

        print("¿Qué quieres cambiar?")
        print("1. Precio")
        print("2. Proveedor / MP")
        print("3. Grupo")
        print("4. Características")
        print("5. Formato")
        print("6. Unidad")
        print("7. Referencia")
        print("8. Marca")
        print("9. Notas")
        print("10. Nombre")
        opcion = input("Elige una opción: ")

        if opcion == "1":
            precio_nuevo = input("Nuevo precio: ")
            precio_nuevo_numero = float(precio_nuevo.replace(",", "."))
            hoja.cell(row=fila, column=6).value = precio_nuevo_numero

            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            nueva_fila_historial = historial.max_row + 1

            historial.cell(row=nueva_fila_historial, column=1).value = fecha
            historial.cell(row=nueva_fila_historial, column=2).value = nombre_articulo
            historial.cell(row=nueva_fila_historial, column=3).value = proveedor_mp
            historial.cell(row=nueva_fila_historial, column=4).value = precio_nuevo_numero
            historial.cell(row=nueva_fila_historial, column=8).value = f"Precio anterior: {precio_actual}"

            print("Precio actualizado y guardado en Historial de Compras.")

        elif opcion == "2":
            proveedor_mp_nuevo = input("Nuevo proveedor / MP: ")
            hoja.cell(row=fila, column=4).value = proveedor_mp_nuevo
            print("Proveedor / MP actualizado.")

        elif opcion == "3":
            grupo_nuevo = input("Nuevo grupo: ")
            hoja.cell(row=fila, column=3).value = grupo_nuevo
            print("Grupo actualizado.")

        elif opcion == "4":
            caracteristicas_nuevas = input("Nuevas características: ")
            hoja.cell(row=fila, column=5).value = caracteristicas_nuevas
            print("Características actualizadas.")

        elif opcion == "5":
            formato_nuevo = input("Nuevo formato: ")
            hoja.cell(row=fila, column=7).value = formato_nuevo
            print("Formato actualizado.")

        elif opcion == "6":
            unidad_nueva = input("Nueva unidad: ")
            hoja.cell(row=fila, column=8).value = unidad_nueva
            print("Unidad actualizada.")

        elif opcion == "7":
            referencia_nueva = input("Nueva referencia: ")
            hoja.cell(row=fila, column=9).value = referencia_nueva
            print("Referencia actualizada.")

        elif opcion == "8":
            marca_nueva = input("Nueva marca: ")
            hoja.cell(row=fila, column=10).value = marca_nueva
            print("Marca actualizada.")

        elif opcion == "9":
            notas_nuevas = input("Nuevas notas: ")
            hoja.cell(row=fila, column=11).value = notas_nuevas
            print("Notas actualizadas.")

        elif opcion == "10":
            nombre_nuevo = input("Nuevo nombre: ")
            hoja.cell(row=fila, column=2).value = nombre_nuevo
            print("Nombre actualizado.")

        excel.save(ARCHIVO_EXCEL)
        break

if encontrado == False:
    print("No he encontrado ese artículo.")