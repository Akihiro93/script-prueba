import os
import requests

def descargar_imagenes(ruta_txt, carpeta_resultados='resultados', nombre_base='imagen', numero_inicial=1, umbral=5, imagen_comparar=None):

    # importar módulos
    from PIL import Image
    import imagehash
    import io

    # Crear carpeta para guardar las imágenes
    carpeta_imagenes = os.path.join('resultados', 'imagenes')
    if not os.path.exists(carpeta_imagenes):
        os.makedirs(carpeta_imagenes)

    carpeta_resultados_imagenes = os.path.join(
        carpeta_imagenes, carpeta_resultados)
    if not os.path.exists(carpeta_resultados_imagenes):
        os.makedirs(carpeta_resultados_imagenes)

    ruta_imagenes = os.path.join('resultados', 'imagenes', carpeta_resultados)

    contador = numero_inicial
    with open(ruta_txt, 'r') as file, open(os.path.join(carpeta_resultados_imagenes, 'links_fallidos.txt'), 'w') as links_file:
        for row in file:
            url_extension = os.path.splitext(row.strip())[1]
            if url_extension.lower() in ['.png', '.jpg', 'jpeg', '']:
                try:
                    response = requests.get(row.strip())
                except requests.exceptions.MissingSchema as e:
                    # si la URL no tiene el formato correcto, imprimimos un mensaje de error y escribimos el enlace fallido en el archivo
                    print(f"Error en la URL: {row.strip()}")
                    links_file.write(row.strip() + '\n')
                    continue
                try:
                    image = Image.open(io.BytesIO(response.content))
                    # si la imagen se puede cargar correctamente, la guardamos
                    if url_extension.lower() == '.png':
                        extension = '.jpg'
                    else:
                        extension = '.jpg'
                    filename = f"{nombre_base}_{contador:04d}{extension}"
                    filepath = os.path.join(
                        carpeta_resultados_imagenes, filename)
                    if imagen_comparar is not None:
                        with Image.open(imagen_comparar) as img:
                            hash_img = imagehash.average_hash(img)
                            hash_descarga = imagehash.average_hash(image)
                            if hash_img - hash_descarga <= umbral:
                                print(f"La imagen {row.strip()} coincide con {imagen_comparar}, omitiendo descarga")
                                continue
                    with open(filepath, 'wb') as image_file:
                        image_file.write(response.content)
                    contador += 1
                except:
                    # si la imagen no se puede cargar, imprimimos un mensaje de error y continuamos con el siguiente archivo
                    print(f"Error al descargar la imagen: {row.strip()}")
                    links_file.write(row.strip() + '\n')
                    continue
    print(f"Descarga completada de las imágenes del archivo: {ruta_txt}")
    return ruta_imagenes


def descargar_videos_gifs(ruta_txt, nombre_carpeta='carpeta_personalizada', nombre_base='media_', numero_inicial=1):
    # Crear carpeta para guardar los videos y gifs
    if not os.path.exists('resultados/media/' + nombre_carpeta):
        os.makedirs('resultados/media/' + nombre_carpeta)

    if not os.path.exists('resultados/media/' + nombre_carpeta + '/videos'):
        os.makedirs('resultados/media/' + nombre_carpeta + '/videos')

    if not os.path.exists('resultados/media/' + nombre_carpeta + '/gifs'):
        os.makedirs('resultados/media/' + nombre_carpeta + '/gifs')

    ruta_videos = os.path.join('resultados', 'media', nombre_carpeta, 'videos')
    ruta_gifs = os.path.join('resultados', 'media', nombre_carpeta, 'gifs')

    contador_videos = numero_inicial
    contador_gifs = numero_inicial
    with open(ruta_txt, 'r') as file:
        for line in file:
            url = line.strip()
            if url.startswith('https://preview.redd.it/') or url.startswith('https://www.redgifs.com/'):
                response = requests.get(url)
                content_type = response.headers.get('content-type')
                if content_type.startswith('video/'):
                    filename = 'resultados/media/' + nombre_carpeta + '/videos/' + \
                        nombre_base + str(contador_videos)
                    if not filename.lower().endswith('.mp4'):
                        filename += '.mp4'
                    with open(filename, 'wb') as video_file:
                        video_file.write(response.content)
                    contador_videos += 1
                elif content_type.startswith('image/gif'):
                    filename = 'resultados/media/' + nombre_carpeta + '/gifs/' + \
                        nombre_base + str(contador_gifs)
                    if not filename.lower().endswith('.gif'):
                        filename += '.gif'
                    with open(filename, 'wb') as gif_file:
                        gif_file.write(response.content)
                    contador_gifs += 1
    return ruta_videos, ruta_gifs


