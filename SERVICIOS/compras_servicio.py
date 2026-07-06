from datetime import datetime
from pathlib import Path
from database import conectar


# ============================================================
# HOST AI - SERVICIO DE COMPRAS
# Sprint 4.6
# ------------------------------------------------------------
# Responsabilidad de este archivo:
# - Configurar stock mínimo / óptimo por artículo.
# - Detectar artículos bajo mínimo.
# - Generar pedidos inteligentes hasta stock óptimo.
# - Exportar pedidos.
#
# Este servicio NO muestra menús. Solo hace lógica de negocio.
# ============================================================


def numero(valor, defecto=0.0):
    try:
        if valor is None or valor == "":
            return defecto
        return float(valor)
    except Exception:
        return defecto


def texto(valor, defecto=""):
    if valor is None:
        return defecto
    valor = str(valor).strip()
    return valor if valor else defecto


def _columnas_tabla(cursor, tabla):
    cursor.execute(f"PRAGMA table_info({tabla})")
    return {fila[1] for fila in cursor.fetchall()}


def _agregar_columna_si_no_existe(cursor, tabla, columna, definicion):
    columnas = _columnas_tabla(cursor, tabla)
    if columna not in columnas:
        cursor.execute(f"ALTER TABLE {tabla} ADD COLUMN {columna} {definicion}")


def asegurar_tablas_compras():
    """Asegura tablas y columnas necesarias para compras/stock inteligente."""
    conexion = conectar()
    cursor = conexion.cursor()

    # Columnas de stock en artículos.
    _agregar_columna_si_no_existe(cursor, "articulos", "stock_actual", "REAL DEFAULT 0")
    _agregar_columna_si_no_existe(cursor, "articulos", "unidad_stock", "TEXT")
    _agregar_columna_si_no_existe(cursor, "articulos", "stock_optimo", "REAL DEFAULT 0")
    _agregar_columna_si_no_existe(cursor, "articulos", "cantidad_compra_habitual", "REAL DEFAULT 0")
    _agregar_columna_si_no_existe(cursor, "articulos", "unidad_compra", "TEXT")

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
    # Primero historial de precios de documentos importados.
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

    # Luego tabla articulo_proveedor.
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


def _calcular_cantidad_a_pedir(stock_actual, stock_minimo, stock_optimo, cantidad_compra_habitual):
    """
    Si hay stock óptimo, se repone hasta el óptimo.
    Si no hay óptimo, se repone hasta el mínimo.
    Si hay cantidad habitual de compra, se redondea hacia arriba a múltiplos.
    """
    stock_actual = numero(stock_actual)
    stock_minimo = numero(stock_minimo)
    stock_optimo = numero(stock_optimo)
    cantidad_compra_habitual = numero(cantidad_compra_habitual)

    objetivo = stock_optimo if stock_optimo > stock_minimo else stock_minimo
    faltante = max(objetivo - stock_actual, 0)

    if faltante <= 0:
        return 0

    if cantidad_compra_habitual > 0:
        import math
        return math.ceil(faltante / cantidad_compra_habitual) * cantidad_compra_habitual

    return faltante


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
            stock_optimo,
            cantidad_compra_habitual,
            unidad_compra,
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
        stock_optimo = numero(fila["stock_optimo"])
        cantidad_compra = numero(fila["cantidad_compra_habitual"])
        cantidad_sugerida = _calcular_cantidad_a_pedir(
            stock_actual,
            stock_minimo,
            stock_optimo,
            cantidad_compra,
        )
        unidad = fila["unidad_stock"] or fila["unidad"] or "ud"
        articulos.append({
            "articulo_id": fila["id"],
            "nombre": fila["nombre"],
            "stock_actual": stock_actual,
            "stock_minimo": stock_minimo,
            "stock_optimo": stock_optimo,
            "cantidad_compra_habitual": cantidad_compra,
            "cantidad_faltante": max(stock_minimo - stock_actual, 0),
            "cantidad_sugerida": cantidad_sugerida,
            "unidad": unidad,
            "unidad_compra": fila["unidad_compra"] or unidad,
            "proveedor_id": proveedor_id,
            "proveedor": proveedor or "Sin proveedor",
            "precio_estimado": precio,
            "importe_estimado": cantidad_sugerida * precio if precio else 0,
            "ubicacion": fila["ubicacion"],
        })

    conexion.close()
    return articulos


def buscar_articulos_para_configurar(restaurante_id=1, busqueda="", limite=25):
    asegurar_tablas_compras()
    conexion = conectar()
    cursor = conexion.cursor()

    patron = f"%{busqueda.strip()}%"
    cursor.execute("""
        SELECT
            id,
            nombre,
            unidad,
            stock_actual,
            unidad_stock,
            stock_minimo,
            stock_optimo,
            cantidad_compra_habitual,
            unidad_compra,
            ubicacion
        FROM articulos
        WHERE restaurante_id = ?
        AND activo = 1
        AND (? = '%%' OR nombre LIKE ?)
        ORDER BY nombre
        LIMIT ?
    """, (restaurante_id, patron, patron, limite))

    filas = cursor.fetchall()
    conexion.close()
    return filas


