import os
from bs4 import BeautifulSoup
import requests
from bs4 import BeautifulSoup


def obtener_todos_los_enlaces(url_1, url_2, usuario, password, ruta_navegador=None, path=1):
    # importar módulos necesarios
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException
    import time
    from lib.interaccion import obtener_opcion_valida
    import platform
    
    enlaces = []

    if platform.system == "Windows":
        extension = ".exe"
        name = "_win32"
    else:
        extension = ""
        name = ""

    if path == 1:
        # controlador para chrome
        chrome_driver_path = f"path\chromedriver{name}\chromedriver{extension}"
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-extensions')
        options.add_argument('--incognito')
        driver = webdriver.Chrome(
            options=options, executable_path=chrome_driver_path)
    
    if path == 2:
        # configurar el controlador de Edge
        edge_driver_path = 'path\edgedriver_win64\msedgedriver.exe'
        edge_options = webdriver.EdgeOptions()
        edge_options.use_chromium = True
        driver = webdriver.Edge(
            executable_path=edge_driver_path, options=edge_options)

    if path == 3 and ruta_navegador != None:
        # configurar el controlador para basados en chromium
        path_chromium = ruta_navegador
        brave_driver_path = f"path\chromedriver{name}\chromedriver{extension}"
        options = webdriver.ChromeOptions()
        options.binary_location = path_chromium
        options.add_argument('--disable-extensions')
        options.add_argument('--incognito')
        driver = webdriver.Chrome(
            options=options, executable_path=brave_driver_path)
    
    if path == 4:
        options = webdriver.Firefox()

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

    # control de error al accionar el botón de login
    try:
        button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[name='Login']")))
        button.click()
    except TimeoutException:
        while True:
            print("No se puede accionar el botón presione usted\nya lo acciono: Y/N")
            confirmacion = obtener_opcion_valida()
            if confirmacion:
                break
            else:
                continue

    # obtener los enlaces guardados del usuario
    driver.get(url_2)
    time.sleep(8)
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Hacer scroll hasta el final de la página
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        # Esperar a que se cargue la página
        time.sleep(5)
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

# enlaces a filtrar
    filtered_rows = [row for row in rows if not (row.startswith('https://www.reddit.com/login') or any(link in row for link in ['https://www.redditinc.com/policies/user-agreement', 'https://www.redditinc.com/policies/privacy-policy',
    'https://www.redditinc.com/policies/content-policy', 'https://www.redditinc.com/policies/moderator-guidelines',
    'https://ads.reddit.com?utm_source=d2x_consumer&utm_name=top_nav_cta', 'https://www.reddit.com/chat'
    ]))]

#sobre escribir el archivo
    with open(ruta_txt, "w") as f:
        f.write('\n'.join(filtered_rows))

    return print("Archivo de enlaces filtrado")


def corregir_enlaces_txt(ruta_txt):
    # verificar el archivo
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