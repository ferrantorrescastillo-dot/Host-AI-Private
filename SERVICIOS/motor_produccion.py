from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from prioridades import generar_prioridades, TareaPrioridad
from dependencias import detectar_dependencias_basicas, sugerencias_agrupacion


@dataclass
class BloquePlanProduccion:
    orden: int
    titulo: str
    tipo: str
    prioridad: int
    accion: str
    motivos: list[str]
    tareas: list[dict[str, Any]]


@dataclass
class PlanProduccionInteligente:
    bloques: list[BloquePlanProduccion]
    resumen: str
    avisos: list[str]
    siguientes_pasos: list[str]


def _tarea_prioridad_a_dict(tarea: TareaPrioridad) -> dict[str, Any]:
    return {
        "id": tarea.id,
        "nombre": tarea.nombre,
        "cantidad": tarea.cantidad,
        "unidad": tarea.unidad,
        "evento": tarea.evento,
        "fecha_evento": tarea.fecha_evento,
        "prioridad": tarea.prioridad,
        "nivel": tarea.nivel,
    }


def generar_plan_produccion_inteligente(restaurante_id: int = 1) -> PlanProduccionInteligente:
    """Primera versión del Motor de Producción Inteligente.

    Todavía no usa fichas técnicas completas, pero ya combina:
    - prioridades culinarias,
    - agrupaciones/dependencias detectadas,
    - explicación de por qué conviene hacer algo primero.
    """
    prioridades = generar_prioridades(restaurante_id)
    dependencias = detectar_dependencias_basicas(restaurante_id)
    bloques: list[BloquePlanProduccion] = []
    avisos: list[str] = []
    siguientes_pasos: list[str] = []

    orden = 1

    # 1) Primero, producciones agrupables o que desbloquean otras.
    for dep in dependencias:
        if dep.importancia < 55:
            continue
        bloques.append(
            BloquePlanProduccion(
                orden=orden,
                titulo=dep.nombre,
                tipo="DEPENDENCIA / PRODUCCIÓN AGRUPABLE",
                prioridad=dep.importancia,
                accion=(
                    "Revisar como producción común. Si realmente es una elaboración base, "
                    "producirla una sola vez y usarla para todos los platos relacionados."
                ),
                motivos=[dep.motivo, "Evita duplicar trabajo y ayuda a producir como un jefe de cocina."],
                tareas=dep.tareas,
            )
        )
        orden += 1

    # 2) Después, las tareas más críticas que no hayan quedado cubiertas.
    tareas_ya_incluidas = set()
    for bloque in bloques:
        for tarea in bloque.tareas:
            if tarea.get("id") is not None:
                tareas_ya_incluidas.add(int(tarea["id"]))

    for tarea in prioridades:
        if tarea.id in tareas_ya_incluidas:
            continue
        if tarea.prioridad < 35 and len(bloques) >= 8:
            continue
        bloques.append(
            BloquePlanProduccion(
                orden=orden,
                titulo=tarea.nombre,
                tipo="TAREA PRIORITARIA",
                prioridad=tarea.prioridad,
                accion=tarea.accion_recomendada,
                motivos=tarea.motivos,
                tareas=[_tarea_prioridad_a_dict(tarea)],
            )
        )
        orden += 1
        if len(bloques) >= 12:
            break

    if not bloques:
        resumen = "No hay producción pendiente suficiente para generar un plan inteligente."
        avisos.append("Crea o genera producción desde eventos para que Host AI pueda priorizar.")
    else:
        resumen = (
            f"Plan generado con {len(bloques)} bloques de producción. "
            "Esta versión prioriza por urgencia, tiempo, reposo y dependencias básicas."
        )

    sugerencias = sugerencias_agrupacion(restaurante_id)
    siguientes_pasos.extend(sugerencias[:5])

    if dependencias:
        avisos.append(
            "Las dependencias detectadas son todavía aproximadas. Se volverán exactas cuando cada plato tenga fichas técnicas completas."
        )
    else:
        avisos.append(
            "Aún no hay árbol gastronómico real. El siguiente paso será vincular platos con elaboraciones."
        )

    siguientes_pasos.append("Crear fichas técnicas de elaboraciones base para sustituir tareas por platos.")
    siguientes_pasos.append("Conectar producción disponible para descontar lo que ya existe antes de producir de nuevo.")

    return PlanProduccionInteligente(
        bloques=bloques,
        resumen=resumen,
        avisos=avisos,
        siguientes_pasos=siguientes_pasos,
    )


def resumen_plan_produccion(restaurante_id: int = 1) -> str:
    plan = generar_plan_produccion_inteligente(restaurante_id)

    lineas = ["========== PLAN DE PRODUCCIÓN INTELIGENTE =========="]
    lineas.append(plan.resumen)
    lineas.append("")

    if not plan.bloques:
        for aviso in plan.avisos:
            lineas.append(f"⚠ {aviso}")
        return "\n".join(lineas)

    for bloque in plan.bloques:
        lineas.append(f"{bloque.orden}. {bloque.titulo}")
        lineas.append(f"   Tipo      : {bloque.tipo}")
        lineas.append(f"   Prioridad : {bloque.prioridad}/100")
        lineas.append(f"   Acción    : {bloque.accion}")
        lineas.append("   Motivos:")
        for motivo in bloque.motivos:
            lineas.append(f"   - {motivo}")
        if bloque.tareas:
            lineas.append("   Tareas/platos relacionados:")
            for tarea in bloque.tareas[:6]:
                cantidad = ""
                if tarea.get("cantidad") is not None:
                    cantidad = f" · {tarea.get('cantidad')} {tarea.get('unidad') or ''}".strip()
                lineas.append(f"   · {tarea.get('nombre')}{cantidad}")
        lineas.append("")

    lineas.append("========== AVISOS ==========")
    for aviso in plan.avisos:
        lineas.append(f"⚠ {aviso}")

    lineas.append("")
    lineas.append("========== SIGUIENTES PASOS ==========")
    for paso in plan.siguientes_pasos:
        lineas.append(f"- {paso}")

    return "\n".join(lineas)
