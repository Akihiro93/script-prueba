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

