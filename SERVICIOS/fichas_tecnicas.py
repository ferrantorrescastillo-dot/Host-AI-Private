# -*- coding: utf-8 -*-
"""
SERVICIOS/fichas_tecnicas.py
Sprint 5.9 corregido estable.

Servicio de fichas técnicas:
- crear demo de carrillera
- crear ficha desde receta pegada
- completar preguntas
- guardar/cargar/listar
- buscar por nombre o código
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from ficha_tecnica import FaseFicha, FichaTecnicaHostAI, IngredienteFicha


BASE_DIR = Path(__file__).resolve().parents[1]
DATOS_DIR = BASE_DIR / "DATOS"
FICHAS_DIR = DATOS_DIR / "fichas_tecnicas"
FICHAS_DIR.mkdir(parents=True, exist_ok=True)


CAMPOS_OBLIGATORIOS = [
    ("codigo", "Código interno"),
    ("nombre", "Nombre de la elaboración/plato"),
    ("familia", "Familia"),
    ("objetivo", "Objetivo de la elaboración"),
    ("rendimiento_final", "Rendimiento final"),
    ("raciones", "Número de raciones"),
    ("peso_racion", "Peso por ración"),
    ("conservacion", "Conservación"),
    ("vida_util", "Vida útil"),
    ("regeneracion", "Regeneración"),
    ("puntos_criticos_haccp", "Puntos críticos HACCP"),
    ("controles_calidad", "Controles de calidad"),
]


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


def _lista_desde_texto(texto: str) -> List[str]:
    if not texto:
        return []
    return [x.strip() for x in texto.replace(";", ",").split(",") if x.strip()]


def _pedir_texto(pregunta: str) -> str:
    print()
    print(pregunta)
    print("ENTER = dejar pendiente")
    return input("> ").strip()


def _pedir_entero(pregunta: str) -> Optional[int]:
    valor = _pedir_texto(pregunta)
    if not valor:
        return None
    try:
        return int(valor)
    except ValueError:
        print("No parece un número entero. Se deja pendiente.")
        return None


def detectar_campos_faltantes(ficha: FichaTecnicaHostAI) -> List[str]:
    faltan: List[str] = []

    for campo, nombre_legible in CAMPOS_OBLIGATORIOS:
        valor = getattr(ficha, campo, None)
        if valor is None or valor == "" or valor == []:
            faltan.append(nombre_legible)

    if not ficha.ingredientes:
        faltan.append("Ingredientes")

    if not ficha.fases:
        faltan.append("Proceso por fases")

    ficha.recalcular_tiempos()

    if ficha.tiempo_activo_min == 0:
        faltan.append("Tiempo activo")

    if ficha.tiempo_total_min == 0:
        faltan.append("Tiempo total")

    if not ficha.maquinaria_imprescindible:
        faltan.append("Maquinaria imprescindible")

    if not ficha.alergenos:
        faltan.append("Alérgenos")

    return faltan


def crear_ficha_carrillera_demo() -> FichaTecnicaHostAI:
    ficha = FichaTecnicaHostAI(
        codigo="ELAB-CAR-001",
        nombre="Carrillera melosa prensada con demi-glace",
        tipo="elaboracion",
        familia="Carnes / Braseados",
        estado="validada_demo",
        objetivo="Obtener una carrillera melosa, limpia, prensada y porcionable, lista para regenerar en servicio con salsa demi-glace.",
        descripcion_corta="Carrillera braseada lentamente, deshuesada, prensada, abatida y racionada.",
        rendimiento_final="65-70% sobre peso limpio inicial",
        raciones=20,
        peso_racion="120-140 g",
        maquinaria_imprescindible=["horno", "abatidor", "cámara", "fuego"],
        maquinaria_opcional=["roner", "envasadora al vacío"],
        utensilios=["GN alta", "colador fino", "peso", "film", "molde/prensa"],
        producciones_previas=["Demi-glace o fondo oscuro"],
        elaboraciones_que_desbloquea=[
            "Taco de carrillera",
            "Lingote de carrillera",
            "Canelón de carrillera",
            "Croqueta de carrillera",
        ],
        conservacion="En cámara a 0-3 ºC, envasada y etiquetada.",
        vida_util="3-5 días en cámara si está abatida y manipulada correctamente.",
        congelacion="Sí. Congelar porciones envasadas al vacío o en bolsas de 10 raciones.",
        regeneracion="Regenerar suave con salsa a 65-70 ºC hasta centro caliente, sin hervir fuerte.",
        alergenos=["sulfitos si se usa vino", "apio si lleva bresa con apio"],
        notas_jefe_cocina="Debe hacerse mínimo el día anterior si se quiere prensar bien.",
    )

    ficha.ingredientes = [
        IngredienteFicha("Carrillera limpia", 4.0, "kg", es_critico=True),
        IngredienteFicha("Cebolla", 1.2, "kg"),
        IngredienteFicha("Zanahoria", 0.8, "kg"),
        IngredienteFicha("Puerro", 0.4, "kg"),
        IngredienteFicha("Ajo", 0.08, "kg"),
        IngredienteFicha("Vino tinto", 0.75, "L", alergenos=["sulfitos"]),
        IngredienteFicha("Fondo oscuro / demi-glace", 2.0, "L", es_critico=True),
        IngredienteFicha("Laurel", 2, "hojas"),
        IngredienteFicha("Romero", 1, "rama"),
        IngredienteFicha("Sal", 40, "g"),
        IngredienteFicha("Pimienta negra", 8, "g"),
    ]

    ficha.fases = [
        FaseFicha(
            "Revisar y limpiar carrilleras",
            1,
            "Retirar grasa dura, nervios e impurezas. Pesar limpio.",
            tiempo_activo_min=40,
            utensilios=["cuchillo", "tabla", "peso"],
            control_calidad="Piezas limpias.",
            tipo="activa",
        ),
        FaseFicha(
            "Cortar bresa",
            2,
            "Cortar cebolla, zanahoria, puerro y ajo.",
            tiempo_activo_min=25,
            utensilios=["cuchillo", "tabla", "GN"],
            tipo="activa",
        ),
        FaseFicha(
            "Marcar carrilleras",
            3,
            "Marcar bien por todas las caras.",
            tiempo_activo_min=35,
            maquinaria=["fuego"],
            punto_critico="No cocer la carne en su propio jugo.",
            control_calidad="Color tostado uniforme.",
            tipo="activa",
        ),
        FaseFicha(
            "Sofreír bresa y desglasar",
            4,
            "Sofreír bresa, desglasar con vino y reducir alcohol.",
            tiempo_activo_min=30,
            maquinaria=["fuego"],
            punto_critico="Reducir bien el vino.",
            tipo="activa",
        ),
        FaseFicha(
            "Brasear carrilleras",
            5,
            "Cubrir con fondo/demi-glace y brasear tapado hasta textura melosa.",
            tiempo_activo_min=10,
            tiempo_pasivo_min=180,
            maquinaria=["horno"],
            depende_de=["Marcar carrilleras", "Sofreír bresa y desglasar"],
            punto_critico="Cocción suave.",
            control_calidad="La carne cede al pinchar.",
            tipo="mixta",
        ),
        FaseFicha(
            "Deshuesar y limpiar",
            6,
            "Separar carne, retirar impurezas y reservar jugos.",
            tiempo_activo_min=45,
            depende_de=["Brasear carrilleras"],
            punto_critico="Trabajar templado.",
            tipo="activa",
        ),
        FaseFicha(
            "Colar y reducir salsa",
            7,
            "Colar la salsa y reducir hasta textura napante.",
            tiempo_activo_min=15,
            tiempo_pasivo_min=45,
            maquinaria=["fuego"],
            depende_de=["Brasear carrilleras"],
            control_calidad="Salsa brillante y sin grasa excesiva.",
            tipo="mixta",
        ),
        FaseFicha(
            "Prensar",
            8,
            "Colocar carrillera en molde y prensar con peso.",
            tiempo_activo_min=25,
            tiempo_pasivo_min=720,
            depende_de=["Deshuesar y limpiar"],
            punto_critico="Prensar mínimo una noche.",
            tipo="mixta",
        ),
        FaseFicha(
            "Abatir",
            9,
            "Abatir rápidamente antes de cámara.",
            tiempo_activo_min=10,
            tiempo_pasivo_min=60,
            maquinaria=["abatidor"],
            depende_de=["Prensar"],
            punto_critico="No meter caliente directo en cámara.",
            tipo="mixta",
        ),
        FaseFicha(
            "Porcionar, envasar, etiquetar y registrar",
            10,
            "Cortar raciones, pesar, envasar y registrar.",
            tiempo_activo_min=45,
            depende_de=["Abatir"],
            control_calidad="Ración limpia y peso correcto.",
            tipo="cierre",
        ),
    ]

    ficha.puntos_criticos_haccp = [
        "Abatir antes de guardar en cámara.",
        "No dejar enfriar a temperatura ambiente durante horas.",
        "Etiquetar con fecha, lote, peso y responsable.",
        "Regenerar sin hervir agresivamente.",
    ]

    ficha.controles_calidad = [
        "Textura melosa.",
        "Sabor profundo y equilibrado.",
        "Salsa sin grasa excesiva.",
        "Corte limpio tras prensado.",
        "Peso de ración correcto.",
    ]

    ficha.errores_frecuentes = [
        "No marcar bien la carne.",
        "No reducir el vino.",
        "Brasear demasiado fuerte.",
        "No prensar suficiente tiempo.",
        "Guardar sin abatir ni etiquetar.",
    ]

    ficha.recalcular_tiempos()
    ficha.preguntas_pendientes = detectar_campos_faltantes(ficha)
    return ficha


def guardar_ficha(ficha: FichaTecnicaHostAI) -> Path:
    ficha.recalcular_tiempos()
    ficha.preguntas_pendientes = detectar_campos_faltantes(ficha)

    if ficha.preguntas_pendientes and ficha.estado.startswith("borrador"):
        ficha.estado = "borrador_incompleto"
    elif not ficha.preguntas_pendientes and ficha.estado.startswith("borrador"):
        ficha.estado = "borrador_completo"

    path = FICHAS_DIR / f"{ficha.codigo}.json"
    path.write_text(json.dumps(ficha.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def guardar_dict_ficha(ficha: Dict) -> Path:
    codigo = ficha.get("codigo") or "BORRADOR-001"
    path = FICHAS_DIR / f"{codigo}.json"
    path.write_text(json.dumps(ficha, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def listar_fichas() -> List[Path]:
    return sorted(FICHAS_DIR.glob("*.json"))


def cargar_ficha(codigo: str) -> Optional[Dict]:
    path = FICHAS_DIR / f"{codigo}.json"
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def buscar_fichas_por_texto(texto: str) -> List[Dict]:
    q = _normalizar(texto)
    resultados: List[Dict] = []

    for path in listar_fichas():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue

        codigo = _normalizar(data.get("codigo", path.stem))
        nombre = _normalizar(data.get("nombre", ""))

        if q == codigo or q in codigo or q in nombre:
            resultados.append(data)

    return resultados


def elegir_ficha_por_nombre_o_codigo(texto: str) -> Optional[Dict]:
    resultados = buscar_fichas_por_texto(texto)

    if not resultados:
        return None

    if len(resultados) == 1:
        return resultados[0]

    print()
    print("He encontrado varias fichas parecidas:")
    for i, ficha in enumerate(resultados, start=1):
        print(f"{i}. {ficha.get('nombre')} | Código: {ficha.get('codigo')} | Estado: {ficha.get('estado', '')}")

    seleccion = input("Elige número: ").strip()

    try:
        idx = int(seleccion)
        if 1 <= idx <= len(resultados):
            return resultados[idx - 1]
    except ValueError:
        pass

    print("Selección no válida.")
    return None


def dict_a_ficha(data: Dict) -> FichaTecnicaHostAI:
    ficha = FichaTecnicaHostAI(
        codigo=data.get("codigo", "BORRADOR-001"),
        nombre=data.get("nombre", "Ficha sin nombre"),
        tipo=data.get("tipo", "elaboracion"),
        familia=data.get("familia", ""),
        version=data.get("version", "1.0"),
        estado=data.get("estado", "borrador"),
        objetivo=data.get("objetivo", ""),
        descripcion_corta=data.get("descripcion_corta", ""),
        rendimiento_final=data.get("rendimiento_final", ""),
        raciones=data.get("raciones"),
        peso_racion=data.get("peso_racion", ""),
        tiempo_total_min=data.get("tiempo_total_min", 0),
        tiempo_activo_min=data.get("tiempo_activo_min", 0),
        tiempo_pasivo_min=data.get("tiempo_pasivo_min", 0),
        maquinaria_imprescindible=data.get("maquinaria_imprescindible", []),
        maquinaria_opcional=data.get("maquinaria_opcional", []),
        utensilios=data.get("utensilios", []),
        producciones_previas=data.get("producciones_previas", []),
        elaboraciones_que_desbloquea=data.get("elaboraciones_que_desbloquea", []),
        puntos_criticos_haccp=data.get("puntos_criticos_haccp", []),
        controles_calidad=data.get("controles_calidad", []),
        errores_frecuentes=data.get("errores_frecuentes", []),
        conservacion=data.get("conservacion", ""),
        vida_util=data.get("vida_util", ""),
        congelacion=data.get("congelacion", ""),
        regeneracion=data.get("regeneracion", ""),
        alergenos=data.get("alergenos", []),
        coste_materia_prima=data.get("coste_materia_prima"),
        coste_mano_obra=data.get("coste_mano_obra"),
        coste_total_estimado=data.get("coste_total_estimado"),
        coste_por_racion=data.get("coste_por_racion"),
        notas_jefe_cocina=data.get("notas_jefe_cocina", ""),
        preguntas_pendientes=data.get("preguntas_pendientes", []),
    )

    ficha.ingredientes = []
    for i in data.get("ingredientes", []):
        ficha.ingredientes.append(
            IngredienteFicha(
                nombre=i.get("nombre", ""),
                cantidad=i.get("cantidad", 0),
                unidad=i.get("unidad", ""),
                merma_porcentaje=i.get("merma_porcentaje"),
                cantidad_neta=i.get("cantidad_neta"),
                proveedor_preferente=i.get("proveedor_preferente", ""),
                coste_unitario=i.get("coste_unitario"),
                alergenos=i.get("alergenos", []),
                es_critico=i.get("es_critico", False),
            )
        )

    ficha.fases = []
    for f in data.get("fases", []):
        ficha.fases.append(
            FaseFicha(
                nombre=f.get("nombre", ""),
                orden=f.get("orden", 0),
                descripcion=f.get("descripcion", ""),
                tiempo_activo_min=f.get("tiempo_activo_min", 0),
                tiempo_pasivo_min=f.get("tiempo_pasivo_min", 0),
                temperatura=f.get("temperatura", ""),
                maquinaria=f.get("maquinaria", []),
                utensilios=f.get("utensilios", []),
                depende_de=f.get("depende_de", []),
                desbloquea=f.get("desbloquea", []),
                punto_critico=f.get("punto_critico", ""),
                control_calidad=f.get("control_calidad", ""),
                tipo=f.get("tipo", "activa"),
            )
        )

    return ficha


def crear_ficha_desde_receta_basica(texto: str) -> FichaTecnicaHostAI:
    lineas = [l.strip() for l in texto.splitlines() if l.strip()]
    nombre = lineas[0] if lineas else "Ficha sin nombre"
    codigo_base = _normalizar(nombre).upper().replace(" ", "-").replace("/", "-")[:25]
    codigo = f"BORRADOR-{codigo_base}" if codigo_base else "BORRADOR-001"

    ficha = FichaTecnicaHostAI(
        codigo=codigo,
        nombre=nombre,
        estado="borrador",
        objetivo="",
        notas_jefe_cocina="Ficha generada desde texto. Requiere revisión.",
    )

    ingredientes = []
    fases = []
    orden = 1

    verbos = (
        "cortar",
        "cocer",
        "marcar",
        "abatir",
        "mezclar",
        "triturar",
        "colar",
        "reservar",
        "freír",
        "freir",
        "confitar",
        "envasar",
        "reducir",
        "hornear",
        "limpiar",
        "picar",
        "pelar",
        "laminar",
        "texturizar",
        "reposar",
        "introducir",
        "sacar",
        "poner",
        "añadir",
        "enrollar",
    )

    for linea in lineas[1:]:
        limpia = linea.strip()
        partes = limpia.replace(",", ".").split()

        if len(partes) >= 3:
            try:
                cantidad = float(partes[0])
                unidad = partes[1]
                nombre_ing = " ".join(partes[2:])
                ingredientes.append(IngredienteFicha(nombre_ing, cantidad, unidad))
                continue
            except ValueError:
                pass

        linea_sin_num = limpia
        if "." in limpia[:3]:
            linea_sin_num = limpia.split(".", 1)[1].strip()
        elif ")" in limpia[:3]:
            linea_sin_num = limpia.split(")", 1)[1].strip()

        if linea_sin_num.lower().startswith(verbos) or limpia[:1].isdigit():
            fases.append(
                FaseFicha(
                    nombre=f"Paso {orden}",
                    orden=orden,
                    descripcion=linea_sin_num,
                    tiempo_activo_min=0,
                    tipo="activa",
                )
            )
            orden += 1

    ficha.ingredientes = ingredientes
    ficha.fases = fases
    ficha.recalcular_tiempos()
    ficha.preguntas_pendientes = detectar_campos_faltantes(ficha)
    return ficha


def preguntas_para_completar(ficha: FichaTecnicaHostAI) -> List[Tuple[str, str]]:
    faltan = detectar_campos_faltantes(ficha)

    mapa = {
        "Código interno": ("codigo", "Código interno para guardar la ficha. Ejemplo: ELAB-CAR-001"),
        "Familia": ("familia", "¿A qué familia pertenece? Ejemplo: carnes, salsas, guarniciones, postres."),
        "Objetivo de la elaboración": ("objetivo", "¿Cuál es el objetivo final de esta elaboración?"),
        "Rendimiento final": ("rendimiento_final", "¿Qué rendimiento final esperas? Ejemplo: 2,8 kg finales o 20 raciones."),
        "Número de raciones": ("raciones", "¿Cuántas raciones salen?"),
        "Peso por ración": ("peso_racion", "¿Qué peso debe tener cada ración?"),
        "Conservación": ("conservacion", "¿Cómo se conserva? Cámara, congelador, vacío, seco..."),
        "Vida útil": ("vida_util", "¿Cuántos días dura en cámara o congelador?"),
        "Regeneración": ("regeneracion", "¿Cómo se regenera antes del servicio?"),
        "Puntos críticos HACCP": ("puntos_criticos_haccp", "¿Qué puntos críticos HACCP hay que controlar? Separados por comas."),
        "Controles de calidad": ("controles_calidad", "¿Cómo sabes que está bien hecha? Separado por comas."),
        "Tiempo activo": ("tiempo_activo_min", "¿Cuánto tiempo activo total requiere en minutos?"),
        "Tiempo total": ("tiempo_total_min", "¿Cuánto tiempo total técnico necesita incluyendo reposos/cocciones? En minutos."),
        "Maquinaria imprescindible": ("maquinaria_imprescindible", "¿Qué maquinaria es imprescindible? Separada por comas."),
        "Alérgenos": ("alergenos", "¿Qué alérgenos contiene? Separados por comas. Si no tiene, escribe ninguno."),
    }

    return [mapa[c] for c in faltan if c in mapa]


def completar_ficha_con_preguntas(ficha: FichaTecnicaHostAI) -> FichaTecnicaHostAI:
    preguntas = preguntas_para_completar(ficha)

    if not preguntas:
        print()
        print("Esta ficha no tiene campos obligatorios pendientes.")
        ficha.preguntas_pendientes = []
        return ficha

    print()
    print("Host AI va a completar la ficha preguntando solo lo que falta.")

    for campo, pregunta in preguntas:
        if campo in ["raciones", "tiempo_activo_min", "tiempo_total_min"]:
            valor = _pedir_entero(pregunta)
            if valor is not None:
                setattr(ficha, campo, valor)
        elif campo in ["puntos_criticos_haccp", "controles_calidad", "maquinaria_imprescindible", "alergenos"]:
            valor = _pedir_texto(pregunta)
            if valor:
                lista = _lista_desde_texto(valor)
                if campo == "alergenos" and len(lista) == 1 and lista[0].lower() == "ninguno":
                    lista = []
                setattr(ficha, campo, lista)
        else:
            valor = _pedir_texto(pregunta)
            if valor:
                setattr(ficha, campo, valor)

    ficha.recalcular_tiempos()

    if ficha.tiempo_total_min and ficha.tiempo_activo_min and ficha.tiempo_total_min >= ficha.tiempo_activo_min:
        ficha.tiempo_pasivo_min = ficha.tiempo_total_min - ficha.tiempo_activo_min

    ficha.preguntas_pendientes = detectar_campos_faltantes(ficha)
    ficha.estado = "borrador_incompleto" if ficha.preguntas_pendientes else "borrador_completo"
    return ficha


def resumen_para_cocinero(ficha: Dict) -> str:
    salida: List[str] = []

    salida.append("")
    salida.append(ficha.get("nombre", "Ficha técnica"))
    salida.append("=" * 70)
    salida.append(f"Código interno: {ficha.get('codigo', '')} | Estado: {ficha.get('estado', '')}")
    salida.append(f"Tipo: {ficha.get('tipo', '')} | Familia: {ficha.get('familia', '')}")
    salida.append(f"Objetivo: {ficha.get('objetivo', '')}")
    salida.append(f"Rendimiento: {ficha.get('rendimiento_final', '')}")
    salida.append(f"Raciones: {ficha.get('raciones', '')} | Peso/ración: {ficha.get('peso_racion', '')}")
    salida.append("")
    salida.append(f"Tiempo activo: {ficha.get('tiempo_activo_min', 0)} min")
    salida.append(f"Tiempo pasivo: {ficha.get('tiempo_pasivo_min', 0)} min")
    salida.append(f"Tiempo total técnico: {ficha.get('tiempo_total_min', 0)} min")
    salida.append("")
    salida.append("INGREDIENTES")
    salida.append("-" * 70)

    for ing in ficha.get("ingredientes", []):
        critico = " ⚠ crítico" if ing.get("es_critico") else ""
        salida.append(f"- {ing.get('cantidad')} {ing.get('unidad')} {ing.get('nombre')}{critico}")

    salida.append("")
    salida.append("PROCESO")
    salida.append("-" * 70)

    for fase in sorted(ficha.get("fases", []), key=lambda f: f.get("orden", 0)):
        salida.append(f"{fase.get('orden')}. {fase.get('nombre')}")
        salida.append(f"   {fase.get('descripcion')}")

        if fase.get("tiempo_activo_min") or fase.get("tiempo_pasivo_min"):
            salida.append(f"   Tiempo activo: {fase.get('tiempo_activo_min', 0)} min | Pasivo: {fase.get('tiempo_pasivo_min', 0)} min")

        if fase.get("punto_critico"):
            salida.append(f"   Punto crítico: {fase.get('punto_critico')}")

        if fase.get("control_calidad"):
            salida.append(f"   Control: {fase.get('control_calidad')}")

    salida.append("")
    salida.append("CONSERVACIÓN / SERVICIO")
    salida.append("-" * 70)
    salida.append(f"Conservación: {ficha.get('conservacion', '')}")
    salida.append(f"Vida útil: {ficha.get('vida_util', '')}")
    salida.append(f"Congelación: {ficha.get('congelacion', '')}")
    salida.append(f"Regeneración: {ficha.get('regeneracion', '')}")

    pendientes = ficha.get("preguntas_pendientes", [])
    if pendientes:
        salida.append("")
        salida.append("PENDIENTE DE COMPLETAR")
        salida.append("-" * 70)
        for p in pendientes:
            salida.append(f"- {p}")

    return "\n".join(salida)


def estado_ficha(ficha: Dict) -> str:
    pendientes = ficha.get("preguntas_pendientes", [])
    if pendientes:
        return f"Incompleta: faltan {len(pendientes)} campos"
    return "Completa"
