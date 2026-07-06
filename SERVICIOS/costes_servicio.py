from database import conectar


def numero(valor, defecto=0):
    try:
        if valor is None or valor == "":
            return defecto
        return float(valor)
    except Exception:
        return defecto


def obtener_coste_menu(menu_id):
    """Devuelve coste estimado por persona/ración para un menú.

    En esta versión usa la información ya importada en platos_menu.coste_racion.
    Más adelante este cálculo bajará hasta ingredientes reales.
    """
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id, nombre, precio_venta, coste_total, food_cost
        FROM menus
        WHERE id = ?
    """, (menu_id,))
    menu = cursor.fetchone()

    if menu is None:
        conexion.close()
        return None

    cursor.execute("""
        SELECT
            nombre,
            cantidad,
            precio_unitario,
            coste_racion
        FROM platos_menu
        WHERE menu_id = ?
        ORDER BY orden
    """, (menu_id,))
    platos = cursor.fetchall()

    coste_total = 0
    lineas = []

    for plato in platos:
        coste = numero(plato["coste_racion"], 0)
        coste_total += coste
        lineas.append({
            "nombre": plato["nombre"],
            "cantidad": plato["cantidad"],
            "coste_racion": coste,
        })

    precio_venta = numero(menu["precio_venta"], 0)
    margen = precio_venta - coste_total if precio_venta else None
    food_cost = (coste_total / precio_venta * 100) if precio_venta else None

    resultado = {
        "id": menu["id"],
        "nombre": menu["nombre"],
        "precio_venta": precio_venta,
        "coste_estimado": coste_total,
        "margen_estimado": margen,
        "food_cost": food_cost,
        "platos": lineas,
    }

    conexion.close()
    return resultado


def listar_costes_menus(restaurante_id=1):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id
        FROM menus
        WHERE restaurante_id = ?
        AND activo = 1
        ORDER BY nombre
    """, (restaurante_id,))
    ids = [fila["id"] for fila in cursor.fetchall()]
    conexion.close()

    return [obtener_coste_menu(menu_id) for menu_id in ids]


def recalcular_costes_menus(restaurante_id=1):
    conexion = conectar()
    cursor = conexion.cursor()

    menus = listar_costes_menus(restaurante_id)
    actualizados = 0

    for menu in menus:
        if menu is None:
            continue
        cursor.execute("""
            UPDATE menus
            SET coste_total = ?, food_cost = ?
            WHERE id = ?
        """, (
            menu["coste_estimado"],
            menu["food_cost"],
            menu["id"],
        ))
        actualizados += 1

    conexion.commit()
    conexion.close()
    return actualizados


def obtener_coste_evento(evento_id):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            eventos.id,
            eventos.nombre,
            eventos.fecha,
            eventos.numero_personas,
            eventos.menu_id,
            menus.nombre AS menu_nombre
        FROM eventos
        LEFT JOIN menus ON eventos.menu_id = menus.id
        WHERE eventos.id = ?
    """, (evento_id,))
    evento = cursor.fetchone()
    conexion.close()

    if evento is None:
        return None

    menu = obtener_coste_menu(evento["menu_id"])
    personas = numero(evento["numero_personas"], 0)
    coste_persona = menu["coste_estimado"] if menu else 0
    precio_persona = menu["precio_venta"] if menu else 0

    return {
        "id": evento["id"],
        "nombre": evento["nombre"],
        "fecha": evento["fecha"],
        "personas": personas,
        "menu_nombre": evento["menu_nombre"],
        "coste_persona": coste_persona,
        "coste_total": coste_persona * personas,
        "precio_persona": precio_persona,
        "venta_total": precio_persona * personas if precio_persona else None,
        "margen_total": (precio_persona - coste_persona) * personas if precio_persona else None,
        "food_cost": (coste_persona / precio_persona * 100) if precio_persona else None,
    }


def listar_costes_eventos(restaurante_id=1, limite=20):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id
        FROM eventos
        WHERE restaurante_id = ?
        ORDER BY fecha
        LIMIT ?
    """, (restaurante_id, limite))
    ids = [fila["id"] for fila in cursor.fetchall()]
    conexion.close()

    return [obtener_coste_evento(evento_id) for evento_id in ids]


