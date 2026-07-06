from database import conectar
from SERVICIOS.stock_servicio import registrar_movimiento_stock, normalizar_unidad


def _obtener_documento(cursor, documento_id):
    cursor.execute("SELECT * FROM documentos_importados WHERE id = ?", (documento_id,))
    return cursor.fetchone()


def _obtener_productos_documento(cursor, documento_id):
    cursor.execute("""
        SELECT *
        FROM productos_documento
        WHERE documento_id = ?
        ORDER BY id
    """, (documento_id,))
    return cursor.fetchall()


def _articulo_para_producto(producto):
    return producto["articulo_id_confirmado"] or producto["articulo_id_sugerido"]


def registrar_entrada_desde_documento(documento_id, restaurante_id=1, interactivo=True):
    conexion = conectar()
    cursor = conexion.cursor()

    documento = _obtener_documento(cursor, documento_id)
    if documento is None:
        conexion.close()
        raise ValueError("Documento no encontrado")

    productos = _obtener_productos_documento(cursor, documento_id)
    if not productos:
        conexion.close()
        raise ValueError("El documento no tiene productos detectados")

    cursor.execute("""
        SELECT id
        FROM entradas_mercancia
        WHERE documento_id = ?
        LIMIT 1
    """, (documento_id,))
    existente = cursor.fetchone()
    if existente:
        conexion.close()
        return {
            "ya_existia": True,
            "entrada_id": existente["id"],
            "lineas": 0,
            "stock_actualizado": 0,
            "incidencias": 0,
        }

    cursor.execute("""
        INSERT INTO entradas_mercancia
        (restaurante_id, documento_id, proveedor, fecha_documento, estado, observaciones)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        restaurante_id,
        documento_id,
        documento["proveedor"],
        documento["fecha_documento"],
        "registrada",
        "Entrada creada desde documento importado.",
    ))
    entrada_id = cursor.lastrowid

    lineas = 0
    stock_actualizado = 0
    incidencias = 0
    sin_articulo = 0

    for producto in productos:
        articulo_id = _articulo_para_producto(producto)
        cantidad_documento = producto["cantidad"] or 0
        cantidad_recibida = cantidad_documento
        unidad = normalizar_unidad(producto["unidad"])
        estado = "recibido"
        observaciones = ""

        if articulo_id is None:
            estado = "sin_articulo"
            sin_articulo += 1
            observaciones = "No se ha podido relacionar con ningún artículo."

        cursor.execute("""
            INSERT INTO lineas_entrada_mercancia
            (
                entrada_id,
                documento_id,
                producto_documento_id,
                articulo_id,
                nombre_detectado,
                cantidad_documento,
                cantidad_recibida,
                unidad,
                precio_unitario,
                importe,
                estado,
                observaciones
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            entrada_id,
            documento_id,
            producto["id"],
            articulo_id,
            producto["nombre_detectado"],
            cantidad_documento,
            cantidad_recibida,
            unidad,
            producto["precio_unitario"],
            producto["importe"],
            estado,
            observaciones,
        ))
        lineas += 1

        if articulo_id is not None and cantidad_recibida:
            registrar_movimiento_stock(
                cursor=cursor,
                restaurante_id=restaurante_id,
                articulo_id=articulo_id,
                tipo_movimiento="entrada",
                cantidad=cantidad_recibida,
                unidad=unidad,
                documento_id=documento_id,
                entrada_id=entrada_id,
                motivo=f"Entrada desde documento {documento_id}",
            )
            stock_actualizado += 1

    if sin_articulo:
        cursor.execute("""
            INSERT INTO incidencias_recepcion
            (restaurante_id, documento_id, entrada_id, tipo, descripcion, estado)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            restaurante_id,
            documento_id,
            entrada_id,
            "productos_sin_articulo",
            f"Hay {sin_articulo} productos sin artículo relacionado. Revisa equivalencias antes de cerrar la recepción.",
            "abierta",
        ))
        incidencias += 1

    cursor.execute("UPDATE documentos_importados SET estado = 'entrada_registrada' WHERE id = ?", (documento_id,))

    conexion.commit()
    conexion.close()

    return {
        "ya_existia": False,
        "entrada_id": entrada_id,
        "lineas": lineas,
        "stock_actualizado": stock_actualizado,
        "incidencias": incidencias,
        "sin_articulo": sin_articulo,
    }


def listar_entradas(restaurante_id=1, limite=20):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT id, proveedor, fecha_documento, estado, fecha_registro, documento_id
        FROM entradas_mercancia
        WHERE restaurante_id = ?
        ORDER BY id DESC
        LIMIT ?
    """, (restaurante_id, limite))
    entradas = cursor.fetchall()
    conexion.close()
    return entradas


def ver_detalle_entrada(entrada_id):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM entradas_mercancia WHERE id = ?", (entrada_id,))
    entrada = cursor.fetchone()
    cursor.execute("""
        SELECT
            lineas_entrada_mercancia.*,
            articulos.nombre AS articulo_nombre
        FROM lineas_entrada_mercancia
        LEFT JOIN articulos ON lineas_entrada_mercancia.articulo_id = articulos.id
        WHERE entrada_id = ?
        ORDER BY lineas_entrada_mercancia.id
    """, (entrada_id,))
    lineas = cursor.fetchall()
    conexion.close()
    return entrada, lineas


def registrar_incidencia_recepcion(
    restaurante_id,
    documento_id=None,
    entrada_id=None,
    producto_documento_id=None,
    articulo_id=None,
    tipo="manual",
    descripcion="",
    cantidad_afectada=None,
    unidad=None,
):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO incidencias_recepcion
        (
            restaurante_id,
            documento_id,
            entrada_id,
            producto_documento_id,
            articulo_id,
            tipo,
            descripcion,
            cantidad_afectada,
            unidad,
            estado
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        restaurante_id,
        documento_id,
        entrada_id,
        producto_documento_id,
        articulo_id,
        tipo,
        descripcion,
        cantidad_afectada,
        unidad,
        "abierta",
    ))
    conexion.commit()
    conexion.close()


def listar_incidencias(restaurante_id=1, limite=30):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT *
        FROM incidencias_recepcion
        WHERE restaurante_id = ?
        ORDER BY id DESC
        LIMIT ?
    """, (restaurante_id, limite))
    filas = cursor.fetchall()
    conexion.close()
    return filas
