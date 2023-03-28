import os
import zipfile
import shutil
import io
import requests
from PIL import Image
import imagehash
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def obtener_todos_los_enlaces(url_1, url_2, usuario, password):
    enlaces = []

    # configurar el controlador de Brave
    brave_path = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
    brave_driver_path = "C:\\Users\\kryst\\chromedriver_win32\\chromedriver.exe"
    options = webdriver.ChromeOptions()
    options.binary_location = brave_path
    options.add_argument('--disable-extensions')
    options.add_argument('--incognito')
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
    time.sleep(8)

    # obtener los enlaces guardados del usuario
    driver.get(url_2)
    time.sleep(8)
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Hacer scroll hasta el final de la página
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        # Esperar a que se cargue la página
        time.sleep(2)
        # Obtener el nuevo alto de la página
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    soup = BeautifulSoup(driver.page_source, "html.parser")
    for link in soup.findAll("a"):
        data = link.get("href")
        if data and "https" in data:
            if data.endswith(",False"):
                data = data[:-6]
            enlaces.append(data)

    # guardar enlaces en un archivo de texto
    if not os.path.exists("resultados"):
        os.makedirs("resultados")
    with open("resultados/enlaces.txt", "w") as f:
        for enlace in enlaces:
            f.write(enlace + "\n")

    # cerrar el navegador
    driver.quit()

    return print("Archivo de texto de enlaces creado")


def obtener_enlaces(url):
    enlaces = []

    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")

    for link in soup.findAll("a"):
        data = link.get("href")
        if "https" in data:
            enlaces.append(data)

    with open("resultados/enlaces.txt", "w") as f:
        f.write('\n'.join(enlaces))

    return print("Archivo txt de enlaces creado")


def filtrar_enlaces(ruta_txt):
    with open(ruta_txt, 'r') as file:
        rows = file.read().splitlines()

    filtered_rows = [row for row in rows if not (row.startswith('https://www.reddit.com/login') or any(link in row for link in ['https://www.redditinc.com/policies/user-agreement', 'https://www.redditinc.com/policies/privacy-policy',
    'https://www.redditinc.com/policies/content-policy', 'https://www.redditinc.com/policies/moderator-guidelines',
    'https://ads.reddit.com?utm_source=d2x_consumer&utm_name=top_nav_cta', 'https://www.reddit.com/chat'
    ]))]

    with open(ruta_txt, "w") as f:
        f.write('\n'.join(filtered_rows))

    return print("Archivo de enlaces filtrado")


def corregir_enlaces_txt(ruta_txt):
    if not os.path.exists(ruta_txt):
        print(f"No se encontró el archivo en la ruta: {ruta_txt}")
        return

    with open(ruta_txt, 'r') as archivo_txt:
        lineas = archivo_txt.readlines()

    with open(ruta_txt, 'w') as archivo_txt:
        for linea in lineas:
            # quitar los caracteres de nueva línea y espacios en blanco al final de la línea
            linea = linea.rstrip()

            # si la última parte de la línea es "False", eliminar esa parte de la cadena
            if linea.endswith('False'):
                linea = linea[:-5]

            # si la última parte de la línea es una coma, eliminarla
            if linea.endswith(','):
                linea = linea[:-1]

            # escribir la línea corregida en el archivo original
            archivo_txt.write(linea + '\n')

    print(f"Archivo {ruta_txt} corregido y sobrescrito.")


def eliminar_duplicados(ruta_txt):
    with open(ruta_txt, 'r') as file:
        rows = file.read().splitlines()

    filtered_rows = list(set(rows))

    with open(ruta_txt, "w") as f:
        f.write('\n'.join(filtered_rows))

    return print("Enlaces duplicados eliminados y archivo sobrescrito")


