from database import conectar
from SERVICIOS.comparador_articulos import normalizar


def obtener_o_crear_proveedor(cursor, restaurante_id, nombre):
    nombre = nombre or "Proveedor documento"
    cursor.execute("""
        SELECT id FROM proveedores
        WHERE restaurante_id = ? AND lower(nombre) = lower(?)
        LIMIT 1
    """, (restaurante_id, nombre))
    r = cursor.fetchone()
    if r:
        return r["id"]
    cursor.execute("""
        INSERT INTO proveedores (restaurante_id, nombre)
        VALUES (?, ?)
    """, (restaurante_id, nombre))
    return cursor.lastrowid


def actualizar_precio_articulo(cursor, articulo_id, proveedor_id, precio):
    if precio is None:
        return
    cursor.execute("""
        SELECT id FROM articulo_proveedor
        WHERE articulo_id = ? AND proveedor_id = ?
        LIMIT 1
    """, (articulo_id, proveedor_id))
    r = cursor.fetchone()
    if r:
        cursor.execute("""
            UPDATE articulo_proveedor
            SET precio = ?, es_principal = 1
            WHERE id = ?
        """, (precio, r["id"]))
    else:
        cursor.execute("""
            INSERT INTO articulo_proveedor (articulo_id, proveedor_id, precio, es_principal)
            VALUES (?, ?, ?, 1)
        """, (articulo_id, proveedor_id, precio))


def aplicar_documento(documento_id, restaurante_id=1):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM documentos_importados WHERE id = ?", (documento_id,))
    documento = cursor.fetchone()
    if documento is None:
        conexion.close()
        raise ValueError("Documento no encontrado")

    proveedor_id = obtener_o_crear_proveedor(cursor, restaurante_id, documento["proveedor"])

    cursor.execute("""
        SELECT * FROM productos_documento
        WHERE documento_id = ?
        ORDER BY id
    """, (documento_id,))
    productos = cursor.fetchall()

    creados = 0
    actualizados = 0
    equivalencias = 0

    for p in productos:
        articulo_id = p["articulo_id_sugerido"]
        accion = p["accion_sugerida"] or "crear_articulo"

        if articulo_id is None or accion == "crear_articulo":
            cursor.execute("""
                INSERT INTO articulos (restaurante_id, nombre, unidad, activo)
                VALUES (?, ?, ?, 1)
            """, (restaurante_id, p["nombre_detectado"], p["unidad"] or "ud"))
            articulo_id = cursor.lastrowid
            creados += 1
        else:
            actualizados += 1

        # Guardar equivalencia aprendida.
        cursor.execute("""
            INSERT OR IGNORE INTO equivalencias_articulos
            (restaurante_id, proveedor, nombre_detectado, nombre_detectado_normalizado, articulo_id, origen)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            restaurante_id,
            documento["proveedor"],
            p["nombre_detectado"],
            normalizar(p["nombre_detectado"]),
            articulo_id,
            "documento",
        ))
        equivalencias += 1

        precio = p["precio_unitario"]
        actualizar_precio_articulo(cursor, articulo_id, proveedor_id, precio)

        cursor.execute("""
            INSERT INTO historial_precios
            (restaurante_id, articulo_id, proveedor_id, documento_id, producto_documento_id,
             precio, cantidad, unidad, fecha_documento, origen)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            restaurante_id,
            articulo_id,
            proveedor_id,
            documento_id,
            p["id"],
            precio,
            p["cantidad"],
            p["unidad"],
            documento["fecha_documento"],
            "importador_documentos",
        ))

        cursor.execute("""
            UPDATE productos_documento
            SET articulo_id_confirmado = ?, estado = 'aplicado'
            WHERE id = ?
        """, (articulo_id, p["id"]))

    cursor.execute("UPDATE documentos_importados SET estado = 'aplicado' WHERE id = ?", (documento_id,))

    conexion.commit()
    conexion.close()

    return {
        "creados": creados,
        "actualizados": actualizados,
        "equivalencias": equivalencias,
        "productos": len(productos),
    }
