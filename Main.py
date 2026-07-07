import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

sys.path.insert(0, str(BASE_DIR / "CORE"))
sys.path.insert(0, str(BASE_DIR / "MODULOS"))
sys.path.insert(0, str(BASE_DIR / "IA"))
sys.path.insert(0, str(BASE_DIR / "IMPORTADORES"))
sys.path.insert(0, str(BASE_DIR / "SERVICIOS"))
sys.path.insert(0, str(BASE_DIR / "Legacy"))
sys.path.insert(0, str(BASE_DIR / "MODELOS"))

from database import crear_base_datos

from importador_excel import (
    importar_articulos_desde_excel,
    importar_menus_desde_excel,
)

from motor import cargar_restaurante

from articulos import (
    mostrar_articulo,
    mostrar_todos_los_articulos,
)

from menus import mostrar_menus
from eventos import menu_eventos
from dashboard import dashboard_cocina, dashboard_rentabilidad
from pruebas_ingesta import probar_ingesta_texto
from recetas import menu_recetas
from produccion_disponible import menu_produccion_disponible
from planificacion import menu_planificacion
from ordenes_produccion import menu_ordenes_produccion
from importadores_menu import menu_importadores
from stock import menu_stock
from costes import menu_costes
from compras import menu_compras
from produccion_inteligente import menu_produccion_inteligente
from asistente import conversar_con_host_ai
from fichas import menu_fichas_tecnicas


crear_base_datos()
importar_articulos_desde_excel()
importar_menus_desde_excel()

motor = cargar_restaurante()
restaurante_id = motor.get("restaurante_id", 1)


while True:
    print("\n======================================")
    print("             HOST AI 2.1 - Sprint 5.7")
    print("======================================")
    print(f"📦 Artículos cargados : {len(motor['articulos'])}")
    print(f"🏢 Proveedores        : {len(motor['proveedores'])}")
    print(f"🍽 Menús              : {motor['menus']}")
    print("======================================")

    print("1. Dashboard Cocina")
    print("2. Dashboard Rentabilidad")
    print("3. Artículos")
    print("4. Menús")
    print("5. Eventos")
    print("6. Asistente IA")
    print("7. Probar ingesta")
    print("8. Recetas / Elaboraciones")
    print("9. Producción Disponible")
    print("10. Planificación / Personal")
    print("11. Órdenes de Producción 2.0")
    print("12. Importar documentos")
    print("13. Stock / Mercancía")
    print("14. Costes / Rentabilidad")
    print("15. Compras / Pedidos")
    print("16. Producción Inteligente")
    print("17. Fichas Técnicas Host AI")
    print("0. Salir")

    opcion = input("\n¿Qué quieres hacer? ")

    if opcion == "1":
        dashboard_cocina(restaurante_id)

    elif opcion == "2":
        dashboard_rentabilidad(restaurante_id)

    elif opcion == "3":
        while True:
            print("\n========== ARTÍCULOS ==========")
            print("1. Buscar artículo")
            print("2. Añadir artículo (desactivado)")
            print("3. Modificar artículo (desactivado)")
            print("4. Eliminar artículo (desactivado)")
            print("5. Mostrar todos")
            print("0. Volver")

            opcion_articulos = input("\n¿Qué quieres hacer? ")

            if opcion_articulos == "1":
                mostrar_articulo()
            elif opcion_articulos == "5":
                mostrar_todos_los_articulos()
            elif opcion_articulos == "0":
                break
            else:
                print("\n⚠️ Función todavía no disponible.")

    elif opcion == "4":
        mostrar_menus()

    elif opcion == "5":
        menu_eventos()

    elif opcion == "6":
        conversar_con_host_ai(motor)

    elif opcion == "7":
        probar_ingesta_texto()

    elif opcion == "8":
        menu_recetas()

    elif opcion == "9":
        menu_produccion_disponible(restaurante_id)

    elif opcion == "10":
        menu_planificacion(restaurante_id)

    elif opcion == "11":
        menu_ordenes_produccion(restaurante_id)

    elif opcion == "12":
        menu_importadores(restaurante_id)

    elif opcion == "13":
        menu_stock(restaurante_id)

    elif opcion == "14":
        menu_costes(restaurante_id)

    elif opcion == "15":
        menu_compras(restaurante_id)

    elif opcion == "16":
        menu_produccion_inteligente()

    elif opcion == "17":
        menu_fichas_tecnicas(restaurante_id)

    elif opcion == "0":
        print("\nHost AI:")
        print("Hasta luego 👨‍🍳")
        break

    else:
        print("\nHost AI:")
        print("Todavía no sé hacer eso.")
