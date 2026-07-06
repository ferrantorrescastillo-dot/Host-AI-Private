from database import conectar


def normalizar_unidad(unidad):
    if unidad is None:
        return "ud"
    texto = str(unidad).strip()
    if not texto or texto.lower() == "none":
        return "ud"
    return texto


def obtener_stock_articulo(articulo_id):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT stock_actual, unidad_stock
        FROM articulos
        WHERE id = ?
    """, (articulo_id,))
    fila = cursor.fetchone()
    conexion.close()
    if fila is None:
        return 0, "ud"
    return fila["stock_actual"] or 0, fila["unidad_stock"] or "ud"


def registrar_movimiento_stock(
    cursor,
    restaurante_id,
    articulo_id,
    tipo_movimiento,
    cantidad,
    unidad="ud",
    documento_id=None,
    entrada_id=None,
    motivo="",
):
    unidad = normalizar_unidad(unidad)
    cantidad = float(cantidad or 0)

    cursor.execute("""
        SELECT stock_actual, unidad_stock
        FROM articulos
        WHERE id = ?
    """, (articulo_id,))
    articulo = cursor.fetchone()

    if articulo is None:
        raise ValueError("Artículo no encontrado")

    stock_anterior = articulo["stock_actual"] or 0

    if tipo_movimiento == "entrada":
        stock_nuevo = stock_anterior + cantidad
    elif tipo_movimiento == "salida":
        stock_nuevo = stock_anterior - cantidad
    elif tipo_movimiento == "ajuste":
        stock_nuevo = cantidad
    else:
        raise ValueError("Tipo de movimiento no válido")

    cursor.execute("""
        UPDATE articulos
        SET stock_actual = ?, unidad_stock = COALESCE(unidad_stock, ?)
        WHERE id = ?
    """, (stock_nuevo, unidad, articulo_id))

    cursor.execute("""
        INSERT INTO movimientos_stock
        (
            restaurante_id,
            articulo_id,
            documento_id,
            entrada_id,
            tipo_movimiento,
            cantidad,
            unidad,
            stock_anterior,
            stock_nuevo,
            motivo
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        restaurante_id,
        articulo_id,
        documento_id,
        entrada_id,
        tipo_movimiento,
        cantidad,
        unidad,
        stock_anterior,
        stock_nuevo,
        motivo,
    ))

    return stock_anterior, stock_nuevo


def listar_stock(restaurante_id=1, limite=50):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT id, nombre, unidad, stock_actual, unidad_stock, stock_minimo, ubicacion
        FROM articulos
        WHERE restaurante_id = ?
        AND activo = 1
        ORDER BY nombre
        LIMIT ?
    """, (restaurante_id, limite))
    filas = cursor.fetchall()
    conexion.close()
    return filas


def listar_movimientos_stock(restaurante_id=1, limite=30):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT
            movimientos_stock.fecha,
            movimientos_stock.tipo_movimiento,
            movimientos_stock.cantidad,
            movimientos_stock.unidad,
            movimientos_stock.stock_anterior,
            movimientos_stock.stock_nuevo,
            movimientos_stock.motivo,
            articulos.nombre AS articulo_nombre
        FROM movimientos_stock
        LEFT JOIN articulos ON movimientos_stock.articulo_id = articulos.id
        WHERE movimientos_stock.restaurante_id = ?
        ORDER BY movimientos_stock.id DESC
        LIMIT ?
    """, (restaurante_id, limite))
    filas = cursor.fetchall()
    conexion.close()
    return filas
