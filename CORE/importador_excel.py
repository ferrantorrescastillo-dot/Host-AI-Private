import pandas as pd

from configuracion import ARCHIVO_EXCEL, HOJA_ARTICULOS
from database import (
    conectar,
    obtener_configuracion,
    asegurar_restaurante_demo,
)


def importar_articulos_desde_excel():
    excel_importado = obtener_configuracion("excel_importado", "NO")

    if excel_importado == "SI":
        print("✅ Excel de artículos ya importado anteriormente.")
        return

    restaurante_id = asegurar_restaurante_demo()

    conexion = conectar()
    cursor = conexion.cursor()

    df = pd.read_excel(
        ARCHIVO_EXCEL,
        sheet_name=HOJA_ARTICULOS,
        header=2
    )

    contador_articulos = 0
    contador_proveedores = 0

    for _, fila in df.iterrows():
        nombre = str(fila.iloc[1]).strip()

        if not nombre or nombre.lower() == "nan":
            continue

        proveedor = ""
        precio = None

        if len(fila) > 3:
            proveedor = str(fila.iloc[3]).strip()

        if len(fila) > 5:
            try:
                precio = float(fila.iloc[5])
            except:
                precio = None

        cursor.execute("""
            INSERT INTO articulos (restaurante_id, nombre)
            VALUES (?, ?)
        """, (restaurante_id, nombre))

        articulo_id = cursor.lastrowid
        contador_articulos += 1

        if proveedor and proveedor.lower() != "nan":
            cursor.execute("""
                SELECT id FROM proveedores
                WHERE restaurante_id = ?
                AND nombre = ?
            """, (restaurante_id, proveedor))

            resultado = cursor.fetchone()

            if resultado:
                proveedor_id = resultado["id"]
            else:
                cursor.execute("""
                    INSERT INTO proveedores (restaurante_id, nombre)
                    VALUES (?, ?)
                """, (restaurante_id, proveedor))

                proveedor_id = cursor.lastrowid
                contador_proveedores += 1

            cursor.execute("""
                INSERT INTO articulo_proveedor
                (
                    articulo_id,
                    proveedor_id,
                    precio,
                    es_principal
                )
                VALUES (?, ?, ?, ?)
            """, (
                articulo_id,
                proveedor_id,
                precio,
                1
            ))

    cursor.execute("""
        INSERT OR REPLACE INTO configuracion (clave, valor)
        VALUES (?, ?)
    """, ("excel_importado", "SI"))

    conexion.commit()
    conexion.close()

    print(f"✅ Artículos importados: {contador_articulos}")
    print(f"✅ Proveedores importados: {contador_proveedores}")


def es_hoja_menu(nombre_hoja):
    nombre = nombre_hoja.lower().strip()

    if nombre == HOJA_ARTICULOS.lower():
        return False

    if nombre.startswith("m.p"):
        return False

    if nombre.startswith("mp "):
        return False

    if "plantilla" in nombre:
        return False

    if nombre.startswith("hoja"):
        return False

    return True


def limpiar_texto(valor):
    if valor is None:
        return ""

    texto = str(valor).strip()

    if texto.lower() == "nan":
        return ""

    return texto


def convertir_numero(valor):
    try:
        if valor is None:
            return None

        if str(valor).lower() == "nan":
            return None

        return float(valor)
    except:
        return None


def importar_menus_desde_excel():
    menus_importados = obtener_configuracion("menus_importados", "NO")

    if menus_importados == "SI":
        print("✅ Menús ya importados anteriormente.")
        return

    restaurante_id = asegurar_restaurante_demo()

    conexion = conectar()
    cursor = conexion.cursor()

    excel = pd.ExcelFile(ARCHIVO_EXCEL)

    contador_menus = 0
    contador_platos = 0

    for hoja in excel.sheet_names:

        if not es_hoja_menu(hoja):
            continue

        df = pd.read_excel(
            ARCHIVO_EXCEL,
            sheet_name=hoja,
            header=None
        )

        nombre_menu = hoja

        for _, fila in df.iterrows():
            posible_nombre = limpiar_texto(fila.iloc[0])

            if posible_nombre:
                nombre_menu = posible_nombre
                break

        cursor.execute("""
            INSERT INTO menus
            (
                restaurante_id,
                nombre,
                hoja_excel
            )
            VALUES (?, ?, ?)
        """, (
            restaurante_id,
            nombre_menu,
            hoja
        ))

        menu_id = cursor.lastrowid
        contador_menus += 1

        orden = 1

        for _, fila in df.iterrows():

            nombre_plato = limpiar_texto(fila.iloc[0])

            if not nombre_plato:
                continue

            nombre_lower = nombre_plato.lower()

            palabras_ignoradas = [
                "menu",
                "menú",
                "aperitivo",
                "entrantes",
                "postres",
                "escandallo",
                "calçotada. aperitivo carta",
                "p.v.p",
            ]

            if any(palabra in nombre_lower for palabra in palabras_ignoradas):
                continue

            cantidad = convertir_numero(fila.iloc[1]) if len(fila) > 1 else None
            precio_unitario = convertir_numero(fila.iloc[2]) if len(fila) > 2 else None
            coste_racion = convertir_numero(fila.iloc[3]) if len(fila) > 3 else None

            if cantidad is None and precio_unitario is None and coste_racion is None:
                continue

            cursor.execute("""
                INSERT INTO platos_menu
                (
                    menu_id,
                    nombre,
                    cantidad,
                    precio_unitario,
                    coste_racion,
                    orden
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                menu_id,
                nombre_plato,
                cantidad,
                precio_unitario,
                coste_racion,
                orden
            ))

            orden += 1
            contador_platos += 1

    cursor.execute("""
        INSERT OR REPLACE INTO configuracion (clave, valor)
        VALUES (?, ?)
    """, ("menus_importados", "SI"))

    conexion.commit()
    conexion.close()

    print(f"✅ Menús importados: {contador_menus}")
    print(f"✅ Platos de menú importados: {contador_platos}")