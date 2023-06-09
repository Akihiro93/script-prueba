from lib import interaccion, enlaces, ficheros, json


def agregar_lista (*args):
    for i in args:
        lista.append(i)

print("Usar alguna configuracion guardada: [Y/N]")
opcional_0 = interaccion.obtener_opcion_valida()
if opcional_0:
    try:
        para_buscar, opcional_1, url_login, usuario, password, path_election, ruta_navegador, opcional_2, nombre_carpeta_1, nombre_imagenes, numero_de_comienzo, verificar_imagen, ruta_imagenes, opcional_3, nombre_carpeta_2, nombre_archivos_2, numero_de_comienzo_2, ruta_videos, ruta_gif, opcional_4, nombre_zip, opcional_4_1 = json.leer_configuracion()
    except TypeError:
        print("ERROR: no se a encontrado configuraciones guardadas")
        para_buscar, opcional_1, url_login, usuario, password, path_election, ruta_navegador, opcional_2, opcional_3, opcional_4 = interaccion.obtener_parametros()
        opcional_0 = False
else:
    para_buscar, opcional_1, url_login, usuario, password, path_election, ruta_navegador, opcional_2, opcional_3, opcional_4 = interaccion.obtener_parametros()

lista = []
ficheros.verificar_carpetas_base()
ruta_txt = "resultados/enlaces.txt"

if opcional_1:
    enlaces.obtener_todos_los_enlaces(
        url_login, para_buscar, usuario, password, ruta_navegador, path_election
    )
    agregar_lista(para_buscar, opcional_1, usuario, password, url_login, ruta_navegador, path_election)
else:
    enlaces.obtener_enlaces(para_buscar)
    agregar_lista(para_buscar, opcional_1, usuario, password, url_login, ruta_navegador, path_election)

enlaces.filtrar_enlaces(ruta_txt)
enlaces.corregir_enlaces_txt(ruta_txt)
enlaces.eliminar_duplicados(ruta_txt)

if opcional_2:
    if not opcional_0:
        nombre_carpeta_1 = input("Nombre para carpeta de las imagenes: ")
        nombre_imagenes = input("Nombre para los archivos: ")
        numero_de_comienzo = interaccion.obtener_entero_positivo()
        print("quiere que se obvie alguna imagen [Y/N]")
        opcional_2_1 = interaccion.obtener_opcion_valida()
        if opcional_2_1:
            print("Ruta del archivo debe ser png o jpg ")
            verificar_imagen = ficheros.verificar_archivo()
        else:
            verificar_imagen = None
    ruta_imagenes = ficheros.descargar_imagenes(
        ruta_txt, nombre_carpeta_1, nombre_imagenes, numero_de_comienzo, imagen_comparar=verificar_imagen
    )
    agregar_lista(opcional_2, nombre_carpeta_1, nombre_imagenes, numero_de_comienzo, verificar_imagen, ruta_imagenes)
else:
    agregar_lista(opcional_2, None, None, None, None, None)
    ruta_imagenes = None
    nombre_carpeta_1 = None

if opcional_3:
    if not opcional_0:
        nombre_carpeta_2 = input("Nombre para carpeta de los medios: ")
        nombre_archivos_2 = input("Nombre para los archivos: ")
        numero_de_comienzo_2 = interaccion.obtener_entero_positivo
    ruta_videos, ruta_gif = ficheros.descargar_videos_gifs(
        ruta_txt, nombre_carpeta_2, nombre_archivos_2, numero_de_comienzo_2)
    agregar_lista(opcional_3, nombre_carpeta_2, nombre_archivos_2, numero_de_comienzo_2, ruta_videos, ruta_gif)
else:
    agregar_lista(opcional_3, None, None, None, None, None)
    ruta_videos = None
    ruta_gif = None
    nombre_carpeta_2 = None

if opcional_4 and (opcional_2 or opcional_3):
    if not opcional_0:
        nombre_zip = input("Nombre para el archivo zip: ")
        print(
            "¿Quiere que se eliminen los archivos fuente y sud carpetas[Y/N]:")
        opcional_4_1 = interaccion.obtener_opcion_valida()
    ficheros.comprimir_archivos(
        nombre_zip, ruta_imagenes, ruta_videos, ruta_gif)
    if opcional_4_1:
        ficheros.retirar_archivos(nombre_carpeta_1, nombre_carpeta_2)
    agregar_lista(opcional_4, nombre_zip, opcional_4_1)
else:
    agregar_lista(opcional_4, None, None)

if not opcional_0:
    print("Guardar los parametros (configuracion): [Y/N]")
    opcional_5 = interaccion.obtener_opcion_valida()
    if opcional_5:
        nombre_de_configuracion = input("El nombre de la configuracion: ")
        lista.insert(0, nombre_de_configuracion)
    json.crear_configuracion(*lista)
