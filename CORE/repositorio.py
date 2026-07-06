from database import conectar


def obtener_articulos(restaurante_id=1):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT
            articulos.id,
            articulos.nombre,
            articulos.familia,
            articulos.unidad,
            articulos.stock_minimo,
            articulos.ubicacion,
            proveedores.nombre AS proveedor,
            articulo_proveedor.precio AS precio
        FROM articulos
        LEFT JOIN articulo_proveedor
            ON articulos.id = articulo_proveedor.articulo_id
            AND articulo_proveedor.es_principal = 1
        LEFT JOIN proveedores
            ON articulo_proveedor.proveedor_id = proveedores.id
        WHERE articulos.restaurante_id = ?
        AND articulos.activo = 1
        ORDER BY articulos.nombre
    """, (restaurante_id,))
    filas = cursor.fetchall()
    conexion.close()
    return [dict(fila) for fila in filas]


def obtener_proveedores(restaurante_id=1):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT DISTINCT nombre
        FROM proveedores
        WHERE restaurante_id = ?
        ORDER BY nombre
    """, (restaurante_id,))
    filas = cursor.fetchall()
    conexion.close()
    return [fila["nombre"] for fila in filas]


def obtener_menus(restaurante_id=1):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT id, nombre, precio_venta, coste_total, food_cost
        FROM menus
        WHERE restaurante_id = ?
        AND activo = 1
        ORDER BY nombre
    """, (restaurante_id,))
    filas = cursor.fetchall()
    conexion.close()
    return [dict(fila) for fila in filas]


def contar_articulos(restaurante_id=1):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM articulos
        WHERE restaurante_id = ?
        AND activo = 1
    """, (restaurante_id,))
    total = cursor.fetchone()["total"]
    conexion.close()
    return total


def contar_proveedores(restaurante_id=1):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM proveedores
        WHERE restaurante_id = ?
    """, (restaurante_id,))
    total = cursor.fetchone()["total"]
    conexion.close()
    return total


def contar_menus(restaurante_id=1):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM menus
        WHERE restaurante_id = ?
        AND activo = 1
    """, (restaurante_id,))
    total = cursor.fetchone()["total"]
    conexion.close()
    return total


def contar_eventos(restaurante_id=1):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM eventos
        WHERE restaurante_id = ?
    """, (restaurante_id,))
    total = cursor.fetchone()["total"]
    conexion.close()
    return total


def contar_tareas_pendientes():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM tareas_produccion
        WHERE estado != 'hecha'
    """)
    total = cursor.fetchone()["total"]
    conexion.close()
    return total
