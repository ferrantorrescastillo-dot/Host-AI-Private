# -*- coding: utf-8 -*-
"""
Planificador por personal - Sprint 5.6.6

Mejora sobre Sprint 5.6.5:
- Mantiene la salida agrupada por Cocinero 1, Cocinero 2, Cocinero 3.
- Añade "dueño de elaboración": quien empieza una elaboración intenta seguirla hasta terminarla.
- Reparte mejor la carga para que Cocinero 2 y Cocinero 3 no se queden demasiado cortos.
- Distingue tiempo activo y tiempo pasivo.
- Las cocciones pasivas ocupan maquinaria, pero no bloquean al cocinero.
- Si no cabe en la jornada de 8 horas, pasa al día siguiente.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


INICIO_DIA = 8 * 60
MINUTOS_JORNADA = 8 * 60


@dataclass
class FaseProduccion:
    nombre: str
    duracion: int
    tipo: str = "activa"  # activa | pasiva | cierre
    recurso: Optional[str] = None
    depende_de: List[str] = field(default_factory=list)
    motivo: str = ""
    elaboracion: str = ""
    prioridad: int = 50
    flexible: bool = False  # tareas genéricas que sirven para rellenar carga


@dataclass
class BloquePlanificado:
    fase: FaseProduccion
    inicio: int
    fin: int
    cocinero: Optional[int] = None
    nota: str = ""

    @property
    def dia(self) -> int:
        return self.inicio // MINUTOS_JORNADA + 1


def _dia(minuto: int) -> int:
    return minuto // MINUTOS_JORNADA + 1


def _fin_del_dia(dia: int) -> int:
    return dia * MINUTOS_JORNADA


def _hora(minuto: int) -> str:
    minuto_dia = minuto % MINUTOS_JORNADA
    total = INICIO_DIA + minuto_dia
    h = total // 60
    m = total % 60
    return f"{h:02d}:{m:02d}"


def tareas_demo_completas() -> List[FaseProduccion]:
    return [
        FaseProduccion(
            "Revisión inicial de producción, cámaras, stock y prioridades",
            20, "activa",
            motivo="Antes de producir, el jefe revisa riesgos, cámaras, pedidos, faltantes y prioridades.",
            elaboracion="Organización", prioridad=100, flexible=True,
        ),
        FaseProduccion(
            "Preparar mesas, GN, bandejas, etiquetas y zona de trabajo",
            20, "activa",
            motivo="Mise en place general para trabajar limpio y no perder tiempo durante la producción.",
            elaboracion="Organización", prioridad=95, flexible=True,
        ),

        # Fondo oscuro
        FaseProduccion(
            "Tostar huesos para fondo oscuro",
            45, "activa", "horno",
            motivo="Fase inicial que desbloquea el fondo oscuro.",
            elaboracion="Fondo oscuro", prioridad=95,
        ),
        FaseProduccion(
            "Cortar bresa para fondo oscuro",
            25, "activa",
            motivo="La misma persona que lleva el fondo intenta preparar también su bresa.",
            elaboracion="Fondo oscuro", prioridad=90,
        ),
        FaseProduccion(
            "Arrancar fondo oscuro con bresa y huesos",
            25, "activa", "marmita",
            ["Tostar huesos para fondo oscuro", "Cortar bresa para fondo oscuro"],
            "Fase activa antes de una cocción pasiva larga.",
            "Fondo oscuro", prioridad=90,
        ),
        FaseProduccion(
            "Cocer fondo oscuro",
            180, "pasiva", "marmita",
            ["Arrancar fondo oscuro con bresa y huesos"],
            "Porción pasiva larga: ocupa marmita, pero el cocinero queda libre para avanzar otras tareas.",
            "Fondo oscuro", prioridad=80,
        ),
        FaseProduccion(
            "Colar y reducir fondo oscuro",
            45, "activa", "marmita",
            ["Cocer fondo oscuro"],
            "No puede empezar hasta terminar las 3 horas reales de cocción.",
            "Fondo oscuro", prioridad=75,
        ),
        FaseProduccion(
            "Abatir, envasar y etiquetar fondo oscuro",
            30, "activa", "abatidor",
            ["Colar y reducir fondo oscuro"],
            "Una producción no está terminada hasta abatir, etiquetar y registrar.",
            "Fondo oscuro", prioridad=70,
        ),

        # Carrilleras
        FaseProduccion(
            "Limpiar y racionar carrilleras",
            40, "activa",
            motivo="Quien empieza carrilleras intenta continuar la elaboración para no perder control.",
            elaboracion="Carrilleras", prioridad=92,
        ),
        FaseProduccion(
            "Cortar verdura/bresa para carrilleras",
            30, "activa",
            motivo="La bresa forma parte de la misma elaboración; idealmente la hace el mismo cocinero.",
            elaboracion="Carrilleras", prioridad=90,
        ),
        FaseProduccion(
            "Marcar carrilleras",
            35, "activa", "fuego",
            ["Limpiar y racionar carrilleras"],
            "Marcado para generar sabor antes del braseado.",
            "Carrilleras", prioridad=88,
        ),
        FaseProduccion(
            "Preparar salsa/base de braseado",
            30, "activa", "fuego",
            ["Cortar verdura/bresa para carrilleras"],
            "Base de cocción para las carrilleras.",
            "Carrilleras", prioridad=86,
        ),
        FaseProduccion(
            "Brasear carrilleras",
            180, "pasiva", "horno",
            ["Marcar carrilleras", "Preparar salsa/base de braseado"],
            "Cocción pasiva larga: ocupa horno, pero libera al cocinero.",
            "Carrilleras", prioridad=80,
        ),
        FaseProduccion(
            "Deshuesar carrilleras y colar salsa",
            45, "activa",
            depende_de=["Brasear carrilleras"],
            motivo="No puede empezar hasta que acabe el braseado real.",
            elaboracion="Carrilleras", prioridad=72,
        ),
        FaseProduccion(
            "Prensar carrilleras",
            25, "activa",
            depende_de=["Deshuesar carrilleras y colar salsa"],
            motivo="El prensado se hace cuando la carne ya está cocinada y limpia.",
            elaboracion="Carrilleras", prioridad=70,
        ),
        FaseProduccion(
            "Abatir carrilleras prensadas",
            40, "activa", "abatidor",
            ["Prensar carrilleras"],
            "Abatir antes de cámara para seguridad y conservación.",
            "Carrilleras", prioridad=68,
        ),

        # Croquetas
        FaseProduccion(
            "Preparar bechamel base",
            45, "activa", "fuego",
            motivo="Producción que puede avanzar en paralelo si hay fuego libre.",
            elaboracion="Croquetas", prioridad=65,
        ),
        FaseProduccion(
            "Enfriar bechamel",
            60, "pasiva", "abatidor",
            ["Preparar bechamel base"],
            "Tiempo pasivo de enfriado. Ocupa abatidor, no al cocinero.",
            "Croquetas", prioridad=50,
        ),
        FaseProduccion(
            "Formar croquetas",
            60, "activa",
            depende_de=["Enfriar bechamel"],
            motivo="Depende de que la bechamel esté fría y trabajable.",
            elaboracion="Croquetas", prioridad=48,
        ),
        FaseProduccion(
            "Empanar croquetas",
            50, "activa",
            depende_de=["Formar croquetas"],
            motivo="Después de formar, se empana y se deja listo para servicio o congelación.",
            elaboracion="Croquetas", prioridad=46,
        ),

        # Relleno y mise en place para equilibrar jornada
        FaseProduccion(
            "Preparar alioli",
            20, "activa", "thermomix",
            motivo="Tarea corta ideal para colocar durante cocciones pasivas.",
            elaboracion="Salsas", prioridad=58, flexible=True,
        ),
        FaseProduccion(
            "Preparar encurtidos",
            30, "activa",
            motivo="Tarea rápida y adelantable.",
            elaboracion="Mise en place", prioridad=56, flexible=True,
        ),
        FaseProduccion(
            "Cortar verduras de guarnición",
            45, "activa",
            motivo="Mise en place que cabe mientras cuecen fondos o braseados.",
            elaboracion="Mise en place", prioridad=54, flexible=True,
        ),
        FaseProduccion(
            "Preparar salsa fría / mise en place de servicio",
            35, "activa",
            motivo="Tarea flexible para equilibrar carga entre cocineros.",
            elaboracion="Mise en place", prioridad=40, flexible=True,
        ),
        FaseProduccion(
            "Revisar cámaras, pesos y producción disponible",
            35, "activa",
            motivo="Trabajo necesario de control para no producir a ciegas.",
            elaboracion="Control", prioridad=38, flexible=True,
        ),
        FaseProduccion(
            "Racionar y etiquetar elaboraciones terminadas",
            45, "activa",
            motivo="Peso, etiqueta, fecha, lote y ubicación. Sin esto la producción no está cerrada.",
            elaboracion="Registro", prioridad=35, flexible=True,
        ),
        FaseProduccion(
            "Adelantar mise en place de mañana",
            60, "activa",
            motivo="Si un cocinero se queda corto, adelanta trabajo útil para mañana.",
            elaboracion="Mise en place", prioridad=25, flexible=True,
        ),

        FaseProduccion(
            "Checklist final de producción, cámaras, limpieza y pendientes de mañana",
            30, "cierre",
            motivo="Se hace al final: revisar terminado, etiquetado, cámaras, limpieza y pendientes.",
            elaboracion="Cierre", prioridad=0, flexible=True,
        ),
    ]


class PlanificadorPersonal:
    def __init__(self, numero_cocineros: int = 3, horas_jornada: int = 8):
        self.numero_cocineros = numero_cocineros
        self.minutos_jornada = horas_jornada * 60
        self.disponible_cocinero: Dict[int, int] = {i: 0 for i in range(1, numero_cocineros + 1)}
        self.disponible_recurso: Dict[str, int] = {}
        self.completadas: Dict[str, int] = {}
        self.dueno_elaboracion: Dict[str, int] = {}
        self.bloques: List[BloquePlanificado] = []

    def _normalizar_recurso(self, recurso) -> Optional[str]:
        if recurso is None:
            return None
        if isinstance(recurso, list):
            return ", ".join(str(x) for x in recurso)
        return str(recurso)

    def _dependencias_cumplidas(self, fase: FaseProduccion) -> bool:
        return all(dep in self.completadas for dep in fase.depende_de)

    def _momento_dependencias(self, fase: FaseProduccion) -> int:
        if not fase.depende_de:
            return 0
        return max(self.completadas.get(dep, 0) for dep in fase.depende_de)

    def _inicio_con_recursos(self, fase: FaseProduccion) -> int:
        inicio = self._momento_dependencias(fase)
        recurso = self._normalizar_recurso(fase.recurso)
        if recurso:
            inicio = max(inicio, self.disponible_recurso.get(recurso, 0))
        return inicio

    def _siguiente_candidato(self, pendientes: List[FaseProduccion]) -> Optional[FaseProduccion]:
        disponibles = [f for f in pendientes if self._dependencias_cumplidas(f)]
        if not disponibles:
            return None

        def clave(fase: FaseProduccion):
            recurso = self._normalizar_recurso(fase.recurso)
            recurso_libre = self.disponible_recurso.get(recurso, 0) if recurso else 0
            dependencias = self._momento_dependencias(fase)
            puede_empezar = max(recurso_libre, dependencias)

            # Se intenta empezar pronto lo largo/pasivo para abrir huecos.
            larga_o_pasiva = 1 if fase.tipo == "pasiva" or fase.duracion >= 90 else 0

            # Las flexibles van después de las elaboraciones principales, salvo que rellenen huecos.
            flexible_penaliza = 1 if fase.flexible else 0

            return (puede_empezar, flexible_penaliza, -fase.prioridad, -larga_o_pasiva, fase.duracion)

        return sorted(disponibles, key=clave)[0]

    def _carga_cocinero(self, cocinero: int) -> int:
        return sum((b.fin - b.inicio) for b in self.bloques if b.cocinero == cocinero)

    def _mejor_cocinero_para_fase(self, fase: FaseProduccion, desde: int) -> Tuple[int, int]:
        candidatos: List[Tuple[int, int, int, int]] = []

        dueno = self.dueno_elaboracion.get(fase.elaboracion) if fase.elaboracion and not fase.flexible else None

        for cocinero, libre in self.disponible_cocinero.items():
            inicio = max(libre, desde)
            dia = _dia(inicio)

            if inicio + fase.duracion > _fin_del_dia(dia):
                inicio = _fin_del_dia(dia)

            mismo_dueno_penaliza = 0
            if dueno and cocinero != dueno:
                # Penaliza cambiar de cocinero dentro de la misma elaboración.
                mismo_dueno_penaliza = 120

            # Para tareas flexibles, favorecemos al cocinero con menos carga.
            carga = self._carga_cocinero(cocinero)

            candidatos.append((mismo_dueno_penaliza, inicio, carga, cocinero))

        elegido = sorted(candidatos, key=lambda x: (x[0], x[1], x[2], x[3]))[0]
        penalizacion, inicio, carga, cocinero = elegido
        return cocinero, inicio

    def planificar(self, fases: Optional[List[FaseProduccion]] = None) -> List[BloquePlanificado]:
        fases = list(fases or tareas_demo_completas())
        cierres = [f for f in fases if f.tipo == "cierre"]
        pendientes = [f for f in fases if f.tipo != "cierre"]

        seguridad = 0
        while pendientes and seguridad < 1000:
            seguridad += 1
            fase = self._siguiente_candidato(pendientes)

            if fase is None:
                fase = pendientes.pop(0)
                fase.motivo += " | AVISO: dependencia no encontrada. Revisar ficha técnica."
            else:
                pendientes.remove(fase)

            self._planificar_fase(fase)

        self._planificar_cierres(cierres)
        self.bloques.sort(key=lambda b: (b.dia, b.cocinero or 99, b.inicio))
        return self.bloques

    def _planificar_fase(self, fase: FaseProduccion) -> None:
        desde = self._inicio_con_recursos(fase)
        recurso = self._normalizar_recurso(fase.recurso)

        if fase.tipo == "pasiva":
            inicio = desde
            fin = inicio + fase.duracion

            if recurso:
                self.disponible_recurso[recurso] = fin

            self.completadas[fase.nombre] = fin
            self.bloques.append(
                BloquePlanificado(
                    fase=fase,
                    inicio=inicio,
                    fin=fin,
                    cocinero=None,
                    nota="Tiempo pasivo: ocupa recurso/maquinaria, pero no bloquea a ningún cocinero.",
                )
            )
            return

        cocinero, inicio = self._mejor_cocinero_para_fase(fase, desde)
        fin = inicio + fase.duracion

        if recurso:
            self.disponible_recurso[recurso] = fin

        self.disponible_cocinero[cocinero] = fin
        self.completadas[fase.nombre] = fin

        # Asignar dueño de elaboración para recetas reales.
        if fase.elaboracion and fase.elaboracion not in ["Organización", "Mise en place", "Control", "Registro", "Cierre"] and not fase.flexible:
            self.dueno_elaboracion.setdefault(fase.elaboracion, cocinero)

        nota = ""
        dueno = self.dueno_elaboracion.get(fase.elaboracion)
        if dueno == cocinero and fase.elaboracion:
            nota = f"Dueño de elaboración: Cocinero {cocinero} intenta seguir {fase.elaboracion}."

        self.bloques.append(BloquePlanificado(fase=fase, inicio=inicio, fin=fin, cocinero=cocinero, nota=nota))

    def _planificar_cierres(self, cierres: List[FaseProduccion]) -> None:
        if not cierres:
            return

        ultimo_fin = max([0] + [b.fin for b in self.bloques])
        ultimo_dia = _dia(ultimo_fin)

        for fase in cierres:
            inicio_objetivo = _fin_del_dia(ultimo_dia) - fase.duracion
            candidatos = []

            for cocinero, libre in self.disponible_cocinero.items():
                if libre <= inicio_objetivo:
                    candidatos.append((self._carga_cocinero(cocinero), cocinero, inicio_objetivo))
                else:
                    dia = _dia(libre)
                    if libre + fase.duracion > _fin_del_dia(dia):
                        dia += 1
                    candidatos.append((self._carga_cocinero(cocinero), cocinero, _fin_del_dia(dia) - fase.duracion))

            _, cocinero, inicio = sorted(candidatos, key=lambda x: (x[2], x[0], x[1]))[0]
            fin = inicio + fase.duracion
            self.disponible_cocinero[cocinero] = fin
            self.completadas[fase.nombre] = fin
            self.bloques.append(
                BloquePlanificado(
                    fase=fase,
                    inicio=inicio,
                    fin=fin,
                    cocinero=cocinero,
                    nota="Cierre colocado al final de la jornada.",
                )
            )


def _imprimir_bloque(bloque: BloquePlanificado) -> None:
    recurso = f" | Recurso: {bloque.fase.recurso}" if bloque.fase.recurso else ""
    print(f"{_hora(bloque.inicio)} - {_hora(bloque.fin)}{recurso}")
    print(f"  {bloque.fase.nombre}")
    if bloque.fase.elaboracion:
        print(f"  Elaboración: {bloque.fase.elaboracion}")
    print(f"  Motivo: {bloque.fase.motivo}")
    if bloque.nota:
        print(f"  Nota: {bloque.nota}")


def imprimir_planificacion_personal_completa(numero_cocineros: int = 3, horas_jornada: int = 8) -> None:
    planificador = PlanificadorPersonal(numero_cocineros=numero_cocineros, horas_jornada=horas_jornada)
    bloques = planificador.planificar()

    print("\n" + "=" * 88)
    print("PLANIFICACIÓN COMPLETA POR TRABAJADORES - SPRINT 5.6.6")
    print("=" * 88)
    print(f"Equipo: {numero_cocineros} cocineros | Jornada: {horas_jornada} horas")
    print("Regla nueva: quien empieza una elaboración intenta acabarla.")
    print("Regla: los tiempos pasivos se ven aparte y NO bloquean al trabajador.")

    for cocinero in range(1, numero_cocineros + 1):
        print("\n" + "-" * 88)
        print(f"COCINERO {cocinero}")
        print("-" * 88)

        bloques_cocinero = [b for b in bloques if b.cocinero == cocinero]
        if not bloques_cocinero:
            print("Sin tareas asignadas.")
            continue

        dia_actual = None
        minutos_activos = 0

        for bloque in sorted(bloques_cocinero, key=lambda b: (b.dia, b.inicio)):
            if bloque.dia != dia_actual:
                if dia_actual is not None:
                    print(f"  Total activo Día {dia_actual}: {minutos_activos // 60}h {minutos_activos % 60}min")
                    minutos_activos = 0
                dia_actual = bloque.dia
                print(f"\nDÍA {dia_actual}")

            minutos_activos += bloque.fin - bloque.inicio
            _imprimir_bloque(bloque)

        if dia_actual is not None:
            print(f"  Total activo Día {dia_actual}: {minutos_activos // 60}h {minutos_activos % 60}min")

    pasivos = [b for b in bloques if b.cocinero is None]
    if pasivos:
        print("\n" + "-" * 88)
        print("COCCIONES / ENFRIADOS / TIEMPOS PASIVOS EN MARCHA")
        print("-" * 88)

        dia_actual = None
        for bloque in sorted(pasivos, key=lambda b: (b.dia, b.inicio)):
            if bloque.dia != dia_actual:
                dia_actual = bloque.dia
                print(f"\nDÍA {dia_actual}")
            _imprimir_bloque(bloque)

    print("\n" + "=" * 88)
    print("LECTURA DE JEFE DE COCINA")
    print("=" * 88)
    print("- Cada cocinero aparece con su jornada completa.")
    print("- El motor intenta que quien empieza Fondo, Carrilleras o Croquetas las siga hasta el final.")
    print("- Las tareas flexibles sirven para rellenar carga en cocineros que se quedan cortos.")
    print("- Si un fondo cuece 3 horas, el cocinero NO queda bloqueado esas 3 horas.")
    print("- Si una tarea no cabe en 8 horas, pasa automáticamente al día siguiente.")


if __name__ == "__main__":
    imprimir_planificacion_personal_completa()
