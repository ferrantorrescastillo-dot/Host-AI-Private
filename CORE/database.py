import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATOS_DIR = BASE_DIR / "DATOS"
DATOS_DIR.mkdir(exist_ok=True)
DB_PATH = DATOS_DIR / "hostai.db"


def conectar():
    conexion = sqlite3.connect(DB_PATH)
    conexion.row_factory = sqlite3.Row
    return conexion


def columna_existe(cursor, tabla, columna):
    cursor.execute(f"PRAGMA table_info({tabla})")
    columnas = cursor.fetchall()
    return any(fila["name"] == columna for fila in columnas)


def agregar_columna_si_no_existe(cursor, tabla, columna, definicion):
    if not columna_existe(cursor, tabla, columna):
        cursor.execute(f"ALTER TABLE {tabla} ADD COLUMN {columna} {definicion}")


def crear_base_datos():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS configuracion (
        clave TEXT PRIMARY KEY,
        valor TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS restaurantes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        direccion TEXT,
        telefono TEXT,
        email TEXT,
        fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        restaurante_id INTEGER,
        nombre TEXT,
        rol TEXT,
        FOREIGN KEY(restaurante_id) REFERENCES restaurantes(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS proveedores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        restaurante_id INTEGER,
        nombre TEXT NOT NULL,
        telefono TEXT,
        email TEXT,
        observaciones TEXT,
        FOREIGN KEY(restaurante_id) REFERENCES restaurantes(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS articulos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        restaurante_id INTEGER,
        nombre TEXT NOT NULL,
        familia TEXT,
        unidad TEXT,
        stock_minimo REAL DEFAULT 0,
        ubicacion TEXT,
        activo INTEGER DEFAULT 1,
        FOREIGN KEY(restaurante_id) REFERENCES restaurantes(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS articulo_proveedor (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        articulo_id INTEGER,
        proveedor_id INTEGER,
        precio REAL,
        formato TEXT,
        es_principal INTEGER DEFAULT 1,
        FOREIGN KEY(articulo_id) REFERENCES articulos(id),
        FOREIGN KEY(proveedor_id) REFERENCES proveedores(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS elaboraciones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        restaurante_id INTEGER,
        nombre TEXT NOT NULL,
        categoria TEXT,
        raciones REAL,
        unidad_resultado TEXT,
        elaboracion TEXT,
        alergenos TEXT,
        activo INTEGER DEFAULT 1,
        FOREIGN KEY(restaurante_id) REFERENCES restaurantes(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ingredientes_elaboracion (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        elaboracion_id INTEGER,
        articulo_id INTEGER,
        cantidad REAL,
        unidad TEXT,
        observaciones TEXT,
        FOREIGN KEY(elaboracion_id) REFERENCES elaboraciones(id),
        FOREIGN KEY(articulo_id) REFERENCES articulos(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS platos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        restaurante_id INTEGER,
        nombre TEXT NOT NULL,
        categoria TEXT,
        descripcion TEXT,
        alergenos TEXT,
        activo INTEGER DEFAULT 1,
        FOREIGN KEY(restaurante_id) REFERENCES restaurantes(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS componentes_plato (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        plato_id INTEGER,
        elaboracion_id INTEGER,
        cantidad REAL,
        unidad TEXT,
        observaciones TEXT,
        FOREIGN KEY(plato_id) REFERENCES platos(id),
        FOREIGN KEY(elaboracion_id) REFERENCES elaboraciones(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS menus (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        restaurante_id INTEGER,
        nombre TEXT NOT NULL,
        hoja_excel TEXT,
        precio_venta REAL,
        coste_total REAL,
        food_cost REAL,
        activo INTEGER DEFAULT 1,
        FOREIGN KEY(restaurante_id) REFERENCES restaurantes(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS platos_menu (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        menu_id INTEGER,
        plato_id INTEGER,
        nombre TEXT NOT NULL,
        cantidad REAL,
        precio_unitario REAL,
        coste_racion REAL,
        orden INTEGER,
        FOREIGN KEY(menu_id) REFERENCES menus(id),
        FOREIGN KEY(plato_id) REFERENCES platos(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS eventos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        restaurante_id INTEGER,
        menu_id INTEGER,
        nombre TEXT NOT NULL,
        fecha TEXT,
        numero_personas INTEGER,
        estado TEXT DEFAULT 'pendiente',
        observaciones TEXT,
        fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(restaurante_id) REFERENCES restaurantes(id),
        FOREIGN KEY(menu_id) REFERENCES menus(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS producciones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        evento_id INTEGER,
        nombre TEXT NOT NULL,
        estado TEXT DEFAULT 'pendiente',
        observaciones TEXT,
        fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(evento_id) REFERENCES eventos(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tareas_produccion (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        produccion_id INTEGER,
        nombre TEXT NOT NULL,
        cantidad REAL,
        unidad TEXT,
        estado TEXT DEFAULT 'pendiente',
        orden INTEGER,
        FOREIGN KEY(produccion_id) REFERENCES producciones(id)
    )
    """)

    agregar_columna_si_no_existe(cursor, "tareas_produccion", "rol_recomendado", "TEXT")
    agregar_columna_si_no_existe(cursor, "tareas_produccion", "persona_asignada", "TEXT")
    agregar_columna_si_no_existe(cursor, "tareas_produccion", "tiempo_estimado_min", "INTEGER")
    agregar_columna_si_no_existe(cursor, "tareas_produccion", "prioridad", "TEXT DEFAULT 'media'")
    agregar_columna_si_no_existe(cursor, "tareas_produccion", "hora_inicio_estimada", "TEXT")
    agregar_columna_si_no_existe(cursor, "tareas_produccion", "hora_fin_estimada", "TEXT")
    agregar_columna_si_no_existe(cursor, "tareas_produccion", "nota_planificacion", "TEXT")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS produccion_disponible (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        restaurante_id INTEGER,
        nombre TEXT NOT NULL,
        cantidad REAL DEFAULT 0,
        unidad TEXT,
        ubicacion TEXT,
        fecha_caducidad TEXT,
        congelado INTEGER DEFAULT 0,
        observaciones TEXT,
        fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(restaurante_id, nombre, unidad, ubicacion, fecha_caducidad, congelado),
        FOREIGN KEY(restaurante_id) REFERENCES restaurantes(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS movimientos_produccion_disponible (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        restaurante_id INTEGER,
        produccion_disponible_id INTEGER,
        tarea_produccion_id INTEGER,
        tipo_movimiento TEXT NOT NULL,
        nombre TEXT NOT NULL,
        cantidad REAL,
        unidad TEXT,
        motivo TEXT,
        fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(restaurante_id) REFERENCES restaurantes(id),
        FOREIGN KEY(produccion_disponible_id) REFERENCES produccion_disponible(id),
        FOREIGN KEY(tarea_produccion_id) REFERENCES tareas_produccion(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS rendimientos_elaboracion (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        restaurante_id INTEGER,
        nombre TEXT NOT NULL,
        cantidad_prevista REAL,
        cantidad_real REAL,
        unidad TEXT,
        diferencia REAL,
        porcentaje_diferencia REAL,
        tarea_produccion_id INTEGER,
        evento_id INTEGER,
        fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(restaurante_id) REFERENCES restaurantes(id),
        FOREIGN KEY(tarea_produccion_id) REFERENCES tareas_produccion(id),
        FOREIGN KEY(evento_id) REFERENCES eventos(id)
    )
    """)

    # v0.8: roles, personal y planificación diaria.
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS roles_cocina (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        restaurante_id INTEGER,
        nombre TEXT NOT NULL,
        nivel_responsabilidad INTEGER DEFAULT 1,
        descripcion TEXT,
        activo INTEGER DEFAULT 1,
        UNIQUE(restaurante_id, nombre),
        FOREIGN KEY(restaurante_id) REFERENCES restaurantes(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS personal_cocina (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        restaurante_id INTEGER,
        nombre TEXT NOT NULL,
        rol_id INTEGER,
        velocidad INTEGER DEFAULT 100,
        activo INTEGER DEFAULT 1,
        observaciones TEXT,
        UNIQUE(restaurante_id, nombre),
        FOREIGN KEY(restaurante_id) REFERENCES restaurantes(id),
        FOREIGN KEY(rol_id) REFERENCES roles_cocina(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS planificaciones_dia (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        restaurante_id INTEGER,
        fecha TEXT,
        nombre TEXT,
        estado TEXT DEFAULT 'abierta',
        observaciones TEXT,
        fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(restaurante_id, fecha),
        FOREIGN KEY(restaurante_id) REFERENCES restaurantes(id)
    )
    """)


    # v2.0: ordenes de producción como entidad central del sistema.
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ordenes_produccion (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        restaurante_id INTEGER,
        origen_tipo TEXT,
        origen_id INTEGER,
        nombre TEXT NOT NULL,
        fecha_objetivo TEXT,
        numero_personas INTEGER,
        estado TEXT DEFAULT 'borrador',
        observaciones TEXT,
        fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(restaurante_id) REFERENCES restaurantes(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS lineas_orden_produccion (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        orden_id INTEGER,
        nombre TEXT NOT NULL,
        tipo TEXT DEFAULT 'plato',
        cantidad REAL,
        unidad TEXT,
        estado TEXT DEFAULT 'pendiente',
        rol_recomendado TEXT,
        prioridad TEXT DEFAULT 'media',
        tiempo_estimado_min INTEGER DEFAULT 60,
        orden INTEGER,
        observaciones TEXT,
        FOREIGN KEY(orden_id) REFERENCES ordenes_produccion(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dependencias_linea_produccion (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        linea_id INTEGER,
        depende_de_linea_id INTEGER,
        tipo_dependencia TEXT,
        observaciones TEXT,
        FOREIGN KEY(linea_id) REFERENCES lineas_orden_produccion(id),
        FOREIGN KEY(depende_de_linea_id) REFERENCES lineas_orden_produccion(id)
    )
    """)



    # Sprint 4.2: documentos, productos detectados, equivalencias e historial de precios.
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS documentos_importados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        restaurante_id INTEGER,
        tipo_archivo TEXT,
        tipo_documento TEXT,
        proveedor TEXT,
        fecha_documento TEXT,
        numero_documento TEXT,
        total REAL,
        archivo_origen TEXT,
        texto_original TEXT,
        estado TEXT DEFAULT 'pendiente_revision',
        fecha_importacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(restaurante_id) REFERENCES restaurantes(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS productos_documento (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        documento_id INTEGER,
        codigo TEXT,
        nombre_detectado TEXT,
        cantidad REAL,
        unidad TEXT,
        precio_unitario REAL,
        importe REAL,
        iva TEXT,
        linea_original TEXT,
        articulo_id_sugerido INTEGER,
        articulo_id_confirmado INTEGER,
        confianza INTEGER DEFAULT 0,
        accion_sugerida TEXT,
        estado TEXT DEFAULT 'pendiente',
        FOREIGN KEY(documento_id) REFERENCES documentos_importados(id),
        FOREIGN KEY(articulo_id_sugerido) REFERENCES articulos(id),
        FOREIGN KEY(articulo_id_confirmado) REFERENCES articulos(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS equivalencias_articulos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        restaurante_id INTEGER,
        proveedor TEXT,
        nombre_detectado TEXT,
        nombre_detectado_normalizado TEXT,
        articulo_id INTEGER,
        origen TEXT,
        fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(restaurante_id, nombre_detectado_normalizado),
        FOREIGN KEY(restaurante_id) REFERENCES restaurantes(id),
        FOREIGN KEY(articulo_id) REFERENCES articulos(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS historial_precios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        restaurante_id INTEGER,
        articulo_id INTEGER,
        proveedor_id INTEGER,
        documento_id INTEGER,
        producto_documento_id INTEGER,
        precio REAL,
        cantidad REAL,
        unidad TEXT,
        fecha_documento TEXT,
        origen TEXT,
        fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(restaurante_id) REFERENCES restaurantes(id),
        FOREIGN KEY(articulo_id) REFERENCES articulos(id),
        FOREIGN KEY(proveedor_id) REFERENCES proveedores(id),
        FOREIGN KEY(documento_id) REFERENCES documentos_importados(id),
        FOREIGN KEY(producto_documento_id) REFERENCES productos_documento(id)
    )
    """)



    # Sprint 4.3: stock de artículos, entradas de mercancía e incidencias de recepción.
    agregar_columna_si_no_existe(cursor, "articulos", "stock_actual", "REAL DEFAULT 0")
    agregar_columna_si_no_existe(cursor, "articulos", "unidad_stock", "TEXT")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS entradas_mercancia (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        restaurante_id INTEGER,
        documento_id INTEGER,
        proveedor TEXT,
        fecha_documento TEXT,
        estado TEXT DEFAULT 'registrada',
        observaciones TEXT,
        fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(restaurante_id) REFERENCES restaurantes(id),
        FOREIGN KEY(documento_id) REFERENCES documentos_importados(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS lineas_entrada_mercancia (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        entrada_id INTEGER,
        documento_id INTEGER,
        producto_documento_id INTEGER,
        articulo_id INTEGER,
        nombre_detectado TEXT,
        cantidad_documento REAL,
        cantidad_recibida REAL,
        unidad TEXT,
        precio_unitario REAL,
        importe REAL,
        estado TEXT DEFAULT 'recibido',
        observaciones TEXT,
        fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(entrada_id) REFERENCES entradas_mercancia(id),
        FOREIGN KEY(documento_id) REFERENCES documentos_importados(id),
        FOREIGN KEY(producto_documento_id) REFERENCES productos_documento(id),
        FOREIGN KEY(articulo_id) REFERENCES articulos(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS movimientos_stock (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        restaurante_id INTEGER,
        articulo_id INTEGER,
        documento_id INTEGER,
        entrada_id INTEGER,
        tipo_movimiento TEXT NOT NULL,
        cantidad REAL,
        unidad TEXT,
        stock_anterior REAL,
        stock_nuevo REAL,
        motivo TEXT,
        fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(restaurante_id) REFERENCES restaurantes(id),
        FOREIGN KEY(articulo_id) REFERENCES articulos(id),
        FOREIGN KEY(documento_id) REFERENCES documentos_importados(id),
        FOREIGN KEY(entrada_id) REFERENCES entradas_mercancia(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS incidencias_recepcion (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        restaurante_id INTEGER,
        documento_id INTEGER,
        entrada_id INTEGER,
        producto_documento_id INTEGER,
        articulo_id INTEGER,
        tipo TEXT,
        descripcion TEXT,
        cantidad_afectada REAL,
        unidad TEXT,
        estado TEXT DEFAULT 'abierta',
        fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(restaurante_id) REFERENCES restaurantes(id),
        FOREIGN KEY(documento_id) REFERENCES documentos_importados(id),
        FOREIGN KEY(entrada_id) REFERENCES entradas_mercancia(id),
        FOREIGN KEY(producto_documento_id) REFERENCES productos_documento(id),
        FOREIGN KEY(articulo_id) REFERENCES articulos(id)
    )
    """)

    conexion.commit()
    conexion.close()

    print("✅ Base de datos preparada correctamente.")


def obtener_configuracion(clave, valor_por_defecto=None):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT valor FROM configuracion WHERE clave = ?", (clave,))
    resultado = cursor.fetchone()
    conexion.close()
    return valor_por_defecto if resultado is None else resultado["valor"]


def guardar_configuracion(clave, valor):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO configuracion (clave, valor)
        VALUES (?, ?)
    """, (clave, str(valor)))


    # Sprint 4.3: stock de artículos, entradas de mercancía e incidencias de recepción.
    agregar_columna_si_no_existe(cursor, "articulos", "stock_actual", "REAL DEFAULT 0")
    agregar_columna_si_no_existe(cursor, "articulos", "unidad_stock", "TEXT")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS entradas_mercancia (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        restaurante_id INTEGER,
        documento_id INTEGER,
        proveedor TEXT,
        fecha_documento TEXT,
        estado TEXT DEFAULT 'registrada',
        observaciones TEXT,
        fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(restaurante_id) REFERENCES restaurantes(id),
        FOREIGN KEY(documento_id) REFERENCES documentos_importados(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS lineas_entrada_mercancia (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        entrada_id INTEGER,
        documento_id INTEGER,
        producto_documento_id INTEGER,
        articulo_id INTEGER,
        nombre_detectado TEXT,
        cantidad_documento REAL,
        cantidad_recibida REAL,
        unidad TEXT,
        precio_unitario REAL,
        importe REAL,
        estado TEXT DEFAULT 'recibido',
        observaciones TEXT,
        fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(entrada_id) REFERENCES entradas_mercancia(id),
        FOREIGN KEY(documento_id) REFERENCES documentos_importados(id),
        FOREIGN KEY(producto_documento_id) REFERENCES productos_documento(id),
        FOREIGN KEY(articulo_id) REFERENCES articulos(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS movimientos_stock (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        restaurante_id INTEGER,
        articulo_id INTEGER,
        documento_id INTEGER,
        entrada_id INTEGER,
        tipo_movimiento TEXT NOT NULL,
        cantidad REAL,
        unidad TEXT,
        stock_anterior REAL,
        stock_nuevo REAL,
        motivo TEXT,
        fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(restaurante_id) REFERENCES restaurantes(id),
        FOREIGN KEY(articulo_id) REFERENCES articulos(id),
        FOREIGN KEY(documento_id) REFERENCES documentos_importados(id),
        FOREIGN KEY(entrada_id) REFERENCES entradas_mercancia(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS incidencias_recepcion (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        restaurante_id INTEGER,
        documento_id INTEGER,
        entrada_id INTEGER,
        producto_documento_id INTEGER,
        articulo_id INTEGER,
        tipo TEXT,
        descripcion TEXT,
        cantidad_afectada REAL,
        unidad TEXT,
        estado TEXT DEFAULT 'abierta',
        fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(restaurante_id) REFERENCES restaurantes(id),
        FOREIGN KEY(documento_id) REFERENCES documentos_importados(id),
        FOREIGN KEY(entrada_id) REFERENCES entradas_mercancia(id),
        FOREIGN KEY(producto_documento_id) REFERENCES productos_documento(id),
        FOREIGN KEY(articulo_id) REFERENCES articulos(id)
    )
    """)

    conexion.commit()
    conexion.close()


def asegurar_restaurante_demo():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT id FROM restaurantes LIMIT 1")
    resultado = cursor.fetchone()
    if resultado:
        conexion.close()
        return resultado["id"]
    cursor.execute("INSERT INTO restaurantes (nombre) VALUES (?)", ("Restaurante Demo",))
    restaurante_id = cursor.lastrowid


    # Sprint 4.3: stock de artículos, entradas de mercancía e incidencias de recepción.
    agregar_columna_si_no_existe(cursor, "articulos", "stock_actual", "REAL DEFAULT 0")
    agregar_columna_si_no_existe(cursor, "articulos", "unidad_stock", "TEXT")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS entradas_mercancia (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        restaurante_id INTEGER,
        documento_id INTEGER,
        proveedor TEXT,
        fecha_documento TEXT,
        estado TEXT DEFAULT 'registrada',
        observaciones TEXT,
        fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(restaurante_id) REFERENCES restaurantes(id),
        FOREIGN KEY(documento_id) REFERENCES documentos_importados(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS lineas_entrada_mercancia (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        entrada_id INTEGER,
        documento_id INTEGER,
        producto_documento_id INTEGER,
        articulo_id INTEGER,
        nombre_detectado TEXT,
        cantidad_documento REAL,
        cantidad_recibida REAL,
        unidad TEXT,
        precio_unitario REAL,
        importe REAL,
        estado TEXT DEFAULT 'recibido',
        observaciones TEXT,
        fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(entrada_id) REFERENCES entradas_mercancia(id),
        FOREIGN KEY(documento_id) REFERENCES documentos_importados(id),
        FOREIGN KEY(producto_documento_id) REFERENCES productos_documento(id),
        FOREIGN KEY(articulo_id) REFERENCES articulos(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS movimientos_stock (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        restaurante_id INTEGER,
        articulo_id INTEGER,
        documento_id INTEGER,
        entrada_id INTEGER,
        tipo_movimiento TEXT NOT NULL,
        cantidad REAL,
        unidad TEXT,
        stock_anterior REAL,
        stock_nuevo REAL,
        motivo TEXT,
        fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(restaurante_id) REFERENCES restaurantes(id),
        FOREIGN KEY(articulo_id) REFERENCES articulos(id),
        FOREIGN KEY(documento_id) REFERENCES documentos_importados(id),
        FOREIGN KEY(entrada_id) REFERENCES entradas_mercancia(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS incidencias_recepcion (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        restaurante_id INTEGER,
        documento_id INTEGER,
        entrada_id INTEGER,
        producto_documento_id INTEGER,
        articulo_id INTEGER,
        tipo TEXT,
        descripcion TEXT,
        cantidad_afectada REAL,
        unidad TEXT,
        estado TEXT DEFAULT 'abierta',
        fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(restaurante_id) REFERENCES restaurantes(id),
        FOREIGN KEY(documento_id) REFERENCES documentos_importados(id),
        FOREIGN KEY(entrada_id) REFERENCES entradas_mercancia(id),
        FOREIGN KEY(producto_documento_id) REFERENCES productos_documento(id),
        FOREIGN KEY(articulo_id) REFERENCES articulos(id)
    )
    """)

    conexion.commit()
    conexion.close()
    return restaurante_id
