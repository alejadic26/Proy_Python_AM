import requests # modulo para hacer solicitudes http
from bs4 import BeautifulSoup #para anañisar documentos html
import time
import pandas as pd #para manejo de los datos de los dataframe


#Decorador para medir tiempo de ejecución
def medir_tiempo(func):
    def wrapper(*args, **kwargs):
        inicio=time.time()
        resultado=func(*args, **kwargs)
        fin=time.time()
        print(f"Tiempo de ejecucion de {func.__name__}: {fin-inicio:.4f} segundos")
        return resultado
    return wrapper

#Fncion para realizar el web scrappinf
@medir_tiempo
def obtener_datos_productos(url):
    response=requests.get(url)
    soup=BeautifulSoup(response.text,"html.parser")
    productos=[]

    #Adaptar los selectores a la estructura del sitio a scrapear
    items=soup.select(".card")

    for item in items:
        brand_element=item.select_one(".listing-card__brand")
        model_element=item.select_one(".listing-card__model")
        year_element=item.select_one(".listing-card__year")
        km_element=item.select_one(".listing-card__km")
        city_element=item.select_one(".listing-card__city")
        price_element=item.select_one(".listing-card__price-value")
       
        #Controlar que ambos elementos existan ants de acceder a su texto
        if brand_element and model_element and year_element and km_element and city_element and price_element:
            brand=brand_element.get_text(strip=True)
            model=model_element.get_text(strip=True)
            year=year_element.get_text(strip=True)
            km=km_element.get_text(strip=True)
            city=city_element.get_text(strip=True)
            price=price_element["content"]
            productos.append((brand, model,year,km,city, price))


        #control de flujo del for
        if not brand_element or model_element or year_element or km_element or city_element or price_element:
            continue
    #time.sleep(1)
    return productos

#Funcion para obtener datos de todas las páginas
@medir_tiempo
def obtener_datos_todas_paginas(base_url):
    productos=[]
    page=1
    while True:
        url=f"{base_url}usado?pidx={page}"
        nuevos_productos=obtener_datos_productos(url)
        if not nuevos_productos:
            break
        productos.extend(nuevos_productos)
        page+=1
    return productos

#Funcion para procesar datos
@medir_tiempo
def procesar_datos(productos):
    datos_procesados=[]
    for marca, modelo, anio, km, ciudad, precio in productos:
        try:
            anio=int(anio)
            km1=km[0:len(km)-2]
            km=int(km1)
            ciudad=ciudad[0:len(ciudad)-2]
            anio=int(anio)
            datos_procesados.append({"Marca":marca,"Modelo":modelo,"Anio":anio,"Kilometraje":km,"Ciudad":ciudad,"Precio":precio})
        except ValueError:
            continue
        
    return datos_procesados

#Fucion para escribir los datos en un .txt
@medir_tiempo
def guardar_datos_en_csv(datos,archivo):
    df=pd.DataFrame(datos)
    df.to_csv(archivo, index=False, encoding="utf-8")
    return df

base_url="https://www.autocosmos.com.ec/auto/"
productos=obtener_datos_todas_paginas(base_url)
datos_procesados=procesar_datos(productos)
df=guardar_datos_en_csv(datos_procesados,'..\..\data\\raw\productosVehiculos.csv')


