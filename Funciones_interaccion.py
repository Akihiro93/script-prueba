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
    print("Introduce el enlace de la página")
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


def agregar_configuraciones(configuraciones):
    for configuracion in configuraciones:
        with open(f"{configuracion['nombre']}.json", "w") as f:
            json.dump(configuracion, f)

    print("Configuraciones agregadas exitosamente!")


def crear_configuracion(lista):
    claves = [
    "nombre", "url_busqueda", "usar_funcion_avanzada", "url_inicio_de_sesion",
    "descarga_imagenes", "nombre_carpeta_imagenes", "numero_de_comienzo_imagenes", "obviar_imagen", "ruta_de_imagen",
    "descarga_videos", "nombre_carpeta_medios", "numero_de_comienzo_videos",
    "comprimir_archivos", "nombre_zip", "eliminar_archivos_fuente" # Agregar esta clave
    ]
    
    # Verificar si existe la carpeta "configuraciones"
    if not os.path.exists("configuraciones"):
        os.makedirs("configuraciones")
    
    # Verificar si existe el archivo "configuraciones.json" dentro de la carpeta "configuraciones"
    if not os.path.isfile("configuraciones/configuraciones.json"):
        with open("configuraciones/configuraciones.json", "w") as f:
            json.dump({}, f)
    
    # Leer las configuraciones existentes del archivo "configuraciones.json"
    try:
        with open("configuraciones/configuraciones.json", "r") as f:
            if os.stat("configuraciones/configuraciones.json").st_size == 0:
                configuraciones = {}
            else:
                configuraciones = json.load(f)
    except json.decoder.JSONDecodeError:
        configuraciones = {}
    
    # Crear una nueva configuración con la lista de valores
    configuracion = {}
    for i, valor in enumerate(lista):
        clave = claves[i]
        configuracion[clave] = valor
    
    # Agregar la nueva configuración a la lista de configuraciones
    configuraciones[configuracion["nombre"]] = configuracion
    
    # Guardar las configuraciones actualizadas en el archivo "configuraciones.json"
    with open("configuraciones/configuraciones.json", "w") as f:
        json.dump(configuraciones, f)
    
    print("Configuración agregada exitosamente!")


def leer_configuracion(nombre_configuracion):
    try:
        with open("configuraciones/configuraciones.json", "r") as f:
            configuraciones = json.load(f)
            configuracion = configuraciones.get(nombre_configuracion)
            if configuracion:
                print(f"Configuración seleccionada: {nombre_configuracion}")
                print("Valores:")
                for clave, valor in configuracion.items():
                    print(f"{clave}: {valor}")
                return (
                    configuracion["url_inicio_de_sesion"],
                    configuracion["url_busqueda"],
                    configuracion["descarga_imagenes"],
                    configuracion["nombre_carpeta_imagenes"],
                    configuracion["numero_de_comienzo_imagenes"],
                    configuracion["obviar_imagen"],
                    configuracion["ruta_de_imagen"],
                    configuracion["descarga_videos"],
                    configuracion["nombre_carpeta_medios"],
                    configuracion["numero_de_comienzo_videos"],
                    configuracion["comprimir_archivos"],
                    configuracion["nombre_zip"],
                    configuracion["eliminar_archivos_fuente"],
                    configuracion["usar_funcion_avanzada"]
                )
            else:
                print(f"La configuración {nombre_configuracion} no existe.")
                return False
    except FileNotFoundError:
        print("El archivo configuraciones.json no existe.")
        return False

def leer_configuracion_2():
    try:
        with open("configuraciones/configuraciones.json", "r") as f:
            configuraciones = json.load(f)
            
            # Imprimir el nombre de todas las configuraciones con un número de índice
            print("Configuraciones:")
            for i, nombre in enumerate(configuraciones):
                print(f"{i+1}. {nombre}")
            
            # Permitir al usuario seleccionar una configuración
            seleccion = int(input("Selecciona una configuración: ")) - 1
            nombre_configuracion = list(configuraciones.keys())[seleccion]
            configuracion = configuraciones[nombre_configuracion]
            
            # Imprimir los valores de la configuración seleccionada
            print("Valores:")
            print(f"Nombre: {nombre_configuracion}")
            print(f"URL de inicio de sesion:{configuracion['url_inicio_de_sesion']}")
            print(f"URL de búsqueda: {configuracion['url_busqueda']}")
            print(f"Descargar imágenes: {configuracion['descarga_imagenes']}")
            print(f"Nombre de la carpeta de imágenes: {configuracion['nombre_carpeta_imagenes']}")
            print(f"Número de comienzo de imágenes: {configuracion['numero_de_comienzo_imagenes']}")
            print(f"Obviar imagen: {configuracion['obviar_imagen']}")
            print(f"Ruta de imagen: {configuracion['ruta_de_imagen']}")
            print(f"Descargar videos: {configuracion['descarga_videos']}")
            print(f"Nombre de la carpeta de medios: {configuracion['nombre_carpeta_medios']}")
            print(f"Número de comienzo de videos: {configuracion['numero_de_comienzo_videos']}")
            print(f"Comprimir archivos: {configuracion['comprimir_archivos']}")
            print(f"Nombre del archivo zip: {configuracion['nombre_zip']}")
            print(f"Eliminar archivos fuente: {configuracion['eliminar_archivos_fuente']}")
            print(f"Usar funcion avanzada:{configuracion['usar_funcion_avanzada']}")

            # Confirmar que los valores son correctos
            print("Los valores son correctos? (Y/N) ")
            confirmacion = obtener_opcion_valida()
            if confirmacion:
                return (configuracion["url_inicio_de_sesion"],
                        configuracion["url_busqueda"],
                        configuracion["descarga_imagenes"],
                        configuracion["nombre_carpeta_imagenes"],
                        configuracion["numero_de_comienzo_imagenes"],
                        configuracion["obviar_imagen"],
                        configuracion["ruta_de_imagen"],
                        configuracion["descarga_videos"],
                        configuracion["nombre_carpeta_medios"],
                        configuracion["numero_de_comienzo_videos"],
                        configuracion["comprimir_archivos"],
                        configuracion["nombre_zip"],
                        configuracion["eliminar_archivos_fuente"],
                        configuracion["usar_funcion_avanzada"]
                        )
            else:
                return False
    except FileNotFoundError:
        print("El archivo de configuraciones no existe.")
        return False