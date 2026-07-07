# -*- coding: utf-8 -*-
"""
SERVICIOS/motor_economico.py
Sprint 6.3 - Motor económico base

Bloque nuevo:
- Escandallos completos
- Stock real
- Compras
- Histórico de precios
- Producción por lotes

Decisiones cerradas:
1. Las elaboraciones intermedias existen como stock propio.
   Ejemplo: fondo oscuro producido queda como litros en stock.
2. Las compras trabajan con unidades convertibles.
   Ejemplo: 1 caja de cebolla = 25 kg.
3. El stock guarda peso/cantidad real comprado.
   La merma se aplica en el escandallo, no al entrar stock.
4. Se guarda histórico de precios.
5. Cada producción genera lote con fecha, caducidad, responsable y cantidad.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict, field
from datetime import date, timedelta
from pathlib import Path
from typing import Dict, List, Optional
import json


BASE_DIR = Path(__file__).resolve().parents[1]
DATOS_DIR = BASE_DIR / "DATOS"
ECONOMIA_DIR = DATOS_DIR / "economia"
ECONOMIA_DIR.mkdir(parents=True, exist_ok=True)

ARTICULOS_PATH = ECONOMIA_DIR / "articulos.json"
STOCK_PATH = ECONOMIA_DIR / "stock.json"
ESCANDALLOS_PATH = ECONOMIA_DIR / "escandallos.json"
HISTORICO_PRECIOS_PATH = ECONOMIA_DIR / "historico_precios.json"
LOTES_PATH = ECONOMIA_DIR / "lotes_produccion.json"
PEDIDOS_PATH = ECONOMIA_DIR / "pedidos_compra.json"


@dataclass
class ArticuloEconomico:
    codigo: str
    nombre: str
    familia: str
    unidad_base: str
    proveedor_principal: str = ""
    precio_actual: float = 0.0
    unidad_compra: str = ""
    factor_compra_a_base: float = 1.0
    stock_minimo: float = 0.0
    stock_ideal: float = 0.0
    es_produccion_intermedia: bool = False
    observaciones: str = ""


@dataclass
class LineaEscandallo:
    codigo_articulo: str
    nombre: str
    cantidad_bruta: float
    unidad: str
    merma_porcentaje: float = 0.0

    @property
    def cantidad_neta_estimada(self) -> float:
        return self.cantidad_bruta * (1 - self.merma_porcentaje / 100)


@dataclass
class Escandallo:
    codigo: str
    nombre: str
    version: str
    rendimiento_final: float
    unidad_rendimiento: str
    raciones: int
    lineas: List[LineaEscandallo] = field(default_factory=list)
    estado: str = "borrador"


@dataclass
class LoteProduccion:
    lote: str
    codigo_articulo: str
    nombre: str
    fecha_produccion: str
    fecha_caducidad: str
    responsable: str
    cantidad_producida: float
    unidad: str
    origen_escandallo: str


def _leer_json(path: Path, defecto):
    if not path.exists():
        return defecto
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return defecto


def _guardar_json(path: Path, data) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def _hoy() -> str:
    return date.today().isoformat()


class MotorEconomico:
    def __init__(self):
        self.articulos: Dict[str, Dict] = _leer_json(ARTICULOS_PATH, {})
        self.stock: Dict[str, Dict] = _leer_json(STOCK_PATH, {})
        self.escandallos: Dict[str, Dict] = _leer_json(ESCANDALLOS_PATH, {})
        self.historico_precios: List[Dict] = _leer_json(HISTORICO_PRECIOS_PATH, [])
        self.lotes: List[Dict] = _leer_json(LOTES_PATH, [])
        self.pedidos: List[Dict] = _leer_json(PEDIDOS_PATH, [])

    def guardar(self) -> None:
        _guardar_json(ARTICULOS_PATH, self.articulos)
        _guardar_json(STOCK_PATH, self.stock)
        _guardar_json(ESCANDALLOS_PATH, self.escandallos)
        _guardar_json(HISTORICO_PRECIOS_PATH, self.historico_precios)
        _guardar_json(LOTES_PATH, self.lotes)
        _guardar_json(PEDIDOS_PATH, self.pedidos)

    def crear_demo(self) -> None:
        articulos = [
            ArticuloEconomico("MAT-CAR-001", "Carrillera limpia", "Carnes", "kg", "Proveedor Carne", 9.50, "kg", 1, 2, 6),
            ArticuloEconomico("MAT-VER-001", "Cebolla", "Verduras", "kg", "Proveedor Verdura", 1.10, "caja", 25, 5, 25),
            ArticuloEconomico("MAT-VER-002", "Zanahoria", "Verduras", "kg", "Proveedor Verdura", 0.95, "caja", 10, 3, 10),
            ArticuloEconomico("MAT-VER-003", "Puerro", "Verduras", "kg", "Proveedor Verdura", 2.20, "kg", 1, 1, 4),
            ArticuloEconomico("MAT-VIN-001", "Vino tinto cocina", "Bodega", "L", "Proveedor Bebidas", 2.40, "botella", 0.75, 2, 6),
            ArticuloEconomico("ELAB-FON-001", "Fondo oscuro", "Producción intermedia", "L", "", 0.0, "L", 1, 2, 10, True),
            ArticuloEconomico("ELAB-CAR-001", "Carrillera melosa prensada", "Elaboraciones", "ración", "", 0.0, "ración", 1, 5, 20, True),
        ]

        for articulo in articulos:
            self.articulos[articulo.codigo] = asdict(articulo)
            self.stock.setdefault(
                articulo.codigo,
                {
                    "codigo_articulo": articulo.codigo,
                    "nombre": articulo.nombre,
                    "cantidad": 0.0,
                    "unidad": articulo.unidad_base,
                    "ubicacion": "cámara/almacén",
                    "ultimo_movimiento": "",
                },
            )

        escandallo = Escandallo(
            codigo="ESC-CAR-001",
            nombre="Carrillera melosa prensada",
            version="1.0",
            rendimiento_final=20,
            unidad_rendimiento="raciones",
            raciones=20,
            estado="validado_demo",
            lineas=[
                LineaEscandallo("MAT-CAR-001", "Carrillera limpia", 4.0, "kg", 5),
                LineaEscandallo("MAT-VER-001", "Cebolla", 1.2, "kg", 12),
                LineaEscandallo("MAT-VER-002", "Zanahoria", 0.8, "kg", 10),
                LineaEscandallo("MAT-VER-003", "Puerro", 0.4, "kg", 15),
                LineaEscandallo("MAT-VIN-001", "Vino tinto cocina", 0.75, "L", 0),
                LineaEscandallo("ELAB-FON-001", "Fondo oscuro", 2.0, "L", 0),
            ],
        )

        self.escandallos[escandallo.codigo] = {
            "codigo": escandallo.codigo,
            "nombre": escandallo.nombre,
            "version": escandallo.version,
            "rendimiento_final": escandallo.rendimiento_final,
            "unidad_rendimiento": escandallo.unidad_rendimiento,
            "raciones": escandallo.raciones,
            "estado": escandallo.estado,
            "lineas": [asdict(linea) for linea in escandallo.lineas],
        }

        self.guardar()

    def registrar_compra(self, codigo_articulo: str, cantidad_compra: float, unidad_compra: str, precio_unitario: float, proveedor: str = "") -> Dict:
        articulo = self.articulos.get(codigo_articulo)
        if not articulo:
            raise ValueError(f"No existe el artículo {codigo_articulo}")

        factor = articulo.get("factor_compra_a_base", 1.0)
        unidad_definida = articulo.get("unidad_compra") or articulo.get("unidad_base")

        if unidad_compra == articulo.get("unidad_base"):
            cantidad_base = cantidad_compra
        elif unidad_compra == unidad_definida:
            cantidad_base = cantidad_compra * factor
        else:
            raise ValueError(f"Unidad no reconocida para {articulo.get('nombre')}: {unidad_compra}")

        stock = self.stock.setdefault(
            codigo_articulo,
            {
                "codigo_articulo": codigo_articulo,
                "nombre": articulo.get("nombre"),
                "cantidad": 0.0,
                "unidad": articulo.get("unidad_base"),
                "ubicacion": "sin definir",
                "ultimo_movimiento": "",
            },
        )

        stock["cantidad"] = round(stock.get("cantidad", 0.0) + cantidad_base, 4)
        stock["ultimo_movimiento"] = _hoy()

        precio_anterior = articulo.get("precio_actual", 0.0)
        articulo["precio_actual"] = precio_unitario
        if proveedor:
            articulo["proveedor_principal"] = proveedor

        self.historico_precios.append(
            {
                "fecha": _hoy(),
                "codigo_articulo": codigo_articulo,
                "nombre": articulo.get("nombre"),
                "precio_anterior": precio_anterior,
                "precio_nuevo": precio_unitario,
                "unidad": articulo.get("unidad_base"),
                "proveedor": proveedor or articulo.get("proveedor_principal", ""),
            }
        )

        self.guardar()

        return {
            "codigo_articulo": codigo_articulo,
            "nombre": articulo.get("nombre"),
            "cantidad_entrada_base": cantidad_base,
            "unidad_base": articulo.get("unidad_base"),
            "stock_actual": stock["cantidad"],
            "precio_actualizado": precio_unitario,
        }

    def coste_escandallo(self, codigo_escandallo: str) -> Dict:
        esc = self.escandallos.get(codigo_escandallo)
        if not esc:
            raise ValueError(f"No existe el escandallo {codigo_escandallo}")

        total = 0.0
        lineas_calculadas = []

        for linea in esc.get("lineas", []):
            codigo = linea["codigo_articulo"]
            articulo = self.articulos.get(codigo, {})
            precio = articulo.get("precio_actual", 0.0)
            cantidad_bruta = float(linea.get("cantidad_bruta", 0.0))
            merma = float(linea.get("merma_porcentaje", 0.0))
            cantidad_neta = cantidad_bruta * (1 - merma / 100)
            coste = cantidad_bruta * precio
            total += coste

            lineas_calculadas.append(
                {
                    "codigo_articulo": codigo,
                    "nombre": linea.get("nombre"),
                    "cantidad_bruta": cantidad_bruta,
                    "unidad": linea.get("unidad"),
                    "merma_porcentaje": merma,
                    "cantidad_neta_estimada": round(cantidad_neta, 4),
                    "precio_unitario": precio,
                    "coste": round(coste, 4),
                }
            )

        raciones = esc.get("raciones") or 1
        coste_racion = total / raciones if raciones else 0

        return {
            "codigo_escandallo": codigo_escandallo,
            "nombre": esc.get("nombre"),
            "coste_total": round(total, 4),
            "raciones": raciones,
            "coste_por_racion": round(coste_racion, 4),
            "lineas": lineas_calculadas,
        }

    def producir_desde_escandallo(self, codigo_escandallo: str, responsable: str, dias_caducidad: int = 5) -> Dict:
        esc = self.escandallos.get(codigo_escandallo)
        if not esc:
            raise ValueError(f"No existe el escandallo {codigo_escandallo}")

        consumos = []
        avisos = []

        for linea in esc.get("lineas", []):
            codigo = linea["codigo_articulo"]
            cantidad = float(linea.get("cantidad_bruta", 0.0))
            stock = self.stock.setdefault(
                codigo,
                {
                    "codigo_articulo": codigo,
                    "nombre": linea.get("nombre"),
                    "cantidad": 0.0,
                    "unidad": linea.get("unidad"),
                    "ubicacion": "sin definir",
                    "ultimo_movimiento": "",
                },
            )

            stock["cantidad"] = round(stock.get("cantidad", 0.0) - cantidad, 4)
            stock["ultimo_movimiento"] = _hoy()

            if stock["cantidad"] < 0:
                avisos.append(f"Stock negativo de {linea.get('nombre')}: {stock['cantidad']} {stock.get('unidad')}")

            consumos.append(
                {
                    "codigo_articulo": codigo,
                    "nombre": linea.get("nombre"),
                    "cantidad_consumida": cantidad,
                    "unidad": linea.get("unidad"),
                    "stock_resultante": stock["cantidad"],
                }
            )

        codigo_producto = "ELAB-CAR-001" if codigo_escandallo == "ESC-CAR-001" else f"PROD-{codigo_escandallo}"
        articulo_producto = self.articulos.setdefault(
            codigo_producto,
            {
                "codigo": codigo_producto,
                "nombre": esc.get("nombre"),
                "familia": "Elaboraciones",
                "unidad_base": esc.get("unidad_rendimiento", "unidad"),
                "precio_actual": 0.0,
                "stock_minimo": 0.0,
                "stock_ideal": 0.0,
                "es_produccion_intermedia": True,
            },
        )

        stock_producto = self.stock.setdefault(
            codigo_producto,
            {
                "codigo_articulo": codigo_producto,
                "nombre": articulo_producto.get("nombre"),
                "cantidad": 0.0,
                "unidad": esc.get("unidad_rendimiento", "unidad"),
                "ubicacion": "cámara producción",
                "ultimo_movimiento": "",
            },
        )

        cantidad_producida = float(esc.get("rendimiento_final", 0.0))
        stock_producto["cantidad"] = round(stock_producto.get("cantidad", 0.0) + cantidad_producida, 4)
        stock_producto["ultimo_movimiento"] = _hoy()

        lote_num = len(self.lotes) + 1
        lote = LoteProduccion(
            lote=f"LOTE-{date.today().strftime('%Y%m%d')}-{lote_num:03d}",
            codigo_articulo=codigo_producto,
            nombre=esc.get("nombre"),
            fecha_produccion=_hoy(),
            fecha_caducidad=(date.today() + timedelta(days=dias_caducidad)).isoformat(),
            responsable=responsable,
            cantidad_producida=cantidad_producida,
            unidad=esc.get("unidad_rendimiento", "unidad"),
            origen_escandallo=codigo_escandallo,
        )

        self.lotes.append(asdict(lote))
        self.guardar()

        return {
            "escandallo": codigo_escandallo,
            "producto_generado": codigo_producto,
            "cantidad_producida": cantidad_producida,
            "unidad": esc.get("unidad_rendimiento", "unidad"),
            "lote": asdict(lote),
            "consumos": consumos,
            "avisos": avisos,
            "stock_producto_final": stock_producto["cantidad"],
        }

    def generar_pedido_reposicion(self) -> List[Dict]:
        pedido_por_proveedor: Dict[str, List[Dict]] = {}

        for codigo, articulo in self.articulos.items():
            stock = self.stock.get(codigo, {})
            cantidad = float(stock.get("cantidad", 0.0))
            minimo = float(articulo.get("stock_minimo", 0.0))
            ideal = float(articulo.get("stock_ideal", 0.0))

            if ideal <= 0:
                continue

            if cantidad < minimo:
                falta = round(ideal - cantidad, 4)
                proveedor = articulo.get("proveedor_principal") or "Proveedor sin definir"
                pedido_por_proveedor.setdefault(proveedor, []).append(
                    {
                        "codigo_articulo": codigo,
                        "nombre": articulo.get("nombre"),
                        "stock_actual": cantidad,
                        "stock_minimo": minimo,
                        "stock_ideal": ideal,
                        "cantidad_a_pedir": falta,
                        "unidad": articulo.get("unidad_base"),
                    }
                )

        pedidos = []
        for proveedor, lineas in pedido_por_proveedor.items():
            pedido = {
                "fecha": _hoy(),
                "proveedor": proveedor,
                "lineas": lineas,
            }
            pedidos.append(pedido)

        self.pedidos = pedidos
        self.guardar()
        return pedidos

    def resumen_stock(self) -> List[Dict]:
        salida = []
        for codigo, stock in sorted(self.stock.items()):
            articulo = self.articulos.get(codigo, {})
            salida.append(
                {
                    "codigo": codigo,
                    "nombre": stock.get("nombre"),
                    "cantidad": stock.get("cantidad", 0.0),
                    "unidad": stock.get("unidad"),
                    "stock_minimo": articulo.get("stock_minimo", 0.0),
                    "stock_ideal": articulo.get("stock_ideal", 0.0),
                    "proveedor": articulo.get("proveedor_principal", ""),
                }
            )
        return salida


def imprimir_coste_escandallo_demo() -> None:
    motor = MotorEconomico()
    motor.crear_demo()
    coste = motor.coste_escandallo("ESC-CAR-001")

    print()
    print("=" * 90)
    print("ESCANDALLO COMPLETO - DEMO")
    print("=" * 90)
    print(f"Escandallo: {coste['nombre']}")
    print(f"Coste total: {coste['coste_total']} €")
    print(f"Raciones: {coste['raciones']}")
    print(f"Coste/ración: {coste['coste_por_racion']} €")
    print()
    print("LÍNEAS")
    print("-" * 90)

    for linea in coste["lineas"]:
        print(f"- {linea['nombre']}: {linea['cantidad_bruta']} {linea['unidad']} | merma {linea['merma_porcentaje']}% | coste {linea['coste']} €")


def imprimir_demo_completa() -> None:
    motor = MotorEconomico()
    motor.crear_demo()

    print()
    print("=" * 90)
    print("MOTOR ECONÓMICO HOST AI - SPRINT 6.3")
    print("=" * 90)

    print()
    print("1) COMPRA DE STOCK")
    print("-" * 90)
    compras = [
        motor.registrar_compra("MAT-CAR-001", 10, "kg", 9.50, "Proveedor Carne"),
        motor.registrar_compra("MAT-VER-001", 1, "caja", 1.10, "Proveedor Verdura"),
        motor.registrar_compra("MAT-VER-002", 1, "caja", 0.95, "Proveedor Verdura"),
        motor.registrar_compra("MAT-VER-003", 4, "kg", 2.20, "Proveedor Verdura"),
        motor.registrar_compra("MAT-VIN-001", 6, "botella", 2.40, "Proveedor Bebidas"),
        motor.registrar_compra("ELAB-FON-001", 8, "L", 0.0, ""),
    ]

    for compra in compras:
        print(f"- {compra['nombre']}: entra {compra['cantidad_entrada_base']} {compra['unidad_base']} | stock actual {compra['stock_actual']}")

    print()
    print("2) COSTE DEL ESCANDALLO")
    print("-" * 90)
    coste = motor.coste_escandallo("ESC-CAR-001")
    print(f"Coste total: {coste['coste_total']} €")
    print(f"Coste/ración: {coste['coste_por_racion']} €")

    print()
    print("3) PRODUCCIÓN POR LOTE")
    print("-" * 90)
    produccion = motor.producir_desde_escandallo("ESC-CAR-001", responsable="Ferran", dias_caducidad=5)
    print(f"Lote generado: {produccion['lote']['lote']}")
    print(f"Producto: {produccion['producto_generado']}")
    print(f"Cantidad producida: {produccion['cantidad_producida']} {produccion['unidad']}")
    print(f"Caducidad: {produccion['lote']['fecha_caducidad']}")

    if produccion["avisos"]:
        print()
        print("AVISOS")
        for aviso in produccion["avisos"]:
            print(f"⚠ {aviso}")

    print()
    print("4) STOCK DESPUÉS DE PRODUCIR")
    print("-" * 90)
    for s in motor.resumen_stock():
        print(f"- {s['nombre']}: {s['cantidad']} {s['unidad']}")

    print()
    print("5) PEDIDO AUTOMÁTICO POR STOCK MÍNIMO")
    print("-" * 90)
    pedidos = motor.generar_pedido_reposicion()

    if not pedidos:
        print("No hay pedidos necesarios.")
    else:
        for pedido in pedidos:
            print(f"\nProveedor: {pedido['proveedor']}")
            for linea in pedido["lineas"]:
                print(f"- {linea['nombre']}: pedir {linea['cantidad_a_pedir']} {linea['unidad']}")

    print()
    print("6) HISTÓRICO DE PRECIOS")
    print("-" * 90)
    for h in motor.historico_precios[-8:]:
        print(f"- {h['fecha']} | {h['nombre']} | {h['precio_anterior']} -> {h['precio_nuevo']} €/{h['unidad']}")

    print()
    print("=" * 90)
    print("LECTURA DE JEFE DE COCINA")
    print("=" * 90)
    print("- El stock guarda la cantidad real comprada.")
    print("- La merma vive en el escandallo.")
    print("- Las compras pueden entrar por caja/botella/kg/L y convertirse a unidad base.")
    print("- La producción genera lote, caducidad, responsable y cantidad producida.")
    print("- Los precios quedan guardados en histórico.")


if __name__ == "__main__":
    imprimir_demo_completa()
