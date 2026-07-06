from SERVICIOS.stock_servicio import listar_stock, listar_movimientos_stock
from SERVICIOS.entradas_mercancia import (
    listar_entradas,
    ver_detalle_entrada,
    listar_incidencias,
)


def ver_stock_articulos(restaurante_id=1):
    print("\n========== STOCK DE ARTÍCULOS ==========" )
    filas = listar_stock(restaurante_id, limite=100)
    if not filas:
        print("No hay artículos.\n")
        input("Pulsa ENTER para volver...")
        return

    for fila in filas:
        stock = fila["stock_actual"] or 0
        unidad = fila["unidad_stock"] or (fila["unidad"] if "unidad" in fila.keys() else None) or "ud"
        minimo = fila["stock_minimo"] or 0
        alerta = " ⚠ BAJO" if minimo and stock <= minimo else ""
        print(f"• {fila['nombre']} → {stock} {unidad}{alerta}")

    print()
    input("Pulsa ENTER para volver...")


def ver_movimientos_stock(restaurante_id=1):
    print("\n========== ÚLTIMOS MOVIMIENTOS DE STOCK ==========" )
    movimientos = listar_movimientos_stock(restaurante_id, limite=40)
    if not movimientos:
        print("No hay movimientos de stock registrados.\n")
        input("Pulsa ENTER para volver...")
        return

    for mov in movimientos:
        print(f"• {mov['fecha']} | {mov['tipo_movimiento']} | {mov['articulo_nombre']}")
        print(f"  Cantidad: {mov['cantidad']} {mov['unidad']}")
        print(f"  Stock: {mov['stock_anterior']} → {mov['stock_nuevo']}")
        if mov["motivo"]:
            print(f"  Motivo: {mov['motivo']}")
        print()

    input("Pulsa ENTER para volver...")


def ver_entradas_mercancia(restaurante_id=1):
    print("\n========== ENTRADAS DE MERCANCÍA ==========" )
    entradas = listar_entradas(restaurante_id, limite=30)
    if not entradas:
        print("No hay entradas registradas.\n")
        input("Pulsa ENTER para volver...")
        return

    for entrada in entradas:
        print(f"{entrada['id']}. {entrada['proveedor']} | {entrada['fecha_documento']} | Doc {entrada['documento_id']} | {entrada['estado']}")

    opcion = input("\nVer detalle de entrada (0 para volver): ").strip()
    if opcion == "0" or not opcion:
        return
    if not opcion.isdigit():
        print("Opción incorrecta.")
        return

    entrada, lineas = ver_detalle_entrada(int(opcion))
    if entrada is None:
        print("Entrada no encontrada.")
        return

    print("\n========== DETALLE ENTRADA ==========" )
    print(f"Proveedor: {entrada['proveedor']}")
    print(f"Fecha    : {entrada['fecha_documento']}")
    print(f"Estado   : {entrada['estado']}\n")

    for linea in lineas:
        articulo = linea["articulo_nombre"] or "SIN ARTÍCULO"
        print(f"• {linea['nombre_detectado']}")
        print(f"  Artículo : {articulo}")
        print(f"  Cantidad : {linea['cantidad_recibida']} {linea['unidad']}")
        print(f"  Estado   : {linea['estado']}")
        if linea["observaciones"]:
            print(f"  Obs      : {linea['observaciones']}")
        print()

    input("Pulsa ENTER para volver...")


def ver_incidencias_recepcion(restaurante_id=1):
    print("\n========== INCIDENCIAS DE RECEPCIÓN ==========" )
    incidencias = listar_incidencias(restaurante_id, limite=40)
    if not incidencias:
        print("No hay incidencias registradas.\n")
        input("Pulsa ENTER para volver...")
        return

    for inc in incidencias:
        print(f"{inc['id']}. {inc['tipo']} | {inc['estado']}")
        print(f"   {inc['descripcion']}")
        if inc["cantidad_afectada"]:
            print(f"   Cantidad afectada: {inc['cantidad_afectada']} {inc['unidad']}")
        print()

    input("Pulsa ENTER para volver...")


def menu_stock(restaurante_id=1):
    while True:
        print("\n========== STOCK / MERCANCÍA ==========" )
        print("1. Ver stock de artículos")
        print("2. Ver movimientos de stock")
        print("3. Ver entradas de mercancía")
        print("4. Ver incidencias de recepción")
        print("0. Volver")

        opcion = input("\n¿Qué quieres hacer? ").strip()

        if opcion == "1":
            ver_stock_articulos(restaurante_id)
        elif opcion == "2":
            ver_movimientos_stock(restaurante_id)
        elif opcion == "3":
            ver_entradas_mercancia(restaurante_id)
        elif opcion == "4":
            ver_incidencias_recepcion(restaurante_id)
        elif opcion == "0":
            break
        else:
            print("\n⚠️ Opción no válida.")
