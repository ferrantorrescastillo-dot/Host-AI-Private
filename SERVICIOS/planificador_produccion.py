from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any

try:
    from prioridades import generar_prioridades, TareaPrioridad
except Exception:
    generar_prioridades = None
    TareaPrioridad = None

try:
    from dependencias import detectar_dependencias_basicas
except Exception:
    detectar_dependencias_basicas = None


@dataclass
class BloqueHorario:
    orden: int
    inicio: str
    fin: str
    tarea: str
    tipo: str
    evento: str | None
    cantidad: float | None
    unidad: str | None
    prioridad: int
    responsable_sugerido: str
    tiempo_activo_min: int
    tiempo_pasivo_min: int
    maquinaria: str
    nota: str
    motivos: list[str]


@dataclass
class HorarioProduccion:
    bloques: list[BloqueHorario]
    hora_inicio: str
    hora_fin_estimada: str
    tiempo_activo_total_min: int
    tiempo_pasivo_total_min: int
    avisos: list[str]
    resumen: str


def _normalizar(texto: str | None) -> str:
    if not texto:
        return ""
    return (
        texto.lower()
        .replace("á", "a")
        .replace("é", "e")
        .replace("í", "i")
        .replace("ó", "o")
        .replace("ú", "u")
        .replace("à", "a")
        .replace("è", "e")
        .replace("ò", "o")
        .replace("ç", "c")
    )


def estimar_tiempos(nombre: str) -> tuple[int, int, str, str, str]:
    """Devuelve tiempo activo, pasivo, maquinaria, responsable y nota.

    Es una primera versión basada en reglas culinarias. Más adelante saldrá de las
    fichas técnicas reales de cada elaboración.
    """
    n = _normalizar(nombre)

    if any(p in n for p in ["demi", "glace", "fondo oscuro", "caldo carne", "salsa naranja", "carrillera", "meloso"]):
        return (
            70,
            240,
            "Horno / marmita / fuego",
            "Cocinero o jefe de partida",
            "Producción larga o base. Empezar pronto porque puede bloquear otras elaboraciones.",
        )

    if any(p in n for p in ["fumet", "caldo pescado", "fondo pescado", "marisco"]):
        return (
            45,
            75,
            "Horno / olla / fuego",
            "Cocinero",
            "Aprovechar horno y fuegos. Mientras cuece, avanzar mise en place.",
        )

    if any(p in n for p in ["bechamel", "croqueta", "canelon", "canelón"]):
        return (
            55,
            180,
            "Fuego / abatidor / cámara",
            "Cocinero",
            "Necesita enfriar o reposar. Conviene hacerla antes de tareas rápidas.",
        )

    if any(p in n for p in ["pure", "puré", "parmentier", "patata"]):
        return (
            40,
            35,
            "Olla / Thermomix opcional",
            "Cocinero o ayudante avanzado",
            "Se puede encajar mientras cuecen fondos o salsas.",
        )

    if any(p in n for p in ["guacamole", "aguacate", "ceviche", "tartar", "ensalada", "brocheta", "frio", "frío"]):
        return (
            35,
            0,
            "Mesa fría / cuchillos",
            "Ayudante o cocinero de frío",
            "Producto fresco: hacerlo cerca del servicio para mantener calidad.",
        )

    if any(p in n for p in ["alioli", "allioli", "mayonesa"]):
        return (
            20,
            0,
            "Thermomix / túrmix",
            "Ayudante avanzado o cocinero",
            "Tarea corta. Encajar mientras otra elaboración está cociendo o reposando.",
        )

    if any(p in n for p in ["pan", "queso", "tabla", "jamon", "jamón", "plato carton", "vaso"]):
        return (
            20,
            0,
            "Mesa de montaje",
            "Ayudante",
            "Mise en place o montaje. No debe bloquear producciones largas.",
        )

    return (
        45,
        0,
        "Según elaboración",
        "Cocinero",
        "Tiempo estimado provisional hasta tener ficha técnica completa.",
    )


def _calcular_hora_fin(inicio: datetime, minutos: int) -> datetime:
    return inicio + timedelta(minutes=max(1, int(minutos)))


