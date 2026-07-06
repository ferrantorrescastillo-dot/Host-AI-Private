# Host AI 2.1 Sprint 4.2

## Nuevo
- Importador de documentos con lectura PDF/Word/TXT.
- Parser de factura Makro.
- Documentos importados guardados en SQLite.
- Comparador inteligente con artículos existentes.
- Equivalencias de nombres de artículos.
- Historial de precios.
- Aplicación confirmada de cambios: crear artículos y actualizar precios.

## Prueba recomendada
1. Instalar dependencias: `py -m pip install pdfplumber PyPDF2 python-docx`
2. Ejecutar `Main.py`.
3. Entrar en `12. Importar documentos`.
4. Importar PDF de Makro.
5. Vista previa / comparar.
6. Aplicar cambios solo si el resumen tiene sentido.
