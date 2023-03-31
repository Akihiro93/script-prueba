# TODO: Agregar las funciones para las configuraciones 
import scripts_funciones
import funciones_interaccion


print("Usar alguna configuracion guardada: ")
opcional_0 = funciones_interaccion.obtener_opcion_valida()
if opcional_0:
    nombre_de_configuracion, para_buscar, opcional_1, url_1, opcional_2, nombre_carpeta_1, numero_de_comienzo, verificar_imagen, opcional_3, nombre_carpeta_2, numero_de_comienzo_2, opcional_4, nombre_zip, opcional_4_1 = funciones_interaccion.leer_configuracion_2()
else:
    para_buscar, opcional_1, opcional_2, opcional_3, opcional_4 = funciones_interaccion.obtener_parametros()


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
    opcional_1, url_1 = None, None

scripts_funciones.filtrar_enlaces(ruta_txt)
scripts_funciones.corregir_enlaces_txt(ruta_txt)
scripts_funciones.eliminar_duplicados(ruta_txt)


if opcional_2:
    nombre_carpeta_1 = input("Nombre para carpeta de las imagenes: ")
    nombre_archivos = input("Nombre para los archivos: ")
    numero_de_comienzo = funciones_interaccion.obtener_entero_positivo()
    print("quiere que se obvie alguna imagen [Y/N]")
    opcional_2_1 = funciones_interaccion.obtener_opcion_valida()
    if opcional_2_1:
        print("Ruta del archivo debe ser png o jpg ")
        verificar_imagen = funciones_interaccion.verificar_archivo()
    else:
        verificar_imagen = None
    ruta_imagenes = scripts_funciones.descargar_imagenes(
        ruta_txt, nombre_carpeta_1, nombre_archivos, numero_de_comienzo, imagen_comparar=verificar_imagen
    )
else:
    opcional_2, nombre_carpeta_1, nombre_archivos, numero_de_comienzo, opcional_2_1, verificar_imagen, ruta_imagenes = (
        None, None, None, None, None, None, None
    )


if opcional_3:
    nombre_carpeta_2 = input("Nombre para carpeta de los medios: ")
    nombre_archivos_2 = input("Nombre para los archivos: ")
    numero_de_comienzo_2 = funciones_interaccion.obtener_entero_positivo()
    ruta_videos_1, ruta_gif_1 = scripts_funciones.descargar_videos_gifs(
        ruta_txt, nombre_carpeta_2, nombre_archivos_2, numero_de_comienzo_2)
else:
    opcional_3, nombre_carpeta_2, nombre_archivos_2, numero_de_comienzo_2, ruta_videos_1, ruta_gif_1 = (
        None, None, None, None, None, None
    )

if opcional_4:
    nombre_zip = input("Nombre para el archivo zip: ")
    scripts_funciones.comprimir_archivos(
        nombre_zip, ruta_imagenes, ruta_videos_1, ruta_gif_1)
    print("¿Quiere que se eliminen los archivos fuente y sul carpetas[Y/N]:")
    opcional_4_1 = funciones_interaccion.obtener_opcion_valida()
    if opcional_4_1:
        scripts_funciones.retirar_archivos(nombre_carpeta_1, nombre_carpeta_2)
else:
    opcional_4, nombre_zip, opcional_4_1 = None, None, None

if not opcional_0:
    print("Guardar los parametros (configuracion): [Y/N]")
    opcional_5 = funciones_interaccion.obtener_opcion_valida()
    if opcional_5:
        nombre_de_configuracion = input("El nombre de la configuracion: ")
        lista = [
            nombre_de_configuracion,
            para_buscar, opcional_1, url_1,
            opcional_2, nombre_carpeta_1, numero_de_comienzo, verificar_imagen, ruta_imagenes,
            opcional_3, nombre_carpeta_2, numero_de_comienzo_2,
            opcional_4, nombre_zip, opcional_4_1
        ]
        print(lista)
        funciones_interaccion.crear_configuracion(lista)
