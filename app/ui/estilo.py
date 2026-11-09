"""
Apariencia común a todas las pantallas (clase 5).

Si cada pantalla elige sus propios colores y letras, el programa termina
pareciendo hecho por varias personas. Acá se decide una vez y todas lo usan.
"""

import tkinter as tk
from tkinter import ttk

import customtkinter as ctk

FUENTE_TABLA = ("Segoe UI", 12)
FUENTE_TABLA_TITULOS = ("Segoe UI", 12, "bold")
COLOR_SELECCION = "#3B8ED0"      # el azul del tema "blue" de CustomTkinter
COLOR_AVISO = "#2E7D32"          # verde para "Cliente guardado."


def preparar():
    """Se llama una vez, antes de crear la primera ventana."""
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")


def titulo(master, texto):
    return ctk.CTkLabel(master, text=texto, font=ctk.CTkFont(size=20, weight="bold"))


def tabla(master, columnas, alto=12):
    """Una tabla (ttk.Treeview) con su barra de desplazamiento.

    CustomTkinter no trae tablas, así que usamos la de tkinter y le damos un
    estilo parecido.

    `columnas` es una lista de (clave, título, ancho, alineación), con
    alineación "w" (izquierda), "center" o "e" (derecha, para números).

    Devuelve (marco, tabla): el marco se ubica en la ventana; la tabla se usa
    para cargar filas.
    """
    _estilo_tabla(master)

    marco = ctk.CTkFrame(master, fg_color="transparent")
    claves = [c[0] for c in columnas]
    arbol = ttk.Treeview(marco, columns=claves, show="headings", height=alto,
                         selectmode="browse")
    for clave, texto, ancho, alineacion in columnas:
        arbol.heading(clave, text=texto, anchor=alineacion)
        # La última columna se estira para ocupar el espacio que sobre.
        arbol.column(clave, width=ancho, anchor=alineacion,
                     stretch=(clave == claves[-1]))

    barra = ctk.CTkScrollbar(marco, command=arbol.yview)
    arbol.configure(yscrollcommand=barra.set)

    arbol.pack(side="left", fill="both", expand=True)
    barra.pack(side="right", fill="y")
    return marco, arbol


def _estilo_tabla(master):
    estilo = ttk.Style(master)
    estilo.theme_use("clam")     # el tema de Windows no deja cambiar colores
    estilo.configure("Treeview", font=FUENTE_TABLA, rowheight=30,
                     background="white", fieldbackground="white")
    estilo.configure("Treeview.Heading", font=FUENTE_TABLA_TITULOS)
    estilo.map("Treeview",
               background=[("selected", COLOR_SELECCION)],
               foreground=[("selected", "white")])


def campo(master, etiqueta, fila, columna, ancho=240):
    """Etiqueta + caja de texto en una grilla. Devuelve la caja."""
    ctk.CTkLabel(master, text=etiqueta).grid(row=fila, column=columna,
                                             sticky="e", padx=(10, 6), pady=5)
    caja = ctk.CTkEntry(master, width=ancho)
    caja.grid(row=fila, column=columna + 1, sticky="w", pady=5)
    return caja


def escribir(caja, texto):
    """Reemplaza el contenido de una caja de texto."""
    caja.delete(0, tk.END)
    caja.insert(0, texto or "")
