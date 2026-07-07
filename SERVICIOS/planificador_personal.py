# -*- coding: utf-8 -*-
"""
SERVICIOS/planificador_personal.py
Sprint 6.2.1 - Hotfix jornadas reales por día

Corrección clave:
- El total activo se calcula POR COCINERO Y POR DÍA.
- Día 1 se rellena de 08:00 a 15:30 para Cocinero 1, 2 y 3.
- Día 2 solo muestra lo que falte para terminar producción; NO se rellena a 7h30.
- Las cocciones/reposos/enfriados siguen en bloque aparte.
- Las elaboraciones mantienen responsable siempre que se pueda.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


INICIO_DIA = 8 * 60
MINUTOS_DIA = 8 * 60
OBJETIVO_DIA_1 = 7 * 60 + 30  # 08:00 - 15:30


@dataclass
class Fase:
    nombre: str
    duracion_activa: int = 0
    duracion_pasiva: int = 0
    recurso: Optional[str] = None
    motivo: str = ""
    punto_critico: str = ""


@dataclass
class Elaboracion:
    nombre: str
    prioridad: int
    fases: List[Fase]
    responsable: Optional[int] = None
    critica: bool = False
    flexible: bool = False


@dataclass
class Bloque:
    elaboracion: str
    fase: str
    inicio: int
    fin: int
    cocinero: Optional[int]
    tipo: str
    recurso: Optional[str] = None
    motivo: str = ""
    punto_critico: str = ""
    relleno: bool = False

    @property
    def dia(self) -> int:
        return self.inicio // MINUTOS_DIA + 1


def _dia(minuto: int) -> int:
    return minuto // MINUTOS_DIA + 1


def _fin_dia(dia: int) -> int:
    return dia * MINUTOS_DIA


def _inicio_dia(dia: int) -> int:
    return (dia - 1) * MINUTOS_DIA


def _hora(minuto: int) -> str:
    minuto_dia = minuto % MINUTOS_DIA
    total = INICIO_DIA + minuto_dia
    return f"{total // 60:02d}:{total % 60:02d}"


def _hora_fin(minuto: int) -> str:
    if minuto > 0 and minuto % MINUTOS_DIA == 0:
        total = INICIO_DIA + MINUTOS_DIA
        return f"{total // 60:02d}:{total % 60:02d}"
    return _hora(minuto)


def _intervalo(inicio: int, fin: int) -> str:
    if _dia(inicio) == _dia(fin - 1 if fin > inicio else fin):
        return f"{_hora(inicio)} - {_hora_fin(fin)}"
    return f"Día {_dia(inicio)} {_hora(inicio)} - Día {_dia(fin - 1)} {_hora_fin(fin)}"


def _cabe_en_dia(inicio: int, duracion: int) -> bool:
    return inicio + duracion <= _fin_dia(_dia(inicio))


def _mover_a_siguiente_dia(inicio: int) -> int:
    return _fin_dia(_dia(inicio))


def elaboraciones_demo() -> List[Elaboracion]:
    return [
        Elaboracion(
            nombre="Carrilleras braseadas prensadas",
            prioridad=100,
            critica=True,
            fases=[
                Fase("Limpiar y racionar carrilleras", 40, motivo="Preparar carne antes de marcar."),
                Fase("Cortar bresa de carrilleras", 30, motivo="Bresa de la misma elaboración."),
                Fase("Marcar carrilleras", 35, recurso="fuego", motivo="Generar sabor antes del braseado."),
                Fase("Sofreír bresa y desglasar", 30, recurso="fuego", motivo="Base de braseado."),
                Fase("Brasear carrilleras", 10, 180, recurso="horno", motivo="Cocción larga: libera cocinero, pero la carrillera no está lista hasta terminar.", punto_critico="No deshuesar hasta acabar el braseado."),
                Fase("Deshuesar y colar salsa", 45, motivo="Solo después de terminar el braseado."),
                Fase("Prensar carrilleras", 25, 120, motivo="Prensado mínimo para corte limpio."),
                Fase("Abatir carrilleras", 10, 60, recurso="abatidor", motivo="Seguridad alimentaria antes de cámara."),
                Fase("Porcionar y etiquetar carrilleras", 35, motivo="Producción cerrada: peso, lote, fecha y cámara."),
            ],
        ),
        Elaboracion(
            nombre="Fondo oscuro / demi-glace",
            prioridad=95,
            critica=True,
            fases=[
                Fase("Tostar huesos", 45, recurso="horno", motivo="Base de sabor."),
                Fase("Cortar bresa de fondo", 25, motivo="Bresa del fondo."),
                Fase("Arrancar fondo con huesos y bresa", 25, recurso="marmita", motivo="Inicio antes de cocción larga."),
                Fase("Cocer fondo oscuro", 5, 180, recurso="marmita", motivo="Tiempo pasivo largo: marmita ocupada, cocinero libre.", punto_critico="No colar antes de acabar la cocción."),
                Fase("Colar fondo", 25, recurso="marmita", motivo="Después de cocer completo."),
                Fase("Reducir demi-glace", 15, 90, recurso="marmita", motivo="Reducción pasiva vigilada."),
                Fase("Abatir y envasar demi-glace", 30, recurso="abatidor", motivo="Bolsas/raciones etiquetadas."),
            ],
        ),
        Elaboracion(
            nombre="Croquetas base",
            prioridad=70,
            fases=[
                Fase("Pesar ingredientes de croquetas", 20, motivo="Preparar todo antes de fuego."),
                Fase("Preparar bechamel", 45, recurso="fuego", motivo="Trabajo activo de base."),
                Fase("Enfriar bechamel", 5, 90, recurso="abatidor", motivo="Enfriado pasivo: abatidor ocupado."),
                Fase("Formar croquetas", 60, motivo="Depende de bechamel fría."),
                Fase("Empanar croquetas", 50, motivo="Dejar listas para servicio o congelación."),
                Fase("Etiquetar croquetas", 20, motivo="Cierre de producción."),
            ],
        ),
        Elaboracion(
            nombre="Salsas y mise en place fría",
            prioridad=55,
            flexible=True,
            fases=[
                Fase("Preparar alioli", 20, recurso="thermomix", motivo="Tarea corta para huecos."),
                Fase("Preparar encurtidos", 30, motivo="Adelantable."),
                Fase("Cortar verduras de guarnición", 45, motivo="Mise en place fría."),
                Fase("Preparar salsa fría de servicio", 35, motivo="Relleno útil."),
                Fase("Revisar y ordenar cámara de producción", 30, motivo="Control real de cocina."),
            ],
        ),
    ]


class MotorPlanificacionElaboraciones:
    def __init__(self, numero_cocineros: int = 3):
        self.numero_cocineros = numero_cocineros
        self.disponible_cocinero: Dict[int, int] = {i: 0 for i in range(1, numero_cocineros + 1)}
        self.disponible_recurso: Dict[str, int] = {}
        self.bloques: List[Bloque] = []
        self.indice_fase: Dict[str, int] = {}
        self.elaboracion_lista_en: Dict[str, int] = {}

    def _recurso_libre(self, recurso: Optional[str]) -> int:
        if not recurso:
            return 0
        return self.disponible_recurso.get(recurso, 0)

    def _carga_total_cocinero(self, cocinero: int) -> int:
        return sum((b.fin - b.inicio) for b in self.bloques if b.cocinero == cocinero)

    def _elegir_responsable_inicial(self, elaboracion: Elaboracion) -> int:
        candidatos = []
        for cocinero in range(1, self.numero_cocineros + 1):
            candidatos.append((self._carga_total_cocinero(cocinero), self.disponible_cocinero[cocinero], cocinero))
        return sorted(candidatos)[0][2]

    def _responsable(self, elaboracion: Elaboracion, asignar: bool) -> int:
        if elaboracion.responsable is None:
            elegido = self._elegir_responsable_inicial(elaboracion)
            if asignar:
                elaboracion.responsable = elegido
            return elegido
        return elaboracion.responsable

    def _inicio_activo(self, cocinero: int, desde: int, duracion: int) -> int:
        inicio = max(self.disponible_cocinero[cocinero], desde)
        if duracion > 0 and not _cabe_en_dia(inicio, duracion):
            inicio = _mover_a_siguiente_dia(inicio)
        return inicio

    def _fase_actual(self, elaboracion: Elaboracion) -> Optional[Fase]:
        idx = self.indice_fase.get(elaboracion.nombre, 0)
        if idx >= len(elaboracion.fases):
            return None
        return elaboracion.fases[idx]

    def _candidato(self, elaboracion: Elaboracion):
        fase = self._fase_actual(elaboracion)
        if not fase:
            return None

        cocinero = self._responsable(elaboracion, asignar=False)
        desde = max(self.elaboracion_lista_en.get(elaboracion.nombre, 0), self._recurso_libre(fase.recurso))

        if fase.duracion_activa > 0:
            inicio = self._inicio_activo(cocinero, desde, fase.duracion_activa)
        else:
            inicio = desde

        return (inicio, -elaboracion.prioridad, -int(elaboracion.critica), elaboracion.nombre, elaboracion, fase)

    def planificar(self, elaboraciones: List[Elaboracion]) -> List[Bloque]:
        self.indice_fase = {e.nombre: 0 for e in elaboraciones}
        self.elaboracion_lista_en = {e.nombre: 0 for e in elaboraciones}

        seguridad = 0
        while seguridad < 1000:
            seguridad += 1
            candidatos = []

            for elaboracion in elaboraciones:
                candidato = self._candidato(elaboracion)
                if candidato:
                    candidatos.append(candidato)

            if not candidatos:
                break

            _, _, _, _, elaboracion, fase = sorted(candidatos)[0]
            self._planificar_fase(elaboracion, fase)
            self.indice_fase[elaboracion.nombre] += 1

        self._rellenar_dia_1_hasta_1530()
        self.bloques.sort(key=lambda b: (b.inicio, b.cocinero or 99, b.tipo))
        return self.bloques

    def _planificar_fase(self, elaboracion: Elaboracion, fase: Fase) -> None:
        cocinero = self._responsable(elaboracion, asignar=True)
        desde = max(self.elaboracion_lista_en.get(elaboracion.nombre, 0), self._recurso_libre(fase.recurso))

        if fase.duracion_activa > 0:
            inicio_activo = self._inicio_activo(cocinero, desde, fase.duracion_activa)
            fin_activo = inicio_activo + fase.duracion_activa
            self.disponible_cocinero[cocinero] = fin_activo

            self.bloques.append(
                Bloque(
                    elaboracion=elaboracion.nombre,
                    fase=fase.nombre,
                    inicio=inicio_activo,
                    fin=fin_activo,
                    cocinero=cocinero,
                    tipo="activo",
                    recurso=fase.recurso,
                    motivo=fase.motivo,
                    punto_critico=fase.punto_critico,
                )
            )
            inicio_pasivo = fin_activo
        else:
            inicio_pasivo = desde
            fin_activo = desde

        if fase.duracion_pasiva > 0:
            inicio_pasivo = max(inicio_pasivo, self._recurso_libre(fase.recurso))
            fin_pasivo = inicio_pasivo + fase.duracion_pasiva

            if fase.recurso:
                self.disponible_recurso[fase.recurso] = fin_pasivo

            self.bloques.append(
                Bloque(
                    elaboracion=elaboracion.nombre,
                    fase=fase.nombre,
                    inicio=inicio_pasivo,
                    fin=fin_pasivo,
                    cocinero=None,
                    tipo="pasivo",
                    recurso=fase.recurso,
                    motivo=fase.motivo,
                    punto_critico=fase.punto_critico,
                )
            )
            self.elaboracion_lista_en[elaboracion.nombre] = fin_pasivo
        else:
            self.elaboracion_lista_en[elaboracion.nombre] = fin_activo

    def _bloques_activos_cocinero_dia(self, cocinero: int, dia: int) -> List[Bloque]:
        return sorted(
            [b for b in self.bloques if b.cocinero == cocinero and b.dia == dia],
            key=lambda b: b.inicio,
        )

    def _rellenar_dia_1_hasta_1530(self) -> None:
        """
        Rellena SOLO el día 1 hasta 15:30.
        Día 2 no se rellena artificialmente: solo aparecerá lo que falte de producción real.
        """
        tareas = [
            ("Control", "Revisión de cámaras, producción disponible y caducidades", "Trabajo real para cerrar huecos del día 1."),
            ("Registro", "Actualizar registros de producción y etiquetas", "Sin registro la producción no está terminada."),
            ("Mise en place", "Adelantar mise en place de mañana", "Trabajo útil si hay hueco durante esperas."),
            ("Organización", "Preparar GN, bolsas y etiquetas para mañana", "Evita pérdidas de tiempo mañana."),
            ("Cierre", "Limpieza profunda de zona de producción", "Cierre operativo real."),
        ]

        inicio_dia = _inicio_dia(1)
        fin_objetivo = inicio_dia + OBJETIVO_DIA_1

        for cocinero in range(1, self.numero_cocineros + 1):
            ocupados = self._bloques_activos_cocinero_dia(cocinero, 1)
            cursor = inicio_dia
            indice = 0

            for bloque in ocupados:
                if bloque.inicio > cursor:
                    cursor = self._crear_relleno_en_hueco(cocinero, cursor, min(bloque.inicio, fin_objetivo), tareas, indice)
                    indice += 1

                cursor = max(cursor, bloque.fin)

                if cursor >= fin_objetivo:
                    break

            if cursor < fin_objetivo:
                self._crear_relleno_en_hueco(cocinero, cursor, fin_objetivo, tareas, indice)

    def _crear_relleno_en_hueco(self, cocinero: int, inicio: int, fin: int, tareas, indice_inicial: int) -> int:
        cursor = inicio
        indice = indice_inicial

        while cursor < fin:
            elaboracion, fase, motivo = tareas[indice % len(tareas)]
            duracion = min(30, fin - cursor)

            self.bloques.append(
                Bloque(
                    elaboracion=elaboracion,
                    fase=fase,
                    inicio=cursor,
                    fin=cursor + duracion,
                    cocinero=cocinero,
                    tipo="activo",
                    motivo=motivo,
                    relleno=True,
                )
            )

            cursor += duracion
            indice += 1

        return cursor


def _imprimir_bloque(bloque: Bloque) -> None:
    marca = " [hueco útil]" if bloque.relleno else ""
    print(f"{_intervalo(bloque.inicio, bloque.fin)} | {bloque.elaboracion}{marca}")
    print(f"  {bloque.fase}")

    if bloque.recurso:
        print(f"  Recurso: {bloque.recurso}")

    if bloque.motivo:
        print(f"  Motivo: {bloque.motivo}")

    if bloque.punto_critico:
        print(f"  Punto crítico: {bloque.punto_critico}")


def imprimir_planificacion_personal_completa(numero_cocineros: int = 3, horas_jornada: int = 8) -> None:
    motor = MotorPlanificacionElaboraciones(numero_cocineros=numero_cocineros)
    bloques = motor.planificar(elaboraciones_demo())

    print()
    print("=" * 96)
    print("PLANIFICACIÓN POR ELABORACIONES - SPRINT 6.2.1")
    print("=" * 96)
    print("Regla: Día 1 se muestra completo de 08:00 a 15:30 para cada cocinero.")
    print("Regla: Día 2 solo muestra producción real pendiente, sin rellenar horas.")

    for cocinero in range(1, numero_cocineros + 1):
        print()
        print("-" * 96)
        print(f"COCINERO {cocinero}")
        print("-" * 96)

        bloques_cocinero = sorted([b for b in bloques if b.cocinero == cocinero], key=lambda b: (b.dia, b.inicio))
        dias = sorted(set(b.dia for b in bloques_cocinero))

        for dia in dias:
            print()
            print(f"DÍA {dia}")

            minutos_dia = 0
            for bloque in [b for b in bloques_cocinero if b.dia == dia]:
                minutos_dia += bloque.fin - bloque.inicio
                _imprimir_bloque(bloque)

            print(f"TOTAL ACTIVO DÍA {dia} COCINERO {cocinero}: {minutos_dia // 60}h {minutos_dia % 60}min")

    pasivos = sorted([b for b in bloques if b.cocinero is None], key=lambda b: (b.dia, b.inicio))

    if pasivos:
        print()
        print("-" * 96)
        print("COCCIONES / REPOSOS / ENFRIADOS EN MARCHA")
        print("-" * 96)

        dia_actual = None
        for bloque in pasivos:
            if bloque.dia != dia_actual:
                dia_actual = bloque.dia
                print()
                print(f"DÍA {dia_actual}")

            recurso = f" | Recurso: {bloque.recurso}" if bloque.recurso else ""
            print(f"{_intervalo(bloque.inicio, bloque.fin)} | {bloque.elaboracion}{recurso}")
            print(f"  {bloque.fase}")
            print("  Nota: está en marcha; libera al cocinero, pero no desbloquea la siguiente fase hasta terminar.")

            if bloque.punto_critico:
                print(f"  Punto crítico: {bloque.punto_critico}")

    print()
    print("=" * 96)
    print("LECTURA DE JEFE DE COCINA")
    print("=" * 96)
    print("- El total ya no se calcula mezclando Día 1 y Día 2.")
    print("- Día 1 queda completo hasta 15:30 para cada cocinero.")
    print("- Día 2 aparece solo si queda producción pendiente real.")
    print("- Los huecos del Día 1 se rellenan con trabajo útil de cocina, no con tareas falsas.")


if __name__ == "__main__":
    imprimir_planificacion_personal_completa()
