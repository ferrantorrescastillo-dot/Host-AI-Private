from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, date
from typing import Any, Iterable

try:
    from database import conectar
except Exception:  # permite importar el módulo en pruebas aisladas
    conectar = None


@dataclass
class TareaPrioridad:
    id: int
    nombre: str
    cantidad: float | None
    unidad: str | None
    estado: str
    evento: str | None
    fecha_evento: str | None
    prioridad: int
    nivel: str
    motivos: list[str]
    accion_recomendada: str


PALABRAS_LARGAS = [
    "fondo", "fumet", "demi", "glace", "demiglace", "caldo", "carrillera",
    "estof", "guis", "confit", "rag", "meloso", "salsa", "reducci",
]

PALABRAS_REPOSO = [
    "prens", "repos", "marinad", "curad", "ferment", "gelatina", "cuajar",
    "abat", "enfri", "congel", "descongel",
]

PALABRAS_FRESCAS = [
    "guacamole", "aguacate", "ceviche", "tartar", "brotes", "ensalada",
    "hierba", "cilantro", "fresa", "pescado", "marisco",
]

PALABRAS_DESBLOQUEAN = [
    "demi", "glace", "fondo", "fumet", "salsa", "bechamel", "pure", "puré",
    "sofrito", "caldo",
]


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


def _parse_fecha(fecha: str | None) -> date | None:
    if not fecha:
        return None
    fecha = fecha.strip()
    formatos = ["%Y-%m-%d", "%d/%m/%Y", "%d/%m/%y", "%d-%m-%Y", "%d-%m-%y"]
    for formato in formatos:
        try:
            return datetime.strptime(fecha, formato).date()
        except ValueError:
            continue
    return None


def _dias_hasta(fecha: str | None) -> int | None:
    f = _parse_fecha(fecha)
    if f is None:
        return None
    return (f - date.today()).days


def calcular_prioridad_tarea(nombre: str, fecha_evento: str | None = None, cantidad: float | None = None) -> tuple[int, list[str]]:
    """Calcula prioridad culinaria básica de una tarea.

    No intenta ser perfecto. Es la primera capa del Motor de Producción Inteligente.
    La lógica está basada en reglas de jefe de cocina:
    - Lo largo primero.
    - Lo que necesita reposo primero.
    - Lo que desbloquea otras elaboraciones primero.
    - Lo perecedero cerca del servicio.
    - Lo urgente por fecha sube mucho.
    """
    texto = _normalizar(nombre)
    puntos = 0
    motivos: list[str] = []

    if any(p in texto for p in PALABRAS_LARGAS):
        puntos += 30
        motivos.append("Elaboración larga o de cocción/reducción: conviene empezarla pronto.")

    if any(p in texto for p in PALABRAS_REPOSO):
        puntos += 25
        motivos.append("Necesita reposo, enfriado, prensado o tiempo pasivo.")

    if any(p in texto for p in PALABRAS_DESBLOQUEAN):
        puntos += 20
        motivos.append("Puede desbloquear otras elaboraciones o platos.")

    if any(p in texto for p in PALABRAS_FRESCAS):
        puntos += 10
        motivos.append("Producto fresco/delicado: controlar cercanía al servicio.")

    dias = _dias_hasta(fecha_evento)
    if dias is not None:
        if dias < 0:
            puntos += 5
            motivos.append("Evento pasado o fecha antigua: revisar si sigue pendiente.")
        elif dias == 0:
            puntos += 35
            motivos.append("Evento hoy: prioridad operativa máxima.")
        elif dias == 1:
            puntos += 30
            motivos.append("Evento mañana: producción crítica.")
        elif dias <= 3:
            puntos += 20
            motivos.append("Evento cercano: conviene asegurar producción.")
        elif dias <= 7:
            puntos += 10
            motivos.append("Evento esta semana: planificar con margen.")

    if cantidad is not None and cantidad >= 50:
        puntos += 8
        motivos.append("Cantidad alta: requiere organización y margen de producción.")

    if not motivos:
        motivos.append("Tarea estándar: prioridad media hasta conocer fases y dependencias reales.")
        puntos += 10

    return min(puntos, 100), motivos


def clasificar_prioridad(puntos: int) -> str:
    if puntos >= 80:
        return "CRÍTICA"
    if puntos >= 60:
        return "ALTA"
    if puntos >= 35:
        return "MEDIA"
    return "BAJA"


def accion_recomendada(nombre: str, puntos: int, motivos: Iterable[str]) -> str:
    texto = _normalizar(nombre)
    if puntos >= 80:
        return "Empezar o revisar ahora. Puede afectar al servicio."
    if any(p in texto for p in ["fondo", "fumet", "demi", "caldo", "salsa"]):
        return "Iniciar pronto y aprovechar tiempos pasivos para adelantar mise en place."
    if any(p in texto for p in ["prens", "repos", "marinad", "abat", "enfri"]):
        return "Producir con antelación para respetar reposo/enfriado."
    if any(p in texto for p in ["guacamole", "ceviche", "brotes", "ensalada"]):
        return "Preparar cerca del servicio para mantener calidad."
    return "Planificar dentro de la jornada según personal y maquinaria disponible."


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


def generar_prioridades(restaurante_id: int = 1) -> list[TareaPrioridad]:
    tareas = obtener_tareas_pendientes(restaurante_id)
    resultado: list[TareaPrioridad] = []

    for tarea in tareas:
        puntos, motivos = calcular_prioridad_tarea(
            tarea.get("nombre"),
            tarea.get("fecha_evento"),
            tarea.get("cantidad"),
        )
        resultado.append(
            TareaPrioridad(
                id=int(tarea.get("id") or 0),
                nombre=tarea.get("nombre") or "Sin nombre",
                cantidad=tarea.get("cantidad"),
                unidad=tarea.get("unidad"),
                estado=tarea.get("estado") or "pendiente",
                evento=tarea.get("evento"),
                fecha_evento=tarea.get("fecha_evento"),
                prioridad=puntos,
                nivel=clasificar_prioridad(puntos),
                motivos=motivos,
                accion_recomendada=accion_recomendada(tarea.get("nombre") or "", puntos, motivos),
            )
        )

    resultado.sort(key=lambda x: x.prioridad, reverse=True)
    return resultado


def obtener_siguiente_accion(restaurante_id: int = 1) -> TareaPrioridad | None:
    prioridades = generar_prioridades(restaurante_id)
    if not prioridades:
        return None
    return prioridades[0]


def resumen_prioridades(restaurante_id: int = 1, limite: int = 10) -> str:
    prioridades = generar_prioridades(restaurante_id)
    if not prioridades:
        return "No hay tareas pendientes de producción."

    lineas = ["========== PRIORIDADES DE PRODUCCIÓN =========="]
    for i, tarea in enumerate(prioridades[:limite], start=1):
        cantidad = ""
        if tarea.cantidad is not None:
            cantidad = f" · {tarea.cantidad} {tarea.unidad or ''}".strip()
        lineas.append(f"{i}. {tarea.nombre}{cantidad}")
        lineas.append(f"   Evento: {tarea.evento or 'Sin evento'} ({tarea.fecha_evento or 'sin fecha'})")
        lineas.append(f"   Prioridad: {tarea.nivel} ({tarea.prioridad}/100)")
        lineas.append(f"   Acción: {tarea.accion_recomendada}")
        lineas.append("   Motivos:")
        for motivo in tarea.motivos:
            lineas.append(f"   - {motivo}")
        lineas.append("")
    return "\n".join(lineas)
