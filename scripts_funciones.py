import zipfile
import shutil
import io
from PIL import Image
import csv
import os
import pandas as pd
from bs4 import BeautifulSoup
import requests
import numpy as np
import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def obtener_todos_los_enlaces(url_1, url_2, usuario, password):
    enlaces = []

    # configurar el controlador de Brave
    brave_path = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
    brave_driver_path = "C:\\Users\\kryst\\chromedriver_win32\\chromedriver.exe"
    options = webdriver.ChromeOptions()
    options.binary_location = brave_path
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-infobars')
    options.add_argument('--incognito=false')
    driver = webdriver.Chrome(
    options=options, executable_path=brave_driver_path)

# iniciar sesión
    driver.get(url_1)
    username = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="username"]')))
    password_1 = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="password"]')))
    username.clear()
    password_1.clear()
    username.send_keys(usuario)
    password_1.send_keys(password)
    time.sleep(7)
    #button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.AnimatedForm[type="submit"]')))
    #button.click()  # Hace clic en el botón
    #* button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.AnimatedForm__submitButton[type="submit"]')))

    # guardar enlaces en un archivo CSV
    if not os.path.exists("resultados"):
        os.makedirs("resultados")

    # obtener los enlaces guardados del usuario
    driver.get(url_2)
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    for link in soup.findAll("a"):
        data = link.get("href")
        if data and "https" in data:
            if data.endswith(",False"):
                data = data[:-6]
            enlaces.append(data)

    # guardar enlaces en un archivo CSV
    if not os.path.exists("resultados"):
        os.makedirs("resultados")
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
            'https://www.redditinc.com/policies/privacy-policy',
            'https://www.redditinc.com/policies/content-policy',
            'https://www.redditinc.com/policies/moderator-guidelines',
            'https://ads.reddit.com?utm_source=d2x_consumer&utm_name=top_nav_cta',
            'https://www.reddit.com/chat']))]

    # Eliminar ",False" del final de los enlaces
    for i in range(len(rows)):
        rows[i][0] = rows[i][0].rstrip(',False')

    with open(ruta_csv, 'w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerows(rows)

    return print("Enlaces filtrados y guardados en el archivo", ruta_csv)

def eliminar_enlaces_duplicados(ruta_archivo):
    # Abre el archivo CSV y lee las filas
    with open(ruta_archivo, newline='', encoding='utf-8') as archivo_csv:
        lector_csv = csv.reader(archivo_csv)
        enlaces = [fila[0] for fila in lector_csv]

    # Elimina los duplicados de la lista de enlaces
    enlaces_unicos = list(set(enlaces))

    # Sobrescribe el archivo original con los enlaces únicos
    with open(ruta_archivo, 'w', newline='', encoding='utf-8') as archivo_csv:
        escritor_csv = csv.writer(archivo_csv)
        for enlace in enlaces_unicos:
            escritor_csv.writerow([enlace])
    return print("Quitado los enlaces duplicados")


def separa_enlaces_videos(ruta_csv):
    # Crea un objeto DataFrame para leer el archivo CSV
    df = pd.read_csv(ruta_csv, header=None, names=["enlace"], delimiter=",")

    # Crea una nueva columna en el DataFrame para marcar los enlaces que comienzan con "https:/example/"
    df["is_example"] = df["enlace"].str.startswith(("https://www.redgifs.com/", "https://www.reddit.com/gallery/"))

    # Filtra el DataFrame para seleccionar solo las filas que tienen el valor False en la columna "is_example"
    df_filtered = df[df["is_example"] == False]

    # Guarda los enlaces filtrados en un nuevo archivo CSV llamado "links_separados.csv" dentro de la carpeta "resultados"
    df_example = df[df["is_example"] == True]
    df_example.to_csv("resultados/links_separados.csv", index=False)

    # Sobrescribe el archivo original con los enlaces filtrados
    df_filtered.to_csv(ruta_csv, index=False, header=False)

    return print("Enlaces que no se pueden descargar, separados y guardados en el archivo", ruta_csv)

def descargar_imagenes_desde_csv(ruta_csv, nombre_base='imagen', numero_inicial=1, carpeta_resultados='resultados'):
    # Crear carpeta para guardar las imágenes
    carpeta_imagenes = os.path.join('resultados', 'imagenes')
    if not os.path.exists(carpeta_imagenes):
        os.makedirs(carpeta_imagenes)

    carpeta_resultados_imagenes = os.path.join(
        carpeta_imagenes, carpeta_resultados)
    if not os.path.exists(carpeta_resultados_imagenes):
        os.makedirs(carpeta_resultados_imagenes)

    ruta_imagenes = os.path.join('resultados', 'imagenes', carpeta_resultados)

    contador = numero_inicial
    with open(ruta_csv, 'r') as file, open(os.path.join(carpeta_resultados_imagenes, 'links_separados.csv'), 'w', newline='') as links_file:
        csv_reader = csv.reader(file)
        csv_writer = csv.writer(links_file)
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
                    filepath = os.path.join(
                        carpeta_resultados_imagenes, filename)
                    with open(filepath, 'wb') as image_file:
                        image_file.write(response.content)
                    contador += 1
                except:
                    # si la imagen no se puede cargar, imprimimos un mensaje de error y continuamos con el siguiente archivo
                    print(f"Error al descargar la imagen: {row[0]}")
                    csv_writer.writerow([row[0]])
                    continue
    print(f"Descarga completada de las imágenes del archivo: {ruta_csv}")


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

        # Comprimir archivos enlaces.csv y links_separados.csv
        if os.path.exists('resultados/enlaces.csv'):
            zipf.write('resultados/enlaces.csv')
        if os.path.exists('resultados/links_separados.csv'):
            zipf.write('resultados/links_separados.csv')

    print('Carpetas comprimidas exitosamente')

def retirar_archivos (nombre_carpeta_1 = None, nombre_carpeta_2 = None):
    contador = 0
    if nombre_carpeta_1 != None:
        shutil.rmtree("resultados/imagenes/" + nombre_carpeta_1)
        contador += 1

    if nombre_carpeta_2 != None:
        shutil.rmtree("resultados/media/" + nombre_carpeta_2)
        contador += 1
    
    ruta_enlaces = os.path.join("resultados", "enlaces.csv")
    ruta_links = os.path.join("resultados", "links_separados.csv")

    if os.path.exists(ruta_enlaces):
        os.remove(ruta_enlaces)

    if os.path.exists(ruta_links):
        os.remove(ruta_links)

    if contador != 2:
        return print("Carpeta retirada")
    else:
        return print("Carpetas retiradas")

def corregir_enlaces_csv(ruta_csv):
    with open(ruta_csv, 'r') as file:
        csv_reader = csv.reader(file)
        rows = []
        for row in csv_reader:
            if row[0].endswith(',False'):
                row[0] = row[0][:-6]
            rows.append(row)

    with open(ruta_csv, 'w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerows(rows)

    nombre_archivo = os.path.basename(ruta_csv)
    print(f"Enlaces corregidos y guardados en el archivo {nombre_archivo}")

