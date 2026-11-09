"""
Menú principal (clase 5). Implementa el boceto de docs/bocetos.md.
"""

import traceback
from tkinter import messagebox

import customtkinter as ctk

from app.ui import estilo
from app.ui.clientes import VentanaClientes


class VentanaPrincipal(ctk.CTk):

    def __init__(self, con):
        super().__init__()
        self.con = con
        # Una sola ventana abierta de cada pantalla: nombre -> ventana.
        self.ventanas = {}

        self.title("Sistema de Reservas")
        self.geometry("320x480")
        self.resizable(False, False)

        estilo.titulo(self, "SISTEMA DE RESERVAS").pack(pady=(24, 16))

        opciones = [
            # texto               pantalla (None = todavía no existe)
            ("Clientes",          VentanaClientes),
            ("Productos",         None),     # clase 6
            ("Lotes",             None),     # clase 6
            ("Reservas",          None),     # clase 6
            ("Exportar a Excel",  None),     # clase 7
        ]
        for texto, pantalla in opciones:
            boton = ctk.CTkButton(
                self, text=texto, height=44,
                command=lambda t=texto, p=pantalla: self.abrir(t, p),
            )
            if pantalla is None:
                # Gris, para que no parezca un botón que anda y no responde.
                boton.configure(state="disabled", fg_color="gray78")
            boton.pack(fill="x", padx=40, pady=5)

        ctk.CTkButton(self, text="Salir", height=44, fg_color="gray45",
                      hover_color="gray35", command=self.destroy
                      ).pack(fill="x", padx=40, pady=(20, 5))

    def abrir(self, nombre, pantalla):
        """Abre una pantalla, o la trae al frente si ya estaba abierta."""
        ventana = self.ventanas.get(nombre)
        if ventana is not None and ventana.winfo_exists():
            ventana.deiconify()      # por si estaba minimizada
            ventana.lift()
            ventana.focus_set()
            return
        self.ventanas[nombre] = pantalla(self, self.con)

    def report_callback_exception(self, tipo, valor, rastro):
        """Tkinter llama a esto cuando un botón produce un error NO previsto
        (no un ErrorNegocio: un error de programación, un archivo bloqueado…).

        Al usuario: un mensaje claro, nunca el error técnico (RNF-04).
        Al programador: el detalle completo en la terminal.
        """
        traceback.print_exception(tipo, valor, rastro)
        messagebox.showerror(
            "Error inesperado",
            "Ocurrió un error inesperado y la operación no se completó.\n"
            "Si se repite, avisá a soporte.",
            parent=self,
        )
