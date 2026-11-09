"""
Dónde está cada cosa (clase 8).

Hay dos tipos de archivos, y van en lugares distintos:

  - Los que VIENEN CON EL PROGRAMA (datos/esquema.sql). Son de solo lectura y
    cambian cuando se instala una versión nueva.
  - Los que GENERA EL USUARIO (reservas.db, errores.log). Son lo valioso y no
    se pueden perder al actualizar el programa.

    Situación                 Archivos del programa      Datos del usuario
    ─────────────────────     ──────────────────────     ──────────────────────────────
    python -m app.main        la carpeta del proyecto    la carpeta del proyecto
    SistemaReservas.exe       junto al .exe (_internal)  %LOCALAPPDATA%\\SistemaReservas
    RESERVAS_CARPETA=…        (igual que arriba)         la carpeta que diga la variable

Hasta la clase 7, bd.py guardaba la base "al lado del código". Mientras
desarrollamos da igual, pero empaquetado eso significa guardar los datos
dentro de la carpeta del programa: Windows no deja escribir en "Archivos de
programa", y una actualización la reemplazaría entera.
"""

import os
import sys
from pathlib import Path

# PyInstaller agrega sys.frozen al programa empaquetado.
EMPAQUETADO = getattr(sys, "frozen", False)

NOMBRE_CARPETA = "SistemaReservas"


def carpeta_programa():
    """Donde están los archivos que vienen con el programa."""
    if EMPAQUETADO:
        # PyInstaller deja ahí los archivos agregados con `datas` en el .spec.
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parent.parent


def carpeta_usuario():
    """Donde se guardan los datos del usuario. La crea si no existe."""
    if os.environ.get("RESERVAS_CARPETA"):
        # Para probar el .exe sin tocar la carpeta real del usuario, o para
        # elegir otra ubicación (por ejemplo, una carpeta con copia de seguridad).
        carpeta = Path(os.environ["RESERVAS_CARPETA"])
    elif EMPAQUETADO:
        # %LOCALAPPDATA% es la carpeta que Windows reserva para los datos de
        # cada programa y cada usuario. Siempre se puede escribir ahí.
        carpeta = Path(os.environ["LOCALAPPDATA"]) / NOMBRE_CARPETA
    else:
        carpeta = carpeta_programa()
    carpeta.mkdir(parents=True, exist_ok=True)
    return carpeta
