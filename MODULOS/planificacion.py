from datetime import date, datetime, timedelta

from database import conectar, asegurar_restaurante_demo


ROLES_BASE = [
    ("Ayudante", 1, "Limpieza, cortes, pesajes, apoyo y tareas básicas."),
    ("Cocinero", 2, "Elaboraciones, fuegos, producción y tareas de cocina."),
    ("Jefe de partida", 3, "Tareas finales, supervisión parcial y elaboraciones delicadas."),
    ("Jefe de cocina", 4, "Supervisión, organización, control de calidad y decisiones."),
]


def inicializar_roles_base(restaurante_id=1):
    conexion = conectar()
    cursor = conexion.cursor()

    for nombre, nivel, descripcion in ROLES_BASE:
        cursor.execute("""
            INSERT OR IGNORE INTO roles_cocina
            (
                restaurante_id,
                nombre,
                nivel_responsabilidad,
                descripcion,
                activo
            )
            VALUES (?, ?, ?, ?, ?)
        """, (restaurante_id, nombre, nivel, descripcion, 1))

    conexion.commit()
    conexion.close()


def obtener_roles(restaurante_id=1):
    inicializar_roles_base(restaurante_id)

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id, nombre, nivel_responsabilidad, descripcion
        FROM roles_cocina
        WHERE restaurante_id = ?
        AND activo = 1
        ORDER BY nivel_responsabilidad
    """, (restaurante_id,))

    roles = cursor.fetchall()
    conexion.close()
    return roles


def mostrar_roles(restaurante_id=1):
    roles = obtener_roles(restaurante_id)

    print("\n========== ROLES DE COCINA ==========\n")

    for rol in roles:
        print(f"{rol['id']}. {rol['nombre']}")
        print(f"   Nivel: {rol['nivel_responsabilidad']}")
        print(f"   {rol['descripcion']}")
        print()

    input("Pulsa ENTER para volver...")


def mostrar_equipo(restaurante_id=1):
    inicializar_roles_base(restaurante_id)

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            personal_cocina.id,
            personal_cocina.nombre,
            personal_cocina.velocidad,
            personal_cocina.observaciones,
            roles_cocina.nombre AS rol_nombre
        FROM personal_cocina
        LEFT JOIN roles_cocina ON personal_cocina.rol_id = roles_cocina.id
        WHERE personal_cocina.restaurante_id = ?
        AND personal_cocina.activo = 1
        ORDER BY roles_cocina.nivel_responsabilidad, personal_cocina.nombre
    """, (restaurante_id,))

    personas = cursor.fetchall()
    conexion.close()

    print("\n========== EQUIPO DE COCINA ==========\n")

    if not personas:
        print("Todavía no hay personal registrado.")
        print("Puedes añadir ayudantes, cocineros o jefes de partida desde este menú.\n")
        input("Pulsa ENTER para volver...")
        return

    for persona in personas:
        print(f"{persona['id']}. {persona['nombre']}")
        print(f"   Rol      : {persona['rol_nombre'] or '-'}")
        print(f"   Velocidad: {persona['velocidad']} %")
        if persona["observaciones"]:
            print(f"   Nota     : {persona['observaciones']}")
        print()

    input("Pulsa ENTER para volver...")


def seleccionar_rol(restaurante_id=1):
    roles = obtener_roles(restaurante_id)

    print("\n========== SELECCIONAR ROL ==========")

    for rol in roles:
        print(f"{rol['id']}. {rol['nombre']}")

    opcion = input("\nRol: ").strip()

    if not opcion.isdigit():
        print("\nOpción incorrecta.")
        return None

    rol_id = int(opcion)

    for rol in roles:
        if rol["id"] == rol_id:
            return rol_id

    print("\nRol no encontrado.")
    return None


