import scripts_funciones


para_buscar = input("El enlace de la pagina: ")
scripts_funciones.obtener_enlaces(para_buscar)
scripts_funciones.filtrar_enlaces("resultados/enlaces.csv")
scripts_funciones.separa_enlaces_videos("resultados/enlaces.csv")
opcional_1 = ''
opcional_2 = ''
opcional_3 = ''


while opcional_1 not in ['Y', 'N']:
    opcional_1 = input("¿Quieres que se descarguen las imagenes? [Y/N]\n")
    if opcional_1.lower() == 'exit':
        exit()
    elif opcional_1 not in ['Y', 'N']:
        print("Opción inválida. Por favor ingresa 'Y' o 'N'")

while opcional_2 not in ['Y', 'N']:
    opcional_2 = input(
        "¿Quieres que se descarguen los videos y gifts? [Y/N]\n")
    if opcional_2.lower() == 'exit':
        exit()
    elif opcional_2 not in ['Y', 'N']:
        print("Opción inválida. Por favor ingresa 'Y' o 'N'")

while opcional_3 not in ['Y', 'N']:
    opcional_3 = input(
        "¿Quieres que se compriman las carpetas [Y/N]\n")
    if opcional_3.lower() == 'exit':
        exit()
    elif opcional_3 not in ['Y', 'N']:
        print("Opción inválida. Por favor ingresa 'Y' o 'N'")


if opcional_1 == "Y":
    nombre_carpeta_1 = input("Nombre para carpeta de las imagenes: ")
    nombre = input("Nombre para los archivos: ")
    try:
        numero_de_comienzo = int(input("numero de comienzo: "))
    except:
        opcional_1_2 = ''
        while opcional_1_2 not in ['Y', 'N']:
            opcional_1_2 = input(
                "ERROR: el valor se asignara como 1, continuar [Y/N]\n")
            if opcional_1_2 == "Y":
                numero_de_comienzo = 1
            elif opcional_1_2 == "N":
                exit()
            elif opcional_1_2 not in ['Y', 'N']:
                print("Opción inválida. Por favor ingresa 'Y' o 'N'")
        numero_de_comienzo = 1
    ruta_imagenes = scripts_funciones.descargar_imagenes_desde_csv(
        "resultados/enlaces.csv", nombre, numero_de_comienzo, nombre_carpeta_1)
else:
    ruta_imagenes = None
    nombre_carpeta_1 = None


if opcional_2 == "Y":
    nombre_carpeta_2 = input("Nombre para carpeta de los medios: ")
    nombre = input("Nombre para los archivos: ")
    try:
        numero_de_comienzo = int(input("numero de comienzo: "))
    except:
        opcional_1_2 = ''
        while opcional_1_2 not in ['Y', 'N']:
            opcional_1_2 = input(
                "ERROR: el valor se asignara como 1, continuar [Y/N]\n")
            if opcional_1_2 == "Y":
                numero_de_comienzo = 1
            elif opcional_1_2 == "N":
                exit()
            elif opcional_1_2 not in ['Y', 'N']:
                print("Opción inválida. Por favor ingresa 'Y' o 'N'")
    ruta_videos_1, ruta_gif_1 = scripts_funciones.descargar_videos_gifs_desde_csv(
        "resultados/enlaces.csv", nombre_carpeta_2, nombre, numero_de_comienzo)
    print("Descarga completada de los videos y gifs del archivo: resultados/enlaces.csv")
else:
    ruta_videos_1 = None
    ruta_gif_1 = None
    nombre_carpeta_2 = None

if opcional_3 == "Y":
    opcional_1_2 = ""
    nombre_zip = input("Nombre para el archivo zip: ")
    scripts_funciones.comprimir_carpeta(
        nombre_zip, ruta_imagenes, ruta_videos_1, ruta_gif_1)
    while opcional_1_2 not in ['Y', 'N']:
        opcional_1_2 = input("Desea eliminar los archivos [Y/N]\n")
        if opcional_1_2 == "Y":
            scripts_funciones.retirar_archivos (nombre_carpeta_1, nombre_carpeta_2)
        elif opcional_1_2 not in ['Y', 'N']:
            print("Opción inválida. Por favor ingresa 'Y' o 'N'")
    print("Terminado la tarea")
else:
    print("Terminado la tarea")
