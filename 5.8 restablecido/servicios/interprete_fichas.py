# -*- coding: utf-8 -*-
"""
Intérprete de cambios para fichas técnicas - Sprint 5.9
"""
from __future__ import annotations
import re
from typing import Dict, Tuple

def _normalizar(texto: str) -> str:
    return texto.strip().lower()

def _extraer_numero(texto: str):
    m = re.search(r"(\d+)", texto)
    return int(m.group(1)) if m else None

def _limpiar_valor(texto: str) -> str:
    texto = texto.strip()
    texto = re.sub(r"^(es|son|será|sera|a|de|para)\s+", "", texto, flags=re.IGNORECASE).strip()
    return texto

def interpretar_cambio(texto: str) -> Tuple[str, object, str]:
    original = texto.strip()
    t = _normalizar(texto)
    if not t:
        return "desconocido", None, "No se ha escrito ningún cambio."
    if "vida útil" in t or "vida util" in t or "caduca" in t or "dura" in t:
        valor = re.sub(r".*(vida útil|vida util|caduca|dura)\s*(es|son|:)?", "", original, flags=re.IGNORECASE).strip()
        valor = _limpiar_valor(valor) or original
        return "vida_util", valor, f"Actualizar vida útil a: {valor}"
    if "regener" in t or "calentar" in t:
        valor = re.sub(r".*(regeneración|regeneracion|regenerar|calentar)\s*(es|a|:)?", "", original, flags=re.IGNORECASE).strip()
        valor = _limpiar_valor(valor) or original
        return "regeneracion", valor, f"Actualizar regeneración a: {valor}"
    if "racion" in t or "ración" in t:
        n = _extraer_numero(t)
        if n is not None and ("sale" in t or "salen" in t or "para" in t or "raciones" in t):
            return "raciones", n, f"Actualizar número de raciones a: {n}"
        valor = re.sub(r".*(peso.*raci[oó]n|raci[oó]n)\s*(es|son|:)?", "", original, flags=re.IGNORECASE).strip()
        valor = _limpiar_valor(valor) or original
        return "peso_racion", valor, f"Actualizar peso por ración a: {valor}"
    if "rendimiento" in t:
        valor = re.sub(r".*rendimiento\s*(es|son|:)?", "", original, flags=re.IGNORECASE).strip()
        valor = _limpiar_valor(valor) or original
        return "rendimiento_final", valor, f"Actualizar rendimiento final a: {valor}"
    if "conserv" in t or "guardar" in t or "cámara" in t or "camara" in t or "congelador" in t:
        valor = re.sub(r".*(conservación|conservacion|conservar|guardar)\s*(es|en|:)?", "", original, flags=re.IGNORECASE).strip()
        valor = _limpiar_valor(valor) or original
        return "conservacion", valor, f"Actualizar conservación a: {valor}"
    if "familia" in t:
        valor = re.sub(r".*familia\s*(es|:)?", "", original, flags=re.IGNORECASE).strip()
        valor = _limpiar_valor(valor) or original
        return "familia", valor, f"Actualizar familia a: {valor}"
    if "objetivo" in t:
        valor = re.sub(r".*objetivo\s*(es|:)?", "", original, flags=re.IGNORECASE).strip()
        valor = _limpiar_valor(valor) or original
        return "objetivo", valor, f"Actualizar objetivo a: {valor}"
    if "alérgeno" in t or "alergeno" in t or "alergia" in t:
        valor = re.sub(r".*(añade|agrega|meter|mete|alérgeno|alergeno|alergia|contiene)\s*", "", original, flags=re.IGNORECASE).strip()
        valor = valor.replace("el ", "").replace("la ", "").strip() or original
        return "alergenos_add", valor, f"Añadir alérgeno: {valor}"
    if any(x in t for x in ["thermomix","horno","abatidor","marmita","roner","freidora","fuego","maquinaria"]):
        valor = re.sub(r".*(añade|agrega|meter|mete|maquinaria|máquina|maquina)\s*", "", original, flags=re.IGNORECASE).strip()
        valor = valor.replace("la ", "").replace("el ", "").strip() or original
        return "maquinaria_imprescindible_add", valor, f"Añadir maquinaria: {valor}"
    if "control" in t or "calidad" in t:
        valor = re.sub(r".*(añade|agrega|control|calidad)\s*", "", original, flags=re.IGNORECASE).strip()
        valor = _limpiar_valor(valor) or original
        return "controles_calidad_add", valor, f"Añadir control de calidad: {valor}"
    if "haccp" in t or "crítico" in t or "critico" in t:
        valor = re.sub(r".*(añade|agrega|haccp|punto crítico|punto critico|crítico|critico)\s*", "", original, flags=re.IGNORECASE).strip()
        valor = _limpiar_valor(valor) or original
        return "puntos_criticos_haccp_add", valor, f"Añadir punto crítico HACCP: {valor}"
    if "nota" in t or "observación" in t or "observacion" in t:
        valor = re.sub(r".*(nota|observación|observacion)\s*(es|:)?", "", original, flags=re.IGNORECASE).strip()
        valor = _limpiar_valor(valor) or original
        return "notas_jefe_cocina", valor, "Actualizar notas de jefe de cocina."
    return "desconocido", original, "No he entendido a qué campo corresponde ese cambio."

def aplicar_cambio_a_dict(ficha: Dict, campo: str, valor: object) -> Dict:
    if campo == "desconocido":
        return ficha
    if campo.endswith("_add"):
        campo_real = campo.replace("_add", "")
        actual = ficha.get(campo_real) or []
        if not isinstance(actual, list):
            actual = [str(actual)]
        nuevos = [x.strip() for x in str(valor).replace(";", ",").split(",") if x.strip()]
        for n in nuevos:
            if n and n not in actual:
                actual.append(n)
        ficha[campo_real] = actual
        return ficha
    ficha[campo] = valor
    return ficha
