from SERVICIOS.compras_servicio import (
    listar_stock_bajo,
    generar_pedido_stock_minimo,
    listar_pedidos,
    obtener_lineas_pedido,
    obtener_ultimo_pedido,
    marcar_pedido_enviado,
    exportar_pedido_txt,
)


def euros(valor):
    try:
        return f"{float(valor or 0):.2f} €"
    except Exception:
        return "0.00 €"


def ver_stock_bajo(restaurante_id=1):
    print("\n========== PRODUCTOS BAJO STOCK MÍNIMO ==========")
    articulos = listar_stock_bajo(restaurante_id)

    if not articulos:
        print("\nNo hay artículos por debajo del stock mínimo.\n")
        input("Pulsa ENTER para volver...")
        return

    total = 0
    for a in articulos:
        total += a["importe_estimado"] or 0
        print(f"\n• {a['nombre']}")
        print(f"  Stock actual : {a['stock_actual']} {a['unidad']}")
        print(f"  Stock mínimo : {a['stock_minimo']} {a['unidad']}")
        print(f"  Comprar      : {a['cantidad_faltante']} {a['unidad']}")
        print(f"  Proveedor    : {a['proveedor']}")
        print(f"  Precio est.  : {euros(a['precio_estimado'])}")
        print(f"  Importe est. : {euros(a['importe_estimado'])}")

    print("\n--------------------------------------")
    print(f"Total estimado de reposición: {euros(total)}")
    input("\nPulsa ENTER para volver...")


def crear_pedido_stock_minimo(restaurante_id=1):
    print("\n========== GENERAR PEDIDO POR STOCK MÍNIMO ==========")
    articulos = listar_stock_bajo(restaurante_id)

    if not articulos:
        print("\nNo hay artículos por debajo del stock mínimo. No hace falta generar pedido.\n")
        input("Pulsa ENTER para volver...")
        return

    print(f"\nHost AI ha detectado {len(articulos)} artículos por debajo del stock mínimo.")
    total = sum(a["importe_estimado"] or 0 for a in articulos)
    print(f"Coste estimado del pedido: {euros(total)}")

    confirmar = input("\n¿Crear pedido sugerido? (s/n): ").strip().lower()
    if confirmar != "s":
        print("\nPedido cancelado.\n")
        return

    pedido_id, _ = generar_pedido_stock_minimo(restaurante_id)
    print(f"\n✅ Pedido sugerido creado correctamente. ID: {pedido_id}\n")
    input("Pulsa ENTER para volver...")


def _mostrar_detalle_pedido(pedido_id):
    lineas = obtener_lineas_pedido(pedido_id)
    if not lineas:
        print("\nEl pedido no tiene líneas.\n")
        return

    proveedor_actual = None
    total = 0
    for linea in lineas:
        proveedor = linea["proveedor"] or "Sin proveedor"
        if proveedor != proveedor_actual:
            proveedor_actual = proveedor
            print(f"\n🏢 {proveedor_actual}")
            print("--------------------------------------")

        total += linea["importe_estimado"] or 0
        print(f"• {linea['nombre_articulo']}")
        print(f"  Cantidad : {linea['cantidad_sugerida']} {linea['unidad']}")
        print(f"  Precio   : {euros(linea['precio_estimado'])}")
        print(f"  Importe  : {euros(linea['importe_estimado'])}")
        print(f"  Motivo   : {linea['motivo']}")

    print("\n--------------------------------------")
    print(f"Total estimado: {euros(total)}")


def ver_pedidos(restaurante_id=1):
    print("\n========== PEDIDOS DE COMPRA ==========")
    pedidos = listar_pedidos(restaurante_id)

    if not pedidos:
        print("\nNo hay pedidos generados todavía.\n")
        input("Pulsa ENTER para volver...")
        return

    for p in pedidos:
        print(f"\n{p['id']}. {p['nombre']}")
        print(f"   Estado        : {p['estado']}")
        print(f"   Origen        : {p['origen']}")
        print(f"   Líneas        : {p['total_lineas']}")
        print(f"   Total estimado: {euros(p['total_estimado'])}")
        print(f"   Fecha         : {p['fecha_creacion']}")

    opcion = input("\nID de pedido para ver detalle (0 para volver): ").strip()
    if opcion == "0" or opcion == "":
        return
    if not opcion.isdigit():
        print("\nOpción incorrecta.")
        return

    print("\n========== DETALLE PEDIDO ==========")
    _mostrar_detalle_pedido(int(opcion))
    input("\nPulsa ENTER para volver...")


def ver_ultimo_pedido(restaurante_id=1):
    pedido = obtener_ultimo_pedido(restaurante_id)
    if pedido is None:
        print("\nNo hay pedidos todavía.\n")
        input("Pulsa ENTER para volver...")
        return

    print("\n========== ÚLTIMO PEDIDO ==========")
    print(f"ID     : {pedido['id']}")
    print(f"Nombre : {pedido['nombre']}")
    print(f"Estado : {pedido['estado']}")
    _mostrar_detalle_pedido(pedido["id"])
    input("\nPulsa ENTER para volver...")


def exportar_ultimo_pedido(restaurante_id=1):
    pedido = obtener_ultimo_pedido(restaurante_id)
    if pedido is None:
        print("\nNo hay pedidos para exportar.\n")
        input("Pulsa ENTER para volver...")
        return

    ruta = exportar_pedido_txt(pedido["id"])
    if ruta is None:
        print("\nNo se ha podido exportar el pedido.\n")
    else:
        print(f"\n✅ Pedido exportado correctamente:\n{ruta}\n")
    input("Pulsa ENTER para volver...")


def marcar_ultimo_pedido_enviado(restaurante_id=1):
    pedido = obtener_ultimo_pedido(restaurante_id)
    if pedido is None:
        print("\nNo hay pedidos para marcar como enviados.\n")
        input("Pulsa ENTER para volver...")
        return

    print(f"\nÚltimo pedido: {pedido['nombre']} (ID {pedido['id']})")
    confirmar = input("¿Marcar como enviado? (s/n): ").strip().lower()
    if confirmar == "s":
        marcar_pedido_enviado(pedido["id"])
        print("\n✅ Pedido marcado como enviado.\n")
    else:
        print("\nNo se ha modificado el pedido.\n")
    input("Pulsa ENTER para volver...")


def menu_compras(restaurante_id=1):
    while True:
        print("\n========== COMPRAS / PEDIDOS ==========")
        print("1. Ver productos bajo stock mínimo")
        print("2. Generar pedido por stock mínimo")
        print("3. Ver pedidos generados")
        print("4. Ver último pedido")
        print("5. Exportar último pedido a TXT")
        print("6. Marcar último pedido como enviado")
        print("0. Volver")

        opcion = input("\n¿Qué quieres hacer? ").strip()

        if opcion == "1":
            ver_stock_bajo(restaurante_id)
        elif opcion == "2":
            crear_pedido_stock_minimo(restaurante_id)
        elif opcion == "3":
            ver_pedidos(restaurante_id)
        elif opcion == "4":
            ver_ultimo_pedido(restaurante_id)
        elif opcion == "5":
            exportar_ultimo_pedido(restaurante_id)
        elif opcion == "6":
            marcar_ultimo_pedido_enviado(restaurante_id)
        elif opcion == "0":
            break
        else:
            print("\n⚠️ Opción no válida.")
