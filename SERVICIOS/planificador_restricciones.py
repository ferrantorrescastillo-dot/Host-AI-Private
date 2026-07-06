# -*- coding: utf-8 -*-
"""
Sprint 5.4 - Motor de planificación por restricciones reales
Host AI

Este servicio no sustituye la base de datos ni el motor de producción anterior.
Añade una capa de inteligencia de cocina sobre tareas de producción:
- tiempo activo / tiempo pasivo
- reposos
- tareas que desbloquean otras
- tareas largas
- tareas solapables
- tareas rápidas durante tiempos muertos
- prioridad por riesgo

Diseñado para funcionar aunque el proyecto todavía no tenga todas las tablas reales.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, Iterable, List, Optional, Tuple


@dataclass
class TareaProduccion:
    nombre: str
    duracion_min: int = 30
    tiempo_activo_min: Optional[int] = None
    tiempo_pasivo_min: Optional[int] = None
    reposo_min: int = 0
    prioridad: int = 3
    riesgo: int = 3
    desbloquea: List[str] = field(default_factory=list)
    dependencias: List[str] = field(default_factory=list)
    recursos: List[str] = field(default_factory=list)
    tipo: str = "produccion"
    motivo: str = ""

    def __post_init__(self) -> None:
        self.duracion_min = max(int(self.duracion_min or 0), 1)
        if self.tiempo_activo_min is None and self.tiempo_pasivo_min is None:
            self.tiempo_activo_min = self.duracion_min
            self.tiempo_pasivo_min = 0
        elif self.tiempo_activo_min is None:
            self.tiempo_activo_min = max(self.duracion_min - int(self.tiempo_pasivo_min or 0), 0)
        elif self.tiempo_pasivo_min is None:
            self.tiempo_pasivo_min = max(self.duracion_min - int(self.tiempo_activo_min or 0), 0)

        self.tiempo_activo_min = max(int(self.tiempo_activo_min or 0), 0)
        self.tiempo_pasivo_min = max(int(self.tiempo_pasivo_min or 0), 0)
        self.reposo_min = max(int(self.reposo_min or 0), 0)
        self.prioridad = max(int(self.prioridad or 0), 0)
        self.riesgo = max(int(self.riesgo or 0), 0)

    @property
    def es_larga(self) -> bool:
        return self.duracion_min >= 90 or self.tiempo_pasivo_min >= 60 or self.reposo_min >= 60

    @property
    def es_rapida(self) -> bool:
        return self.duracion_min <= 30 and self.tiempo_pasivo_min == 0

    @property
    def es_solapable(self) -> bool:
        return self.tiempo_pasivo_min >= 20 or self.reposo_min >= 20


@dataclass
class BloqueHorario:
    inicio: datetime
    fin: datetime
    tarea: str
    fase: str
    motivo: str
    aviso: str = ""

    def como_lineas(self) -> List[str]:
        rango = f"{self.inicio.strftime('%H:%M')} - {self.fin.strftime('%H:%M')}"
        lineas = [rango, self.tarea]
        if self.fase:
            lineas.append(f"Fase: {self.fase}")
        if self.motivo:
            lineas.append(f"Motivo: {self.motivo}")
        if self.aviso:
            lineas.append(f"Aviso: {self.aviso}")
        return lineas


class PlanificadorRestricciones:
    """Planificador simple, explícito y ampliable para cocina real."""

    def __init__(self, hora_inicio: str = "08:00") -> None:
        self.hora_inicio = hora_inicio

    def crear_tareas_demo(self) -> List[TareaProduccion]:
        """Datos de prueba para poder validar el Sprint 5.4 sin depender todavía de BBDD."""
        return [
            TareaProduccion(
                nombre="Preparar bresa / mise en place inicial",
                duracion_min=20,
                tiempo_activo_min=20,
                prioridad=8,
                riesgo=7,
                desbloquea=["Fondo oscuro / demi-glace"],
                tipo="mise_en_place",
                motivo="Desbloquea fondos, salsas y cocciones largas.",
            ),
            TareaProduccion(
                nombre="Marcar huesos o espinas al horno",
                duracion_min=25,
                tiempo_activo_min=10,
                tiempo_pasivo_min=15,
                prioridad=7,
                riesgo=7,
                recursos=["horno"],
                desbloquea=["Fondo oscuro / demi-glace"],
                tipo="horno",
                motivo="Ocupa horno al principio y permite avanzar otras tareas mientras se tuesta.",
            ),
            TareaProduccion(
                nombre="Sofreír verduras del fondo",
                duracion_min=25,
                tiempo_activo_min=25,
                prioridad=7,
                riesgo=6,
                dependencias=["Preparar bresa / mise en place inicial"],
                desbloquea=["Fondo oscuro / demi-glace"],
                tipo="coccion_activa",
                motivo="Fase activa necesaria antes de una cocción larga.",
            ),
            TareaProduccion(
                nombre="Fondo oscuro / demi-glace",
                duracion_min=180,
                tiempo_activo_min=15,
                tiempo_pasivo_min=165,
                prioridad=10,
                riesgo=10,
                dependencias=["Marcar huesos o espinas al horno", "Sofreír verduras del fondo"],
                desbloquea=["Salsa final", "Carrillera glaseada"],
                tipo="coccion_larga",
                motivo="Producción larga y de alto riesgo: si empieza tarde, bloquea salsas y servicio.",
            ),
            TareaProduccion(
                nombre="Preparar alioli",
                duracion_min=20,
                tiempo_activo_min=20,
                prioridad=4,
                riesgo=3,
                tipo="tarea_rapida",
                motivo="Tarea corta que cabe dentro de un tiempo muerto.",
            ),
            TareaProduccion(
                nombre="Bechamel base croquetas",
                duracion_min=45,
                tiempo_activo_min=40,
                tiempo_pasivo_min=5,
                reposo_min=240,
                prioridad=8,
                riesgo=8,
                tipo="reposo",
                motivo="Necesita reposo largo antes de bolear o porcionar.",
            ),
            TareaProduccion(
                nombre="Cortar guarnición fría",
                duracion_min=25,
                tiempo_activo_min=25,
                prioridad=3,
                riesgo=2,
                tipo="tarea_rapida",
                motivo="Tarea rápida, mejor colocarla cuando una cocción larga queda en marcha.",
            ),
        ]

    def puntuacion(self, tarea: TareaProduccion) -> int:
        puntos = 0
        puntos += tarea.prioridad * 10
        puntos += tarea.riesgo * 12
        puntos += len(tarea.desbloquea) * 18
        if tarea.es_larga:
            puntos += 35
        if tarea.reposo_min >= 60:
            puntos += 30
        if tarea.tiempo_pasivo_min >= 60:
            puntos += 25
        if tarea.es_rapida:
            puntos -= 12
        return puntos

    def explicar_orden(self, tarea: TareaProduccion) -> str:
        razones: List[str] = []
        if tarea.desbloquea:
            razones.append("desbloquea " + ", ".join(tarea.desbloquea))
        if tarea.tiempo_pasivo_min >= 60:
            razones.append("tiene tiempo pasivo largo")
        if tarea.reposo_min >= 60:
            razones.append("necesita reposo")
        if tarea.riesgo >= 8:
            razones.append("tiene riesgo alto")
        if tarea.es_rapida:
            razones.append("es rápida y se puede encajar en huecos")
        if tarea.recursos:
            razones.append("usa recurso: " + ", ".join(tarea.recursos))
        if tarea.motivo:
            razones.append(tarea.motivo)
        return "; ".join(razones) + "." if razones else "Ordenada por prioridad general."

    def ordenar_tareas(self, tareas: Iterable[TareaProduccion]) -> List[TareaProduccion]:
        return sorted(tareas, key=self.puntuacion, reverse=True)

    def _parse_hora(self, fecha_base: Optional[datetime] = None) -> datetime:
        fecha = fecha_base or datetime.now()
        hora, minuto = self.hora_inicio.split(":")
        return fecha.replace(hour=int(hora), minute=int(minuto), second=0, microsecond=0)

    def generar_horario(self, tareas: Optional[List[TareaProduccion]] = None) -> List[BloqueHorario]:
        tareas = list(tareas or self.crear_tareas_demo())
        pendientes = self.ordenar_tareas(tareas)
        completadas: set[str] = set()
        bloques: List[BloqueHorario] = []
        ahora = self._parse_hora()

        # Algoritmo simple y claro: primero desbloqueos/largas/reposos; tareas rápidas dentro de pasivos.
        while pendientes:
            disponibles = [t for t in pendientes if all(dep in completadas for dep in t.dependencias)]
            if not disponibles:
                # Si faltan dependencias con nombres no encontrados, no bloqueamos el prototipo.
                disponibles = pendientes[:]

            tarea = self.ordenar_tareas(disponibles)[0]
            pendientes.remove(tarea)

            activo = max(tarea.tiempo_activo_min, 1)
            fin_activo = ahora + timedelta(minutes=activo)
            bloques.append(
                BloqueHorario(
                    inicio=ahora,
                    fin=fin_activo,
                    tarea=tarea.nombre,
                    fase="Trabajo activo",
                    motivo=self.explicar_orden(tarea),
                    aviso="Esta tarea desbloquea otras." if tarea.desbloquea else "",
                )
            )
            ahora = fin_activo
            completadas.add(tarea.nombre)

            if tarea.tiempo_pasivo_min > 0:
                fin_pasivo = ahora + timedelta(minutes=tarea.tiempo_pasivo_min)
                bloques.append(
                    BloqueHorario(
                        inicio=ahora,
                        fin=fin_pasivo,
                        tarea=tarea.nombre,
                        fase="Tiempo pasivo / cocción / espera",
                        motivo="Durante este bloque se pueden adelantar tareas rápidas sin parar la producción principal.",
                    )
                )

                # Encajar tareas rápidas dentro del pasivo.
                hueco_inicio = ahora + timedelta(minutes=5)
                rapidas = [t for t in pendientes if t.es_rapida and all(dep in completadas for dep in t.dependencias)]
                for rapida in self.ordenar_tareas(rapidas):
                    if hueco_inicio + timedelta(minutes=rapida.duracion_min) <= fin_pasivo:
                        pendientes.remove(rapida)
                        bloques.append(
                            BloqueHorario(
                                inicio=hueco_inicio,
                                fin=hueco_inicio + timedelta(minutes=rapida.duracion_min),
                                tarea=rapida.nombre,
                                fase="Tarea encajada en tiempo muerto",
                                motivo=self.explicar_orden(rapida),
                            )
                        )
                        completadas.add(rapida.nombre)
                        hueco_inicio += timedelta(minutes=rapida.duracion_min + 5)

                ahora = fin_pasivo

            if tarea.reposo_min > 0:
                bloques.append(
                    BloqueHorario(
                        inicio=ahora,
                        fin=ahora + timedelta(minutes=tarea.reposo_min),
                        tarea=tarea.nombre,
                        fase="Reposo / enfriado / maduración",
                        motivo="No requiere trabajo constante, pero condiciona cuándo se puede terminar la elaboración.",
                    )
                )
                # El jefe no espera todo el reposo si puede seguir trabajando.
                ahora = ahora + timedelta(minutes=5)

        return sorted(bloques, key=lambda b: (b.inicio, b.fin, b.tarea))

    def generar_resumen_riesgos(self, tareas: Optional[List[TareaProduccion]] = None) -> List[str]:
        tareas = list(tareas or self.crear_tareas_demo())
        riesgos: List[str] = []
        for tarea in self.ordenar_tareas(tareas):
            if tarea.riesgo >= 8:
                riesgos.append(f"⚠ {tarea.nombre}: riesgo alto si se retrasa.")
            if tarea.tiempo_pasivo_min >= 120:
                riesgos.append(f"⚠ {tarea.nombre}: cocción/espera larga de {tarea.tiempo_pasivo_min} min.")
            if tarea.reposo_min >= 120:
                riesgos.append(f"⚠ {tarea.nombre}: necesita reposo de {tarea.reposo_min} min.")
            if tarea.desbloquea:
                riesgos.append(f"⚠ {tarea.nombre}: desbloquea {', '.join(tarea.desbloquea)}.")
        return riesgos


def imprimir_horario_restricciones(tareas: Optional[List[TareaProduccion]] = None, hora_inicio: str = "08:00") -> None:
    planificador = PlanificadorRestricciones(hora_inicio=hora_inicio)
    bloques = planificador.generar_horario(tareas)
    riesgos = planificador.generar_resumen_riesgos(tareas)

    print("\n" + "=" * 70)
    print("HORARIO INTELIGENTE POR RESTRICCIONES REALES - SPRINT 5.4")
    print("=" * 70)

    if riesgos:
        print("\nRIESGOS DETECTADOS")
        for riesgo in riesgos[:8]:
            print(f"- {riesgo}")

    print("\nPLAN DE PRODUCCIÓN")
    for bloque in bloques:
        print("\n" + "-" * 70)
        for linea in bloque.como_lineas():
            print(linea)

    print("\n" + "=" * 70)
    print("Lectura de jefe de cocina:")
    print("Primero se colocan tareas largas, con reposo, pasivas o que desbloquean otras.")
    print("Luego se encajan tareas rápidas en los tiempos muertos.")
    print("Sprint 5.5 conectará esto con personal, maquinaria y cuellos de botella reales.")
    print("=" * 70 + "\n")