def descargar_imagenes(ruta_txt, carpeta_resultados='resultados', nombre_base='imagen', numero_inicial=1, umbral=5, imagen_comparar=None):
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
    with open(ruta_txt, 'r') as file, open(os.path.join(carpeta_resultados_imagenes, 'links_fallidos.txt'), 'w') as links_file:
        for row in file:
            url_extension = os.path.splitext(row.strip())[1]
            if url_extension.lower() in ['.png', '.jpg', 'jpeg', '']:
                response = requests.get(row.strip())
                try:
                    image = Image.open(io.BytesIO(response.content))
                    # si la imagen se puede cargar correctamente, la guardamos
                    if url_extension.lower() == '.png':
                        extension = '.jpg'
                    else:
                        extension = '.jpg'
                    filename = f"{nombre_base}_{contador:04d}{extension}"
                    filepath = os.path.join(
                        carpeta_resultados_imagenes, filename)
                    if imagen_comparar is not None:
                        with Image.open(imagen_comparar) as img:
                            hash_img = imagehash.average_hash(img)
                            hash_descarga = imagehash.average_hash(image)
                            if hash_img - hash_descarga <= umbral:
                                print(f"La imagen {row.strip()} coincide con {imagen_comparar}, omitiendo descarga")
                                continue
                    with open(filepath, 'wb') as image_file:
                        image_file.write(response.content)
                    contador += 1
                except:
                    # si la imagen no se puede cargar, imprimimos un mensaje de error y continuamos con el siguiente archivo
                    print(f"Error al descargar la imagen: {row.strip()}")
                    links_file.write(row.strip() + '\n')
                    continue
    print(f"Descarga completada de las imágenes del archivo: {ruta_txt}")
    return ruta_imagenes


def descargar_videos_gifs(ruta_txt, nombre_carpeta='carpeta_personalizada', nombre_base='media_', numero_inicial=1):
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
    with open(ruta_txt, 'r') as file:
        for line in file:
            url = line.strip()
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


def comprimir_archivos(nombre_carpeta_comprimida, ruta_carpeta_imagenes='imagenes', ruta_carpeta_videos='videos', ruta_carpeta_gifs='gifs'):

    # Crear carpeta para guardar el archivo comprimido
    if not os.path.exists('resultados/' + nombre_carpeta_comprimida):
        os.makedirs('resultados/' + nombre_carpeta_comprimida)

    # Comprimir archivos
    with zipfile.ZipFile('resultados/' + nombre_carpeta_comprimida + '/' + nombre_carpeta_comprimida + '.zip', mode='w', compression=zipfile.ZIP_DEFLATED) as zipf:

        # Comprimir imágenes
        if os.path.exists(ruta_carpeta_imagenes):
            for root, dirs, files in os.walk(ruta_carpeta_imagenes):
                for file in files:
                    zipf.write(os.path.join(root, file), arcname=os.path.join(
                        nombre_carpeta_comprimida, 'imagenes', file))

        # Comprimir videos
        if ruta_carpeta_videos != None:
            if os.path.exists(ruta_carpeta_videos):
                for root, dirs, files in os.walk(ruta_carpeta_videos):
                    for file in files:
                        zipf.write(os.path.join(root, file), arcname=os.path.join(
                            nombre_carpeta_comprimida, 'videos', file))

        # Comprimir gifs
        if ruta_carpeta_gifs != None:
            if os.path.exists(ruta_carpeta_gifs):
                for root, dirs, files in os.walk(ruta_carpeta_gifs):
                    for file in files:
                        zipf.write(os.path.join(root, file), arcname=os.path.join(
                            nombre_carpeta_comprimida, 'gifs', file))

        # Comprimir archivos enlaces.csv y links_separados.csv
        if os.path.exists('resultados/enlaces.txt'):
            zipf.write('resultados/enlaces.txt',
                    arcname=os.path.join(nombre_carpeta_comprimida, 'enlaces.txt'))

    print(
        f'Archivo {nombre_carpeta_comprimida}.zip creado en la carpeta resultados/')


def retirar_archivos(nombre_carpeta_1=None, nombre_carpeta_2=None):
    contador = 0
    if nombre_carpeta_1 != None:
        shutil.rmtree("resultados/imagenes/" + nombre_carpeta_1)
        contador += 1

    if nombre_carpeta_2 != None:
        shutil.rmtree("resultados/media/" + nombre_carpeta_2)
        contador += 1

    ruta_enlaces = os.path.join("resultados", "enlaces.txt")

    if os.path.exists(ruta_enlaces):
        os.remove(ruta_enlaces)

    if contador != 2:
        return print("Carpeta retirada")
    else:
        return print("Carpetas retiradas")

# Privatizar módulos 
__all__ = [
    obtener_enlaces, obtener_todos_los_enlaces,
    filtrar_enlaces, eliminar_duplicados, corregir_enlaces_txt,
    descargar_imagenes, descargar_videos_gifs,
    comprimir_archivos, retirar_archivos
]
