"""
Punto de entrada del programa (clase 5; registro de errores en la clase 8).

Correr desde la carpeta del proyecto, con el entorno activado:
    python -m app.main

Empaquetado, es lo primero que ejecuta SistemaReservas.exe.
"""

import logging
import sys
import tkinter as tk
from tkinter import messagebox

from app import bd, ubicaciones
from app.ui import estilo
from app.ui.principal import VentanaPrincipal

RUTA_REGISTRO = ubicaciones.carpeta_usuario() / "errores.log"


def configurar_registro():
    """El detalle de los errores imprevistos va a errores.log.

    Durante el desarrollo también sale en la terminal. El .exe no tiene
    terminal (sys.stderr es None): sin este archivo, ese detalle se perdería
    y nadie podría averiguar qué pasó.
    """
    # delay=True: el archivo se crea recién con el primer error. Si no hay
    # errores.log, no hubo errores.
    manejadores = [logging.FileHandler(RUTA_REGISTRO, encoding="utf-8", delay=True)]
    if sys.stderr is not None:
        manejadores.append(logging.StreamHandler())
    logging.basicConfig(
        level=logging.WARNING,
        format="%(asctime)s  %(levelname)s  %(message)s",
        handlers=manejadores,
    )


def main():
    configurar_registro()
    try:
        con = bd.conectar()
        if not bd.base_creada(con):
            # Primera vez en una PC nueva: base vacía, sin datos de ejemplo.
            bd.crear_base(con)
    except Exception:
        # Si ni siquiera se puede abrir la base, no hay menú donde mostrar el
        # error: se avisa con una ventana suelta y se termina.
        logging.exception("No se pudo abrir la base %s", bd.RUTA_BD)
        tk.Tk().withdraw()
        messagebox.showerror(
            "Sistema de Reservas",
            f"No se pudo abrir la base de datos:\n{bd.RUTA_BD}\n\n"
            f"El detalle quedó en:\n{RUTA_REGISTRO}",
        )
        return

    estilo.preparar()
    try:
        VentanaPrincipal(con).mainloop()
    finally:
        # Se cierre como se cierre la ventana (Salir, la X o un error),
        # la base se cierra bien.
        con.close()


if __name__ == "__main__":
    main()
