# import mysql.connector
# import pandas as pd
# import re
# import matplotlib.pyplot as plt
# import seaborn as sns
# import statsmodels.api as sm
# from sklearn.linear_model import LinearRegression
# import numpy as np
# from scipy import stats

# # Conectar con MySQL
# conn = mysql.connector.connect(
#     host="localhost",
#     user="root",  # Cambia esto si usas otro usuario
#     password="Juniordg712#",  # Agrega tu contraseña si la tienes
#     database="VentasDB",
#     port=3306
# )
# cursor = conn.cursor()

# # Datos con errores
# ventas_data = """enero,100
# febrero,-50
# marzo,120
# abril,200
# mayo,180
# junio,abc
# julio,250
# agosto,###
# septiembre,280
# octubre,350
# noviembre,
# diciembre,320
# enero,280
# febrero,350
# marzo,320
# abril,400
# mayo,380
# junio,420
# julio,390""".split("\n")

# # Procesar datos
# ventas_limpias = []

# for linea in ventas_data:
#     try:
#         mes, venta = linea.split(",")
#         if not re.match(r'^\d+$', venta):  # Filtrar valores no numéricos
#             continue
#         venta = int(venta)
#         if venta < 0:  # Filtrar valores negativos
#             continue
#         ventas_limpias.append((mes, venta))
#     except ValueError:
#         continue

# # Insertar en MySQL
# cursor.executemany("INSERT INTO ventas_mensuales (mes, ventas) VALUES (%s, %s)", ventas_limpias)
# conn.commit()

# # Guardar en Excel
# df = pd.DataFrame(ventas_limpias, columns=["Mes", "Ventas"])
# df.to_excel("ventas.xlsx", index=False)

# print("Datos guardados en MySQL y Excel correctamente.")

# # Cargar datos en Pandas para análisis
# df["Ventas Acumuladas"] = df["Ventas"].cumsum()

# # Graficar ventas mensuales
# plt.figure(figsize=(10, 5))
# sns.lineplot(x=df["Mes"], y=df["Ventas"], marker="o", label="Ventas")
# sns.lineplot(x=df["Mes"], y=df["Ventas Acumuladas"], marker="o", label="Crecimiento Acumulado")
# plt.xticks(rotation=45)
# plt.title("Ventas Mensuales y Crecimiento Acumulado")
# plt.legend()
# plt.show()

# # Descomposición de la serie temporal
# ts = df.set_index("Mes")["Ventas"]
# decomposed = sm.tsa.seasonal_decompose(ts, model="additive", period=6)
# decomposed.plot()
# plt.show()

# # Predicción con regresión lineal
# X = np.arange(len(df)).reshape(-1, 1)
# y = df["Ventas"]
# model = LinearRegression()
# model.fit(X, y)
# y_pred = model.predict(X)

# plt.figure(figsize=(10, 5))
# plt.scatter(X, y, color="blue", label="Ventas reales")
# plt.plot(X, y_pred, color="red", label="Predicción")
# plt.title("Predicción de Ventas")
# plt.legend()
# plt.show()

# # Análisis de Autocorrelación
# plt.figure(figsize=(10, 5))
# sm.graphics.tsa.plot_acf(df["Ventas"], lags=12)
# plt.title("Autocorrelación de Ventas")
# plt.show()

# # Prueba Estadística: ANOVA para diferencias entre meses
# f_stat, p_value = stats.f_oneway(*[df[df["Mes"] == mes]["Ventas"] for mes in df["Mes"].unique()])
# print(f"Prueba ANOVA - F-Statistic: {f_stat}, P-Value: {p_value}")
# if p_value < 0.05:
#     print("Existe una diferencia significativa entre los meses.")
# else:
#     print("No hay diferencias significativas entre los meses.")

# # Cerrar conexión
# cursor.close()
# conn.close()


import mysql.connector
import pandas as pd
import re
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression
import numpy as np
from scipy import stats

# Conectar con MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",  # Cambia esto si usas otro usuario
    password="Juniordg712#",  # Agrega tu contraseña si la tienes
    database="VentasDB",
    port=3306
)
cursor = conn.cursor()

# Datos con errores
ventas_data = """enero,100
febrero,-50
marzo,120
abril,200
mayo,180
junio,abc
julio,250
agosto,###
septiembre,280
octubre,350
noviembre,
diciembre,320
enero,280
febrero,350
marzo,320
abril,400
mayo,380
junio,420
julio,390""".split("\n")

