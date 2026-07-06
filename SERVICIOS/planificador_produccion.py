# -*- coding: utf-8 -*-
"""
Sprint 5.3 + compatibilidad Sprint 5.4
Planificador de producción.

Mantiene una función sencilla de horario y añade puente hacia el nuevo motor
por restricciones reales sin romper imports anteriores.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Iterable, List, Dict, Any


def _normalizar_tarea(tarea: Any) -> Dict[str, Any]:
    if isinstance(tarea, dict):
        return tarea
    return {
        "nombre": getattr(tarea, "nombre", str(tarea)),
        "duracion_min": getattr(tarea, "duracion_min", 30),
        "prioridad": getattr(tarea, "prioridad", 3),
    }


def generar_horario_basico(tareas: Iterable[Any] | None = None, hora_inicio: str = "08:00") -> List[Dict[str, str]]:
    """Horario lineal básico del Sprint 5.3."""
    tareas_norm = [_normalizar_tarea(t) for t in (tareas or _tareas_demo_basicas())]
    hora, minuto = hora_inicio.split(":")
    actual = datetime.now().replace(hour=int(hora), minute=int(minuto), second=0, microsecond=0)
    horario: List[Dict[str, str]] = []

    for tarea in tareas_norm:
        duracion = int(tarea.get("duracion_min", tarea.get("duracion", 30)) or 30)
        fin = actual + timedelta(minutes=max(duracion, 1))
        horario.append(
            {
                "inicio": actual.strftime("%H:%M"),
                "fin": fin.strftime("%H:%M"),
                "tarea": str(tarea.get("nombre", "Tarea de producción")),
                "motivo": str(tarea.get("motivo", "Ordenado por duración/prioridad básica.")),
            }
        )
        actual = fin
    return horario


def imprimir_horario_basico(tareas: Iterable[Any] | None = None, hora_inicio: str = "08:00") -> None:
    print("\nHORARIO DE PRODUCCIÓN INTELIGENTE - SPRINT 5.3")
    print("=" * 60)
    for bloque in generar_horario_basico(tareas, hora_inicio):
        print(f"\n{bloque['inicio']} - {bloque['fin']}")
        print(bloque["tarea"])
        print(f"Motivo: {bloque['motivo']}")
    print()


def imprimir_horario_restricciones(tareas=None, hora_inicio: str = "08:00") -> None:
    """Puente hacia Sprint 5.4."""
    from SERVICIOS.planificador_restricciones import imprimir_horario_restricciones as _imprimir

    _imprimir(tareas=tareas, hora_inicio=hora_inicio)


def _tareas_demo_basicas() -> List[Dict[str, Any]]:
    return [
        {"nombre": "Preparar mise en place inicial", "duracion_min": 20, "motivo": "Desbloquea el resto del trabajo."},
        {"nombre": "Iniciar fondo / fumet", "duracion_min": 180, "motivo": "Tarea larga que debe empezar pronto."},
        {"nombre": "Preparar salsa corta", "duracion_min": 30, "motivo": "Tarea rápida para avanzar producción."},
    ]
