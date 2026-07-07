# -*- coding: utf-8 -*-
"""
Modelo de Ficha Técnica Host AI v1.0

La ficha técnica no es solo una receta.
Es la fuente de verdad para:
- producción
- planificación
- compras
- stock
- costes
- calidad
- formación
- IA futura
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional


@dataclass
class IngredienteFicha:
    nombre: str
    cantidad: float
    unidad: str
    merma_porcentaje: Optional[float] = None
    cantidad_neta: Optional[float] = None
    proveedor_preferente: str = ""
    coste_unitario: Optional[float] = None
    alergenos: List[str] = field(default_factory=list)
    es_critico: bool = False


@dataclass
class FaseFicha:
    nombre: str
    orden: int
    descripcion: str
    tiempo_activo_min: int = 0
    tiempo_pasivo_min: int = 0
    temperatura: str = ""
    maquinaria: List[str] = field(default_factory=list)
    utensilios: List[str] = field(default_factory=list)
    depende_de: List[str] = field(default_factory=list)
    desbloquea: List[str] = field(default_factory=list)
    punto_critico: str = ""
    control_calidad: str = ""
    tipo: str = "activa"  # activa | pasiva | mixta | control | cierre


@dataclass
class FichaTecnicaHostAI:
    codigo: str
    nombre: str
    tipo: str = "elaboracion"
    familia: str = ""
    version: str = "1.0"
    estado: str = "borrador"

    objetivo: str = ""
    descripcion_corta: str = ""

    rendimiento_final: str = ""
    raciones: Optional[int] = None
    peso_racion: str = ""

    ingredientes: List[IngredienteFicha] = field(default_factory=list)
    fases: List[FaseFicha] = field(default_factory=list)

    tiempo_total_min: int = 0
    tiempo_activo_min: int = 0
    tiempo_pasivo_min: int = 0

    maquinaria_imprescindible: List[str] = field(default_factory=list)
    maquinaria_opcional: List[str] = field(default_factory=list)
    utensilios: List[str] = field(default_factory=list)

    producciones_previas: List[str] = field(default_factory=list)
    elaboraciones_que_desbloquea: List[str] = field(default_factory=list)

    puntos_criticos_haccp: List[str] = field(default_factory=list)
    controles_calidad: List[str] = field(default_factory=list)
    errores_frecuentes: List[str] = field(default_factory=list)

    conservacion: str = ""
    vida_util: str = ""
    congelacion: str = ""
    regeneracion: str = ""

    alergenos: List[str] = field(default_factory=list)
    coste_materia_prima: Optional[float] = None
    coste_mano_obra: Optional[float] = None
    coste_total_estimado: Optional[float] = None
    coste_por_racion: Optional[float] = None

    notas_jefe_cocina: str = ""
    preguntas_pendientes: List[str] = field(default_factory=list)

    def recalcular_tiempos(self) -> None:
        self.tiempo_activo_min = sum(f.tiempo_activo_min for f in self.fases)
        self.tiempo_pasivo_min = sum(f.tiempo_pasivo_min for f in self.fases)
        self.tiempo_total_min = self.tiempo_activo_min + self.tiempo_pasivo_min

    def to_dict(self) -> Dict:
        self.recalcular_tiempos()
        return asdict(self)