def añadir_persona(restaurante_id=1):
    inicializar_roles_base(restaurante_id)

    print("\n========== AÑADIR PERSONA ==========")

    nombre = input("Nombre: ").strip()

    if not nombre:
        print("\nNecesito un nombre.")
        return

    rol_id = seleccionar_rol(restaurante_id)

    if rol_id is None:
        return

    velocidad_texto = input("Velocidad estimada % [100]: ").strip()

    if velocidad_texto.isdigit():
        velocidad = int(velocidad_texto)
    else:
        velocidad = 100

    observaciones = input("Observaciones: ").strip()

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO personal_cocina
        (
            restaurante_id,
            nombre,
            rol_id,
            velocidad,
            activo,
            observaciones
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (restaurante_id, nombre, rol_id, velocidad, 1, observaciones))

    conexion.commit()
    conexion.close()

    print("\n✅ Persona añadida correctamente.\n")


def recomendar_rol_para_tarea(nombre_tarea):
    texto = (nombre_tarea or "").lower()

    palabras_ayudante = [
        "pelar", "cortar", "limpiar", "lavar", "picar", "pesar",
        "rallar", "porcionar verduras", "mise", "montar bandejas"
    ]

    palabras_jefe = [
        "revisar", "supervisar", "finalizar", "emplatar", "pase", "terminar",
        "reducir salsa", "marcar solomillo", "marcar carne"
    ]

    palabras_cocinero = [
        "fumet", "fondo", "caldo", "demi", "bechamel", "salsa", "crema",
        "puré", "arroz", "carrillera", "meloso", "cocer", "guisar", "confitar",
        "croqueta", "brandada", "pilpil", "alioli"
    ]

    if any(palabra in texto for palabra in palabras_ayudante):
        return "Ayudante"

    if any(palabra in texto for palabra in palabras_jefe):
        return "Jefe de partida"

    if any(palabra in texto for palabra in palabras_cocinero):
        return "Cocinero"

    return "Cocinero"


def estimar_minutos_tarea(nombre_tarea):
    texto = (nombre_tarea or "").lower()

    reglas = [
        (["fumet", "fondo", "caldo"], 180),
        (["demi", "glace"], 240),
        (["bechamel", "croqueta"], 90),
        (["puré", "crema"], 60),
        (["salsa", "alioli", "pilpil"], 45),
        (["cortar", "pelar", "limpiar"], 45),
        (["marcar", "emplatar", "pase"], 30),
    ]

    for palabras, minutos in reglas:
        if any(palabra in texto for palabra in palabras):
            return minutos

    return 60


def prioridad_tarea(nombre_tarea):
    texto = (nombre_tarea or "").lower()

    if any(p in texto for p in ["fumet", "fondo", "demi", "caldo", "carrillera", "meloso"]):
        return "alta"

    if any(p in texto for p in ["bechamel", "croqueta", "crema", "puré"]):
        return "media"

    return "media"


