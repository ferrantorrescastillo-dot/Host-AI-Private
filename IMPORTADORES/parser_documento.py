import re
from pathlib import Path
from .modelos_documento import DocumentoImportado, ProductoDocumento


def _numero(texto):
    if texto is None:
        return None
    texto = str(texto).strip().replace(".", "").replace(",", ".")
    try:
        return float(texto)
    except Exception:
        return None


def detectar_proveedor(texto):
    t = texto.lower()
    if "makro" in t:
        if "tarragona" in t:
            return "Makro Tarragona"
        return "Makro"
    if "gavald" in t or "gavaldà" in t or "gavalda" in t:
        return "Gavaldà Gastronomia"
    return ""


def detectar_tipo_documento(texto):
    t = texto.lower()
    if "factura" in t:
        return "FACTURA"
    if "albar" in t:
        return "ALBARAN"
    if "presupuesto" in t or "pressupost" in t:
        return "PRESUPUESTO"
    return "DOCUMENTO"


def detectar_fecha(texto):
    patrones = [
        r"Fecha de venta:\s*(\d{2}/\d{2}/\d{4})",
        r"Fecha[:\s]+(\d{2}/\d{2}/\d{4})",
        r"(\d{2}/\d{2}/\d{4})",
        r"(\d{2}-\d{2}-\d{4})",
    ]
    for patron in patrones:
        m = re.search(patron, texto, re.IGNORECASE)
        if m:
            return m.group(1)
    return ""


def detectar_numero_documento(texto):
    patrones = [
        r"Factura:\s*([^\n]+)",
        r"Albar[aá]n[:\s]+([^\n]+)",
        r"Documento[:\s]+([^\n]+)",
    ]
    for patron in patrones:
        m = re.search(patron, texto, re.IGNORECASE)
        if m:
            return m.group(1).strip()[:120]
    return ""


def detectar_total(texto):
    patrones = [
        r"Total a pagar\s+(\d+[\.,]\d{2})",
        r"IMPORTE:\s*(\d+[\.,]\d{2})\s*EUR",
        r"TOTAL\s+(\d+[\.,]\d{2})",
    ]
    for patron in patrones:
        m = re.search(patron, texto, re.IGNORECASE)
        if m:
            return _numero(m.group(1))
    return None


def _limpiar_nombre(nombre):
    nombre = re.sub(r"\s+", " ", nombre).strip()
    nombre = nombre.replace("�", "Ñ")
    return nombre


def _parsear_linea_makro(linea):
    linea = re.sub(r"\s+", " ", linea.strip())
    # Formato habitual Makro:
    # GTIN DESCRIPCION PREC_CONT CONT PRECIO CANT IMPORTE IMP
    patron = re.compile(
        r"^(?P<codigo>\d{8,14})\s+"
        r"(?P<nombre>.+?)\s+"
        r"(?P<prec_cont>\d+[,.]\d{3})\s+"
        r"(?P<cont>\d+)\s+"
        r"(?P<precio>\d+[,.]\d{2})\s+"
        r"(?P<cantidad>\d+(?:[,.]\d+)?)\s+"
        r"(?P<importe>\d+[,.]\d{2})"
        r"(?:\s+(?P<iva>\d+))?"
    )
    m = patron.search(linea)
    if not m:
        return None
    return ProductoDocumento(
        codigo=m.group("codigo"),
        nombre=_limpiar_nombre(m.group("nombre")),
        cantidad=_numero(m.group("cantidad")),
        unidad="ud",
        precio_unitario=_numero(m.group("precio")),
        importe=_numero(m.group("importe")),
        iva=m.group("iva") or "",
        linea_original=linea,
    )


def detectar_productos(texto):
    productos = []
    vistos = set()
    for linea in texto.splitlines():
        linea_limpia = linea.strip()
        if not linea_limpia:
            continue
        producto = _parsear_linea_makro(linea_limpia)
        if producto:
            clave = (producto.codigo, producto.nombre, producto.importe)
            if clave not in vistos:
                productos.append(producto)
                vistos.add(clave)
    return productos


def parsear_documento(texto, archivo_origen=""):
    documento = DocumentoImportado(
        tipo_archivo=Path(archivo_origen).suffix.lower().replace(".", "").upper() if archivo_origen else "TEXTO",
        tipo_documento=detectar_tipo_documento(texto),
        proveedor=detectar_proveedor(texto),
        fecha=detectar_fecha(texto),
        numero_documento=detectar_numero_documento(texto),
        total=detectar_total(texto),
        texto_original=texto,
        archivo_origen=str(archivo_origen),
        productos=detectar_productos(texto),
    )
    return documento
