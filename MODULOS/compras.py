from SERVICIOS.compras_servicio import (
    listar_stock_bajo,
    generar_pedido_stock_minimo,
    listar_pedidos,
    obtener_lineas_pedido,
    obtener_ultimo_pedido,
    marcar_pedido_enviado,
    exportar_pedido_txt,
    buscar_articulos_para_configurar,
    listar_articulos_sin_stock_minimo,
    actualizar_configuracion_stock,
    obtener_articulo,
    generar_pedido_articulos_seleccionados,
)


# ============================================================
# HOST AI - MÓDULO COMPRAS / PEDIDOS
# Sprint 4.6
# ------------------------------------------------------------
# Menú de usuario para configurar stock mínimo/óptimo y generar
# pedidos inteligentes.
# ============================================================


def euros(valor):
    try:
        return f"{float(valor or 0):.2f} €"
    except Exception:
        return "0.00 €"


def numero_input(texto, permitir_vacio=True):
    valor = input(texto).strip().replace(",", ".")
    if permitir_vacio and valor == "":
        return None
    try:
        return float(valor)
    except Exception:
        print("Valor no válido. Se dejará sin cambiar.")
        return None


def ver_stock_bajo(restaurante_id=1):
    print("\n========== PRODUCTOS BAJO STOCK MÍNIMO ==========")
    articulos = listar_stock_bajo(restaurante_id)

    if not articulos:
        print("\nNo hay artículos por debajo del stock mínimo.\n")
        print("Si todavía no has configurado mínimos, entra en:")
        print("15. Compras / Pedidos → 7. Ver artículos sin stock mínimo")
        print("15. Compras / Pedidos → 6. Configurar stock mínimo")
        input("\nPulsa ENTER para volver...")
        return

    total = 0
    for a in articulos:
        total += a["importe_estimado"] or 0
        objetivo = a["stock_optimo"] or a["stock_minimo"]
        print(f"\n• {a['nombre']}")
        print(f"  Stock actual       : {a['stock_actual']} {a['unidad']}")
        print(f"  Stock mínimo       : {a['stock_minimo']} {a['unidad']}")
        print(f"  Stock óptimo       : {objetivo} {a['unidad']}")
        print(f"  Compra sugerida    : {a['cantidad_sugerida']} {a['unidad']}")
        if a["cantidad_compra_habitual"]:
            print(f"  Compra habitual    : {a['cantidad_compra_habitual']} {a['unidad_compra']}")
        print(f"  Proveedor          : {a['proveedor']}")
        print(f"  Precio est.        : {euros(a['precio_estimado'])}")
        print(f"  Importe est.       : {euros(a['importe_estimado'])}")

    print("\n--------------------------------------")
    print(f"Total estimado de reposición: {euros(total)}")
    input("\nPulsa ENTER para volver...")


def crear_pedido_stock_minimo(restaurante_id=1):
    print("\n========== GENERAR PEDIDO POR STOCK MÍNIMO ==========")
    articulos = listar_stock_bajo(restaurante_id)

    if not articulos:
        print("\nNo hay artículos por debajo del stock mínimo. No hace falta generar pedido.\n")
        print("Consejo: configura stock mínimo y stock óptimo primero.")
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


def _imprimir_articulo_configuracion(a):
    unidad = a["unidad_stock"] or a["unidad"] or "ud"
    print(f"{a['id']}. {a['nombre']}")
    print(f"   Stock actual : {a['stock_actual'] or 0} {unidad}")
    print(f"   Mínimo       : {a['stock_minimo'] or 0} {unidad}")
    print(f"   Óptimo       : {a['stock_optimo'] or 0} {unitad if False else unidad}")
    print(f"   Compra hab.  : {a['cantidad_compra_habitual'] or 0} {a['unidad_compra'] or unidad}")