def obtener_personas_por_rol(restaurante_id=1):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            personal_cocina.nombre,
            personal_cocina.velocidad,
            roles_cocina.nombre AS rol_nombre
        FROM personal_cocina
        LEFT JOIN roles_cocina ON personal_cocina.rol_id = roles_cocina.id
        WHERE personal_cocina.restaurante_id = ?
        AND personal_cocina.activo = 1
        ORDER BY roles_cocina.nivel_responsabilidad DESC, personal_cocina.velocidad DESC
    """, (restaurante_id,))

    personas = cursor.fetchall()
    conexion.close()

    resultado = {}

    for persona in personas:
        rol = persona["rol_nombre"] or "Cocinero"
        resultado.setdefault(rol, []).append(persona)

    return resultado


def elegir_persona_para_rol(personas_por_rol, rol_recomendado, contador_por_persona):
    candidatos = personas_por_rol.get(rol_recomendado, [])

    if not candidatos and rol_recomendado == "Ayudante":
        candidatos = personas_por_rol.get("Cocinero", [])

    if not candidatos and rol_recomendado == "Cocinero":
        candidatos = personas_por_rol.get("Jefe de partida", []) or personas_por_rol.get("Jefe de cocina", [])

    if not candidatos and rol_recomendado == "Jefe de partida":
        candidatos = personas_por_rol.get("Jefe de cocina", []) or personas_por_rol.get("Cocinero", [])

    if not candidatos:
        return "Sin asignar"

    candidatos_ordenados = sorted(
        candidatos,
        key=lambda p: (contador_por_persona.get(p["nombre"], 0), -(p["velocidad"] or 100))
    )

    elegido = candidatos_ordenados[0]["nombre"]
    contador_por_persona[elegido] = contador_por_persona.get(elegido, 0) + 1
    return elegido


def asignar_tareas_pendientes(restaurante_id=1):
    inicializar_roles_base(restaurante_id)
    personas_por_rol = obtener_personas_por_rol(restaurante_id)
    contador_por_persona = {}

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            tareas_produccion.id,
            tareas_produccion.nombre,
            eventos.restaurante_id
        FROM tareas_produccion
        JOIN producciones ON tareas_produccion.produccion_id = producciones.id
        JOIN eventos ON producciones.evento_id = eventos.id
        WHERE eventos.restaurante_id = ?
        AND tareas_produccion.estado != 'hecha'
        ORDER BY eventos.fecha, tareas_produccion.orden
    """, (restaurante_id,))

    tareas = cursor.fetchall()

    if not tareas:
        conexion.close()
        print("\nNo hay tareas pendientes para asignar.\n")
        input("Pulsa ENTER para volver...")
        return

    for tarea in tareas:
        rol = recomendar_rol_para_tarea(tarea["nombre"])
        persona = elegir_persona_para_rol(personas_por_rol, rol, contador_por_persona)
        minutos = estimar_minutos_tarea(tarea["nombre"])
        prioridad = prioridad_tarea(tarea["nombre"])

        cursor.execute("""
            UPDATE tareas_produccion
            SET rol_recomendado = ?,
                persona_asignada = ?,
                tiempo_estimado_min = ?,
                prioridad = ?
            WHERE id = ?
        """, (rol, persona, minutos, prioridad, tarea["id"]))

    conexion.commit()
    conexion.close()

    print("\n✅ Tareas asignadas por rol y persona.")
    print("Host AI ha repartido la producción según responsabilidad y tipo de tarea.\n")
    input("Pulsa ENTER para volver...")


