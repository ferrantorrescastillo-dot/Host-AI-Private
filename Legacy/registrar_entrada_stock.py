import pandas as pd

archivo = "articulos.xlsx"

df = pd.read_excel(archivo)

articulo = input("¿Qué artículo ha llegado? ")
cantidad = float(input("¿Qué cantidad ha llegado? "))

encontrado = False

for i, fila in df.iterrows():
    if str(fila["Articulo"]).lower() == articulo.lower():
        stock_actual = fila["Stock"]

        if pd.isna(stock_actual):
            stock_actual = 0

        df.at[i, "Stock"] = stock_actual + cantidad
        encontrado = True
        print("Stock actualizado correctamente.")
        print("Nuevo stock:", df.at[i, "Stock"])
        break

if not encontrado:
    print("No he encontrado ese artículo en el listado.")

df.to_excel(archivo, index=False)