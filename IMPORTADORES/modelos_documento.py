from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ProductoDocumento:
    codigo: str = ""
    nombre: str = ""
    cantidad: Optional[float] = None
    unidad: str = ""
    precio_unitario: Optional[float] = None
    importe: Optional[float] = None
    iva: str = ""
    linea_original: str = ""


@dataclass
class DocumentoImportado:
    tipo_archivo: str = ""
    tipo_documento: str = "DESCONOCIDO"
    proveedor: str = ""
    fecha: str = ""
    numero_documento: str = ""
    total: Optional[float] = None
    texto_original: str = ""
    archivo_origen: str = ""
    productos: List[ProductoDocumento] = field(default_factory=list)

    def resumen(self) -> str:
        return (
            f"Tipo: {self.tipo_documento}\n"
            f"Proveedor: {self.proveedor or '-'}\n"
            f"Fecha: {self.fecha or '-'}\n"
            f"Documento: {self.numero_documento or '-'}\n"
            f"Productos: {len(self.productos)}\n"
            f"Total: {self.total if self.total is not None else '-'}"
        )