def comprimir_archivos(nombre_carpeta_comprimida, ruta_carpeta_imagenes='imagenes', ruta_carpeta_videos='videos', ruta_carpeta_gifs='gifs'):
    import zipfile

    # Crear carpeta para guardar el archivo comprimido
    if not os.path.exists('resultados/' + nombre_carpeta_comprimida):
        os.makedirs('resultados/' + nombre_carpeta_comprimida)

    # Comprimir archivos
    with zipfile.ZipFile('resultados/' + nombre_carpeta_comprimida + '/' + nombre_carpeta_comprimida + '.zip', mode='w', compression=zipfile.ZIP_DEFLATED) as zipf:

        # Comprimir imágenes
        if os.path.exists(ruta_carpeta_imagenes):
            for root, dirs, files in os.walk(ruta_carpeta_imagenes):
                for file in files:
                    zipf.write(os.path.join(root, file), arcname=os.path.join(
                        nombre_carpeta_comprimida, 'imagenes', file))

        # Comprimir videos
        if ruta_carpeta_videos != None:
            if os.path.exists(ruta_carpeta_videos):
                for root, dirs, files in os.walk(ruta_carpeta_videos):
                    for file in files:
                        zipf.write(os.path.join(root, file), arcname=os.path.join(
                            nombre_carpeta_comprimida, 'videos', file))

        # Comprimir gifs
        if ruta_carpeta_gifs != None:
            if os.path.exists(ruta_carpeta_gifs):
                for root, dirs, files in os.walk(ruta_carpeta_gifs):
                    for file in files:
                        zipf.write(os.path.join(root, file), arcname=os.path.join(
                            nombre_carpeta_comprimida, 'gifs', file))

        # Comprimir archivos enlaces.csv y links_separados.csv
        if os.path.exists('resultados/enlaces.txt'):
            zipf.write('resultados/enlaces.txt',
                    arcname=os.path.join(nombre_carpeta_comprimida, 'enlaces.txt'))

    print(
        f'Archivo {nombre_carpeta_comprimida}.zip creado en la carpeta resultados/')


def retirar_archivos(nombre_carpeta_1=None, nombre_carpeta_2=None):
    import shutil

    contador = 0

#retirar la carpeta dentro de imagenes
    if nombre_carpeta_1 != None:
        shutil.rmtree("resultados/imagenes/" + nombre_carpeta_1)
        contador += 1

# retirar la carpeta dentro de media
    if nombre_carpeta_2 != None:
        shutil.rmtree("resultados/media/" + nombre_carpeta_2)
        contador += 1
    ruta_enlaces = os.path.join("resultados", "enlaces.txt")

    if os.path.exists(ruta_enlaces):
        os.remove(ruta_enlaces)

    if contador != 2:
        return print("Carpeta retirada")
    else:
        return print("Carpetas retiradas")
        


def verificar_archivo():
    while True:
        ruta = input("Introduce la ruta del archivo: ")
        if os.path.exists(ruta):
            extension = os.path.splitext(ruta)[1].lower()
            if extension == ".png" or extension == ".jpg":
                return ruta
        print("Ruta de archivo inválida. Introduce una ruta válida.")


def verificar_carpetas_base():
    # Comprobar si existe resultados
    if not os.path.exists('resultados'):
        os.makedirs('resultados')
    # Comprobar si existe configuraciones
    if not os.path.exists('configuraciones'):
        os.makedirs('configuraciones')
        ruta_json = "configuraciones/configuraciones.json"
        with open(ruta_json, 'w') as archivo_json:
            pass
    # Comprobar el txt enlaces
    ruta = "resultados/enlaces.txt"
    with open(ruta, 'w') as archivo:
        pass