def mostrar_planning(restaurante_id=1):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            tareas_produccion.nombre,
            tareas_produccion.cantidad,
            tareas_produccion.unidad,
            tareas_produccion.estado,
            tareas_produccion.rol_recomendado,
            tareas_produccion.persona_asignada,
            tareas_produccion.tiempo_estimado_min,
            tareas_produccion.prioridad,
            tareas_produccion.hora_inicio_estimada,
            tareas_produccion.hora_fin_estimada,
            eventos.nombre AS evento_nombre,
            eventos.fecha AS evento_fecha
        FROM tareas_produccion
        JOIN producciones ON tareas_produccion.produccion_id = producciones.id
        JOIN eventos ON producciones.evento_id = eventos.id
        WHERE eventos.restaurante_id = ?
        AND tareas_produccion.estado != 'hecha'
        ORDER BY
            CASE tareas_produccion.prioridad
                WHEN 'alta' THEN 1
                WHEN 'media' THEN 2
                ELSE 3
            END,
            eventos.fecha,
            tareas_produccion.orden
    """, (restaurante_id,))

    tareas = cursor.fetchall()
    conexion.close()

    print("\n========== PLANNING DE PRODUCCIÓN ==========")

    if not tareas:
        print("\nNo hay tareas pendientes.\n")
        input("Pulsa ENTER para volver...")
        return

    tareas_por_persona = {}

    for tarea in tareas:
        persona = tarea["persona_asignada"] or "Sin asignar"
        tareas_por_persona.setdefault(persona, []).append(tarea)

    for persona, lista in tareas_por_persona.items():
        print(f"\n👤 {persona}")
        print("--------------------------------------")

        total_minutos = 0

        for tarea in lista:
            minutos = tarea["tiempo_estimado_min"] or 0
            total_minutos += minutos
            prioridad = tarea["prioridad"] or "media"
            rol = tarea["rol_recomendado"] or "-"

            inicio = tarea["hora_inicio_estimada"] if "hora_inicio_estimada" in tarea.keys() else None
            fin = tarea["hora_fin_estimada"] if "hora_fin_estimada" in tarea.keys() else None
            horario = f"{inicio}-{fin}" if inicio and fin else "sin horario"
            print(f"• {tarea['nombre']}")
            print(f"  Horario  : {horario}")
            print(f"  Evento   : {tarea['evento_nombre']} ({tarea['evento_fecha']})")
            print(f"  Cantidad : {tarea['cantidad']} {tarea['unidad']}")
            print(f"  Rol      : {rol}")
            print(f"  Prioridad: {prioridad}")
            print(f"  Tiempo   : {minutos} min")
            print()

        horas = round(total_minutos / 60, 2)
        print(f"Total estimado para {persona}: {horas} h")

    print("\nHost AI:")
    print("Esta es una primera distribución automática. Revísala como jefe de cocina.\n")
    input("Pulsa ENTER para volver...")


def dashboard_planificacion(restaurante_id=1):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM personal_cocina
        WHERE restaurante_id = ?
        AND activo = 1
    """, (restaurante_id,))
    total_personas = cursor.fetchone()["total"]

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM tareas_produccion
        JOIN producciones ON tareas_produccion.produccion_id = producciones.id
        JOIN eventos ON producciones.evento_id = eventos.id
        WHERE eventos.restaurante_id = ?
        AND tareas_produccion.estado != 'hecha'
    """, (restaurante_id,))
    tareas_pendientes = cursor.fetchone()["total"]

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM tareas_produccion
        JOIN producciones ON tareas_produccion.produccion_id = producciones.id
        JOIN eventos ON producciones.evento_id = eventos.id
        WHERE eventos.restaurante_id = ?
        AND tareas_produccion.estado != 'hecha'
        AND (tareas_produccion.persona_asignada IS NULL OR tareas_produccion.persona_asignada = '')
    """, (restaurante_id,))
    sin_asignar = cursor.fetchone()["total"]

    conexion.close()

    print("\n========== DASHBOARD PLANIFICACIÓN ==========")
    print(f"👥 Personal activo        : {total_personas}")
    print(f"🍳 Tareas pendientes     : {tareas_pendientes}")
    print(f"⚠️ Tareas sin asignar     : {sin_asignar}")

    if tareas_pendientes and sin_asignar:
        print("\nHost AI:")
        print("Hay tareas pendientes sin repartir. Te recomiendo generar la asignación automática.")
    elif tareas_pendientes:
        print("\nHost AI:")
        print("La producción está repartida. Revisa el planning antes de empezar.")
    else:
        print("\nHost AI:")
        print("No hay tareas de producción pendientes ahora mismo.")

    print()
    input("Pulsa ENTER para volver...")



def _parse_hora(hora_texto):
    texto = (hora_texto or "").strip()
    if not texto:
        texto = "08:00"
    for formato in ["%H:%M", "%H.%M"]:
        try:
            return datetime.strptime(texto, formato)
        except ValueError:
            pass
    print("\nHora no válida. Uso 08:00 por defecto.")
    return datetime.strptime("08:00", "%H:%M")


def _hora_texto(dt):
    return dt.strftime("%H:%M")


def _orden_planificacion(tarea):
    prioridad = tarea["prioridad"] or "media"
    minutos = tarea["tiempo_estimado_min"] or 60
    nombre = (tarea["nombre"] or "").lower()

    prioridad_num = {"alta": 1, "media": 2, "baja": 3}.get(prioridad, 2)

    # Tareas largas o con cocción/fondo primero.
    bonus_larga = 0 if minutos >= 120 else 1
    bonus_fondo = 0 if any(p in nombre for p in ["fumet", "fondo", "caldo", "demi", "glace", "carrillera", "meloso"]) else 1

    return (prioridad_num, bonus_fondo, bonus_larga, tarea["evento_fecha"] or "", tarea["orden"] or 999)


