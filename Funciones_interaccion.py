import os
import urllib.request
import json


def obtener_url_valida():
    while True:
        url = input("Introduce una URL válida: ")
        try:
            urllib.request.urlopen(url)
            return url
        except:
            print("La URL introducida no es válida. Por favor, inténtalo de nuevo.")


def obtener_entero_positivo():
    while True:
        try:
            valor = int(input("ingresa un numero de inicio: "))
            if valor < 1:
                raise ValueError
            return valor
        except ValueError:
            print("Ingresa un número entero positivo mayor que cero")
            # Agregamos un continue para seguir con el siguiente ciclo
            continue


def verificar_archivo ():
    while True:
        ruta = input("Introduce la ruta del archivo: ")
        if os.path.exists(ruta):
            extension = os.path.splitext(ruta)[1].lower()
            if extension == ".png" or extension == ".jpg":
                return ruta
        print("Ruta de archivo inválida. Introduce una ruta válida.")

def obtener_opcion_valida(opcion_exit=True):
    opciones_validas = ["Y", "N"]
    while True:
        opcion = input().strip()
        if opcion in opciones_validas:
            if opcion == "Y":
                return True
            else:
                return False
        elif opcion == "exit" and opcion_exit:
            return False
        else:
            print("Opción inválida. Por favor ingresa una de las opciones siguientes: Y, N")


def obtener_parametros():
    evasiones = 0
    print("Introduce el enlace de la página:")
    para_buscar = obtener_url_valida()

    print("¿Quieres usar la función avanzada para login en redes sociales y recorrer toda la página? [Y/N]:")
    opcional_1 = obtener_opcion_valida()

    print("¿Quieres descargar las imágenes? [Y/N]:")
    opcional_2 = obtener_opcion_valida()
    if opcional_2 == False:
        evasiones += 1

    print("¿Quieres descargar los videos? [Y/N]:")
    opcional_3 = obtener_opcion_valida()
    if opcional_3 == False:
        evasiones += 1

    if evasiones != 2:
        print("¿Quieres comprimir los archivos? [Y/N]:")
        opcional_4 = obtener_opcion_valida()
    else:
        opcional_4 = False

    return para_buscar, opcional_1, opcional_2, opcional_3, opcional_4


def agregar_configuracion(
        nombre, url_busqueda, descarga_imagenes, nombre_carpeta_imagenes, numero_de_comienzo_1, obviar_imagen, ruta_obviar, descarga_videos, nombre_carpeta_medios, numero_de_comienzo_2, comprimir_archivos, nombre_de_zip, eliminar_archivos_fuente
        ):

    configuracion = {
        "nombre": nombre,
        "url_busqueda": url_busqueda,
        "descarga_imagenes": descarga_imagenes,
        "nombre_carpeta_imagenes": nombre_carpeta_imagenes,
        "numero_de_comienzo_imagenes": numero_de_comienzo_1,
        "obviar_imagen": obviar_imagen,
        "ruta_de_imagen": ruta_obviar,
        "descarga_videos": descarga_videos,
        "nombre_carpeta_medios": nombre_carpeta_medios,
        "numero_de_comienzo_imagenes": numero_de_comienzo_2,
        "comprimir_archivos": comprimir_archivos,
        "nombre_zip": nombre_de_zip,
        "eliminar_archivos_fuente": eliminar_archivos_fuente
    }
    with open(f"{nombre}.json", "w") as f:
        json.dump(configuracion, f)

    print("Configuración agregada exitosamente!")
