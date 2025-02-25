# Importamos las bibliotecas necesarias
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import mysql.connector
from sqlalchemy import create_engine
import pymysql

# Conexión a la base de datos MySQL
# Reemplaza con tus credenciales
def conectar_bd():
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="QWERTY0707",
        database="car_data"
    )
    return conexion

# Configurar la conexión con SQLAlchemy para pandas
def crear_engine():
    engine = create_engine('mysql+pymysql://root:QWERTY0707@localhost/car_data')
    return engine

# 1. Descarga una base de datos desde el servidor Kengle
# (Ya completado según lo mencionado)

# 2. Identificar y seleccionar una tabla principal para el análisis
# Usaremos la tabla 'table_car' que ya se mostró en la captura de pantalla

# Importar la tabla a un DataFrame de pandas
def importar_datos():
    engine = crear_engine()
    query = "SELECT * FROM table_car"
    df = pd.read_sql(query, engine)
    return df

df = importar_datos()


# 3. Clasificación de columnas en variables categóricas y numéricas
def clasificar_columnas(df):
    # Variables categóricas
    categoricas = ['Brand', 'Model', 'Fuel_Type', 'Transmission']
    
    # Variables numéricas
    numericas = ['Year', 'Engine_Size', 'Mileage', 'Doors', 'Owner_Count', 'Price']
    
    return categoricas, numericas

categoricas, numericas = clasificar_columnas(df)
print("\n3.")
print("\nVariables categóricas:", categoricas)
print("Variables numéricas:", numericas)

# 4. Estadísticas descriptivas para variables numéricas
def estadisticas_descriptivas(df, columnas_numericas):
    stats = df[columnas_numericas].describe(percentiles=[0.25, 0.5, 0.75, 0.9])
    return stats

stats_numericas = estadisticas_descriptivas(df, numericas)
print("\n4.")
print("\nEstadísticas descriptivas para variables numéricas:")
print(stats_numericas)

# 5. Generar gráficos para variables categóricas y numéricas
def generar_graficos(df, cat_cols, num_cols):
    # a. Histograma para una variable numérica (Price)
    plt.figure(figsize=(10, 6))
    sns.histplot(df['Price'], kde=True)
    plt.title('Distribución de Precios de Vehículos')
    plt.xlabel('Precio')
    plt.ylabel('Frecuencia')
    plt.savefig('histograma_precios.png')
    plt.close()
    
    # b. Gráfico de barras para una variable categórica (Brand)
    plt.figure(figsize=(12, 6))
    sns.countplot(y='Brand', data=df, order=df['Brand'].value_counts().index)
    plt.title('Frecuencia de Marcas de Vehículos')
    plt.xlabel('Cantidad')
    plt.ylabel('Marca')
    plt.savefig('barras_marcas.png')
    plt.close()
    
    # Gráfico adicional: Relación entre Año y Precio
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='Year', y='Price', data=df, hue='Fuel_Type')
    plt.title('Relación entre Año y Precio por Tipo de Combustible')
    plt.savefig('scatter_año_precio.png')
    plt.close()
    print("\n5.")
    print("Gráficas guardadas como imágenes")

generar_graficos(df, categoricas, numericas)

# 6. Examinar y limpiar los datos
def limpiar_datos(df):
    # a. Valores nulos
    print("\n6.1.")
    print("\nValores nulos por columna:")
    print(df.isnull().sum())
    
    # Rellenar valores nulos si existen
    if df.isnull().any().any():
        # Rellenar numéricas con la mediana
        for col in numericas:
            if df[col].isnull().sum() > 0:
                df[col] = df[col].fillna(df[col].median())
        
        # # Rellenar categóricas con el modo
        # for col in categoricas:
        #     if df[col].isnull().sum() > 0:
        #         df[col] = df[col].fillna(df[col].mode()[0])
    
    # b. Valores duplicados
    duplicados = df.duplicated().sum()
    print(f"Número de filas duplicadas: {duplicados}")
    if duplicados > 0:
        df = df.drop_duplicates()
    
    # c. Valores inconsistentes o fuera de rango
    # Verificar años fuera de rango (asumiendo que los coches son de 1980 a 2025)
    df.loc[df['Year'] < 1980, 'Year'] = df['Year'].median()
    df.loc[df['Year'] > 2025, 'Year'] = df['Year'].median()
    
    # Verificar valores negativos en campos que no deben tenerlos
    for col in ['Engine_Size', 'Mileage', 'Doors', 'Owner_Count', 'Price']:
        df.loc[df[col] < 0, col] = df[col].median()
    
    # Uniformidad en variables categóricas (convertir a mayúsculas)
    for col in categoricas:
        if df[col].dtype == 'object':
            df[col] = df[col].str.title()
    
    return df

