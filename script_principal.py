import scripts_funciones


para_buscar = input("El enlace de la pagina: ")
scripts_funciones.obtener_enlaces(para_buscar)
scripts_funciones.filtrar_enlaces("resultados/enlaces.csv")
opcional_1 = ''
opcional_2 = ''


while opcional_1 not in ['Y', 'N']:
    opcional_1 = input("¿Quieres que se descarguen las imagenes? [Y/N]\n")
    if opcional_1.lower() == 'exit':
        exit()
    elif opcional_1 not in ['Y', 'N']:
        print("Opción inválida. Por favor ingresa 'Y' o 'N'")

while opcional_2 not in ['Y', 'N']:
    opcional_2 = input("¿Quieres que se descarguen los videos y gifts? [Y/N]\n")
    if opcional_2.lower() == 'exit':
        exit()
    elif opcional_2 not in ['Y', 'N']:
        print("Opción inválida. Por favor ingresa 'Y' o 'N'")


if opcional_1 == "Y":
    nombre_carpeta = input("Nombre para carpeta de las imagenes: ")
    nombre = input("Nombre para los archivos: ")
    try:
        numero_de_comienzo = int(input("numero de comienzo: "))
    except:
        opcional_1_2 = ''
        while opcional_1_2 not in ['Y', 'N']:
            opcional_1_2 = input("ERROR: el valor se asignara como 1, continuar [Y/N]\n")
            if opcional_1_2 == "Y":
                numero_de_comienzo = 1
            elif opcional_1_2 == "N":
                exit()
            elif opcional_1_2 not in ['Y', 'N']:
                print("Opción inválida. Por favor ingresa 'Y' o 'N'")
        numero_de_comienzo = 1
    scripts_funciones.descargar_imagenes_desde_csv("resultados/enlaces.csv", nombre, numero_de_comienzo, nombre_carpeta)



if opcional_2 == "Y":
    nombre_carpeta = input("Nombre para carpeta de los medios: ")
    nombre = input("Nombre para los archivos: ")
    try:
        numero_de_comienzo = int(input("numero de comienzo: "))
    except:
        opcional_1_2 = ''
        while opcional_1_2 not in ['Y', 'N']:
            opcional_1_2 = input("ERROR: el valor se asignara como 1, continuar [Y/N]\n")
            if opcional_1_2 == "Y":
                numero_de_comienzo = 1
            elif opcional_1_2 == "N":
                exit()
            elif opcional_1_2 not in ['Y', 'N']:
                print("Opción inválida. Por favor ingresa 'Y' o 'N'")
    scripts_funciones.descargar_videos_gifs_desde_csv("resultados/enlaces.csv", nombre_carpeta, nombre, numero_de_comienzo)

else:
    print("Terminado la tarea")
