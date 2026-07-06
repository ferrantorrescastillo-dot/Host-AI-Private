from database import conectar


def guardar_documento_importado(documento, restaurante_id=1):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        INSERT INTO documentos_importados
        (restaurante_id, tipo_archivo, tipo_documento, proveedor, fecha_documento,
         numero_documento, total, archivo_origen, texto_original, estado)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        restaurante_id,
        documento.tipo_archivo,
        documento.tipo_documento,
        documento.proveedor,
        documento.fecha,
        documento.numero_documento,
        documento.total,
        documento.archivo_origen,
        documento.texto_original,
        "pendiente_revision",
    ))
    documento_id = cursor.lastrowid

    for producto in documento.productos:
        cursor.execute("""
            INSERT INTO productos_documento
            (documento_id, codigo, nombre_detectado, cantidad, unidad,
             precio_unitario, importe, iva, linea_original, estado)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            documento_id,
            producto.codigo,
            producto.nombre,
            producto.cantidad,
            producto.unidad,
            producto.precio_unitario,
            producto.importe,
            producto.iva,
            producto.linea_original,
            "pendiente",
        ))

    conexion.commit()
    conexion.close()
    return documento_id