def generar_horario_produccion(restaurante_id: int = 1, hora_inicio: str = "08:00", limite: int = 20) -> HorarioProduccion:
    if generar_prioridades is None:
        return HorarioProduccion([], hora_inicio, hora_inicio, 0, 0, ["No se pudo cargar el motor de prioridades."], "Sin datos.")

    prioridades = generar_prioridades(restaurante_id)[:limite]
    avisos: list[str] = []
    bloques: list[BloqueHorario] = []

    if not prioridades:
        return HorarioProduccion([], hora_inicio, hora_inicio, 0, 0, ["No hay tareas pendientes."], "No hay producción pendiente.")

    try:
        reloj = datetime.strptime(hora_inicio.strip(), "%H:%M")
    except ValueError:
        reloj = datetime.strptime("08:00", "%H:%M")
        avisos.append("Hora no válida. Se ha usado 08:00.")

    # Primero lo que tiene pasivo o riesgo alto, después tareas cortas/frescas.
    tareas_enriquecidas = []
    for tarea in prioridades:
        activo, pasivo, maquinaria, responsable, nota = estimar_tiempos(tarea.nombre)
        score = tarea.prioridad + min(pasivo // 10, 30) + (10 if activo >= 60 else 0)
        tareas_enriquecidas.append((score, tarea, activo, pasivo, maquinaria, responsable, nota))

    tareas_enriquecidas.sort(key=lambda x: x[0], reverse=True)

    activo_total = 0
    pasivo_total = 0
    orden = 1

    for score, tarea, activo, pasivo, maquinaria, responsable, nota in tareas_enriquecidas:
        inicio = reloj
        fin_activo = _calcular_hora_fin(inicio, activo)
        reloj = fin_activo
        activo_total += activo
        pasivo_total += pasivo

        motivos = list(tarea.motivos)
        if pasivo > 0:
            motivos.append(f"Tiene {pasivo} min de tiempo pasivo/reposo/cocción que conviene iniciar pronto.")
        if activo >= 60:
            motivos.append("Tiene bastante tiempo activo y debe colocarse al principio del día.")

        bloques.append(
            BloqueHorario(
                orden=orden,
                inicio=inicio.strftime("%H:%M"),
                fin=fin_activo.strftime("%H:%M"),
                tarea=tarea.nombre,
                tipo="Producción prioritaria" if tarea.prioridad >= 75 else "Producción normal",
                evento=tarea.evento,
                cantidad=tarea.cantidad,
                unidad=tarea.unidad,
                prioridad=tarea.prioridad,
                responsable_sugerido=responsable,
                tiempo_activo_min=activo,
                tiempo_pasivo_min=pasivo,
                maquinaria=maquinaria,
                nota=nota,
                motivos=motivos,
            )
        )
        orden += 1

    hora_fin = reloj.strftime("%H:%M")

    if pasivo_total > activo_total:
        avisos.append("Hay mucho tiempo pasivo. Aprovecha esos huecos para mise en place, limpieza, cortes o pedidos.")
    if activo_total > 420:
        avisos.append("El tiempo activo supera una jornada de 7 horas. Revisa personal o adelanta producción otro día.")

    if detectar_dependencias_basicas is not None:
        deps = detectar_dependencias_basicas(restaurante_id)
        deps_fuertes = [d for d in deps if d.importancia >= 60]
        if deps_fuertes:
            avisos.append("Se han detectado producciones agrupables. Revisa si conviene hacer una sola producción común.")

    resumen = (
        f"Plan generado desde {hora_inicio}. Tiempo activo estimado: {activo_total} min. "
        f"Tiempo pasivo estimado: {pasivo_total} min. Fin activo aproximado: {hora_fin}."
    )

    return HorarioProduccion(bloques, hora_inicio, hora_fin, activo_total, pasivo_total, avisos, resumen)


def _formato_minutos(minutos: int) -> str:
    h = minutos // 60
    m = minutos % 60
    if h and m:
        return f"{h} h {m} min"
    if h:
        return f"{h} h"
    return f"{m} min"


def resumen_horario_produccion(restaurante_id: int = 1, hora_inicio: str = "08:00") -> str:
    plan = generar_horario_produccion(restaurante_id, hora_inicio)
    lineas: list[str] = []

    lineas.append("========== HORARIO DE PRODUCCIÓN INTELIGENTE ==========")
    lineas.append(plan.resumen)
    lineas.append("")

    if plan.avisos:
        lineas.append("⚠ Avisos")
        for aviso in plan.avisos:
            lineas.append(f"- {aviso}")
        lineas.append("")

    if not plan.bloques:
        lineas.append("No hay bloques de producción.")
        return "\n".join(lineas)

    for bloque in plan.bloques:
        lineas.append(f"{bloque.orden}. {bloque.inicio} - {bloque.fin} | {bloque.tarea}")
        lineas.append(f"   Evento       : {bloque.evento or 'Sin evento'}")
        if bloque.cantidad is not None:
            lineas.append(f"   Cantidad     : {bloque.cantidad} {bloque.unidad or ''}".rstrip())
        lineas.append(f"   Responsable  : {bloque.responsable_sugerido}")
        lineas.append(f"   Maquinaria   : {bloque.maquinaria}")
        lineas.append(f"   Activo       : {_formato_minutos(bloque.tiempo_activo_min)}")
        if bloque.tiempo_pasivo_min:
            lineas.append(f"   Pasivo       : {_formato_minutos(bloque.tiempo_pasivo_min)}")
        lineas.append(f"   Prioridad    : {bloque.prioridad}/100")
        lineas.append(f"   Nota         : {bloque.nota}")
        lineas.append("   Motivos:")
        for motivo in bloque.motivos[:4]:
            lineas.append(f"   - {motivo}")
        lineas.append("")

    lineas.append("Host AI:")
    lineas.append("Este horario todavía es una propuesta. Revísalo según maquinaria real, personal y ritmo de cocina.")
    return "\n".join(lineas)
