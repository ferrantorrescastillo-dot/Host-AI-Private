from datetime import datetime, date

from repositorio import (
    contar_articulos,
    contar_proveedores,
    contar_menus,
    contar_eventos,
    contar_tareas_pendientes,
)
from database import conectar


def _parse_fecha(fecha_texto):
    if not fecha_texto:
        return None
    texto = str(fecha_texto).strip()
    formatos = ["%Y-%m-%d", "%d/%m/%Y", "%d/%m/%y", "%d-%m-%Y", "%d-%m-%y"]
    for formato in formatos:
        try:
            return datetime.strptime(texto, formato).date()
        except ValueError:
            continue
    return None


def _dias_hasta(fecha_texto):
    fecha = _parse_fecha(fecha_texto)
    if fecha is None:
        return None
    return (fecha - date.today()).days


def dashboard_cocina(restaurante_id=1):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT eventos.nombre, eventos.fecha, eventos.numero_personas, menus.nombre AS menu_nombre
        FROM eventos
        LEFT JOIN menus ON eventos.menu_id = menus.id
        WHERE eventos.restaurante_id = ?
        ORDER BY eventos.fecha
        LIMIT 8
    """, (restaurante_id,))
    eventos = cursor.fetchall()

    cursor.execute("""
        SELECT tareas_produccion.nombre, tareas_produccion.cantidad, tareas_produccion.unidad,
               tareas_produccion.estado, tareas_produccion.rol_recomendado,
               tareas_produccion.persona_asignada, tareas_produccion.tiempo_estimado_min,
               tareas_produccion.prioridad,
               eventos.nombre AS evento_nombre, eventos.fecha AS evento_fecha
        FROM tareas_produccion
        JOIN producciones ON tareas_produccion.produccion_id = producciones.id
        JOIN eventos ON producciones.evento_id = eventos.id
        WHERE tareas_produccion.estado != 'hecha'
        ORDER BY eventos.fecha, tareas_produccion.orden
        LIMIT 10
    """)
    tareas = cursor.fetchall()

    cursor.execute("""
        SELECT id, nombre, cantidad, unidad, ubicacion, fecha_caducidad, congelado
        FROM produccion_disponible
        WHERE restaurante_id = ?
        AND cantidad != 0
        ORDER BY fecha_caducidad, nombre
        LIMIT 10
    """, (restaurante_id,))
    disponible = cursor.fetchall()

    conexion.close()

    print("\n======================================")
    print("        DASHBOARD COCINA")
    print("======================================")
    print("Buenos días. Esto es lo importante ahora:\n")
    print(f"📦 Artículos registrados : {contar_articulos(restaurante_id)}")
    print(f"🏢 Proveedores           : {contar_proveedores(restaurante_id)}")
    print(f"🍽 Menús                 : {contar_menus(restaurante_id)}")
    print(f"📅 Eventos               : {contar_eventos(restaurante_id)}")
    print(f"🍳 Tareas pendientes     : {contar_tareas_pendientes()}")

    tareas_asignadas = [t for t in tareas if t["persona_asignada"]]
    print(f"👥 Tareas asignadas      : {len(tareas_asignadas)}")

    print("\n🔴 PRIMERA TAREA RECOMENDADA")
    print("--------------------------------------")
    if tareas:
        primera = tareas[0]
        print(f"Empieza por: {primera['nombre']}")
        print(f"Evento     : {primera['evento_nombre']}")
        print(f"Previsto   : {primera['cantidad']} {primera['unidad']}")
    else:
        print("No hay tareas de producción pendientes.")

    print("\n📅 PRÓXIMOS EVENTOS")
    print("--------------------------------------")
    if not eventos:
        print("No hay eventos creados.")
    else:
        for evento in eventos:
            dias = _dias_hasta(evento["fecha"])
            if dias is None:
                tiempo = "fecha sin interpretar"
            elif dias == 0:
                tiempo = "hoy"
            elif dias == 1:
                tiempo = "mañana"
            elif dias > 1:
                tiempo = f"en {dias} días"
            else:
                tiempo = f"hace {abs(dias)} días"
            print(f"• {evento['fecha']} ({tiempo}) - {evento['nombre']} ({evento['numero_personas']} pax)")
            print(f"  Menú: {evento['menu_nombre']}")

    print("\n🍳 PRODUCCIÓN PENDIENTE")
    print("--------------------------------------")
    if not tareas:
        print("No hay tareas pendientes.")
    else:
        for tarea in tareas:
            print(f"• {tarea['nombre']} - {tarea['cantidad']} {tarea['unidad']}")
            print(f"  Evento: {tarea['evento_nombre']}")
            if tarea["persona_asignada"]:
                print(f"  Asignado: {tarea['persona_asignada']} ({tarea['rol_recomendado'] or '-'})")
                print(f"  Tiempo  : {tarea['tiempo_estimado_min'] or '-'} min · Prioridad: {tarea['prioridad'] or 'media'}")

    print("\n📦 PRODUCCIÓN DISPONIBLE")
    print("--------------------------------------")
    if not disponible:
        print("No hay producción disponible registrada.")
    else:
        for item in disponible:
            dias = _dias_hasta(item["fecha_caducidad"])
            if item["fecha_caducidad"]:
                if dias is not None and dias <= 1:
                    aviso = "⚠ caduca pronto"
                elif dias is not None and dias < 0:
                    aviso = "❌ caducada"
                else:
                    aviso = f"caduca: {item['fecha_caducidad']}"
            else:
                aviso = "sin caducidad"
            congelado = "congelado" if item["congelado"] else "fresco"
            print(f"• {item['nombre']} - {item['cantidad']} {item['unidad'] or ''}")
            print(f"  {congelado} · {aviso} · {item['ubicacion'] or '-'}")

    print("\nHost AI:")
    if tareas and not tareas_asignadas:
        print("Mi recomendación: entra en Planificación y reparte las tareas por roles antes de empezar.\n")
    else:
        print("Mi recomendación: revisa primero la tarea recomendada y luego confirma consumos reales del día.\n")

    input("Pulsa ENTER para volver al menú...")


def dashboard_rentabilidad(restaurante_id=1):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT menus.id, menus.nombre,
               COUNT(platos_menu.id) AS total_platos,
               SUM(COALESCE(platos_menu.coste_racion, 0)) AS coste_estimado
        FROM menus
        LEFT JOIN platos_menu ON menus.id = platos_menu.menu_id
        WHERE menus.restaurante_id = ?
        AND menus.activo = 1
        GROUP BY menus.id, menus.nombre
        ORDER BY coste_estimado DESC
    """, (restaurante_id,))
    menus = cursor.fetchall()

    cursor.execute("""
        SELECT nombre,
               COUNT(*) AS veces,
               AVG(cantidad_prevista) AS prevista_media,
               AVG(cantidad_real) AS real_media,
               AVG(porcentaje_diferencia) AS diferencia_media,
               unidad
        FROM rendimientos_elaboracion
        WHERE restaurante_id = ?
        GROUP BY nombre, unidad
        ORDER BY ABS(COALESCE(diferencia_media, 0)) DESC
        LIMIT 8
    """, (restaurante_id,))
    rendimientos = cursor.fetchall()

    conexion.close()

    print("\n======================================")
    print("      DASHBOARD RENTABILIDAD")
    print("======================================")
    print("Versión básica: todavía sin TPV ni facturación real.\n")

    if menus:
        print("🍽 MENÚS CON MAYOR COSTE ESTIMADO")
        print("--------------------------------------")
        for menu in menus[:10]:
            coste = round(menu["coste_estimado"] or 0, 2)
            print(f"• {menu['nombre']}")
            print(f"  Platos: {menu['total_platos']}")
            print(f"  Coste estimado actual: {coste}")
            print()
    else:
        print("No hay datos de menús para analizar.\n")

    print("📊 RENDIMIENTOS REALES")
    print("--------------------------------------")
    if not rendimientos:
        print("Todavía no hay suficientes rendimientos registrados.")
    else:
        for item in rendimientos:
            diferencia = item["diferencia_media"]
            diferencia_texto = "-" if diferencia is None else f"{round(diferencia, 2)} %"
            print(f"• {item['nombre']}")
            print(f"  Previsto medio: {round(item['prevista_media'] or 0, 2)} {item['unidad'] or ''}")
            print(f"  Real medio    : {round(item['real_media'] or 0, 2)} {item['unidad'] or ''}")
            print(f"  Diferencia    : {diferencia_texto}")
            print()

    print("Host AI:")
    print("Cuando conectemos ventas, compras y stock, aquí diré dónde ganas y dónde pierdes dinero.\n")

    input("Pulsa ENTER para volver al menú...")
