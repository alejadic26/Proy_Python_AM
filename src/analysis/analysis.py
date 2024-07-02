import pandas as pd
import os
from pathlib import Path
from ..decoradores.decorators import timeit, logit

@logit
@timeit
def carga_data(data_path):
    if data_path.endswith(".csv"):
        df=pd.read_csv(data_path)
    elif data_path.endswith(".xlsx"):
        df=pd.read_excel(data_path)
    else:
        raise ValueError("Formato del archivo no es correcto")
    print("Datos cargados correctamente")
    return df #retorna dataframe con datos cargados

@logit
@timeit
def limpiar_data(df):
    df["Kilometraje"]=df["Kilometraje"].astype(int)
    print("Datos limpiados correctamente")
    return df

@logit
@timeit
def analisis_datos(df):
    print("Analisis Básico de datos: ")
    print(df.describe())
    print("\n Top 5 de los Vehículos con los precios más bajos:")
    precios_bajos=df.nsmallest(5,"Precio")
    print(precios_bajos)
    print("\n Top 5 de los Vehículos con el kilometraje más bajos:")
    km_bajos=df.nsmallest(10,"Kilometraje")
    print(km_bajos)
    print("\n *************Vehículos por Ciudad***************")
    ciudad = df["Ciudad"].value_counts()
    print(ciudad)
    print("\n Resumen de disponibilidad de vehículos por marca, modelo y más actual:")
    resumen_marca=df.groupby("Marca").agg(
        Vehiculo_por_Marcas=("Marca","count"),
        Modelos_por_Marca=("Modelo","nunique"),
        Anio_Vehiculo=("Anio","max")
    ).reset_index().sort_values("Vehiculo_por_Marcas",ascending=False)
    print(resumen_marca)
    
    return resumen_marca


@logit
@timeit
def guardar_datos_esta(df,ruta_salida):
    if ruta_salida.endswith(".csv"):
        df.to_csv(ruta_salida,index=False)
    elif ruta_salida.endswith(".xlsx"):
        df.to_excel(ruta_salida,index=False)
    else:
        raise ValueError("Error de formato de archivos")
    print(f"Datos depurados guardados en: {ruta_salida}")

def guardar_datos_excel(df,ruta_salida2):
    #Guarda datos procesados en un archivo de excel
    df.to_csv(ruta_salida2,index=False)

def generar_reporte(data_path,ruta_salida2):
    #Tomalos datod de entrada, genera el reporte y lo guarda

    #lee los datos
    df=carga_data(data_path)

    #Procesar datos paa crear resumen de ventas
    resumen_marca=analisis_datos(df)
    
    #Guardar el reporte en un archivo excel nuevo
    guardar_datos_excel(resumen_marca,ruta_salida2)

if __name__ == "__main__":
    data_path='./data/raw/productosVehiculos.csv'
    ruta_salida="./data/process/datos_limpios.csv"
    ruta_salida2="./data/process/resumen_analisis.csv"
    
    df=carga_data(data_path)
    df=limpiar_data(df)
    analisis_datos(df)
    guardar_datos_esta(df,ruta_salida)
    generar_reporte(data_path,ruta_salida2)

