from database import conectar
from IMPORTADORES.importador import importar_documento_desde_archivo
from SERVICIOS.comparador_articulos import comparar_documento
from SERVICIOS.actualizador_documentos import aplicar_documento
from SERVICIOS.entradas_mercancia import registrar_entrada_desde_documento, listar_entradas, listar_incidencias


def _ultimo_documento_id(restaurante_id=1):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT id FROM documentos_importados
        WHERE restaurante_id = ?
        ORDER BY id DESC
        LIMIT 1
    """, (restaurante_id,))
    r = cursor.fetchone()
    conexion.close()
    return None if r is None else r["id"]


def importar_documento(restaurante_id=1):
    ruta = input("\nRuta del archivo PDF/Word/TXT: ").strip().replace('"', '')
    if not ruta:
        print("\nNo has indicado ruta.\n")
        return
    try:
        documento_id, documento = importar_documento_desde_archivo(ruta, restaurante_id, guardar=True)
    except Exception as exc:
        print(f"\n❌ Error importando documento: {exc}\n")
        return

    print("\n========== DOCUMENTO IMPORTADO ==========")
    print(documento.resumen())
    print("\nProductos detectados:")
    for producto in documento.productos[:25]:
        precio = producto.precio_unitario if producto.precio_unitario is not None else "-"
        print(f"• {producto.nombre} | Cant: {producto.cantidad} | Precio: {precio} | Importe: {producto.importe}")
    if len(documento.productos) > 25:
        print(f"... y {len(documento.productos) - 25} productos más")
    print(f"\n✅ Documento guardado con ID {documento_id}.\n")


def listar_documentos(restaurante_id=1):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT id, tipo_documento, proveedor, fecha_documento, total, estado
        FROM documentos_importados
        WHERE restaurante_id = ?
        ORDER BY id DESC
        LIMIT 20
    """, (restaurante_id,))
    documentos = cursor.fetchall()
    conexion.close()

    print("\n========== DOCUMENTOS IMPORTADOS ==========")
    if not documentos:
        print("No hay documentos importados.\n")
        return
    for d in documentos:
        print(f"{d['id']}. {d['tipo_documento']} | {d['proveedor']} | {d['fecha_documento']} | Total: {d['total']} | {d['estado']}")
    print()


def vista_previa_comparacion(restaurante_id=1):
    documento_id_txt = input("\nID del documento (vacío = último): ").strip()
    documento_id = int(documento_id_txt) if documento_id_txt.isdigit() else _ultimo_documento_id(restaurante_id)
    if documento_id is None:
        print("\nNo hay documentos.\n")
        return

    resultados = comparar_documento(documento_id, restaurante_id)

    print("\n========== VISTA PREVIA DE CAMBIOS ==========")
    crear = actualizar = revisar = 0
    for r in resultados:
        accion = r["accion"]
        if accion == "crear_articulo":
            crear += 1
        elif accion == "actualizar_precio":
            actualizar += 1
        else:
            revisar += 1

        print(f"\n• {r['nombre_detectado']}")
        if r["articulo_id"]:
            print(f"  Coincide con: {r['articulo_nombre']} ({r['confianza']}%)")
            print(f"  Precio actual: {r['precio_actual']}")
            print(f"  Precio nuevo : {r['precio_nuevo']}")
            print(f"  Acción       : {accion}")
        else:
            print("  No encontrado en artículos.")
            print("  Acción       : crear artículo")

    print("\n---------- RESUMEN ----------")
    print(f"Crear artículos      : {crear}")
    print(f"Actualizar/relacionar: {actualizar}")
    print(f"Revisar              : {revisar}")
    print("\nNo se ha modificado la base todavía. Usa 'Aplicar cambios' si estás de acuerdo.\n")


