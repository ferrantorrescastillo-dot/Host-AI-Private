# -*- coding: utf-8 -*-
"""Versionado e historial de fichas técnicas - Sprint 5.9"""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List
BASE_DIR = Path(__file__).resolve().parents[1]
DATOS_DIR = BASE_DIR / "DATOS"
HISTORIAL_DIR = DATOS_DIR / "historial_fichas"
VERSIONES_DIR = DATOS_DIR / "versiones_fichas"
HISTORIAL_DIR.mkdir(parents=True, exist_ok=True)
VERSIONES_DIR.mkdir(parents=True, exist_ok=True)

def guardar_version(ficha: Dict, motivo: str = "cambio") -> Path:
    codigo = ficha.get("codigo", "SIN-CODIGO")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = VERSIONES_DIR / f"{codigo}_{timestamp}.json"
    path.write_text(json.dumps(ficha, ensure_ascii=False, indent=2), encoding="utf-8")
    return path

def registrar_cambio(codigo: str, campo: str, anterior, nuevo, motivo: str = "") -> None:
    path = HISTORIAL_DIR / f"{codigo}_historial.json"
    historial = json.loads(path.read_text(encoding="utf-8")) if path.exists() else []
    historial.append({"fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "campo": campo, "anterior": anterior, "nuevo": nuevo, "motivo": motivo})
    path.write_text(json.dumps(historial, ensure_ascii=False, indent=2), encoding="utf-8")

def leer_historial(codigo: str) -> List[Dict]:
    path = HISTORIAL_DIR / f"{codigo}_historial.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else []
