from ingesta import (
    procesar_texto,
    mostrar_resultado_ingesta,
)


def probar_ingesta_texto():
    print("\n========== PRUEBA INGESTA ==========")

    texto = input("\nPega un texto de prueba: ")

    resultado = procesar_texto(texto)

    mostrar_resultado_ingesta(resultado)