# -*- coding: utf-8 -*-
"""
MODULOS/fichas.py
Sprint 5.9 corregido estable.

Menú de fichas técnicas.
"""

from __future__ import annotations

import copy

from fichas_tecnicas import (
    buscar_fichas_por_texto,
    cargar_ficha,
    completar_ficha_con_preguntas,
    crear_ficha_carrillera_demo,
    crear_ficha_desde_receta_basica,
    dict_a_ficha,
    elegir_ficha_por_nombre_o_codigo,
    estado_ficha,
    guardar_dict_ficha,
    guardar_ficha,
    listar_fichas,
    preguntas_para_completar,
    resumen_para_cocinero,
)
from interprete_fichas import aplicar_cambio_a_dict, interpretar_cambio
from versionado_fichas import guardar_version, leer_historial, registrar_cambio


def _pausa() -> None:
    input("\nPulsa ENTER para continuar...")


def _pedir_ficha_por_nombre() -> dict | None:
    texto = input("\nNombre del plato/elaboración o código interno: ").strip()

    if not texto:
        print("\nNo has escrito ningún nombre.")
        return None

    ficha = elegir_ficha_por_nombre_o_codigo(texto)

    if not ficha:
        print("\nNo he encontrado ninguna ficha con ese nombre o código.")
        return None

    return ficha


def _crear_demo_carrillera() -> None:
    ficha = crear_ficha_carrillera_demo()
    path = guardar_ficha(ficha)

    print("\nFicha demo creada correctamente.")
    print(f"Archivo: {path}")
    print("Puedes buscarla escribiendo: carrillera")


def _listar_fichas() -> None:
    fichas = listar_fichas()

    if not fichas:
        print("\nNo hay fichas guardadas todavía.")
        return

    print("\nFICHAS TÉCNICAS GUARDADAS")
    print("=" * 70)

    for f in fichas:
        try:
            data = cargar_ficha(f.stem)
            if not data:
                print(f"- {f.stem}")
                continue

            nombre = data.get("nombre", f.stem)
            estado = estado_ficha(data)
            print(f"- {nombre} | Código interno: {f.stem} | {estado}")

        except Exception:
            print(f"- {f.stem}")


def _ver_ficha() -> None:
    ficha = _pedir_ficha_por_nombre()

    if not ficha:
        return

    print(resumen_para_cocinero(ficha))


def _crear_borrador_desde_texto() -> None:
    print("\nPega una receta básica.")
    print("Cuando termines, escribe una línea solo con FIN.")

    lineas = []

    while True:
        linea = input()
        if linea.strip().upper() == "FIN":
            break
        lineas.append(linea)

    texto = "\n".join(lineas)
    ficha = crear_ficha_desde_receta_basica(texto)

    print("\nBORRADOR GENERADO")
    print("=" * 70)
    print(f"Nombre detectado: {ficha.nombre}")
    print(f"Código interno propuesto: {ficha.codigo}")
    print(f"Ingredientes detectados: {len(ficha.ingredientes)}")
    print(f"Fases detectadas: {len(ficha.fases)}")

    preguntas = preguntas_para_completar(ficha)

    if preguntas:
        print("\nHost AI necesita completar estos campos:")
        for i, (_, pregunta) in enumerate(preguntas, start=1):
            print(f"{i}. {pregunta}")

    responder = input("\n¿Quieres responder ahora las preguntas y completar la ficha? (s/n): ").strip().lower()

    if responder == "s":
        ficha = completar_ficha_con_preguntas(ficha)

    path = guardar_ficha(ficha)
    print(f"\nFicha guardada en: {path}")


def _completar_ficha_existente() -> None:
    ficha_dict = _pedir_ficha_por_nombre()

    if not ficha_dict:
        return

    ficha = dict_a_ficha(ficha_dict)
    ficha = completar_ficha_con_preguntas(ficha)
    path = guardar_ficha(ficha)

    print(f"\nFicha actualizada en: {path}")


def _editar_ficha_inteligente() -> None:
    ficha = _pedir_ficha_por_nombre()

    if not ficha:
        return

    print("\nFicha seleccionada:")
    print(f"{ficha.get('nombre')} | Código interno: {ficha.get('codigo')}")

    print("\nEscribe el cambio en lenguaje natural.")
    print("Ejemplos:")
    print("- La vida útil son 5 días")
    print("- Añade Thermomix")
    print("- Esta receta sale para 32 raciones")
    print("- La regeneración es a 68 grados")
    print("- Añade el alérgeno leche")

    texto = input("\n¿Qué quieres cambiar? ").strip()

    if not texto:
        print("\nNo has escrito ningún cambio.")
        return

    campo, valor, descripcion = interpretar_cambio(texto)

    print(f"\nInterpretación: {descripcion}")

    if campo == "desconocido":
        print("No aplico cambios porque no he entendido el campo.")
        return

    confirmar = input("¿Aplicar cambio? (s/n): ").strip().lower()

    if confirmar != "s":
        print("Cambio cancelado.")
        return

    codigo = ficha.get("codigo")
    campo_real = campo.replace("_add", "")
    anterior = copy.deepcopy(ficha.get(campo_real))

    guardar_version(ficha, motivo="antes de edición inteligente")

    ficha = aplicar_cambio_a_dict(ficha, campo, valor)
    guardar_dict_ficha(ficha)

    registrar_cambio(
        codigo=codigo,
        campo=campo,
        anterior=anterior,
        nuevo=valor,
        motivo="edición inteligente desde consola",
    )

    print("\nCambio guardado correctamente.")


