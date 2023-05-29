import json
import os


def agregar_configuraciones(configuraciones):
    for configuracion in configuraciones:
        with open(f"{configuracion['nombre']}.json", "w") as f:
            json.dump(configuracion, f, indent=4)

    print("Configuraciones agregadas exitosamente!")


def crear_configuracion(
    nombre, url_busqueda, func_avanzada, usuario, password, url_inicio_sesion, ruta_navegador, path, descarga_imagenes, carpeta_imagenes, nombre_imagenes, n_comienzo1, obviar, ruta_imagen, descarga_videos, carpeta_medios, nombre_medios, n_comienzo2, ruta_videos, ruta_gifs, comprimir, nombre_zip, eliminar_fuente):

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
    
    configuracion = {"nombre":nombre, "url_busqueda":url_busqueda, "usar_funcion_avanzada":func_avanzada, "usuario":usuario, "password":password, "url_inicio_de_sesion":url_inicio_sesion, "ruta_navegador":ruta_navegador, "path":path,
        "descarga_imagenes":descarga_imagenes, "nombre_carpeta_imagenes":carpeta_imagenes, "nombre_imagenes":nombre_imagenes, "numero_de_comienzo_imagenes":n_comienzo1, "obviar_imagen":obviar, "ruta_de_imagen":ruta_imagen,
        "descarga_videos":descarga_videos, "nombre_carpeta_medios":carpeta_medios, "nombre_medios":nombre_medios, "numero_de_comienzo_videos":n_comienzo2, "ruta_videos":ruta_videos, "ruta_gifs":ruta_gifs,
        "comprimir_archivos":comprimir, "nombre_zip":nombre_zip, "eliminar_archivos_fuente":eliminar_fuente
    }

    # Agregar la nueva configuración a la lista de configuraciones
    configuraciones[configuracion["nombre"]] = configuracion

    # Guardar las configuraciones actualizadas en el archivo "configuraciones.json"
    with open("configuraciones/configuraciones.json", "w") as f:
        json.dump(configuraciones, f)

    print("Configuración agregada exitosamente!")


def leer_configuracion():
    from lib.interaccion import obtener_opcion_valida
    try:
        try:
            with open("configuraciones/configuraciones.json", "r") as f:
                configuraciones = json.load(f)
        except json.JSONDecodeError:
            return False

        # Imprimir el nombre de todas las configuraciones con un número de índice
        while True:
            print("Configuraciones:")
            for i, nombre in enumerate(configuraciones):
                print(f"{i+1}. {nombre}")

            # Permitir al usuario seleccionar una configuración
            while True:
                try:
                    seleccion = int(
                        input("Selecciona una configuración: ")) - 1
                    nombre_configuracion = list(
                        configuraciones.keys())[seleccion]
                    configuracion = configuraciones[nombre_configuracion]
                except:
                    print("error introduce bien el numero")
                else:
                    break

            # Imprimir los valores de la configuración seleccionada

            print("Valores:")
            print(f"Nombre: {nombre_configuracion}")
            print(f"URL de búsqueda: {configuracion['url_busqueda']}")
            print(
                f"Usar funcion avanzada:{configuracion['usar_funcion_avanzada']}")
            print(
                f"URL de inicio de sesion:{configuracion['url_inicio_de_sesion']}")
            print(f"La elección de el path: {configuracion['path']}")
            print(
                f"La ruta a el ejecutable del navegador: {configuracion['ruta_navegador']}")
            print(f"El usuario es: {configuracion['usuario']}")
            print(f"La contraseña es: {configuracion['password']}")
            print(f"Descargar imágenes: {configuracion['descarga_imagenes']}")
            print(
                f"Nombre de la carpeta de imágenes: {configuracion['nombre_carpeta_imagenes']}")
            print(
                f"Nombre de las imagenes: {configuracion['nombre_imagenes']}")
            print(
                f"Número de comienzo de imágenes: {configuracion['numero_de_comienzo_imagenes']}")
            print(f"Obviar imagen: {configuracion['obviar_imagen']}")
            print(f"Ruta de imagen: {configuracion['ruta_de_imagen']}")
            print(f"Descargar videos: {configuracion['descarga_videos']}")
            print(
                f"Nombre de la carpeta de medios: {configuracion['nombre_carpeta_medios']}")
            print(f"Nombre de los medios: {configuracion['nombre_medios']}")
            print(
                f"Número de comienzo de videos: {configuracion['numero_de_comienzo_videos']}")
            print(f"Ruta de videos: {configuracion['ruta_videos']}")
            print(f"Ruta de gifs: {configuracion['ruta_gifs']}")
            print(f"Comprimir archivos: {configuracion['comprimir_archivos']}")
            print(f"Nombre del archivo zip: {configuracion['nombre_zip']}")
            print(
                f"Eliminar archivos fuente: {configuracion['eliminar_archivos_fuente']}")

            # Confirmar que los valores son correctos
            print("Los valores son correctos? (Y/N) ")
            confirmacion = obtener_opcion_valida()
            if confirmacion:
                return (
                    configuracion["url_busqueda"],
                    configuracion["usar_funcion_avanzada"],
                    configuracion["url_inicio_de_sesion"],
                    configuracion["usuario"],
                    configuracion["password"],
                    configuracion["path"],
                    configuracion["ruta_navegador"],
                    configuracion["descarga_imagenes"],
                    configuracion["nombre_carpeta_imagenes"],
                    configuracion["nombre_imagenes"],
                    configuracion["numero_de_comienzo_imagenes"],
                    configuracion["obviar_imagen"],
                    configuracion["ruta_de_imagen"],
                    configuracion["descarga_videos"],
                    configuracion["nombre_carpeta_medios"],
                    configuracion["nombre_medios"],
                    configuracion["numero_de_comienzo_videos"],
                    configuracion["ruta_videos"],
                    configuracion["ruta_gifs"],
                    configuracion["comprimir_archivos"],
                    configuracion["nombre_zip"],
                    configuracion["eliminar_archivos_fuente"],
                )
            else:
                pass
    except FileNotFoundError:
        print("El archivo de configuraciones no existe.")
        return False