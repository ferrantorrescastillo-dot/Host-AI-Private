from datetime import datetime
from database import conectar


def numero(valor, defecto=0.0):
    try:
        if valor is None or valor == "":
            return defecto
        return float(valor)
    except Exception:
        return defecto


def asegurar_tablas_compras():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pedidos_compra (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            restaurante_id INTEGER,
            nombre TEXT NOT NULL,
            origen TEXT,
            estado TEXT DEFAULT 'borrador',
            observaciones TEXT,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lineas_pedido_compra (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pedido_id INTEGER,
            restaurante_id INTEGER,
            articulo_id INTEGER,
            proveedor_id INTEGER,
            nombre_articulo TEXT,
            proveedor TEXT,
            cantidad_sugerida REAL,
            unidad TEXT,
            precio_estimado REAL,
            importe_estimado REAL,
            motivo TEXT,
            estado TEXT DEFAULT 'pendiente',
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(pedido_id) REFERENCES pedidos_compra(id),
            FOREIGN KEY(articulo_id) REFERENCES articulos(id),
            FOREIGN KEY(proveedor_id) REFERENCES proveedores(id)
        )
    """)

    conexion.commit()
    conexion.close()


def _ultimo_precio(cursor, restaurante_id, articulo_id):
    """Devuelve proveedor/precio más reciente para un artículo."""
    cursor.execute("""
        SELECT
            historial_precios.precio,
            historial_precios.proveedor_id,
            proveedores.nombre AS proveedor
        FROM historial_precios
        LEFT JOIN proveedores ON historial_precios.proveedor_id = proveedores.id
        WHERE historial_precios.restaurante_id = ?
        AND historial_precios.articulo_id = ?
        AND historial_precios.precio IS NOT NULL
        ORDER BY historial_precios.id DESC
        LIMIT 1
    """, (restaurante_id, articulo_id))
    fila = cursor.fetchone()
    if fila:
        return fila["proveedor_id"], fila["proveedor"], numero(fila["precio"])

    cursor.execute("""
        SELECT
            articulo_proveedor.precio,
            articulo_proveedor.proveedor_id,
            proveedores.nombre AS proveedor
        FROM articulo_proveedor
        LEFT JOIN proveedores ON articulo_proveedor.proveedor_id = proveedores.id
        WHERE articulo_proveedor.articulo_id = ?
        ORDER BY articulo_proveedor.es_principal DESC, articulo_proveedor.id DESC
        LIMIT 1
    """, (articulo_id,))
    fila = cursor.fetchone()
    if fila:
        return fila["proveedor_id"], fila["proveedor"], numero(fila["precio"])

    return None, "Sin proveedor", 0.0


def listar_stock_bajo(restaurante_id=1):
    asegurar_tablas_compras()
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            id,
            nombre,
            unidad,
            stock_actual,
            unidad_stock,
            stock_minimo,
            ubicacion
        FROM articulos
        WHERE restaurante_id = ?
        AND activo = 1
        AND COALESCE(stock_minimo, 0) > 0
        AND COALESCE(stock_actual, 0) < COALESCE(stock_minimo, 0)
        ORDER BY (COALESCE(stock_minimo, 0) - COALESCE(stock_actual, 0)) DESC, nombre
    """, (restaurante_id,))

    articulos = []
    for fila in cursor.fetchall():
        proveedor_id, proveedor, precio = _ultimo_precio(cursor, restaurante_id, fila["id"])
        stock_actual = numero(fila["stock_actual"])
        stock_minimo = numero(fila["stock_minimo"])
        cantidad_faltante = max(stock_minimo - stock_actual, 0)
        unidad = fila["unidad_stock"] or fila["unidad"] or "ud"
        articulos.append({
            "articulo_id": fila["id"],
            "nombre": fila["nombre"],
            "stock_actual": stock_actual,
            "stock_minimo": stock_minimo,
            "cantidad_faltante": cantidad_faltante,
            "unidad": unidad,
            "proveedor_id": proveedor_id,
            "proveedor": proveedor or "Sin proveedor",
            "precio_estimado": precio,
            "importe_estimado": cantidad_faltante * precio if precio else 0,
            "ubicacion": fila["ubicacion"],
        })

    conexion.close()
    return articulos


