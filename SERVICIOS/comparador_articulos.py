import re
from difflib import SequenceMatcher
from database import conectar


def normalizar(texto):
    texto = (texto or "").lower().strip()
    reemplazos = {
        "á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u",
        "à": "a", "è": "e", "ï": "i", "ò": "o", "ù": "u",
        "ñ": "n", "ç": "c",
    }
    for a, b in reemplazos.items():
        texto = texto.replace(a, b)
    texto = re.sub(r"[^a-z0-9]+", " ", texto)
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto


def similitud(a, b):
    a_n = normalizar(a)
    b_n = normalizar(b)
    if not a_n or not b_n:
        return 0
    if a_n == b_n:
        return 100
    if a_n in b_n or b_n in a_n:
        return 92
    return int(SequenceMatcher(None, a_n, b_n).ratio() * 100)


def buscar_equivalencia(cursor, restaurante_id, nombre_detectado, proveedor=""):
    cursor.execute("""
        SELECT articulo_id
        FROM equivalencias_articulos
        WHERE restaurante_id = ?
        AND nombre_detectado_normalizado = ?
        LIMIT 1
    """, (restaurante_id, normalizar(nombre_detectado)))
    return cursor.fetchone()


def cargar_articulos(cursor, restaurante_id):
    cursor.execute("""
        SELECT id, nombre
        FROM articulos
        WHERE restaurante_id = ?
        AND activo = 1
    """, (restaurante_id,))
    return cursor.fetchall()


def obtener_precio_actual(cursor, articulo_id):
    cursor.execute("""
        SELECT precio
        FROM articulo_proveedor
        WHERE articulo_id = ?
        AND es_principal = 1
        ORDER BY id DESC
        LIMIT 1
    """, (articulo_id,))
    r = cursor.fetchone()
    return None if r is None else r["precio"]


def comparar_producto(cursor, restaurante_id, producto):
    eq = buscar_equivalencia(cursor, restaurante_id, producto["nombre_detectado"])
    if eq:
        cursor.execute("SELECT id, nombre FROM articulos WHERE id = ?", (eq["articulo_id"],))
        art = cursor.fetchone()
        if art:
            precio_actual = obtener_precio_actual(cursor, art["id"])
            return {
                "producto_id": producto["id"],
                "nombre_detectado": producto["nombre_detectado"],
                "articulo_id": art["id"],
                "articulo_nombre": art["nombre"],
                "confianza": 100,
                "accion": "actualizar_precio" if producto["precio_unitario"] is not None else "relacionar",
                "precio_actual": precio_actual,
                "precio_nuevo": producto["precio_unitario"],
            }

    mejor = None
    mejor_score = 0
    for art in cargar_articulos(cursor, restaurante_id):
        score = similitud(producto["nombre_detectado"], art["nombre"])
        if score > mejor_score:
            mejor = art
            mejor_score = score

    if mejor and mejor_score >= 82:
        precio_actual = obtener_precio_actual(cursor, mejor["id"])
        accion = "actualizar_precio" if producto["precio_unitario"] is not None else "relacionar"
        return {
            "producto_id": producto["id"],
            "nombre_detectado": producto["nombre_detectado"],
            "articulo_id": mejor["id"],
            "articulo_nombre": mejor["nombre"],
            "confianza": mejor_score,
            "accion": accion,
            "precio_actual": precio_actual,
            "precio_nuevo": producto["precio_unitario"],
        }

    return {
        "producto_id": producto["id"],
        "nombre_detectado": producto["nombre_detectado"],
        "articulo_id": None,
        "articulo_nombre": "",
        "confianza": mejor_score,
        "accion": "crear_articulo",
        "precio_actual": None,
        "precio_nuevo": producto["precio_unitario"],
    }


def comparar_documento(documento_id, restaurante_id=1):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id, nombre_detectado, precio_unitario
        FROM productos_documento
        WHERE documento_id = ?
        ORDER BY id
    """, (documento_id,))
    productos = cursor.fetchall()

    resultados = []
    for producto in productos:
        resultado = comparar_producto(cursor, restaurante_id, producto)
        resultados.append(resultado)

        cursor.execute("""
            UPDATE productos_documento
            SET articulo_id_sugerido = ?, confianza = ?, accion_sugerida = ?
            WHERE id = ?
        """, (
            resultado["articulo_id"],
            resultado["confianza"],
            resultado["accion"],
            producto["id"],
        ))

    conexion.commit()
    conexion.close()
    return resultados