def aplicar_cambios_documento(restaurante_id=1):
    documento_id_txt = input("\nID del documento (vacío = último): ").strip()
    documento_id = int(documento_id_txt) if documento_id_txt.isdigit() else _ultimo_documento_id(restaurante_id)
    if documento_id is None:
        print("\nNo hay documentos.\n")
        return

    confirmar = input("\nEsto creará artículos nuevos y actualizará precios. ¿Confirmar? (s/n): ").lower().strip()
    if confirmar != "s":
        print("\nCancelado.\n")
        return

    # Asegura que exista comparación antes de aplicar.
    comparar_documento(documento_id, restaurante_id)
    resumen = aplicar_documento(documento_id, restaurante_id)

    print("\n✅ Cambios aplicados.")
    print(f"Productos procesados : {resumen['productos']}")
    print(f"Artículos creados    : {resumen['creados']}")
    print(f"Artículos actualizados: {resumen['actualizados']}")
    print(f"Equivalencias guardadas: {resumen['equivalencias']}\n")



def registrar_entrada_documento(restaurante_id=1):
    documento_id_txt = input("\nID del documento (vacío = último): ").strip()
    documento_id = int(documento_id_txt) if documento_id_txt.isdigit() else _ultimo_documento_id(restaurante_id)
    if documento_id is None:
        print("\nNo hay documentos.\n")
        return

    print("\nHost AI:")
    print("Voy a registrar una entrada de mercancía desde este documento.")
    print("Esto sumará cantidades al stock de artículos relacionados.")
    confirmar = input("\n¿Confirmar entrada de mercancía? (s/n): ").lower().strip()
    if confirmar != "s":
        print("\nCancelado.\n")
        return

    try:
        resumen = registrar_entrada_desde_documento(documento_id, restaurante_id)
    except Exception as exc:
        print(f"\n❌ Error registrando entrada: {exc}\n")
        return

    if resumen.get("ya_existia"):
        print("\n⚠️ Este documento ya tenía una entrada de mercancía registrada.")
        print(f"Entrada ID: {resumen['entrada_id']}\n")
        return

    print("\n✅ Entrada de mercancía registrada.")
    print(f"Entrada ID          : {resumen['entrada_id']}")
    print(f"Líneas procesadas   : {resumen['lineas']}")
    print(f"Stock actualizado   : {resumen['stock_actualizado']}")
    print(f"Sin artículo        : {resumen.get('sin_articulo', 0)}")
    print(f"Incidencias creadas : {resumen['incidencias']}\n")


def ver_resumen_recepcion(restaurante_id=1):
    print("\n========== RESUMEN RECEPCIÓN ==========")
    entradas = listar_entradas(restaurante_id, limite=10)
    incidencias = listar_incidencias(restaurante_id, limite=10)

    print("\nÚltimas entradas:")
    if not entradas:
        print("No hay entradas registradas.")
    else:
        for entrada in entradas:
            print(f"• {entrada['id']} | {entrada['proveedor']} | {entrada['fecha_documento']} | {entrada['estado']}")

    print("\nIncidencias abiertas:")
    abiertas = [i for i in incidencias if i['estado'] == 'abierta']
    if not abiertas:
        print("No hay incidencias abiertas.")
    else:
        for inc in abiertas:
            print(f"• {inc['tipo']}: {inc['descripcion']}")
    print()

def menu_importadores(restaurante_id=1):
    while True:
        print("\n========== IMPORTADOR DE DOCUMENTOS ==========")
        print("1. Importar documento desde archivo")
        print("2. Ver documentos importados")
        print("3. Vista previa / comparar con artículos")
        print("4. Aplicar cambios del documento")
        print("5. Registrar entrada de mercancía desde documento")
        print("6. Ver resumen de recepción")
        print("0. Volver")
        opcion = input("\n¿Qué quieres hacer? ")

        if opcion == "1":
            importar_documento(restaurante_id)
        elif opcion == "2":
            listar_documentos(restaurante_id)
        elif opcion == "3":
            vista_previa_comparacion(restaurante_id)
        elif opcion == "4":
            aplicar_cambios_documento(restaurante_id)
        elif opcion == "5":
            registrar_entrada_documento(restaurante_id)
        elif opcion == "6":
            ver_resumen_recepcion(restaurante_id)
        elif opcion == "0":
            break
        else:
            print("\n⚠️ Opción no válida.")
