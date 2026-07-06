from repositorio import (
    obtener_articulos,
    obtener_proveedores,
    contar_menus,
)


def cargar_restaurante(restaurante_id=1):
    print("\n======================================")
    print("        CARGANDO HOST AI")
    print("======================================")

    articulos = obtener_articulos(restaurante_id)
    proveedores = obtener_proveedores(restaurante_id)
    total_menus = contar_menus(restaurante_id)

    motor = {
        "restaurante_id": restaurante_id,
        "articulos": articulos,
        "proveedores": proveedores,
        "menus": total_menus,
        "hojas_escandallos": [],
    }

    print("\nMotor de Cocina preparado.")
    print("--------------------------------------")
    print(f"Artículos cargados  : {len(articulos)}")
    print(f"Proveedores         : {len(proveedores)}")
    print(f"Menús               : {total_menus}")
    print("--------------------------------------")

    return motor
