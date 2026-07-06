from __future__ import annotations

from prioridades import generar_prioridades, obtener_siguiente_accion, resumen_prioridades
from dependencias import resumen_dependencias
from motor_produccion import resumen_plan_produccion


def mostrar_siguiente_accion(restaurante_id: int = 1):
    accion = obtener_siguiente_accion(restaurante_id)

    print("\n========== SIGUIENTE ACCIÓN RECOMENDADA ==========")

    if accion is None:
        print("\nNo hay tareas pendientes de producción.\n")
        input("Pulsa ENTER para volver...")
        return

    print(f"\n👉 {accion.nombre}")
    print(f"Evento    : {accion.evento or 'Sin evento'}")
    print(f"Fecha     : {accion.fecha_evento or 'Sin fecha'}")
    if accion.cantidad is not None:
        print(f"Cantidad  : {accion.cantidad} {accion.unidad or ''}")
    print(f"Prioridad : {accion.nivel} ({accion.prioridad}/100)")
    print(f"\nAcción recomendada:\n{accion.accion_recomendada}")
    print("\nMotivos:")
    for motivo in accion.motivos:
        print(f"- {motivo}")

    print("\nHost AI:")
    print("Esta recomendación combina urgencia, tipo de elaboración, cantidad y fecha del evento.")
    print("En los próximos sprints se añadirá maquinaria, producción disponible y fases reales.\n")
    input("Pulsa ENTER para volver...")


def mostrar_prioridades(restaurante_id: int = 1):
    print()
    print(resumen_prioridades(restaurante_id, limite=20))
    print("\nHost AI:")
    print("Orden basado en urgencia, tiempo, reposo, cantidad y tipo de elaboración.\n")
    input("Pulsa ENTER para volver...")


def mostrar_dependencias(restaurante_id: int = 1):
    print()
    print(resumen_dependencias(restaurante_id))
    print("\nHost AI:")
    print("Esto todavía es una detección aproximada. Cuando conectemos platos con elaboraciones será exacta.\n")
    input("Pulsa ENTER para volver...")


def mostrar_plan_inteligente(restaurante_id: int = 1):
    print()
    print(resumen_plan_produccion(restaurante_id))
    print("\nHost AI:")
    print("Este es el primer plan que mezcla prioridades y dependencias. Revísalo como jefe de cocina.\n")
    input("Pulsa ENTER para volver...")


def menu_produccion_inteligente(restaurante_id: int = 1):
    while True:
        print("\n========== PRODUCCIÓN INTELIGENTE ==========")
        print("1. Ver siguiente acción recomendada")
        print("2. Ver prioridades de producción")
        print("3. Ver dependencias / producciones agrupables")
        print("4. Generar plan de producción inteligente")
        print("0. Volver")

        opcion = input("\n¿Qué quieres hacer? ").strip()

        if opcion == "1":
            mostrar_siguiente_accion(restaurante_id)
        elif opcion == "2":
            mostrar_prioridades(restaurante_id)
        elif opcion == "3":
            mostrar_dependencias(restaurante_id)
        elif opcion == "4":
            mostrar_plan_inteligente(restaurante_id)
        elif opcion == "0":
            break
        else:
            print("\n⚠️ Opción no válida.")
