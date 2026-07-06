from SERVICIOS.costes_servicio import (
    listar_costes_menus,
    listar_costes_eventos,
    listar_cambios_precio,
    listar_ultimos_precios_importados,
    listar_productos_mas_caros_documentos,
    recalcular_costes_menus,
)


def formato_euros(valor):
    if valor is None:
        return "-"
    try:
        return f"{float(valor):.2f} €"
    except Exception:
        return "-"


def formato_porcentaje(valor):
    if valor is None:
        return "-"
    try:
        return f"{float(valor):.1f}%"
    except Exception:
        return "-"


def ver_costes_menus(restaurante_id=1):
    print("\n========== COSTES DE MENÚS ==========")
    menus = listar_costes_menus(restaurante_id)

    if not menus:
        print("No hay menús para analizar.\n")
        input("Pulsa ENTER para volver...")
        return

    for menu in menus:
        if menu is None:
            continue
        print(f"\n• {menu['nombre']}")
        print(f"  Coste estimado por persona : {formato_euros(menu['coste_estimado'])}")
        print(f"  Precio venta               : {formato_euros(menu['precio_venta']) if menu['precio_venta'] else 'No definido'}")
        print(f"  Margen estimado            : {formato_euros(menu['margen_estimado']) if menu['margen_estimado'] is not None else 'No calculable'}")
        print(f"  Food cost                  : {formato_porcentaje(menu['food_cost']) if menu['food_cost'] is not None else 'No calculable'}")

    print("\nHost AI:")
    print("Estos costes son básicos: todavía usan los costes importados del menú. El siguiente salto será bajarlos hasta ingredientes reales.\n")
    input("Pulsa ENTER para volver...")


def ver_costes_eventos(restaurante_id=1):
    print("\n========== COSTES DE EVENTOS ==========")
    eventos = listar_costes_eventos(restaurante_id)

    if not eventos:
        print("No hay eventos para analizar.\n")
        input("Pulsa ENTER para volver...")
        return

    for evento in eventos:
        if evento is None:
            continue
        print(f"\n• {evento['nombre']} | {evento['fecha']} | {int(evento['personas']) if evento['personas'] else 0} pax")
        print(f"  Menú              : {evento['menu_nombre']}")
        print(f"  Coste/persona     : {formato_euros(evento['coste_persona'])}")
        print(f"  Coste total       : {formato_euros(evento['coste_total'])}")
        if evento['venta_total'] is not None:
            print(f"  Venta estimada    : {formato_euros(evento['venta_total'])}")
            print(f"  Margen estimado   : {formato_euros(evento['margen_total'])}")
            print(f"  Food cost         : {formato_porcentaje(evento['food_cost'])}")
        else:
            print("  Venta estimada    : No calculable: falta precio venta del menú")

    input("\nPulsa ENTER para volver...")


def ver_cambios_precio(restaurante_id=1):
    print("\n========== CAMBIOS DE PRECIO DETECTADOS ==========")
    cambios = listar_cambios_precio(restaurante_id)

    if not cambios:
        print("Todavía no hay suficientes precios históricos para comparar.\n")
        input("Pulsa ENTER para volver...")
        return

    for cambio in cambios:
        signo = "+" if cambio['diferencia'] > 0 else ""
        alerta = "⚠ SUBE" if cambio['diferencia'] > 0 else "✅ BAJA"
        print(f"\n{alerta} • {cambio['articulo']}")
        print(f"  Anterior : {formato_euros(cambio['precio_anterior'])}")
        print(f"  Nuevo    : {formato_euros(cambio['precio_nuevo'])}")
        print(f"  Cambio   : {signo}{formato_euros(cambio['diferencia'])} ({signo}{cambio['porcentaje']:.1f}%)")
        if cambio['proveedor']:
            print(f"  Proveedor: {cambio['proveedor']}")
        if cambio['fecha']:
            print(f"  Fecha    : {cambio['fecha']}")

    input("\nPulsa ENTER para volver...")


def ver_ultimos_precios(restaurante_id=1):
    print("\n========== ÚLTIMOS PRECIOS IMPORTADOS ==========")
    filas = listar_ultimos_precios_importados(restaurante_id)

    if not filas:
        print("No hay precios importados todavía.\n")
        input("Pulsa ENTER para volver...")
        return

    for fila in filas:
        proveedor = fila['proveedor_nombre'] or fila['proveedor_documento'] or "Proveedor no detectado"
        print(f"\n• {fila['articulo_nombre'] or 'SIN ARTÍCULO'}")
        print(f"  Precio   : {formato_euros(fila['precio'])}")
        print(f"  Cantidad : {fila['cantidad']} {fila['unidad']}")
        print(f"  Proveedor: {proveedor}")
        print(f"  Fecha    : {fila['fecha_documento'] or fila['fecha_registro']}")

    input("\nPulsa ENTER para volver...")


def ver_productos_caros(restaurante_id=1):
    print("\n========== PRODUCTOS MÁS CAROS DETECTADOS EN DOCUMENTOS ==========")
    filas = listar_productos_mas_caros_documentos(restaurante_id)

    if not filas:
        print("No hay productos de documentos para analizar.\n")
        input("Pulsa ENTER para volver...")
        return

    for fila in filas:
        print(f"\n• {fila['nombre_detectado']}")
        print(f"  Precio unidad: {formato_euros(fila['precio_unitario'])}")
        print(f"  Cantidad     : {fila['cantidad']} {fila['unidad']}")
        print(f"  Importe      : {formato_euros(fila['importe'])}")
        print(f"  Proveedor    : {fila['proveedor']}")
        print(f"  Fecha        : {fila['fecha_documento']}")

    input("\nPulsa ENTER para volver...")


def recalcular_menus(restaurante_id=1):
    print("\n========== RECALCULAR COSTES ==========")
    total = recalcular_costes_menus(restaurante_id)
    print(f"\n✅ Menús recalculados: {total}")
    print("\nHost AI:")
    print("He actualizado coste_total y food_cost de los menús con la información disponible actualmente.\n")
    input("Pulsa ENTER para volver...")


def menu_costes(restaurante_id=1):
    while True:
        print("\n========== COSTES / RENTABILIDAD ==========")
        print("1. Ver coste de menús")
        print("2. Ver coste de eventos")
        print("3. Ver cambios de precio detectados")
        print("4. Ver últimos precios importados")
        print("5. Ver productos más caros de documentos")
        print("6. Recalcular costes de menús")
        print("0. Volver")

        opcion = input("\n¿Qué quieres hacer? ").strip()

        if opcion == "1":
            ver_costes_menus(restaurante_id)
        elif opcion == "2":
            ver_costes_eventos(restaurante_id)
        elif opcion == "3":
            ver_cambios_precio(restaurante_id)
        elif opcion == "4":
            ver_ultimos_precios(restaurante_id)
        elif opcion == "5":
            ver_productos_caros(restaurante_id)
        elif opcion == "6":
            recalcular_menus(restaurante_id)
        elif opcion == "0":
            break
        else:
            print("\n⚠️ Opción no válida.")