def _nota_para_tarea(nombre_tarea):
    texto = (nombre_tarea or "").lower()

    if any(p in texto for p in ["fumet", "fondo", "caldo", "demi", "glace"]):
        return "Tarea larga: empieza pronto. Mientras reduce o hierve, avanza cortes, mise en place o preparaciones cortas."

    if any(p in texto for p in ["bechamel", "croqueta"]):
        return "Tiene fase de enfriado: hazla pronto para no bloquear la producción más tarde."

    if any(p in texto for p in ["alioli", "pilpil", "salsa"]):
        return "Tarea corta: encájala mientras otra elaboración está en cocción o reposo."

    if any(p in texto for p in ["pelar", "cortar", "limpiar", "picar"]):
        return "Tarea ideal para ayudante. Avánzala mientras el cocinero trabaja fondos o fuegos."

    if any(p in texto for p in ["marcar", "emplatar", "pase", "terminar"]):
        return "Tarea final o delicada: dejar para perfil con más responsabilidad o cerca del servicio."

    return "Revisar como jefe de cocina y ajustar si hace falta."


def generar_horario_inteligente(restaurante_id=1):
    """Genera un horario simple por persona a partir de tareas ya asignadas."""
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            tareas_produccion.id,
            tareas_produccion.nombre,
            tareas_produccion.cantidad,
            tareas_produccion.unidad,
            tareas_produccion.estado,
            tareas_produccion.rol_recomendado,
            tareas_produccion.persona_asignada,
            tareas_produccion.tiempo_estimado_min,
            tareas_produccion.prioridad,
            tareas_produccion.orden,
            eventos.nombre AS evento_nombre,
            eventos.fecha AS evento_fecha
        FROM tareas_produccion
        JOIN producciones ON tareas_produccion.produccion_id = producciones.id
        JOIN eventos ON producciones.evento_id = eventos.id
        WHERE eventos.restaurante_id = ?
        AND tareas_produccion.estado != 'hecha'
        ORDER BY eventos.fecha, tareas_produccion.orden
    """, (restaurante_id,))

    tareas = cursor.fetchall()

    if not tareas:
        conexion.close()
        print("\nNo hay tareas pendientes para planificar.\n")
        input("Pulsa ENTER para volver...")
        return

    sin_asignar = [t for t in tareas if not t["persona_asignada"]]
    if sin_asignar:
        conexion.close()
        print("\nHay tareas sin persona asignada.")
        print("Primero usa: 5. Asignar tareas pendientes automáticamente\n")
        input("Pulsa ENTER para volver...")
        return

    hora_inicio_texto = input("\nHora de inicio de la jornada [08:00]: ").strip()
    hora_inicio = _parse_hora(hora_inicio_texto)

    tareas_por_persona = {}
    for tarea in tareas:
        persona = tarea["persona_asignada"] or "Sin asignar"
        tareas_por_persona.setdefault(persona, []).append(tarea)

    print("\n========== HORARIO INTELIGENTE ==========")
    print("Host AI ha ordenado primero tareas largas, fondos, cocciones y prioridades altas.\n")

    for persona, lista in tareas_por_persona.items():
        momento = hora_inicio
        lista_ordenada = sorted(lista, key=_orden_planificacion)

        print(f"👤 {persona}")
        print("--------------------------------------")

        total_minutos = 0

        for tarea in lista_ordenada:
            minutos = tarea["tiempo_estimado_min"] or 60
            inicio = momento
            fin = momento + timedelta(minutes=minutos)
            nota = _nota_para_tarea(tarea["nombre"])

            cursor.execute("""
                UPDATE tareas_produccion
                SET hora_inicio_estimada = ?,
                    hora_fin_estimada = ?,
                    nota_planificacion = ?
                WHERE id = ?
            """, (_hora_texto(inicio), _hora_texto(fin), nota, tarea["id"]))

            print(f"{_hora_texto(inicio)} - {_hora_texto(fin)}")
            print(f"• {tarea['nombre']}")
            print(f"  Evento: {tarea['evento_nombre']}")
            print(f"  Nota  : {nota}")
            print()

            momento = fin
            total_minutos += minutos

        print(f"Total estimado: {round(total_minutos / 60, 2)} h\n")

    conexion.commit()
    conexion.close()

    print("Host AI:")
    print("Este horario es una primera propuesta. Ajusta como jefe de cocina según maquinaria, ritmo real y prioridades del día.\n")
    input("Pulsa ENTER para volver...")


def ver_horario_guardado(restaurante_id=1):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            tareas_produccion.nombre,
            tareas_produccion.cantidad,
            tareas_produccion.unidad,
            tareas_produccion.persona_asignada,
            tareas_produccion.hora_inicio_estimada,
            tareas_produccion.hora_fin_estimada,
            tareas_produccion.nota_planificacion,
            eventos.nombre AS evento_nombre,
            eventos.fecha AS evento_fecha
        FROM tareas_produccion
        JOIN producciones ON tareas_produccion.produccion_id = producciones.id
        JOIN eventos ON producciones.evento_id = eventos.id
        WHERE eventos.restaurante_id = ?
        AND tareas_produccion.estado != 'hecha'
        ORDER BY tareas_produccion.persona_asignada, tareas_produccion.hora_inicio_estimada
    """, (restaurante_id,))

    tareas = cursor.fetchall()
    conexion.close()

    print("\n========== HORARIO GUARDADO ==========")

    if not tareas:
        print("\nNo hay tareas pendientes.\n")
        input("Pulsa ENTER para volver...")
        return

    tareas_por_persona = {}
    for tarea in tareas:
        persona = tarea["persona_asignada"] or "Sin asignar"
        tareas_por_persona.setdefault(persona, []).append(tarea)

    for persona, lista in tareas_por_persona.items():
        print(f"\n👤 {persona}")
        print("--------------------------------------")
        for tarea in lista:
            inicio = tarea["hora_inicio_estimada"] or "--:--"
            fin = tarea["hora_fin_estimada"] or "--:--"
            print(f"{inicio} - {fin} · {tarea['nombre']}")
            print(f"  Evento: {tarea['evento_nombre']}")
            if tarea["nota_planificacion"]:
                print(f"  Nota  : {tarea['nota_planificacion']}")

    print()
    input("Pulsa ENTER para volver...")

