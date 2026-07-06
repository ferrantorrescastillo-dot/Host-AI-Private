from pathlib import Path

from database import conectar, asegurar_restaurante_demo

try:
    from docx import Document
except ImportError:
    Document = None


def leer_docx(ruta_archivo):
    if Document is None:
        raise RuntimeError("Falta instalar python-docx. Ejecuta: py -m pip install python-docx")

    documento = Document(ruta_archivo)
    lineas = []

    for parrafo in documento.paragraphs:
        texto = parrafo.text.strip()
        if texto:
            lineas.append(texto)

    return lineas


def es_titulo_mayusculas(linea):
    texto = str(linea).strip()

    if not texto:
        return False

    if len(texto) > 90:
        return False

    letras = [caracter for caracter in texto if caracter.isalpha()]

    if not letras:
        return False

    letras_mayusculas = [caracter for caracter in letras if caracter.isupper()]
    porcentaje_mayusculas = len(letras_mayusculas) / len(letras)

    return porcentaje_mayusculas >= 0.80


def detectar_elaboraciones(lineas):
    elaboraciones = []
    elaboracion_actual = None

    for linea in lineas:
        if es_titulo_mayusculas(linea):
            if elaboracion_actual is not None:
                elaboraciones.append(elaboracion_actual)

            elaboracion_actual = {
                "nombre": linea.strip(),
                "contenido": [],
            }
        else:
            if elaboracion_actual is not None:
                elaboracion_actual["contenido"].append(linea.strip())

    if elaboracion_actual is not None:
        elaboraciones.append(elaboracion_actual)

    return elaboraciones


def mostrar_elaboraciones_detectadas(elaboraciones):
    print("\n========== ELABORACIONES DETECTADAS ==========")
    print("Criterio usado: títulos en MAYÚSCULAS.\n")

    for numero, elaboracion in enumerate(elaboraciones, start=1):
        print(f"{numero}. {elaboracion['nombre']}")
        print(f"   Líneas detectadas: {len(elaboracion['contenido'])}")

    print()


def guardar_elaboraciones(elaboraciones, restaurante_id=1):
    conexion = conectar()
    cursor = conexion.cursor()

    contador = 0
    omitidas = 0

    for elaboracion in elaboraciones:
        nombre = elaboracion["nombre"].strip()
        contenido = "\n".join(elaboracion["contenido"]).strip()

        if not nombre:
            continue

        cursor.execute("""
            SELECT id
            FROM elaboraciones
            WHERE restaurante_id = ?
            AND LOWER(nombre) = LOWER(?)
            LIMIT 1
        """, (restaurante_id, nombre))

        existe = cursor.fetchone()

        if existe:
            omitidas += 1
            continue

        cursor.execute("""
            INSERT INTO elaboraciones
            (
                restaurante_id,
                nombre,
                elaboracion,
                activo
            )
            VALUES (?, ?, ?, ?)
        """, (
            restaurante_id,
            nombre,
            contenido,
            1,
        ))

        contador += 1

    conexion.commit()
    conexion.close()

    print(f"\n✅ Elaboraciones guardadas: {contador}")
    print(f"ℹ️ Elaboraciones omitidas por duplicado: {omitidas}\n")


def importar_recetas_desde_word():
    restaurante_id = asegurar_restaurante_demo()

    print("\nPega la ruta completa del archivo .docx.")
    print("Ejemplo: C:\\Users\\ferra\\OneDrive\\Documentos\\Recetas Ferran.docx")

    ruta = input("\nRuta del archivo Word: ").strip().replace('"', "")

    if not ruta:
        print("\nNo has indicado ninguna ruta.\n")
        return

    ruta_archivo = Path(ruta)

    if not ruta_archivo.exists():
        print("\nNo he encontrado ese archivo.\n")
        return

    if ruta_archivo.suffix.lower() != ".docx":
        print("\nDe momento solo acepto archivos .docx\n")
        return

    try:
        lineas = leer_docx(ruta_archivo)
    except RuntimeError as error:
        print(f"\n{error}\n")
        return

    elaboraciones = detectar_elaboraciones(lineas)

    if not elaboraciones:
        print("\nNo he detectado elaboraciones.\n")
        return

    mostrar_elaboraciones_detectadas(elaboraciones)

    confirmar = input("¿Quieres guardar estas elaboraciones? (s/n): ").lower().strip()

    if confirmar != "s":
        print("\nImportación cancelada.\n")
        return

    guardar_elaboraciones(elaboraciones, restaurante_id)
