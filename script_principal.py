# TODO: Depuración pendiente
import scripts_funciones
import funciones_interaccion


print("Usar alguna configuracion guardada: [Y/N]")
opcional_0 = funciones_interaccion.obtener_opcion_valida()
if opcional_0:
    para_buscar, opcional_1, url_login, usuario, password, opcional_2, nombre_carpeta_1, nombre_imagenes, numero_de_comienzo, verificar_imagen, ruta_imagenes, opcional_3, nombre_carpeta_2, nombre_archivos_2, numero_de_comienzo_2, ruta_videos, ruta_gif, opcional_4, nombre_zip, opcional_4_1 = funciones_interaccion.leer_configuracion()
    if para_buscar == False:
        para_buscar, opcional_1, url_login, usuario, password, opcional_2, opcional_3, opcional_4 = funciones_interaccion.obtener_parametros()
else:
    para_buscar, opcional_1, url_login, usuario, password, opcional_2, opcional_3, opcional_4 = funciones_interaccion.obtener_parametros()

lista = []

ruta_txt = "resultados/enlaces.txt"


if opcional_1:
    scripts_funciones.obtener_todos_los_enlaces(
        url_login, para_buscar, usuario, password
    )
    lista.append(para_buscar)
    lista.append(opcional_1)
    lista.append(usuario)
    lista.append(password)
    lista.append(url_login)
else:
    scripts_funciones.obtener_enlaces(para_buscar)
    lista.append(para_buscar)
    lista.append(opcional_1)
    lista.append(usuario)
    lista.append(password)
    lista.append(url_login)

scripts_funciones.filtrar_enlaces(ruta_txt)
scripts_funciones.corregir_enlaces_txt(ruta_txt)
scripts_funciones.eliminar_duplicados(ruta_txt)


if opcional_2:
    if not opcional_0:
        nombre_carpeta_1 = input("Nombre para carpeta de las imagenes: ")
        nombre_imagenes = input("Nombre para los archivos: ")
        numero_de_comienzo = funciones_interaccion.obtener_entero_positivo()
        print("quiere que se obvie alguna imagen [Y/N]")
        opcional_2_1 = funciones_interaccion.obtener_opcion_valida()
        if opcional_2_1:
            print("Ruta del archivo debe ser png o jpg ")
            verificar_imagen = funciones_interaccion.verificar_archivo()
        else:
            verificar_imagen = None
    ruta_imagenes = scripts_funciones.descargar_imagenes(
        ruta_txt, nombre_carpeta_1, nombre_imagenes, numero_de_comienzo, imagen_comparar=verificar_imagen
    )
    lista.append(opcional_2)
    lista.append(nombre_carpeta_1)
    lista.append(nombre_imagenes)
    lista.append(numero_de_comienzo)
    lista.append(verificar_imagen)
    lista.append(ruta_imagenes)
else:
    lista.append(opcional_2)
    lista.append(None)
    lista.append(None)
    lista.append(None)
    lista.append(None)
    ruta_imagenes = None
    nombre_carpeta_1 = None


if opcional_3:
    if not opcional_0:
        nombre_carpeta_2 = input("Nombre para carpeta de los medios: ")
        nombre_archivos_2 = input("Nombre para los archivos: ")
        numero_de_comienzo_2 = funciones_interaccion.obtener_entero_positivo()
    ruta_videos, ruta_gif = scripts_funciones.descargar_videos_gifs(
        ruta_txt, nombre_carpeta_2, nombre_archivos_2, numero_de_comienzo_2)
    lista.append(opcional_3)
    lista.append(nombre_carpeta_2)
    lista.append(nombre_archivos_2)
    lista.append(numero_de_comienzo_2)
    lista.append(ruta_videos)
    lista.append(ruta_gif)

else:
    lista.append(opcional_3)
    lista.append(None)
    lista.append(None)
    lista.append(None)
    lista.append(None)
    lista.append(None)
    ruta_videos = None
    ruta_gif = None
    nombre_archivos_2 = None


if opcional_4 and (opcional_2 or opcional_3):
    if not opcional_0:
        nombre_zip = input("Nombre para el archivo zip: ")
        print("¿Quiere que se eliminen los archivos fuente y sul carpetas[Y/N]:")
        opcional_4_1 = funciones_interaccion.obtener_opcion_valida()
    scripts_funciones.comprimir_archivos(
        nombre_zip, ruta_imagenes, ruta_videos, ruta_gif)
    if opcional_4_1:
        scripts_funciones.retirar_archivos(nombre_carpeta_1, nombre_carpeta_2)
    lista.append(opcional_4)
    lista.append(nombre_zip)
    lista.append(opcional_4_1)
else:
    lista.append(opcional_4)
    lista.append(None)
    lista.append(None)


if not opcional_0:
    print("Guardar los parametros (configuracion): [Y/N]")
    opcional_5 = funciones_interaccion.obtener_opcion_valida()
    if opcional_5:
        nombre_de_configuracion = input("El nombre de la configuracion: ")
        lista.insert(0, nombre_de_configuracion)
        funciones_interaccion.crear_configuracion(lista)
