from __future__ import annotations

from dataclasses import dataclass
from typing import Any

try:
    from database import conectar
except Exception:
    conectar = None


@dataclass
class DependenciaDetectada:
    clave: str
    nombre: str
    tareas: list[dict[str, Any]]
    importancia: int
    motivo: str


PALABRAS_COMPONENTES = {
    "demi_glace": ["demi", "glace", "demiglace", "salsa carne", "salsa naranja", "salsa vino", "pimienta"],
    "fumet": ["fumet", "caldo pescado", "fondo pescado", "marisco"],
    "fondo_oscuro": ["fondo oscuro", "fondo carne", "carrillera", "meloso", "rag", "ragu", "estof"],
    "bechamel": ["bechamel", "croqueta", "canelon", "canelón"],
    "pure_patata": ["pure", "puré", "parmentier", "patata"],
    "alioli": ["alioli", "allioli", "mayonesa ajo"],
    "guacamole": ["guacamole", "aguacate"],
    "mise_frio": ["ceviche", "tartar", "ensalada", "brocheta", "queso", "jamon", "jamón", "frio", "frío"],
}

NOMBRES_BONITOS = {
    "demi_glace": "Demi-glace / salsas madre de carne",
    "fumet": "Fumet / caldo de pescado",
    "fondo_oscuro": "Fondo oscuro / base de carnes",
    "bechamel": "Bechamel / masas y rellenos",
    "pure_patata": "Puré / parmentier de patata",
    "alioli": "Alioli / emulsionados",
    "guacamole": "Guacamole / aguacate",
    "mise_frio": "Mise en place fría",
}


def normalizar(texto: str | None) -> str:
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


def obtener_tareas_pendientes(restaurante_id: int = 1) -> list[dict[str, Any]]:
    if conectar is None:
        return []

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            tareas_produccion.id AS id,
            tareas_produccion.nombre AS nombre,
            tareas_produccion.cantidad AS cantidad,
            tareas_produccion.unidad AS unidad,
            tareas_produccion.estado AS estado,
            eventos.nombre AS evento,
            eventos.fecha AS fecha_evento
        FROM tareas_produccion
        JOIN producciones ON tareas_produccion.produccion_id = producciones.id
        JOIN eventos ON producciones.evento_id = eventos.id
        WHERE COALESCE(tareas_produccion.estado, 'pendiente') != 'hecha'
        ORDER BY eventos.fecha, tareas_produccion.orden
    """)

    filas = [dict(fila) for fila in cursor.fetchall()]
    conexion.close()
    return filas


def detectar_componentes_en_tarea(tarea: dict[str, Any]) -> list[str]:
    texto = normalizar(tarea.get("nombre"))
    claves = []

    for clave, palabras in PALABRAS_COMPONENTES.items():
        if any(palabra in texto for palabra in palabras):
            claves.append(clave)

    return claves


def detectar_dependencias_basicas(restaurante_id: int = 1) -> list[DependenciaDetectada]:
    """Detecta dependencias y agrupaciones básicas sin necesitar todavía fichas técnicas completas.

    Es una capa intermedia: mientras Host AI aprende las elaboraciones reales,
    este motor ya ayuda a detectar bases comunes como fondos, salsas, purés,
    bechamel, fumet y mise en place fría.
    """
    tareas = obtener_tareas_pendientes(restaurante_id)
    grupos: dict[str, list[dict[str, Any]]] = {clave: [] for clave in PALABRAS_COMPONENTES}

    for tarea in tareas:
        for clave in detectar_componentes_en_tarea(tarea):
            grupos[clave].append(tarea)

    dependencias: list[DependenciaDetectada] = []

    for clave, tareas_grupo in grupos.items():
        if not tareas_grupo:
            continue

        importancia = 40 + (len(tareas_grupo) * 10)
        if clave in ["demi_glace", "fumet", "fondo_oscuro", "bechamel"]:
            importancia += 20
        importancia = min(importancia, 100)

        if len(tareas_grupo) == 1:
            motivo = "Aparece en una producción pendiente. Conviene revisar si es una elaboración común."
        else:
            motivo = f"Aparece relacionada con {len(tareas_grupo)} tareas pendientes. Puede ser una producción agrupable."

        dependencias.append(
            DependenciaDetectada(
                clave=clave,
                nombre=NOMBRES_BONITOS.get(clave, clave),
                tareas=tareas_grupo,
                importancia=importancia,
                motivo=motivo,
            )
        )

    dependencias.sort(key=lambda d: d.importancia, reverse=True)
    return dependencias


def resumen_dependencias(restaurante_id: int = 1) -> str:
    dependencias = detectar_dependencias_basicas(restaurante_id)

    if not dependencias:
        return (
            "No he detectado dependencias comunes todavía.\n"
            "Cuando haya fichas técnicas completas, Host AI podrá construir el árbol real de elaboraciones."
        )

    lineas = ["========== DEPENDENCIAS / AGRUPACIONES DETECTADAS =========="]

    for i, dep in enumerate(dependencias, start=1):
        lineas.append(f"{i}. {dep.nombre}")
        lineas.append(f"   Importancia: {dep.importancia}/100")
        lineas.append(f"   Motivo     : {dep.motivo}")
        lineas.append("   Tareas relacionadas:")
        for tarea in dep.tareas[:8]:
            cantidad = ""
            if tarea.get("cantidad") is not None:
                cantidad = f" · {tarea.get('cantidad')} {tarea.get('unidad') or ''}".strip()
            lineas.append(f"   - {tarea.get('nombre')}{cantidad} · Evento: {tarea.get('evento')}")
        if len(dep.tareas) > 8:
            lineas.append(f"   ... y {len(dep.tareas) - 8} más")
        lineas.append("")

    return "\n".join(lineas)


def sugerencias_agrupacion(restaurante_id: int = 1) -> list[str]:
    dependencias = detectar_dependencias_basicas(restaurante_id)
    sugerencias = []

    for dep in dependencias:
        if len(dep.tareas) >= 2:
            sugerencias.append(
                f"Agrupar '{dep.nombre}' en una única producción en vez de tratar cada plato por separado."
            )
        elif dep.clave in ["demi_glace", "fumet", "fondo_oscuro", "bechamel"]:
            sugerencias.append(
                f"Revisar '{dep.nombre}': aunque solo aparezca una vez, puede desbloquear producciones futuras."
            )

    return sugerencias