# Procesar datos
ventas_limpias = []

for linea in ventas_data:
    try:
        mes, venta = linea.split(",")
        if not re.match(r'^\d+$', venta):  # Filtrar valores no numéricos
            continue
        venta = int(venta)
        if venta < 0:  # Filtrar valores negativos
            continue
        ventas_limpias.append((mes, venta))
    except ValueError:
        continue

# Insertar en MySQL
cursor.executemany("INSERT INTO ventas_mensuales (mes, ventas) VALUES (%s, %s)", ventas_limpias)
conn.commit()

# Guardar en Excel
df = pd.DataFrame(ventas_limpias, columns=["Mes", "Ventas"])
df.to_excel("ventas.xlsx", index=False)

print("Datos guardados en MySQL y Excel correctamente.")

# Cargar datos en Pandas para análisis
df["Ventas Acumuladas"] = df["Ventas"].cumsum()

# Graficar ventas mensuales
plt.figure(figsize=(10, 5))
sns.lineplot(x=df["Mes"], y=df["Ventas"], marker="o", label="Ventas")
sns.lineplot(x=df["Mes"], y=df["Ventas Acumuladas"], marker="o", label="Crecimiento Acumulado")
plt.xticks(rotation=45)
plt.title("Ventas Mensuales y Crecimiento Acumulado")
plt.legend()
plt.show()

# Descomposición de la serie temporal si hay suficientes datos
if len(df) >= 12:
    ts = df.set_index("Mes")["Ventas"]
    decomposed = sm.tsa.seasonal_decompose(ts, model="additive", period=min(6, len(df)//2))
    decomposed.plot()
    plt.show()
else:
    print("No hay suficientes datos para la descomposición de la serie temporal.")

# Predicción con regresión lineal
X = np.arange(len(df)).reshape(-1, 1)
y = df["Ventas"]
model = LinearRegression()
model.fit(X, y)
y_pred = model.predict(X)

plt.figure(figsize=(10, 5))
plt.scatter(X, y, color="blue", label="Ventas reales")
plt.plot(X, y_pred, color="red", label="Predicción")
plt.title("Predicción de Ventas")
plt.legend()
plt.show()

# Análisis de Autocorrelación
plt.figure(figsize=(10, 5))
sm.graphics.tsa.plot_acf(df["Ventas"], lags=min(6, len(df)//2))
plt.title("Autocorrelación de Ventas")
plt.show()

# Prueba Estadística: ANOVA para diferencias entre meses
f_stat, p_value = stats.f_oneway(*[df[df["Mes"] == mes]["Ventas"] for mes in df["Mes"].unique()])
print(f"Prueba ANOVA - F-Statistic: {f_stat}, P-Value: {p_value}")
if p_value < 0.05:
    print("Existe una diferencia significativa entre los meses.")
else:
    print("No hay diferencias significativas entre los meses.")

# Menú de consultas con switch-case
while True:
    print("\nSeleccione una consulta:")
    print("1. Ventas totales del último año")
    print("2. Mes con mayor ventas")
    print("3. Mes con menor ventas")
    print("4. Promedio mensual de ventas")
    print("5. Salir")
    opcion = input("Ingrese el número de la opción: ")
    
    if opcion == "1":
        cursor.execute("SELECT SUM(ventas) FROM ventas_mensuales")
        total = cursor.fetchone()[0]
        print(f"Ventas totales del último año: {total}")
    elif opcion == "2":
        cursor.execute("SELECT mes, ventas FROM ventas_mensuales WHERE ventas = (SELECT MAX(ventas) FROM ventas_mensuales)")
        mes, max_venta = cursor.fetchone()
        print(f"Mes con mayor ventas: {mes} ({max_venta})")
    elif opcion == "3":
        cursor.execute("SELECT mes, ventas FROM ventas_mensuales WHERE ventas = (SELECT MIN(ventas) FROM ventas_mensuales)")
        mes, min_venta = cursor.fetchone()
        print(f"Mes con menor ventas: {mes} ({min_venta})")
    elif opcion == "4":
        cursor.execute("SELECT AVG(ventas) FROM ventas_mensuales")
        promedio = cursor.fetchone()[0]
        print(f"Promedio mensual de ventas: {promedio:.2f}")
    elif opcion == "5":
        print("Saliendo...")
        break
    else:
        print("Opción no válida. Intente de nuevo.")

# Cerrar conexión
cursor.close()
conn.close()
