# -*- coding: utf-8 -*-
"""
SERVICIOS/produccion_desde_fichas.py
Sprint 6.1

Planificación realista desde fichas técnicas.

Corrige el problema del Sprint 6.0:
- Una fase posterior no puede empezar cuando empieza una cocción pasiva.
- Solo puede empezar cuando la fase anterior termina de verdad.
- Mientras una fase pasiva está en marcha, el cocinero queda libre para otras tareas.
- El mismo cocinero intenta continuar la elaboración.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple


BASE_DIR = Path(__file__).resolve().parents[1]
FICHAS_DIR = BASE_DIR / "DATOS" / "fichas_tecnicas"

INICIO_DIA = 8 * 60
MINUTOS_JORNADA = 8 * 60


def _normalizar(texto: str) -> str:
    texto = (texto or "").lower().strip()
    cambios = {
        "á": "a",
        "é": "e",
        "í": "i",
        "ó": "o",
        "ú": "u",
        "ü": "u",
        "ñ": "n",
    }
    for a, b in cambios.items():
        texto = texto.replace(a, b)
    return texto


def _hora_desde_minuto(minuto: int) -> str:
    minuto_dia = minuto % MINUTOS_JORNADA
    total = INICIO_DIA + minuto_dia
    h = total // 60
    m = total % 60
    return f"{h:02d}:{m:02d}"


def _dia(minuto: int) -> int:
    return minuto // MINUTOS_JORNADA + 1


def _fin_dia(dia: int) -> int:
    return dia * MINUTOS_JORNADA


def listar_fichas_disponibles() -> List[Dict]:
    fichas: List[Dict] = []

    if not FICHAS_DIR.exists():
        return fichas

    for path in sorted(FICHAS_DIR.glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            fichas.append(data)
        except Exception:
            continue

    return fichas


def buscar_fichas(texto: str) -> List[Dict]:
    q = _normalizar(texto)
    resultados: List[Dict] = []

    for ficha in listar_fichas_disponibles():
        codigo = _normalizar(ficha.get("codigo", ""))
        nombre = _normalizar(ficha.get("nombre", ""))
        familia = _normalizar(ficha.get("familia", ""))

        if q in codigo or q in nombre or q in familia:
            resultados.append(ficha)

    return resultados


def elegir_ficha() -> Optional[Dict]:
    texto = input("\n¿Qué ficha quieres convertir en producción? Escribe nombre o código: ").strip()

    if not texto:
        print("\nNo has escrito nada.")
        return None

    resultados = buscar_fichas(texto)

    if not resultados:
        print("\nNo he encontrado fichas con ese nombre.")
        return None

    if len(resultados) == 1:
        return resultados[0]

    print("\nHe encontrado varias fichas:")
    for i, ficha in enumerate(resultados, start=1):
        print(f"{i}. {ficha.get('nombre')} | Código: {ficha.get('codigo')} | Estado: {ficha.get('estado', '')}")

    seleccion = input("\nElige número: ").strip()

    try:
        idx = int(seleccion)
        if 1 <= idx <= len(resultados):
            return resultados[idx - 1]
    except ValueError:
        pass

    print("\nSelección no válida.")
    return None


def fase_a_tarea(ficha: Dict, fase: Dict) -> Dict:
    tiempo_activo = int(fase.get("tiempo_activo_min") or 0)
    tiempo_pasivo = int(fase.get("tiempo_pasivo_min") or 0)

    if tiempo_activo > 0 and tiempo_pasivo > 0:
        tipo = "mixta"
    elif tiempo_pasivo > 0:
        tipo = "pasiva"
    else:
        tipo = "activa"

    maquinaria = fase.get("maquinaria") or []
    if isinstance(maquinaria, str):
        maquinaria = [maquinaria]

    return {
        "id": fase.get("nombre", "Fase sin nombre"),
        "elaboracion": ficha.get("nombre", ""),
        "codigo_ficha": ficha.get("codigo", ""),
        "estado_ficha": ficha.get("estado", ""),
        "orden": int(fase.get("orden") or 0),
        "nombre": fase.get("nombre", "Fase sin nombre"),
        "descripcion": fase.get("descripcion", ""),
        "tipo": tipo,
        "tiempo_activo_min": tiempo_activo,
        "tiempo_pasivo_min": tiempo_pasivo,
        "tiempo_total_min": tiempo_activo + tiempo_pasivo,
        "maquinaria": maquinaria,
        "depende_de": fase.get("depende_de") or [],
        "desbloquea": fase.get("desbloquea") or [],
        "punto_critico": fase.get("punto_critico", ""),
        "control_calidad": fase.get("control_calidad", ""),
    }


def generar_tareas_desde_ficha(ficha: Dict) -> List[Dict]:
    fases = ficha.get("fases") or []
    tareas = [fase_a_tarea(ficha, fase) for fase in fases]
    tareas.sort(key=lambda t: t.get("orden", 0))

    # Si una ficha no trae depende_de en todas las fases, aplicamos dependencia secuencial real.
    # Esto evita que se pueda deshuesar durante el braseado.
    nombre_anterior = None
    for tarea in tareas:
        if nombre_anterior and not tarea.get("depende_de"):
            tarea["depende_de"] = [nombre_anterior]
            tarea["dependencia_auto"] = True
        else:
            tarea["dependencia_auto"] = False
        nombre_anterior = tarea["nombre"]

    return tareas


def analizar_riesgos_ficha(ficha: Dict, tareas: List[Dict]) -> List[str]:
    riesgos: List[str] = []

    estado = ficha.get("estado", "")
    if estado not in ["validada", "validada_demo", "produccion"]:
        riesgos.append("La ficha no está validada. Revisar antes de usar en producción real.")

    if ficha.get("preguntas_pendientes"):
        riesgos.append(f"La ficha tiene {len(ficha.get('preguntas_pendientes', []))} campos pendientes.")

    if not ficha.get("maquinaria_imprescindible"):
        riesgos.append("No hay maquinaria imprescindible definida.")

    if not ficha.get("vida_util"):
        riesgos.append("No hay vida útil definida.")

    if not ficha.get("regeneracion"):
        riesgos.append("No hay regeneración definida.")

    if not tareas:
        riesgos.append("La ficha no tiene fases de producción.")

    if tareas and all(t.get("tiempo_activo_min", 0) == 0 for t in tareas):
        riesgos.append("Las fases no tienen tiempos activos definidos.")

    if any(t.get("tiempo_pasivo_min", 0) >= 120 for t in tareas):
        riesgos.append("Hay tiempos pasivos largos. Conviene empezar con antelación.")

    if any("abatidor" in [m.lower() for m in t.get("maquinaria", [])] for t in tareas):
        riesgos.append("La producción necesita abatidor. Comprobar disponibilidad.")

    return riesgos


class PlanificadorFichaRealista:
    def __init__(self, numero_cocineros: int = 1):
        self.numero_cocineros = numero_cocineros
        self.disponible_cocinero: Dict[int, int] = {i: 0 for i in range(1, numero_cocineros + 1)}
        self.disponible_recurso: Dict[str, int] = {}
        self.completadas: Dict[str, int] = {}
        self.responsable_elaboracion: Dict[str, int] = {}
        self.bloques: List[Dict] = []

    def _normalizar_recurso(self, recurso) -> Optional[str]:
        if not recurso:
            return None
        if isinstance(recurso, list):
            if not recurso:
                return None
            return ", ".join(str(x) for x in recurso)
        return str(recurso)

    def _dependencias_cumplidas(self, tarea: Dict) -> bool:
        return all(dep in self.completadas for dep in tarea.get("depende_de", []))

    def _fin_dependencias(self, tarea: Dict) -> int:
        deps = tarea.get("depende_de", [])
        if not deps:
            return 0
        return max(self.completadas.get(dep, 0) for dep in deps)

    def _recurso_disponible(self, maquinaria: List[str]) -> int:
        if not maquinaria:
            return 0
        return max(self.disponible_recurso.get(m, 0) for m in maquinaria)

    def _mejor_cocinero(self, tarea: Dict, desde: int, duracion: int) -> Tuple[int, int]:
        elaboracion = tarea.get("elaboracion", "")
        responsable = self.responsable_elaboracion.get(elaboracion)
        candidatos: List[Tuple[int, int, int]] = []

        for cocinero, libre in self.disponible_cocinero.items():
            inicio = max(libre, desde)

            dia = _dia(inicio)
            if inicio + duracion > _fin_dia(dia):
                inicio = _fin_dia(dia)

            penalizacion = 0
            if responsable and cocinero != responsable:
                penalizacion = 120

            candidatos.append((penalizacion, inicio, cocinero))

        elegido = sorted(candidatos, key=lambda x: (x[0], x[1], x[2]))[0]
        return elegido[2], elegido[1]

    def _registrar_responsable(self, tarea: Dict, cocinero: int) -> None:
        elaboracion = tarea.get("elaboracion", "")
        if elaboracion and elaboracion not in self.responsable_elaboracion:
            self.responsable_elaboracion[elaboracion] = cocinero

    def planificar(self, tareas: List[Dict]) -> List[Dict]:
        pendientes = list(tareas)
        seguridad = 0

        while pendientes and seguridad < 1000:
            seguridad += 1

            disponibles = [t for t in pendientes if self._dependencias_cumplidas(t)]

            if not disponibles:
                # Si algo está mal escrito en dependencias, no bloqueamos todo:
                # lanzamos aviso y desbloqueamos la primera pendiente.
                tarea = pendientes.pop(0)
                tarea["aviso_dependencia"] = "Dependencia no encontrada o no completada. Revisar ficha técnica."
            else:
                disponibles.sort(key=lambda t: (self._fin_dependencias(t), t.get("orden", 0)))
                tarea = disponibles[0]
                pendientes.remove(tarea)

            self._planificar_tarea(tarea)

        self.bloques.sort(key=lambda b: (b.get("inicio", 0), b.get("cocinero") or 99, b.get("tipo_bloque", "")))
        return self.bloques

    def _planificar_tarea(self, tarea: Dict) -> None:
        activo = int(tarea.get("tiempo_activo_min") or 0)
        pasivo = int(tarea.get("tiempo_pasivo_min") or 0)
        maquinaria = tarea.get("maquinaria") or []

        desde = max(self._fin_dependencias(tarea), self._recurso_disponible(maquinaria))

        # Fase con parte activa.
        if activo > 0:
            cocinero, inicio_activo = self._mejor_cocinero(tarea, desde, activo)
            fin_activo = inicio_activo + activo

            self._registrar_responsable(tarea, cocinero)
            self.disponible_cocinero[cocinero] = fin_activo

            self.bloques.append(
                {
                    "tipo_bloque": "activo",
                    "tarea": tarea,
                    "inicio": inicio_activo,
                    "fin": fin_activo,
                    "cocinero": cocinero,
                    "nota": "Trabajo activo del cocinero.",
                }
            )

            inicio_pasivo = fin_activo

        else:
            # Fase solo pasiva: arranca cuando dependencias y recursos están disponibles.
            inicio_pasivo = desde
            fin_activo = desde

        # Fase con parte pasiva.
        if pasivo > 0:
            inicio_pasivo = max(inicio_pasivo, self._recurso_disponible(maquinaria))
            fin_pasivo = inicio_pasivo + pasivo

            for recurso in maquinaria:
                self.disponible_recurso[recurso] = fin_pasivo

            self.bloques.append(
                {
                    "tipo_bloque": "pasivo",
                    "tarea": tarea,
                    "inicio": inicio_pasivo,
                    "fin": fin_pasivo,
                    "cocinero": None,
                    "nota": "Tiempo pasivo real: ocupa maquinaria/recurso, pero no bloquea al cocinero.",
                }
            )

            # CLAVE 6.1:
            # La tarea no se considera completada al empezar el pasivo ni al acabar la parte activa,
            # sino al terminar de verdad la cocción/reposo/enfriado.
            self.completadas[tarea["nombre"]] = fin_pasivo

        else:
            self.completadas[tarea["nombre"]] = fin_activo

        if tarea.get("aviso_dependencia"):
            self.bloques[-1]["aviso_dependencia"] = tarea["aviso_dependencia"]


def crear_horario_realista(tareas: List[Dict], numero_cocineros: int = 1) -> List[Dict]:
    planificador = PlanificadorFichaRealista(numero_cocineros=numero_cocineros)
    return planificador.planificar(tareas)


def imprimir_produccion_desde_ficha(ficha: Dict) -> None:
    tareas = generar_tareas_desde_ficha(ficha)
    riesgos = analizar_riesgos_ficha(ficha, tareas)
    horario = crear_horario_realista(tareas, numero_cocineros=1)

    print()
    print("=" * 90)
    print("PRODUCCIÓN REALISTA DESDE FICHA TÉCNICA - SPRINT 6.1")
    print("=" * 90)
    print(f"Ficha: {ficha.get('nombre')}")
    print(f"Código interno: {ficha.get('codigo')}")
    print(f"Estado: {ficha.get('estado', '')}")
    print(f"Familia: {ficha.get('familia', '')}")
    print(f"Rendimiento: {ficha.get('rendimiento_final', '')}")
    print(f"Raciones: {ficha.get('raciones', '')} | Peso/ración: {ficha.get('peso_racion', '')}")

    print()
    print("TIEMPOS DE FICHA")
    print("-" * 90)
    print(f"Tiempo activo total: {ficha.get('tiempo_activo_min', 0)} min")
    print(f"Tiempo pasivo total: {ficha.get('tiempo_pasivo_min', 0)} min")
    print(f"Tiempo técnico total: {ficha.get('tiempo_total_min', 0)} min")

    if riesgos:
        print()
        print("RIESGOS / AVISOS")
        print("-" * 90)
        for riesgo in riesgos:
            print(f"⚠ {riesgo}")

    print()
    print("FASES CONVERTIDAS EN PRODUCCIÓN")
    print("-" * 90)

    for tarea in tareas:
        maquinaria_tarea = ", ".join(tarea.get("maquinaria") or []) or "Sin maquinaria"
        deps = ", ".join(tarea.get("depende_de") or []) or "Sin dependencias"

        print(f"{tarea.get('orden')}. {tarea.get('nombre')}")
        print(f"   Tipo: {tarea.get('tipo')}")
        print(f"   Activo: {tarea.get('tiempo_activo_min')} min | Pasivo: {tarea.get('tiempo_pasivo_min')} min")
        print(f"   Maquinaria: {maquinaria_tarea}")
        print(f"   Depende de: {deps}")

        if tarea.get("dependencia_auto"):
            print("   Nota: dependencia secuencial añadida automáticamente por Host AI.")

        if tarea.get("punto_critico"):
            print(f"   Punto crítico: {tarea.get('punto_critico')}")

        if tarea.get("control_calidad"):
            print(f"   Control: {tarea.get('control_calidad')}")

    print()
    print("HORARIO REALISTA DESDE FICHA")
    print("-" * 90)
    print("Regla: una fase posterior no empieza hasta que la fase anterior termina de verdad.")

    dia_actual = None

    for bloque in horario:
        dia = _dia(bloque.get("inicio", 0))
        if dia != dia_actual:
            dia_actual = dia
            print()
            print(f"DÍA {dia_actual}")

        tarea = bloque.get("tarea", {})
        etiqueta = "ACTIVO" if bloque.get("tipo_bloque") == "activo" else "PASIVO / EN MARCHA"

        responsable = f"Cocinero {bloque.get('cocinero')}" if bloque.get("cocinero") else "Maquinaria / tiempo pasivo"

        print(f"{_hora_desde_minuto(bloque.get('inicio', 0))} - {_hora_desde_minuto(bloque.get('fin', 0))} | {etiqueta} | {responsable}")
        print(f"  {tarea.get('nombre')}")

        if bloque.get("tipo_bloque") == "pasivo":
            print("  Motivo: esta fase está en marcha, pero el cocinero puede avanzar otras tareas.")
            print("  Importante: la siguiente fase no se desbloquea hasta que esto termine.")

        if bloque.get("nota"):
            print(f"  Nota: {bloque.get('nota')}")

        if bloque.get("aviso_dependencia"):
            print(f"  ⚠ {bloque.get('aviso_dependencia')}")

    print()
    print("=" * 90)
    print("LECTURA DE JEFE DE COCINA")
    print("=" * 90)
    print("- Ya no se puede deshuesar una carrillera mientras todavía está braseando.")
    print("- Una cocción pasiva libera al cocinero, pero no desbloquea la siguiente fase hasta terminar.")
    print("- Host AI añade dependencias secuenciales si la ficha no las trae.")
    print("- En Sprint 6.2 conectaremos esto con escandallos completos.")


def menu_produccion_desde_fichas() -> None:
    ficha = elegir_ficha()

    if not ficha:
        return

    imprimir_produccion_desde_ficha(ficha)