def generar_pedido_stock_minimo(restaurante_id=1, nombre=None):
    asegurar_tablas_compras()
    articulos = listar_stock_bajo(restaurante_id)

    if not articulos:
        return None, []

    conexion = conectar()
    cursor = conexion.cursor()

    if not nombre:
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
        nombre = f"Pedido stock mínimo - {fecha}"

    cursor.execute("""
        INSERT INTO pedidos_compra
        (restaurante_id, nombre, origen, estado, observaciones)
        VALUES (?, ?, ?, ?, ?)
    """, (
        restaurante_id,
        nombre,
        "stock_minimo",
        "borrador",
        "Pedido generado automáticamente a partir de artículos bajo stock mínimo.",
    ))
    pedido_id = cursor.lastrowid

    for articulo in articulos:
        cursor.execute("""
            INSERT INTO lineas_pedido_compra
            (
                pedido_id,
                restaurante_id,
                articulo_id,
                proveedor_id,
                nombre_articulo,
                proveedor,
                cantidad_sugerida,
                unidad,
                precio_estimado,
                importe_estimado,
                motivo,
                estado
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            pedido_id,
            restaurante_id,
            articulo["articulo_id"],
            articulo["proveedor_id"],
            articulo["nombre"],
            articulo["proveedor"],
            articulo["cantidad_faltante"],
            articulo["unidad"],
            articulo["precio_estimado"],
            articulo["importe_estimado"],
            f"Stock actual {articulo['stock_actual']} < mínimo {articulo['stock_minimo']}",
            "pendiente",
        ))

    conexion.commit()
    conexion.close()

    return pedido_id, articulos


def obtener_ultimo_pedido(restaurante_id=1):
    asegurar_tablas_compras()
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT *
        FROM pedidos_compra
        WHERE restaurante_id = ?
        ORDER BY id DESC
        LIMIT 1
    """, (restaurante_id,))
    pedido = cursor.fetchone()
    conexion.close()
    return pedido


def listar_pedidos(restaurante_id=1, limite=20):
    asegurar_tablas_compras()
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT
            pedidos_compra.*,
            COUNT(lineas_pedido_compra.id) AS total_lineas,
            SUM(COALESCE(lineas_pedido_compra.importe_estimado, 0)) AS total_estimado
        FROM pedidos_compra
        LEFT JOIN lineas_pedido_compra ON pedidos_compra.id = lineas_pedido_compra.pedido_id
        WHERE pedidos_compra.restaurante_id = ?
        GROUP BY pedidos_compra.id
        ORDER BY pedidos_compra.id DESC
        LIMIT ?
    """, (restaurante_id, limite))
    filas = cursor.fetchall()
    conexion.close()
    return filas


def obtener_lineas_pedido(pedido_id):
    asegurar_tablas_compras()
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT *
        FROM lineas_pedido_compra
        WHERE pedido_id = ?
        ORDER BY proveedor, nombre_articulo
    """, (pedido_id,))
    lineas = cursor.fetchall()
    conexion.close()
    return lineas


def marcar_pedido_enviado(pedido_id):
    asegurar_tablas_compras()
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
        UPDATE pedidos_compra
        SET estado = 'enviado'
        WHERE id = ?
    """, (pedido_id,))
    conexion.commit()
    conexion.close()


def exportar_pedido_txt(pedido_id, carpeta_salida=None):
    asegurar_tablas_compras()
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM pedidos_compra WHERE id = ?", (pedido_id,))
    pedido = cursor.fetchone()
    conexion.close()

    if pedido is None:
        return None

    lineas = obtener_lineas_pedido(pedido_id)

    from pathlib import Path
    base_dir = Path(__file__).resolve().parent.parent
    if carpeta_salida is None:
        carpeta_salida = base_dir / "DOCUMENTOS" / "PEDIDOS"
    carpeta_salida = Path(carpeta_salida)
    carpeta_salida.mkdir(parents=True, exist_ok=True)

    nombre_seguro = "".join(c if c.isalnum() or c in "-_ " else "_" for c in pedido["nombre"])
    ruta = carpeta_salida / f"{nombre_seguro}_ID{pedido_id}.txt"

    total = sum(numero(l["importe_estimado"]) for l in lineas)

    grupos = {}
    for linea in lineas:
        proveedor = linea["proveedor"] or "Sin proveedor"
        grupos.setdefault(proveedor, []).append(linea)

    contenido = []
    contenido.append("======================================")
    contenido.append("              HOST AI")
    contenido.append("           PEDIDO COMPRA")
    contenido.append("======================================")
    contenido.append(f"Pedido : {pedido['nombre']}")
    contenido.append(f"Estado : {pedido['estado']}")
    contenido.append(f"Origen : {pedido['origen']}")
    contenido.append(f"Total estimado: {total:.2f} €")
    contenido.append("")

    for proveedor, lineas_proveedor in grupos.items():
        contenido.append(f"PROVEEDOR: {proveedor}")
        contenido.append("--------------------------------------")
        for linea in lineas_proveedor:
            importe = numero(linea["importe_estimado"])
            precio = numero(linea["precio_estimado"])
            contenido.append(
                f"- {linea['nombre_articulo']} | {linea['cantidad_sugerida']} {linea['unidad']} | "
                f"precio est. {precio:.2f} | importe est. {importe:.2f} €"
            )
        contenido.append("")

    ruta.write_text("\n".join(contenido), encoding="utf-8")
    return ruta
