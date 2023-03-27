# TODO: Agregar las funciones para las configuraciones 
import scripts_funciones
from Funciones_interaccion import obtener_url_valida, verificar_archivo, obtener_opcion_valida, obtener_entero_positivo, obtener_parametros

para_buscar, opcional_1, opcional_2, opcional_3, opcional_4 = obtener_parametros()

ruta_txt = "resultados/enlaces.txt"


if opcional_1:
    url_1, url_2, usuario_1, contraseña_1 = (
        "https://www.reddit.com/login/",
        para_buscar,
        "Akihiro9",
        "TLq9JHzg*q%n1JpR"
    )
    scripts_funciones.obtener_todos_los_enlaces(
        url_1, url_2, usuario_1, contraseña_1
    )
else:
    scripts_funciones.obtener_enlaces(para_buscar)

scripts_funciones.filtrar_enlaces(ruta_txt)
scripts_funciones.corregir_enlaces_txt(ruta_txt)
scripts_funciones.eliminar_duplicados(ruta_txt)


if opcional_2:
    nombre_carpeta_1 = input("Nombre para carpeta de las imagenes: ")
    nombre_archivos = input("Nombre para los archivos: ")
    numero_de_comienzo = obtener_entero_positivo()
    print("quiere que se obvie alguna imagen [Y/N]")
    opcional_2_1 = obtener_opcion_valida()
    if opcional_2_1:
        verificar_imagen = print(
            "Ruta del archivo debe ser png o jpg "), verificar_archivo()
    else:
        verificar_imagen = None
    ruta_imagenes = scripts_funciones.descargar_imagenes(
        ruta_txt, nombre_carpeta_1, nombre_archivos, numero_de_comienzo, imagen_comparar=verificar_imagen
    )
else:
    ruta_imagenes = None
    nombre_carpeta_1 = None


if opcional_3:
    nombre_carpeta_2 = input("Nombre para carpeta de los medios: ")
    nombre_archivos_2 = input("Nombre para los archivos: ")
    numero_de_comienzo_2 = obtener_entero_positivo()
    ruta_videos_1, ruta_gif_1 = scripts_funciones.descargar_videos_gifs(
        ruta_txt, nombre_carpeta_2, nombre_archivos_2, numero_de_comienzo_2)
else:
    ruta_videos_1 = None
    ruta_gif_1 = None
    nombre_carpeta_2 = None

if opcional_4:
    nombre_zip = input("Nombre para el archivo zip: ")
    scripts_funciones.comprimir_archivos(
        nombre_zip, ruta_imagenes, ruta_videos_1, ruta_gif_1)
    print("¿Quiere que se eliminen los archivos fuente y sul carpetas[Y/N]:")
    opcional_4_1 = obtener_opcion_valida()
    if opcional_4_1:
        scripts_funciones.retirar_archivos(nombre_carpeta_1, nombre_carpeta_2)
    print("Terminado la tarea")
else:
    print('Terminado la tarea')