def configurar_stock_minimo(restaurante_id=1):
    print("\n========== CONFIGURAR STOCK MÍNIMO ==========")
    busqueda = input("Buscar artículo: ").strip()
    articulos = buscar_articulos_para_configurar(restaurante_id, busqueda, limite=30)

    if not articulos:
        print("\nNo he encontrado artículos.\n")
        input("Pulsa ENTER para volver...")
        return

    print("\nArtículos encontrados:\n")
    for a in articulos:
        _imprimir_articulo_configuracion(a)
        print()

    opcion = input("ID del artículo a configurar (0 para volver): ").strip()
    if opcion == "0" or opcion == "":
        return
    if not opcion.isdigit():
        print("\nOpción incorrecta.")
        return

    articulo_id = int(opcion)
    articulo = obtener_articulo(articulo_id)
    if articulo is None:
        print("\nArtículo no encontrado.")
        return

    print(f"\nConfigurando: {articulo['nombre']}")
    print("Deja vacío un campo si no quieres cambiarlo.\n")

    stock_minimo = numero_input("Stock mínimo: ")
    stock_optimo = numero_input("Stock óptimo: ")
    cantidad_compra = numero_input("Cantidad habitual de compra: ")
    unidad_stock = input("Unidad de stock (kg, L, ud...) [vacío = no cambiar]: ").strip()
    unidad_compra = input("Unidad de compra (caja, saco, botella...) [vacío = no cambiar]: ").strip()

    ok = actualizar_configuracion_stock(
        articulo_id,
        stock_minimo=stock_minimo,
        stock_optimo=stock_optimo,
        cantidad_compra_habitual=cantidad_compra,
        unidad_stock=unidad_stock,
        unidad_compra=unidad_compra,
    )

    if ok:
        print("\n✅ Configuración de stock guardada.\n")
    else:
        print("\nNo se ha podido guardar.\n")

    input("Pulsa ENTER para volver...")


def ver_articulos_sin_stock_minimo(restaurante_id=1):
    print("\n========== ARTÍCULOS SIN STOCK MÍNIMO ==========")
    articulos = listar_articulos_sin_stock_minimo(restaurante_id, limite=120)

    if not articulos:
        print("\nTodos los artículos listados tienen stock mínimo configurado.\n")
        input("Pulsa ENTER para volver...")
        return

    print(f"\nMostrando {len(articulos)} artículos sin mínimo configurado:\n")
    for a in articulos:
        unidad = a["unidad_stock"] or a["unidad"] or "ud"
        print(f"{a['id']}. {a['nombre']} | Stock actual: {a['stock_actual'] or 0} {unidad}")

    print("\nConsejo: configura primero los artículos críticos: nata, huevos, harina, mantequilla, carnes, pescados, etc.")
    input("\nPulsa ENTER para volver...")


def generar_pedido_manual_prueba(restaurante_id=1):
    print("\n========== PEDIDO MANUAL / PRUEBA ==========")
    print("Busca artículos y escribe los IDs separados por coma.")
    busqueda = input("Buscar artículo: ").strip()
    articulos = buscar_articulos_para_configurar(restaurante_id, busqueda, limite=40)

    if not articulos:
        print("\nNo he encontrado artículos.\n")
        input("Pulsa ENTER para volver...")
        return

    print()
    for a in articulos:
        _imprimir_articulo_configuracion(a)
        print()

    texto_ids = input("IDs para añadir al pedido (ej. 12,18,25): ").strip()
    if not texto_ids:
        print("\nPedido cancelado.\n")
        return

    ids = []
    for parte in texto_ids.split(","):
        parte = parte.strip()
        if parte.isdigit():
            ids.append(int(parte))

    if not ids:
        print("\nNo has indicado IDs válidos.\n")
        return

    pedido_id, lineas = generar_pedido_articulos_seleccionados(restaurante_id, ids)
    if pedido_id is None:
        print("\nNo se ha podido generar el pedido.\n")
        return

    print(f"\n✅ Pedido manual creado. ID: {pedido_id}")
    print(f"Líneas añadidas: {len(lineas)}")
    print("\nPuedes verlo en: 15 → 3. Ver pedidos generados")
    input("\nPulsa ENTER para volver...")


def menu_compras(restaurante_id=1):
    while True:
        print("\n========== COMPRAS / PEDIDOS ==========")
        print("1. Ver productos bajo stock mínimo")
        print("2. Generar pedido por stock mínimo")
        print("3. Ver pedidos generados")
        print("4. Ver último pedido")
        print("5. Exportar último pedido a TXT")
        print("6. Configurar stock mínimo / óptimo")
        print("7. Ver artículos sin stock mínimo")
        print("8. Generar pedido manual / prueba")
        print("9. Marcar último pedido como enviado")
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
            configurar_stock_minimo(restaurante_id)
        elif opcion == "7":
            ver_articulos_sin_stock_minimo(restaurante_id)
        elif opcion == "8":
            generar_pedido_manual_prueba(restaurante_id)
        elif opcion == "9":
            marcar_ultimo_pedido_enviado(restaurante_id)
        elif opcion == "0":
            break
        else:
            print("\n⚠️ Opción no válida.")
