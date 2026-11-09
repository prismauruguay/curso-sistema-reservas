"""
Pantalla de Clientes (clase 5) — RF-01 y RF-02.

Implementa el boceto de docs/bocetos.md: búsqueda arriba, listado en el medio,
formulario abajo. Todo en UNA ventana. El sistema original abría una ventana
aparte para agregar, otra para modificar y otra para buscar.

Lo que esta pantalla hace y lo que NO:
  - Muestra datos y pide datos.
  - Para LEER llama a bd (listar, obtener).
  - Para GUARDAR llama a negocio, que controla las reglas.
  - No escribe SQL ni decide qué es válido: si negocio dice que no, muestra
    el mensaje tal cual.
"""

from tkinter import messagebox

import customtkinter as ctk

from app import bd, negocio
from app.negocio import ErrorNegocio
from app.ui import estilo

COLUMNAS = [
    # clave       título      ancho  alineación
    ("id",       "Nº",          50, "center"),
    ("nombre",   "Nombre",     220, "w"),
    ("telefono", "Teléfono",   120, "w"),
    ("email",    "Email",      200, "w"),
]


class VentanaClientes(ctk.CTkToplevel):

    def __init__(self, master, con):
        super().__init__(master)
        self.con = con
        # None = el formulario es para un cliente NUEVO.
        # Un número = se está modificando ese cliente.
        self.cliente_id = None

        self.title("Clientes")
        self.geometry("720x600")
        self.minsize(640, 540)
        self.transient(master)       # queda siempre delante del menú

        self._armar_busqueda()
        self._armar_tabla()
        self._armar_formulario()
        self._armar_botones()

        self.actualizar_tabla()
        self.nuevo()

    # -----------------------------------------------------------------
    #  Armado de la pantalla (solo se ejecuta una vez)
    # -----------------------------------------------------------------

    def _armar_busqueda(self):
        fila = ctk.CTkFrame(self, fg_color="transparent")
        fila.pack(fill="x", padx=16, pady=(16, 8))
        ctk.CTkLabel(fila, text="Buscar (nombre o teléfono):").pack(side="left", padx=(0, 6))

        self.texto_buscar = ctk.StringVar()
        # Cada vez que cambia el texto, se vuelve a filtrar la tabla.
        self.texto_buscar.trace_add("write", lambda *_: self.actualizar_tabla())
        ctk.CTkEntry(fila, textvariable=self.texto_buscar, width=240).pack(side="left")

    def _armar_tabla(self):
        marco, self.tabla = estilo.tabla(self, COLUMNAS, alto=10)
        marco.pack(fill="both", expand=True, padx=16)
        self.tabla.bind("<<TreeviewSelect>>", self._al_seleccionar)

    def _armar_formulario(self):
        marco = ctk.CTkFrame(self)
        marco.pack(fill="x", padx=16, pady=(12, 0))

        self.modo = ctk.CTkLabel(marco, font=ctk.CTkFont(weight="bold"))
        self.modo.grid(row=0, column=0, columnspan=4, sticky="w", padx=10, pady=(8, 2))

        self.campos = {
            "nombre":    estilo.campo(marco, "Nombre:",    1, 0),
            "direccion": estilo.campo(marco, "Dirección:", 2, 0),
            "telefono":  estilo.campo(marco, "Teléfono:",  3, 0, ancho=140),
            "email":     estilo.campo(marco, "Email:",     3, 2, ancho=200),
        }
        # Enter en cualquier campo del formulario = Guardar.
        for caja in self.campos.values():
            caja.bind("<Return>", lambda _evento: self.guardar())

    def _armar_botones(self):
        fila = ctk.CTkFrame(self, fg_color="transparent")
        fila.pack(fill="x", padx=16, pady=16)
        ctk.CTkButton(fila, text="Nuevo", width=110, command=self.nuevo).pack(side="left")
        ctk.CTkButton(fila, text="Guardar", width=110,
                      command=self.guardar).pack(side="left", padx=8)
        # Confirmaciones discretas: un texto que se lee y no hay que cerrar.
        self.aviso = ctk.CTkLabel(fila, text="", text_color=estilo.COLOR_AVISO)
        self.aviso.pack(side="left", padx=8)

    # -----------------------------------------------------------------
    #  Comportamiento
    # -----------------------------------------------------------------

    def actualizar_tabla(self, seleccionar=None):
        """Vuelve a leer los clientes. Si se indica un id, lo deja marcado."""
        self.tabla.delete(*self.tabla.get_children())
        for c in bd.listar_clientes(self.con, self.texto_buscar.get()):
            # iid = identificador de la fila: usamos el id del cliente.
            self.tabla.insert("", "end", iid=str(c["id"]),
                              values=(c["id"], c["nombre"], c["telefono"], c["email"] or ""))
        if seleccionar is not None and self.tabla.exists(str(seleccionar)):
            self.tabla.selection_set(str(seleccionar))
            self.tabla.see(str(seleccionar))

    def _al_seleccionar(self, _evento=None):
        """Al marcar un cliente en la tabla, se cargan sus datos para modificarlos."""
        seleccion = self.tabla.selection()
        if not seleccion:
            return
        cliente = bd.obtener_cliente(self.con, int(seleccion[0]))
        for clave, caja in self.campos.items():
            estilo.escribir(caja, cliente[clave])
        # Ojo: este evento también llega cuando guardar() vuelve a marcar el
        # cliente recién guardado. En ese caso el aviso "guardado" se deja.
        if cliente["id"] != self.cliente_id:
            self.aviso.configure(text="")
        self.cliente_id = cliente["id"]
        self.modo.configure(text=f"Modificando el cliente Nº {cliente['id']}")

    def nuevo(self):
        """Deja el formulario vacío para cargar un cliente nuevo."""
        self.tabla.selection_remove(*self.tabla.selection())
        for caja in self.campos.values():
            estilo.escribir(caja, "")
        self.cliente_id = None
        self.aviso.configure(text="")
        # El número NO se muestra: lo asigna la base recién al guardar.
        self.modo.configure(text="Cliente nuevo")
        self.campos["nombre"].focus_set()

    def guardar(self):
        datos = {clave: caja.get() for clave, caja in self.campos.items()}
        try:
            if self.cliente_id is None:
                self.cliente_id = negocio.agregar_cliente(self.con, **datos)
            else:
                negocio.modificar_cliente(self.con, self.cliente_id, **datos)
        except ErrorNegocio as error:
            # parent=self: el aviso aparece sobre esta ventana, no sobre el menú.
            messagebox.showwarning("No se pudo guardar", str(error), parent=self)
            return

        guardado = self.cliente_id
        self.texto_buscar.set("")      # que el cliente guardado se vea en la lista
        self.actualizar_tabla(seleccionar=guardado)
        self.aviso.configure(text=f"Cliente Nº {guardado} guardado.")