def menu_planificacion(restaurante_id=1):
    restaurante_id = restaurante_id or asegurar_restaurante_demo()
    inicializar_roles_base(restaurante_id)

    while True:
        print("\n========== PLANIFICACIÓN / PERSONAL ==========")
        print("1. Dashboard planificación")
        print("2. Ver roles")
        print("3. Ver equipo")
        print("4. Añadir persona")
        print("5. Asignar tareas pendientes automáticamente")
        print("6. Ver planning de producción")
        print("7. Generar horario inteligente")
        print("8. Ver horario guardado")
        print("0. Volver")

        opcion = input("\n¿Qué quieres hacer? ")

        if opcion == "1":
            dashboard_planificacion(restaurante_id)
        elif opcion == "2":
            mostrar_roles(restaurante_id)
        elif opcion == "3":
            mostrar_equipo(restaurante_id)
        elif opcion == "4":
            añadir_persona(restaurante_id)
        elif opcion == "5":
            asignar_tareas_pendientes(restaurante_id)
        elif opcion == "6":
            mostrar_planning(restaurante_id)
        elif opcion == "7":
            generar_horario_inteligente(restaurante_id)
        elif opcion == "8":
            ver_horario_guardado(restaurante_id)
        elif opcion == "0":
            break
        else:
            print("\n⚠️ Opción no válida.")
