import csv
import requests
import os
import pandas as pd
from bs4 import BeautifulSoup
import requests
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def obtener_todos_los_enlaces(url):
    enlaces = []

    # configurar el controlador de Brave
    brave_path = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
    brave_driver_path = "D:\chromedriver_win32\chromedriver.exe"  # reemplaza la ruta con la ruta a tu archivo BraveDriver.exe
    options = webdriver.ChromeOptions()
    options.binary_location = brave_path
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-infobars')
    options.add_argument('--incognito=false')
    driver = webdriver.Chrome(options=options, executable_path=brave_driver_path)

    driver.get(url)
    
    # desplazarse hasta el final de la página
    while True:
        last_height = driver.execute_script("return document.body.scrollHeight")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # extraer todos los enlaces de la página
    soup = BeautifulSoup(driver.page_source, "html.parser")
    for link in soup.findAll("a"):
        data = link.get("href")
        if data and "https" in data:
            enlaces.append(data)

    # guardar enlaces en un archivo CSV
    np.savetxt("resultados/enlaces.csv", enlaces, delimiter=',', fmt="%s")
    
    # cerrar el navegador
    driver.close()

    return print("Archivo CSV de enlaces creado")
    

def obtener_enlaces(url):
    enlaces = []

    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")

    for link in soup.findAll("a"):
        data = link.get("href")
        if "https" in data:
            enlaces.append(data)

    np.savetxt("resultados/enlaces.csv", enlaces, delimiter=',', fmt="%s")
    return print("Archivo CSV de enlaces creado")


def filtrar_enlaces(ruta_csv):
    with open(ruta_csv, 'r') as file:
        csv_reader = csv.reader(file)
        rows = [row for row in csv_reader if not (row[0].startswith('https://www.reddit.com/login') or any(link in row[0] for link in ['https://www.redditinc.com/policies/user-agreement',
                                                'https://www.redditinc.com/policies/privacy-policy', 'https://www.redditinc.com/policies/content-policy', 'https://www.redditinc.com/policies/moderator-guidelines']))]

    with open(ruta_csv, 'w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerows(rows)

    return print("Enlaces filtrados y guardados en el archivo", ruta_csv)


from PIL import Image
import io

def descargar_imagenes_desde_csv(ruta_csv, nombre_base='imagen', numero_inicial=1, carpeta_resultados='resultados'):
    # Crear carpeta para guardar las imágenes
    carpeta_imagenes = os.path.join('resultados' ,'imagenes')
    if not os.path.exists(carpeta_imagenes):
        os.makedirs(carpeta_imagenes)
        
    carpeta_resultados_imagenes = os.path.join(carpeta_imagenes, carpeta_resultados)
    if not os.path.exists(carpeta_resultados_imagenes):
        os.makedirs(carpeta_resultados_imagenes)
    
    ruta_imagenes = os.path.join('resultados', 'imagenes', carpeta_resultados)

    contador = numero_inicial
    with open(ruta_csv, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for row in csv_reader:
            url_extension = os.path.splitext(row[0])[1]
            if url_extension.lower() in ['.png', '.jpg', '']:
                response = requests.get(row[0])
                try:
                    image = Image.open(io.BytesIO(response.content))
                    # si la imagen se puede cargar correctamente, la guardamos
                    if url_extension.lower() == '.png':
                        extension = '.jpg'
                    else:
                        extension = '.jpg'
                    filename = f"{nombre_base}_{contador:03d}{extension}"
                    filepath = os.path.join(carpeta_resultados_imagenes, filename)
                    with open(filepath, 'wb') as image_file:
                        image_file.write(response.content)
                    contador += 1
                except:
                    # si la imagen no se puede cargar, ignoramos este archivo y continuamos con el siguiente
                    print(f"Error al descargar la imagen: {row[0]}")
                    continue
    print(f"Descarga completada de las imágenes del archivo: {ruta_csv}"), ruta_imagenes

def descargar_videos_gifs_desde_csv(ruta_csv, nombre_carpeta='carpeta_personalizada', nombre_base='media_', numero_inicial=1):
    # Crear carpeta para guardar los videos y gifs
    if not os.path.exists('resultados/media/' + nombre_carpeta):
        os.makedirs('resultados/media/' + nombre_carpeta)

    if not os.path.exists('resultados/media/' + nombre_carpeta + '/videos'):
        os.makedirs('resultados/media/' + nombre_carpeta + '/videos')

    if not os.path.exists('resultados/media/' + nombre_carpeta + '/gifs'):
        os.makedirs('resultados/media/' + nombre_carpeta + '/gifs')

    ruta_videos = os.path.join('resultados', 'media', nombre_carpeta, 'videos')
    ruta_gifs = os.path.join('resultados', 'media', nombre_carpeta, 'gifs')

    contador_videos = numero_inicial
    contador_gifs = numero_inicial
    with open(ruta_csv, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for row in csv_reader:
            url = row[0]
            if url.startswith('https://preview.redd.it/') or url.startswith('https://www.redgifs.com/'):
                response = requests.get(url)
                content_type = response.headers.get('content-type')
                if content_type.startswith('video/'):
                    filename = 'resultados/media/' + nombre_carpeta + '/videos/' + \
                        nombre_base + str(contador_videos)
                    if not filename.lower().endswith('.mp4'):
                        filename += '.mp4'
                    with open(filename, 'wb') as video_file:
                        video_file.write(response.content)
                    contador_videos += 1
                elif content_type.startswith('image/gif'):
                    filename = 'resultados/media/' + nombre_carpeta + '/gifs/' + \
                        nombre_base + str(contador_gifs)
                    if not filename.lower().endswith('.gif'):
                        filename += '.gif'
                    with open(filename, 'wb') as gif_file:
                        gif_file.write(response.content)
                    contador_gifs += 1
    return ruta_videos, ruta_gifs



import shutil
import zipfile

def comprimir_carpeta(nombre_carpeta_comprimida, ruta_carpeta_imagenes=None, ruta_carpeta_videos=None, ruta_carpeta_gifs=None):
    # Crear carpeta para guardar el archivo comprimido
    if not os.path.exists('resultados/' + nombre_carpeta_comprimida):
        os.makedirs('resultados/' + nombre_carpeta_comprimida)
    
    # Comprimir carpetas
    with zipfile.ZipFile('resultados/' + nombre_carpeta_comprimida + '/' + nombre_carpeta_comprimida + '.zip', mode='w', compression=zipfile.ZIP_DEFLATED) as zipf:
        if ruta_carpeta_imagenes and os.path.exists(ruta_carpeta_imagenes):
            for root, dirs, files in os.walk(ruta_carpeta_imagenes):
                for file in files:
                    zipf.write(os.path.join(root, file))
        
        if ruta_carpeta_videos and os.path.exists(ruta_carpeta_videos):
            for root, dirs, files in os.walk(ruta_carpeta_videos):
                for file in files:
                    zipf.write(os.path.join(root, file))
        
        if ruta_carpeta_gifs and os.path.exists(ruta_carpeta_gifs):
            for root, dirs, files in os.walk(ruta_carpeta_gifs):
                for file in files:
                    zipf.write(os.path.join(root, file))
    
    print('Carpetas comprimidas exitosamente')