df_limpio = limpiar_datos(df)

# Recalcular estadísticas después de la limpieza
stats_post_limpieza = estadisticas_descriptivas(df_limpio, numericas)
print("\n6.2.")
print("\nEstadísticas descriptivas después de la limpieza:")
print(stats_post_limpieza)

# 7 y 8. Consulta SQL y importación a DataFrame
# Esta consulta se debe ejecutar primero en MySQL Shell
# """
# -- Consulta SQL para obtener vehículos diésel o eléctricos con precio menor a 10000
# SELECT * FROM table_car 
# WHERE (Fuel_Type = 'Diesel' OR Fuel_Type = 'Electric') 
# AND Price < 10000;
# """

def consulta_sql_a_dataframe():
    conexion = conectar_bd()
    cursor = conexion.cursor(dictionary=True)
    
    # Consulta SQL
    consulta = """
    SELECT * FROM table_car 
    WHERE (Fuel_Type = 'Diesel' OR Fuel_Type = 'Electric') 
    AND Price < 10000;
    """
    
    cursor.execute(consulta)
    resultados = cursor.fetchall()
    
    cursor.close()
    conexion.close()
    
    # Convertir a DataFrame
    df_subconjunto = pd.DataFrame(resultados)
    return df_subconjunto

df_subconjunto = consulta_sql_a_dataframe()
print("\n7/8.")
print("\nSubconjunto de datos (Diésel y Eléctricos < 10000):")
print(df_subconjunto.head(10))

# 9. Comparar estadísticas del subconjunto con el conjunto completo
stats_subconjunto = estadisticas_descriptivas(df_subconjunto, numericas)
print("\n9.")
print("\nEstadísticas del subconjunto:")
print(stats_subconjunto)

print("\nComparación de medias entre conjunto completo y subconjunto:")
for col in numericas:
    print(f"{col}: Completo = {df_limpio[col].mean():.2f}, Subconjunto = {df_subconjunto[col].mean():.2f}")

# 10. Realizar consultas directamente desde Python
def consultas_python():
    engine = crear_engine()
    
    # Consulta 1: Promedio de precio por marca
    query1 = """
    SELECT Brand, AVG(Price) as Precio_Promedio
    FROM table_car
    GROUP BY Brand
    ORDER BY Precio_Promedio DESC
    LIMIT 5;
    """
    df_query1 = pd.read_sql(query1, engine)
    print("\nPromedio de precio por marca (Top 5):")
    print(df_query1)
    
    # Consulta 2: Cantidad de vehículos por tipo de combustible y transmisión
    query2 = """
    SELECT Fuel_Type, Transmission, COUNT(*) as Cantidad
    FROM table_car
    GROUP BY Fuel_Type, Transmission
    ORDER BY Cantidad DESC;
    """
    df_query2 = pd.read_sql(query2, engine)
    print("\n10.")
    print("\nCantidad de vehículos por tipo de combustible y transmisión:")
    print(df_query2)
    
    return df_query1, df_query2

df_marca_precio, df_fuel_transmission = consultas_python()

def Tabla_Antes_Cambio():
    engine = crear_engine()
    query = "SELECT * FROM table_car WHERE Brand = 'BMW'"
    df_bmw = pd.read_sql(query, engine)
    print("\nDatos de BMW antes de la actualización:")
    print(df_bmw[['Brand', 'Model', 'Price']])
    return df_bmw

Tabla_Antes_Cambio()

# 11. Actualizar registros desde Python
def actualizar_registro():
    conexion = conectar_bd()
    cursor = conexion.cursor()
    
    # Actualizar el precio de todos los vehículos BMW aumentándolo en un 5%
    update_query = """
    UPDATE table_car
    SET Price = Price * 1.05
    WHERE Brand = 'BMW';
    """
    
    cursor.execute(update_query)
    filas_afectadas = cursor.rowcount
    
    conexion.commit()
    cursor.close()
    conexion.close()
    
    print("\n11.")
    print(f"\nRegistros actualizados: {filas_afectadas} vehículos BMW con precio incrementado en 5%")
    return filas_afectadas

filas_actualizadas = actualizar_registro()

# Verificar cambios después de actualización
def verificar_actualizacion():
    engine = crear_engine()
    query = "SELECT * FROM table_car WHERE Brand = 'BMW'"
    df_bmw = pd.read_sql(query, engine)
    print("\nDatos de BMW después de la actualización:")
    print(df_bmw[['Brand', 'Model', 'Price', 'Year']])
    return df_bmw

df_bmw_actualizado = verificar_actualizacion()
