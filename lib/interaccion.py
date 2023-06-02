import os
import urllib.request


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
            print(
                "Opción inválida. Por favor ingresa una de las opciones siguientes: Y, N")


def navegador_a_utilizar():
    print("Que navegador utilizas:\n1.Chrome 2.Edge 3.Firefox 4.Basado en chromium")
    while True:
        opcion = obtener_entero_positivo()

        if opcion == 4:
            while True:
                ruta = input("Introduce la ruta del ejecutable del navegador: ")
                if ruta == "exit":
                    break
                elif not os.path.exists(ruta):
                    print("ERROR: El ejecutable no existe.")
                else:
                    return (opcion, ruta)
                continue

        elif opcion in (1, 3):
            return opcion, None

        else:
            print("Error: selección inválida.")


def obtener_parametros():
    evasiones = 0
    print("Introduce el enlace de la página")
    para_buscar = obtener_url_valida()

    print(
        "¿Quieres usar la función avanzada para login en redes sociales y recorrer toda la página? [Y/N]:")
    opcional_1 = obtener_opcion_valida()
    if opcional_1:
        url_login = obtener_url_valida()
        usuario = input("Su usuario: ")
        password = input("La contraseña: ")
        election, navegador = navegador_a_utilizar()
    else:
        url_login = None
        usuario = None
        password = None
        election = None
        navegador = None

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

    return para_buscar, opcional_1, url_login, usuario, password, election, navegador, opcional_2, opcional_3, opcional_4