def listar_articulos_sin_stock_minimo(restaurante_id=1, limite=80):
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
            stock_optimo,
            cantidad_compra_habitual,
            unidad_compra
        FROM articulos
        WHERE restaurante_id = ?
        AND activo = 1
        AND COALESCE(stock_minimo, 0) = 0
        ORDER BY nombre
        LIMIT ?
    """, (restaurante_id, limite))
    filas = cursor.fetchall()
    conexion.close()
    return filas


def actualizar_configuracion_stock(
    articulo_id,
    stock_minimo=None,
    stock_optimo=None,
    cantidad_compra_habitual=None,
    unidad_stock=None,
    unidad_compra=None,
):
    asegurar_tablas_compras()
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("SELECT id FROM articulos WHERE id = ?", (articulo_id,))
    if cursor.fetchone() is None:
        conexion.close()
        return False

    cursor.execute("""
        UPDATE articulos
        SET
            stock_minimo = COALESCE(?, stock_minimo),
            stock_optimo = COALESCE(?, stock_optimo),
            cantidad_compra_habitual = COALESCE(?, cantidad_compra_habitual),
            unidad_stock = COALESCE(NULLIF(?, ''), unidad_stock),
            unidad_compra = COALESCE(NULLIF(?, ''), unidad_compra)
        WHERE id = ?
    """, (
        stock_minimo,
        stock_optimo,
        cantidad_compra_habitual,
        unidad_stock,
        unidad_compra,
        articulo_id,
    ))

    conexion.commit()
    conexion.close()
    return True


def obtener_articulo(articulo_id):
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
            stock_optimo,
            cantidad_compra_habitual,
            unidad_compra,
            ubicacion
        FROM articulos
        WHERE id = ?
    """, (articulo_id,))
    fila = cursor.fetchone()
    conexion.close()
    return fila


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
        "Pedido generado automáticamente hasta stock óptimo o mínimo.",
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
            articulo["cantidad_sugerida"],
            articulo["unidad"],
            articulo["precio_estimado"],
            articulo["importe_estimado"],
            (
                f"Stock actual {articulo['stock_actual']} < mínimo {articulo['stock_minimo']}. "
                f"Objetivo {articulo['stock_optimo'] or articulo['stock_minimo']}."
            ),
            "pendiente",
        ))

    conexion.commit()
    conexion.close()

    return pedido_id, articulos


def generar_pedido_articulos_seleccionados(restaurante_id=1, articulo_ids=None, nombre=None):
    asegurar_tablas_compras()
    articulo_ids = articulo_ids or []
    if not articulo_ids:
        return None, []

    conexion = conectar()
    cursor = conexion.cursor()

    if not nombre:
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
        nombre = f"Pedido manual - {fecha}"

    cursor.execute("""
        INSERT INTO pedidos_compra
        (restaurante_id, nombre, origen, estado, observaciones)
        VALUES (?, ?, ?, ?, ?)
    """, (
        restaurante_id,
        nombre,
        "manual",
        "borrador",
        "Pedido generado manualmente desde artículos seleccionados.",
    ))
    pedido_id = cursor.lastrowid

    lineas = []
    for articulo_id in articulo_ids:
        cursor.execute("""
            SELECT
                id,
                nombre,
                unidad,
                stock_actual,
                unidad_stock,
                stock_minimo,
                stock_optimo,
                cantidad_compra_habitual,
                unidad_compra
            FROM articulos
            WHERE id = ?
            AND restaurante_id = ?
            AND activo = 1
        """, (articulo_id, restaurante_id))
        fila = cursor.fetchone()
        if fila is None:
            continue

        proveedor_id, proveedor, precio = _ultimo_precio(cursor, restaurante_id, fila["id"])
        unidad = fila["unidad_stock"] or fila["unidad"] or "ud"
        cantidad = numero(fila["cantidad_compra_habitual"])
        if cantidad <= 0:
            stock_actual = numero(fila["stock_actual"])
            objetivo = numero(fila["stock_optimo"]) or numero(fila["stock_minimo"]) or 1
            cantidad = max(objetivo - stock_actual, 1)

        importe = cantidad * precio if precio else 0
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
            fila["id"],
            proveedor_id,
            fila["nombre"],
            proveedor or "Sin proveedor",
            cantidad,
            unidad,
            precio,
            importe,
            "Pedido manual / prueba",
            "pendiente",
        ))
        lineas.append(fila)

    conexion.commit()
    conexion.close()
    return pedido_id, lineas


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