def _duplicar_ficha() -> None:
    ficha = _pedir_ficha_por_nombre()

    if not ficha:
        return

    nuevo_nombre = input("\nNuevo nombre de la ficha duplicada: ").strip()
    nuevo_codigo = input("Nuevo código interno: ").strip()

    if not nuevo_nombre or not nuevo_codigo:
        print("Nombre y código son obligatorios.")
        return

    nueva = copy.deepcopy(ficha)
    nueva["nombre"] = nuevo_nombre
    nueva["codigo"] = nuevo_codigo
    nueva["estado"] = "borrador"

    guardar_dict_ficha(nueva)

    registrar_cambio(
        nuevo_codigo,
        "duplicada_desde",
        ficha.get("codigo"),
        nuevo_codigo,
        "duplicar ficha",
    )

    print("\nFicha duplicada correctamente.")


def _validar_ficha() -> None:
    ficha = _pedir_ficha_por_nombre()

    if not ficha:
        return

    pendientes = ficha.get("preguntas_pendientes", [])

    if pendientes:
        print("\nLa ficha todavía tiene campos pendientes:")
        for p in pendientes:
            print(f"- {p}")

        confirmar = input("\n¿Validarla igualmente? (s/n): ").strip().lower()

        if confirmar != "s":
            print("Validación cancelada.")
            return

    anterior = ficha.get("estado")

    guardar_version(ficha, motivo="antes de validar")

    ficha["estado"] = "validada"
    guardar_dict_ficha(ficha)

    registrar_cambio(
        ficha.get("codigo"),
        "estado",
        anterior,
        "validada",
        "validación manual",
    )

    print("\nFicha validada.")


def _historial_ficha() -> None:
    ficha = _pedir_ficha_por_nombre()

    if not ficha:
        return

    historial = leer_historial(ficha.get("codigo"))

    if not historial:
        print("\nNo hay historial para esta ficha.")
        return

    print("\nHISTORIAL")
    print("=" * 70)

    for h in historial:
        print(f"{h.get('fecha')} | {h.get('campo')}")
        print(f"  Antes: {h.get('anterior')}")
        print(f"  Nuevo: {h.get('nuevo')}")

        if h.get("motivo"):
            print(f"  Motivo: {h.get('motivo')}")


def _buscar_fichas() -> None:
    texto = input("\nBuscar por nombre, código, ingrediente, maquinaria o familia: ").strip()

    if not texto:
        print("\nNo has escrito nada para buscar.")
        return

    resultados = buscar_fichas_por_texto(texto)
    q = texto.lower()

    for f in listar_fichas():
        data = cargar_ficha(f.stem)

        if not data or data in resultados:
            continue

        campos = [
            data.get("familia", ""),
            " ".join(data.get("maquinaria_imprescindible", [])),
            " ".join(data.get("alergenos", [])),
            " ".join(i.get("nombre", "") for i in data.get("ingredientes", [])),
        ]

        if q in " ".join(campos).lower():
            resultados.append(data)

    if not resultados:
        print("\nNo he encontrado fichas.")
        return

    print("\nRESULTADOS")
    print("=" * 70)

    for r in resultados:
        print(
            f"- {r.get('nombre')} | "
            f"Código interno: {r.get('codigo')} | "
            f"Familia: {r.get('familia', '')}"
        )


def _explicar_ficha_host_ai() -> None:
    print("\nFICHA TÉCNICA HOST AI v1.0")
    print("=" * 70)
    print("La ficha técnica es la fuente de verdad para producción, compras, stock, costes y planificación.")
    print("\nSprint 5.9 añade:")
    print("- edición inteligente")
    print("- búsqueda por nombre")
    print("- duplicado")
    print("- validación")
    print("- historial")


def menu_fichas_tecnicas(restaurante_id: int = 1) -> None:
    while True:
        print("\n" + "=" * 60)
        print("17. FICHAS TÉCNICAS HOST AI")
        print("=" * 60)
        print("1. Crear ficha demo completa: Carrillera melosa")
        print("2. Listar fichas guardadas")
        print("3. Ver ficha como cocinero")
        print("4. Crear borrador desde receta pegada y completar preguntas")
        print("5. Explicar estructura Ficha Técnica Host AI v1.0")
        print("6. Completar ficha existente")
        print("7. Editar ficha inteligente")
        print("8. Duplicar ficha")
        print("9. Validar ficha")
        print("10. Ver historial de cambios")
        print("11. Buscar fichas")
        print("0. Volver")

        opcion = input("\nElige una opción: ").strip()

        if opcion == "1":
            _crear_demo_carrillera()
            _pausa()

        elif opcion == "2":
            _listar_fichas()
            _pausa()

        elif opcion == "3":
            _ver_ficha()
            _pausa()

        elif opcion == "4":
            _crear_borrador_desde_texto()
            _pausa()

        elif opcion == "5":
            _explicar_ficha_host_ai()
            _pausa()

        elif opcion == "6":
            _completar_ficha_existente()
            _pausa()

        elif opcion == "7":
            _editar_ficha_inteligente()
            _pausa()

        elif opcion == "8":
            _duplicar_ficha()
            _pausa()

        elif opcion == "9":
            _validar_ficha()
            _pausa()

        elif opcion == "10":
            _historial_ficha()
            _pausa()

        elif opcion == "11":
            _buscar_fichas()
            _pausa()

        elif opcion == "0":
            break

        else:
            print("Opción no válida.")


if __name__ == "__main__":
    menu_fichas_tecnicas()
