"""
Apariencia común a todas las pantallas (clase 5).

Si cada pantalla elige sus propios colores y letras, el programa termina
pareciendo hecho por varias personas. Acá se decide una vez y todas lo usan.
"""

import tkinter as tk
from tkinter import messagebox, ttk

import customtkinter as ctk

FUENTE_TABLA = ("Segoe UI", 12)
FUENTE_TABLA_TITULOS = ("Segoe UI", 12, "bold")
COLOR_SELECCION = "#3B8ED0"      # el azul del tema "blue" de CustomTkinter
COLOR_AVISO = "#2E7D32"          # verde para "Cliente guardado."
COLOR_APAGADO = "gray55"         # filas de lotes anulados y reservas canceladas


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
        # Las columnas de texto (alineadas a la izquierda: nombre, cliente,
        # producto) se reparten el espacio que sobre. Números y fechas no:
        # quedan con su ancho, pegados a su título.
        arbol.column(clave, width=ancho, minwidth=40, anchor=alineacion,
                     stretch=(alineacion == "w"))

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


def avisar(ventana, error):
    """Muestra un error previsto (ErrorNegocio o ErrorFormato) tal cual.
    parent=ventana: el aviso aparece sobre esa ventana, no sobre el menú."""
    messagebox.showwarning("No se pudo", str(error), parent=ventana)


def confirmar(ventana, titulo, texto):
    """Pregunta Sí/No antes de algo que no tiene vuelta atrás."""
    return messagebox.askyesno(titulo, texto, parent=ventana)


class Selector(ctk.CTkOptionMenu):
    """Lista desplegable que MUESTRA textos pero DEVUELVE ids.

    El usuario elige "Ferretería Norte (Nº 1)"; el programa necesita el 1.
        selector.cargar([(1, "Ferretería Norte (Nº 1)"), (2, "Casa Rodríguez (Nº 2)")])
        selector.valor()  ->  1

    Un id None sirve para opciones como "Todos".
    """

    def __init__(self, master, vacio="(no hay)", width=240, al_cambiar=None):
        super().__init__(master, values=[vacio], width=width, dynamic_resizing=False,
                         command=lambda _texto: al_cambiar and al_cambiar())
        self._vacio = vacio
        self._ids = {}           # texto -> id

    def cargar(self, opciones):
        """Reemplaza las opciones. Si lo que estaba elegido sigue estando,
        queda elegido (importa al actualizar una pantalla abierta)."""
        anterior = self.valor()
        self._ids = {texto: id_ for id_, texto in opciones}
        textos = list(self._ids) or [self._vacio]
        self.configure(values=textos)
        textos_por_id = {id_: texto for texto, id_ in self._ids.items()}
        self.set(textos_por_id.get(anterior, textos[0]))

    def valor(self):
        return self._ids.get(self.get())
