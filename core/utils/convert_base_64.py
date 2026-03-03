import base64

from core.utils import helpers
import os


# def buscar_archivo(nombre_archivo, raiz="."):
#     for carpeta_actual, subcarpetas, archivos in os.walk(raiz):
#         if nombre_archivo in archivos:
#             return os.path.join(carpeta_actual, nombre_archivo)
#     return None
#
#
# # Ejemplo de uso
# ruta_encontrada = buscar_archivo("TEST.doc", raiz=".")
# if ruta_encontrada:
#     print(f"Archivo encontrado: {ruta_encontrada}")
# else:
#     print("Archivo no encontrado.")


import os
import base64

def convertir_a_base64(ruta_archivo):
    carpeta = os.path.dirname(ruta_archivo) or "."  # Usa "." si está en la raíz
    print(f"📁 Archivos en la carpeta '{carpeta}':")

    # for archivo in os.listdir(carpeta):
    #     print(" -", archivo)

    with open(ruta_archivo, "rb") as archivo:
        contenido = archivo.read()
        base64_str = base64.b64encode(contenido).decode("utf-8")
        return base64_str


ruta = "../../resources/uploads/HazardousResponse.pdf"  # Cambia esto por la ruta real de tu archivo
base64_resultado = convertir_a_base64(ruta)
print(base64_resultado)
