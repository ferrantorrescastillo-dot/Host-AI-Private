# -*- coding: utf-8 -*-
"""
Módulo de consola - Producción Inteligente
Sprint 5.4: planificación por restricciones reales.
"""

from __future__ import annotations


def _pausa() -> None:
    input("\nPulsa ENTER para continuar...")


def _siguiente_accion() -> None:
    try:
        from SERVICIOS.planificador_restricciones import PlanificadorRestricciones
        plan = PlanificadorRestricciones()
        tarea = plan.ordenar_tareas(plan.crear_tareas_demo())[0]
        print("\nSIGUIENTE ACCIÓN RECOMENDADA")
        print("=" * 60)
        print(tarea.nombre)
        print(f"Motivo: {plan.explicar_orden(tarea)}")
    except Exception as e:
        print(f"\nNo se pudo calcular la siguiente acción: {e}")


def _ver_prioridades() -> None:
    try:
        from SERVICIOS.planificador_restricciones import PlanificadorRestricciones
        plan = PlanificadorRestricciones()
        print("\nPRIORIDADES DE PRODUCCIÓN")
        print("=" * 60)
        for i, tarea in enumerate(plan.ordenar_tareas(plan.crear_tareas_demo()), start=1):
            print(f"{i}. {tarea.nombre} | puntos: {plan.puntuacion(tarea)}")
            print(f"   {plan.explicar_orden(tarea)}")
    except Exception as e:
        print(f"\nNo se pudieron ver prioridades: {e}")


def _ver_dependencias() -> None:
    try:
        from SERVICIOS.planificador_restricciones import PlanificadorRestricciones
        plan = PlanificadorRestricciones()
        print("\nDEPENDENCIAS / PRODUCCIONES AGRUPABLES")
        print("=" * 60)
        for tarea in plan.crear_tareas_demo():
            deps = ", ".join(tarea.dependencias) if tarea.dependencias else "Sin dependencias"
            desbloquea = ", ".join(tarea.desbloquea) if tarea.desbloquea else "No desbloquea otras"
            print(f"\n- {tarea.nombre}")
            print(f"  Depende de: {deps}")
            print(f"  Desbloquea: {desbloquea}")
    except Exception as e:
        print(f"\nNo se pudieron ver dependencias: {e}")


def _plan_inteligente() -> None:
    _ver_prioridades()


def _horario_basico() -> None:
    try:
        from SERVICIOS.planificador_produccion import imprimir_horario_basico
        imprimir_horario_basico()
    except Exception as e:
        print(f"\nNo se pudo generar el horario básico: {e}")


def _horario_restricciones() -> None:
    try:
        from SERVICIOS.planificador_restricciones import imprimir_horario_restricciones
        imprimir_horario_restricciones()
    except Exception as e:
        print(f"\nNo se pudo generar el horario por restricciones: {e}")


def menu_produccion_inteligente() -> None:
    while True:
        print("\n" + "=" * 60)
        print("16. PRODUCCIÓN INTELIGENTE")
        print("=" * 60)
        print("1. Ver siguiente acción recomendada")
        print("2. Ver prioridades de producción")
        print("3. Ver dependencias / producciones agrupables")
        print("4. Generar plan de producción inteligente")
        print("5. Generar horario de producción inteligente")
        print("6. Generar horario por restricciones reales (Sprint 5.4)")
        print("0. Volver")

        opcion = input("\nElige una opción: ").strip()

        if opcion == "1":
            _siguiente_accion()
            _pausa()
        elif opcion == "2":
            _ver_prioridades()
            _pausa()
        elif opcion == "3":
            _ver_dependencias()
            _pausa()
        elif opcion == "4":
            _plan_inteligente()
            _pausa()
        elif opcion == "5":
            _horario_basico()
            _pausa()
        elif opcion == "6":
            _horario_restricciones()
            _pausa()
        elif opcion == "0":
            break
        else:
            print("Opción no válida.")


# Alias por compatibilidad con nombres posibles usados en Main.py
mostrar_menu = menu_produccion_inteligente
menu = menu_produccion_inteligente


if __name__ == "__main__":
    menu_produccion_inteligente()
