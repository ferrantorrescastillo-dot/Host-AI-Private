"""
Host AI
--------

Listado oficial de intenciones del sistema.

Todos los motores utilizarán estas constantes para
comunicarse entre ellos.

Nunca escribir las cadenas directamente dentro del código.
"""


# ==========================================
# GENERALES
# ==========================================

NO_ENTENDIDO = "NO_ENTENDIDO"


# ==========================================
# BÚSQUEDA
# ==========================================

BUSCAR = "BUSCAR"

BUSCAR_ARTICULO = "BUSCAR_ARTICULO"

BUSCAR_RECETA = "BUSCAR_RECETA"

BUSCAR_PROVEEDOR = "BUSCAR_PROVEEDOR"

BUSCAR_COMPRA = "BUSCAR_COMPRA"


# ==========================================
# CONSULTAS
# ==========================================

CONSULTAR_PRECIO = "CONSULTAR_PRECIO"

CONSULTAR_STOCK = "CONSULTAR_STOCK"

CONSULTAR_PROVEEDOR = "CONSULTAR_PROVEEDOR"

CONSULTAR_RECETA = "CONSULTAR_RECETA"


# ==========================================
# STOCK
# ==========================================

AÑADIR_STOCK = "AÑADIR_STOCK"

QUITAR_STOCK = "QUITAR_STOCK"

MODIFICAR_STOCK = "MODIFICAR_STOCK"


# ==========================================
# COMPRAS
# ==========================================

CREAR_PEDIDO = "CREAR_PEDIDO"

AÑADIR_COMPRA = "AÑADIR_COMPRA"

ACTUALIZAR_PRECIOS = "ACTUALIZAR_PRECIOS"


# ==========================================
# RECETAS
# ==========================================

CREAR_RECETA = "CREAR_RECETA"

MODIFICAR_RECETA = "MODIFICAR_RECETA"

ELIMINAR_RECETA = "ELIMINAR_RECETA"


# ==========================================
# EVENTOS
# ==========================================

CREAR_EVENTO = "CREAR_EVENTO"

PLANIFICAR_EVENTO = "PLANIFICAR_EVENTO"


# ==========================================
# AUTOMATIZACIONES
# ==========================================

GENERAR_LISTA_COMPRA = "GENERAR_LISTA_COMPRA"

GENERAR_PREVISION = "GENERAR_PREVISION"