def listar_ultimos_precios_importados(restaurante_id=1, limite=40):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            historial_precios.fecha_registro,
            historial_precios.fecha_documento,
            historial_precios.precio,
            historial_precios.cantidad,
            historial_precios.unidad,
            articulos.nombre AS articulo_nombre,
            proveedores.nombre AS proveedor_nombre,
            documentos_importados.proveedor AS proveedor_documento
        FROM historial_precios
        LEFT JOIN articulos ON historial_precios.articulo_id = articulos.id
        LEFT JOIN proveedores ON historial_precios.proveedor_id = proveedores.id
        LEFT JOIN documentos_importados ON historial_precios.documento_id = documentos_importados.id
        WHERE historial_precios.restaurante_id = ?
        ORDER BY historial_precios.id DESC
        LIMIT ?
    """, (restaurante_id, limite))

    filas = cursor.fetchall()
    conexion.close()
    return filas


def listar_cambios_precio(restaurante_id=1, limite=30):
    """Compara los dos últimos precios conocidos por artículo."""
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT DISTINCT articulo_id
        FROM historial_precios
        WHERE restaurante_id = ?
        AND articulo_id IS NOT NULL
    """, (restaurante_id,))
    articulos = [fila["articulo_id"] for fila in cursor.fetchall()]

    cambios = []
    for articulo_id in articulos:
        cursor.execute("""
            SELECT
                historial_precios.precio,
                historial_precios.fecha_documento,
                historial_precios.fecha_registro,
                articulos.nombre AS articulo_nombre,
                documentos_importados.proveedor AS proveedor_documento
            FROM historial_precios
            LEFT JOIN articulos ON historial_precios.articulo_id = articulos.id
            LEFT JOIN documentos_importados ON historial_precios.documento_id = documentos_importados.id
            WHERE historial_precios.restaurante_id = ?
            AND historial_precios.articulo_id = ?
            ORDER BY historial_precios.id DESC
            LIMIT 2
        """, (restaurante_id, articulo_id))
        precios = cursor.fetchall()

        if len(precios) < 2:
            continue

        nuevo = numero(precios[0]["precio"], 0)
        anterior = numero(precios[1]["precio"], 0)
        if anterior == 0 or nuevo == anterior:
            continue

        diferencia = nuevo - anterior
        porcentaje = diferencia / anterior * 100
        cambios.append({
            "articulo": precios[0]["articulo_nombre"],
            "proveedor": precios[0]["proveedor_documento"],
            "precio_anterior": anterior,
            "precio_nuevo": nuevo,
            "diferencia": diferencia,
            "porcentaje": porcentaje,
            "fecha": precios[0]["fecha_documento"] or precios[0]["fecha_registro"],
        })

    conexion.close()

    cambios.sort(key=lambda x: abs(x["porcentaje"]), reverse=True)
    return cambios[:limite]


def listar_productos_mas_caros_documentos(restaurante_id=1, limite=20):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            productos_documento.nombre_detectado,
            productos_documento.precio_unitario,
            productos_documento.cantidad,
            productos_documento.unidad,
            productos_documento.importe,
            documentos_importados.proveedor,
            documentos_importados.fecha_documento
        FROM productos_documento
        JOIN documentos_importados ON productos_documento.documento_id = documentos_importados.id
        WHERE documentos_importados.restaurante_id = ?
        AND productos_documento.precio_unitario IS NOT NULL
        ORDER BY productos_documento.precio_unitario DESC
        LIMIT ?
    """, (restaurante_id, limite))

    filas = cursor.fetchall()
    conexion.close()
    return filas
