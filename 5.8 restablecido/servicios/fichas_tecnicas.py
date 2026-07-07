# -*- coding: utf-8 -*-
"""Servicio de Fichas Técnicas Host AI - Sprint 5.9"""
from __future__ import annotations
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from ficha_tecnica import FaseFicha, FichaTecnicaHostAI, IngredienteFicha
BASE_DIR = Path(__file__).resolve().parents[1]
DATOS_DIR = BASE_DIR / "DATOS"
FICHAS_DIR = DATOS_DIR / "fichas_tecnicas"
FICHAS_DIR.mkdir(parents=True, exist_ok=True)
CAMPOS_OBLIGATORIOS=[("codigo","Código interno"),("nombre","Nombre de la elaboración/plato"),("familia","Familia"),("objetivo","Objetivo de la elaboración"),("rendimiento_final","Rendimiento final"),("raciones","Número de raciones"),("peso_racion","Peso por ración"),("conservacion","Conservación"),("vida_util","Vida útil"),("regeneracion","Regeneración"),("puntos_criticos_haccp","Puntos críticos HACCP"),("controles_calidad","Controles de calidad")]

def _lista_desde_texto(texto:str)->List[str]: return [x.strip() for x in (texto or '').replace(';',',').split(',') if x.strip()]
def _pedir_texto(pregunta:str)->str:
    print(f"
{pregunta}"); print("ENTER = dejar pendiente"); return input('> ').strip()
def _pedir_entero(pregunta:str):
    v=_pedir_texto(pregunta)
    if not v: return None
    try: return int(v)
    except ValueError: print('No parece un número entero. Se deja pendiente.'); return None
def _normalizar_busqueda(texto:str)->str:
    texto=(texto or '').lower().strip()
    for a,b in {'á':'a','é':'e','í':'i','ó':'o','ú':'u','ü':'u','ñ':'n'}.items(): texto=texto.replace(a,b)
    return texto

def crear_ficha_carrillera_demo()->FichaTecnicaHostAI:
    ficha=FichaTecnicaHostAI(codigo='ELAB-CAR-001',nombre='Carrillera melosa prensada con demi-glace',tipo='elaboracion',familia='Carnes / Braseados',estado='validada_demo',objetivo='Obtener una carrillera melosa, limpia, prensada y porcionable, lista para regenerar en servicio con salsa demi-glace.',descripcion_corta='Carrillera braseada lentamente, deshuesada, prensada, abatida y racionada.',rendimiento_final='Aproximadamente 65-70% sobre peso limpio inicial',raciones=20,peso_racion='120-140 g',maquinaria_imprescindible=['horno','abatidor','cámara','fuego'],maquinaria_opcional=['roner','envasadora al vacío'],utensilios=['GN alta','colador fino','peso','film','papel sulfurizado','molde/prensa'],producciones_previas=['Demi-glace o fondo oscuro'],elaboraciones_que_desbloquea=['Taco de carrillera','Lingote de carrillera','Canelón de carrillera','Croqueta de carrillera'],conservacion='En cámara a 0-3 ºC, envasada y etiquetada.',vida_util='3-5 días en cámara si está abatida y manipulada correctamente.',congelacion='Sí. Congelar porciones envasadas al vacío o en bolsas de 10 raciones.',regeneracion='Regenerar suave con salsa a 65-70 ºC hasta centro caliente, sin hervir fuerte.',alergenos=['sulfitos si se usa vino','apio si lleva bresa con apio'],notas_jefe_cocina='Debe hacerse mínimo el día anterior si se quiere prensar bien.')
    ficha.ingredientes=[IngredienteFicha('Carrillera limpia',4.0,'kg',es_critico=True),IngredienteFicha('Cebolla',1.2,'kg'),IngredienteFicha('Zanahoria',0.8,'kg'),IngredienteFicha('Puerro',0.4,'kg'),IngredienteFicha('Ajo',0.08,'kg'),IngredienteFicha('Vino tinto',0.75,'L',alergenos=['sulfitos']),IngredienteFicha('Fondo oscuro / demi-glace',2.0,'L',es_critico=True),IngredienteFicha('Laurel',2,'hojas'),IngredienteFicha('Romero',1,'rama'),IngredienteFicha('Sal',40,'g'),IngredienteFicha('Pimienta negra',8,'g')]
    ficha.fases=[FaseFicha('Revisar y limpiar carrilleras',1,'Retirar grasa dura, nervios e impurezas. Pesar limpio.',40,utensilios=['cuchillo','tabla','peso'],control_calidad='Piezas limpias.',tipo='activa'),FaseFicha('Cortar bresa',2,'Cortar cebolla, zanahoria, puerro y ajo.',25,utensilios=['cuchillo','tabla','GN'],tipo='activa'),FaseFicha('Marcar carrilleras',3,'Marcar bien por todas las caras.',35,maquinaria=['fuego'],punto_critico='No cocer la carne en su propio jugo.',control_calidad='Color tostado uniforme.',tipo='activa'),FaseFicha('Sofreír bresa y desglasar',4,'Sofreír bresa, desglasar con vino y reducir alcohol.',30,maquinaria=['fuego'],punto_critico='Reducir bien el vino.',tipo='activa'),FaseFicha('Brasear carrilleras',5,'Cubrir con fondo/demi-glace y brasear tapado hasta textura melosa.',10,180,maquinaria=['horno'],depende_de=['Marcar carrilleras','Sofreír bresa y desglasar'],punto_critico='Cocción suave.',control_calidad='La carne cede al pinchar.',tipo='mixta'),FaseFicha('Deshuesar y limpiar',6,'Separar carne, retirar impurezas y reservar jugos.',45,depende_de=['Brasear carrilleras'],punto_critico='Trabajar templado.',tipo='activa'),FaseFicha('Colar y reducir salsa',7,'Colar la salsa y reducir hasta textura napante.',15,45,maquinaria=['fuego'],depende_de=['Brasear carrilleras'],control_calidad='Salsa brillante y sin grasa excesiva.',tipo='mixta'),FaseFicha('Prensar',8,'Colocar carrillera en molde y prensar con peso.',25,720,depende_de=['Deshuesar y limpiar'],punto_critico='Prensar mínimo una noche.',tipo='mixta'),FaseFicha('Abatir',9,'Abatir rápidamente antes de cámara.',10,60,maquinaria=['abatidor'],depende_de=['Prensar'],punto_critico='No meter caliente directo en cámara.',tipo='mixta'),FaseFicha('Porcionar, envasar, etiquetar y registrar',10,'Cortar raciones, pesar, envasar y registrar.',45,depende_de=['Abatir'],control_calidad='Ración limpia y peso correcto.',tipo='cierre')]
    ficha.puntos_criticos_haccp=['Abatir antes de guardar en cámara.','No dejar enfriar a temperatura ambiente durante horas.','Etiquetar con fecha, lote, peso y responsable.','Regenerar sin hervir agresivamente.']
    ficha.controles_calidad=['Textura melosa.','Sabor profundo y equilibrado.','Salsa sin grasa excesiva.','Corte limpio tras prensado.','Peso de ración correcto.']
    ficha.errores_frecuentes=['No marcar bien la carne.','No reducir el vino.','Brasear demasiado fuerte.','No prensar suficiente tiempo.','Guardar sin abatir ni etiquetar.']
    ficha.recalcular_tiempos(); ficha.preguntas_pendientes=detectar_campos_faltantes(ficha); return ficha

def detectar_campos_faltantes(ficha:FichaTecnicaHostAI)->List[str]:
    faltan=[]
    for campo,nombre in CAMPOS_OBLIGATORIOS:
        v=getattr(ficha,campo,None)
        if v is None or v=='' or v==[]: faltan.append(nombre)
    if not ficha.ingredientes: faltan.append('Ingredientes')
    if not ficha.fases: faltan.append('Proceso por fases')
    if ficha.tiempo_activo_min==0: faltan.append('Tiempo activo')
    if ficha.tiempo_total_min==0: faltan.append('Tiempo total')
    if not ficha.maquinaria_imprescindible: faltan.append('Maquinaria imprescindible')
    if not ficha.alergenos: faltan.append('Alérgenos')
    return faltan

def guardar_ficha(ficha:FichaTecnicaHostAI)->Path:
    ficha.recalcular_tiempos(); ficha.preguntas_pendientes=detectar_campos_faltantes(ficha)
    if ficha.preguntas_pendientes and ficha.estado.startswith('borrador'): ficha.estado='borrador_incompleto'
    elif not ficha.preguntas_pendientes and ficha.estado.startswith('borrador'): ficha.estado='borrador_completo'
    path=FICHAS_DIR/f'{ficha.codigo}.json'; path.write_text(json.dumps(ficha.to_dict(),ensure_ascii=False,indent=2),encoding='utf-8'); return path

def guardar_dict_ficha(ficha:Dict)->Path:
    codigo=ficha.get('codigo') or 'BORRADOR-001'; path=FICHAS_DIR/f'{codigo}.json'; path.write_text(json.dumps(ficha,ensure_ascii=False,indent=2),encoding='utf-8'); return path
def listar_fichas()->List[Path]: return sorted(FICHAS_DIR.glob('*.json'))
def cargar_ficha(codigo:str)->Optional[Dict]:
    path=FICHAS_DIR/f'{codigo}.json'; return json.loads(path.read_text(encoding='utf-8')) if path.exists() else None

def buscar_fichas_por_texto(texto:str)->List[Dict]:
    q=_normalizar_busqueda(texto); resultados=[]
    for path in listar_fichas():
        try: data=json.loads(path.read_text(encoding='utf-8'))
        except Exception: continue
        codigo=_normalizar_busqueda(data.get('codigo',path.stem)); nombre=_normalizar_busqueda(data.get('nombre',''))
        if q==codigo or q in codigo or q in nombre: resultados.append(data)
    return resultados

def elegir_ficha_por_nombre_o_codigo(texto:str)->Optional[Dict]:
    resultados=buscar_fichas_por_texto(texto)
    if not resultados: return None
    if len(resultados)==1: return resultados[0]
    print('
He encontrado varias fichas parecidas:')
    for i,f in enumerate(resultados,1): print(f"{i}. {f.get('nombre')} | Código interno: {f.get('codigo')} | Estado: {f.get('estado','')}")
    try:
        idx=int(input('
Elige número: ').strip())
        if 1<=idx<=len(resultados): return resultados[idx-1]
    except ValueError: pass
    print('Selección no válida.'); return None

def dict_a_ficha(data:Dict)->FichaTecnicaHostAI:
    kwargs={k:data.get(k) for k in FichaTecnicaHostAI.__dataclass_fields__.keys() if k in data and k not in ['ingredientes','fases']}
    ficha=FichaTecnicaHostAI(**kwargs)
    ficha.ingredientes=[IngredienteFicha(**i) for i in data.get('ingredientes',[])]
    ficha.fases=[FaseFicha(**f) for f in data.get('fases',[])]
    return ficha

def crear_ficha_desde_receta_basica(texto:str)->FichaTecnicaHostAI:
    lineas=[l.strip() for l in texto.splitlines() if l.strip()]; nombre=lineas[0] if lineas else 'Ficha sin nombre'
    codigo_base=_normalizar_busqueda(nombre).upper().replace(' ','-').replace('/','-')[:25]; codigo=f'BORRADOR-{codigo_base}' if codigo_base else 'BORRADOR-001'
    ficha=FichaTecnicaHostAI(codigo=codigo,nombre=nombre,estado='borrador',objetivo='',notas_jefe_cocina='Ficha generada desde texto. Requiere revisión.')
    ingredientes=[]; fases=[]; orden=1
    verbos=('cortar','cocer','marcar','abatir','mezclar','triturar','colar','reservar','freír','freir','confitar','envasar','reducir','hornear','limpiar','picar','pelar','laminar','texturizar','reposar','introducir','sacar','poner','añadir','enrollar')
    for linea in lineas[1:]:
        limpia=linea.strip(); partes=limpia.replace(',','.').split()
        if len(partes)>=3:
            try: ingredientes.append(IngredienteFicha(' '.join(partes[2:]),float(partes[0]),partes[1])); continue
            except ValueError: pass
        linea_sin_num=limpia.split('.',1)[1].strip() if '.' in limpia[:3] else (limpia.split(')',1)[1].strip() if ')' in limpia[:3] else limpia)
        if linea_sin_num.lower().startswith(verbos) or limpia[:1].isdigit(): fases.append(FaseFicha(nombre=f'Paso {orden}',orden=orden,descripcion=linea_sin_num,tiempo_activo_min=0,tipo='activa')); orden+=1
    ficha.ingredientes=ingredientes; ficha.fases=fases; ficha.recalcular_tiempos(); ficha.preguntas_pendientes=detectar_campos_faltantes(ficha); return ficha

def preguntas_para_completar(ficha:FichaTecnicaHostAI)->List[Tuple[str,str]]:
    mapa={'Código interno':('codigo','Código interno para guardar la ficha. Ejemplo: ELAB-CAR-001'),'Familia':('familia','¿A qué familia pertenece?'),'Objetivo de la elaboración':('objetivo','¿Cuál es el objetivo final?'),'Rendimiento final':('rendimiento_final','¿Qué rendimiento final esperas?'),'Número de raciones':('raciones','¿Cuántas raciones salen?'),'Peso por ración':('peso_racion','¿Qué peso debe tener cada ración?'),'Conservación':('conservacion','¿Cómo se conserva?'),'Vida útil':('vida_util','¿Cuántos días dura?'),'Regeneración':('regeneracion','¿Cómo se regenera?'),'Puntos críticos HACCP':('puntos_criticos_haccp','¿Qué puntos críticos HACCP hay que controlar? Separados por comas.'),'Controles de calidad':('controles_calidad','¿Cómo sabes que está bien hecha? Separado por comas.'),'Tiempo activo':('tiempo_activo_min','¿Cuánto tiempo activo total requiere en minutos?'),'Tiempo total':('tiempo_total_min','¿Cuánto tiempo total técnico necesita en minutos?'),'Maquinaria imprescindible':('maquinaria_imprescindible','¿Qué maquinaria es imprescindible? Separada por comas.'),'Alérgenos':('alergenos','¿Qué alérgenos contiene? Si no tiene, escribe ninguno.')}
    return [mapa[c] for c in detectar_campos_faltantes(ficha) if c in mapa]

def completar_ficha_con_preguntas(ficha:FichaTecnicaHostAI)->FichaTecnicaHostAI:
    preguntas=preguntas_para_completar(ficha)
    if not preguntas: print('
Esta ficha no tiene campos obligatorios pendientes.'); ficha.preguntas_pendientes=[]; return ficha
    print('
Host AI va a completar la ficha preguntando solo lo que falta.')
    for campo,pregunta in preguntas:
        if campo in ['raciones','tiempo_activo_min','tiempo_total_min']:
            v=_pedir_entero(pregunta)
            if v is not None: setattr(ficha,campo,v)
        elif campo in ['puntos_criticos_haccp','controles_calidad','maquinaria_imprescindible','alergenos']:
            v=_pedir_texto(pregunta)
            if v:
                lista=_lista_desde_texto(v)
                if campo=='alergenos' and len(lista)==1 and lista[0].lower()=='ninguno': lista=[]
                setattr(ficha,campo,lista)
        else:
            v=_pedir_texto(pregunta)
            if v: setattr(ficha,campo,v)
    ficha.recalcular_tiempos()
    if ficha.tiempo_total_min and ficha.tiempo_activo_min and ficha.tiempo_total_min>=ficha.tiempo_activo_min: ficha.tiempo_pasivo_min=ficha.tiempo_total_min-ficha.tiempo_activo_min
    ficha.preguntas_pendientes=detectar_campos_faltantes(ficha); ficha.estado='borrador_incompleto' if ficha.preguntas_pendientes else 'borrador_completo'; return ficha

def resumen_para_cocinero(ficha:Dict)->str:
    salida=[f"
{ficha.get('nombre','Ficha técnica')}",'='*70,f"Código interno: {ficha.get('codigo','')} | Estado: {ficha.get('estado','')}",f"Tipo: {ficha.get('tipo','')} | Familia: {ficha.get('familia','')}",f"Objetivo: {ficha.get('objetivo','')}",f"Rendimiento: {ficha.get('rendimiento_final','')}",f"Raciones: {ficha.get('raciones','')} | Peso/ración: {ficha.get('peso_racion','')}",'',f"Tiempo activo: {ficha.get('tiempo_activo_min',0)} min",f"Tiempo pasivo: {ficha.get('tiempo_pasivo_min',0)} min",f"Tiempo total técnico: {ficha.get('tiempo_total_min',0)} min",'','INGREDIENTES','-'*70]
    for ing in ficha.get('ingredientes',[]): salida.append(f"- {ing.get('cantidad')} {ing.get('unidad')} {ing.get('nombre')}{' ⚠ crítico' if ing.get('es_critico') else ''}")
    salida+=['','PROCESO','-'*70]
    for fase in sorted(ficha.get('fases',[]),key=lambda f:f.get('orden',0)):
        salida.append(f"{fase.get('orden')}. {fase.get('nombre')}"); salida.append(f"   {fase.get('descripcion')}")
        if fase.get('tiempo_activo_min') or fase.get('tiempo_pasivo_min'): salida.append(f"   Tiempo activo: {fase.get('tiempo_activo_min',0)} min | Pasivo: {fase.get('tiempo_pasivo_min',0)} min")
        if fase.get('punto_critico'): salida.append(f"   Punto crítico: {fase.get('punto_critico')}")
        if fase.get('control_calidad'): salida.append(f"   Control: {fase.get('control_calidad')}")
    salida+=['','CONSERVACIÓN / SERVICIO','-'*70,f"Conservación: {ficha.get('conservacion','')}",f"Vida útil: {ficha.get('vida_util','')}",f"Congelación: {ficha.get('congelacion','')}",f"Regeneración: {ficha.get('regeneracion','')}"]
    if ficha.get('preguntas_pendientes'):
        salida+=['','PENDIENTE DE COMPLETAR','-'*70]+[f"- {p}" for p in ficha.get('preguntas_pendientes',[])]
    return '
'.join(salida)

def estado_ficha(ficha:Dict)->str:
    pendientes=ficha.get('preguntas_pendientes',[]); return f'Incompleta: faltan {len(pendientes)} campos' if pendientes else 'Completa'
