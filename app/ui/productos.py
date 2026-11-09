"""
Pantalla de Productos (clase 6) — RF-03 y RF-04.

Misma forma que Clientes: tabla arriba, formulario abajo. La diferencia está
en las columnas Disponible y Reservado: no se escriben en ningún lado, las
calcula la vista v_productos sumando los lotes (modelo_er.md §4.2).
"""

import customtkinter as ctk

from app import bd, negocio
from app.negocio import ErrorNegocio
from app.ui import estilo

COLUMNAS = [
    ("id",         "Nº",          50, "center"),
    ("nombre",     "Producto",   260, "w"),
    ("disponible", "Disponible", 100, "e"),
    ("reservado",  "Reservado",  100, "e"),
]


class VentanaProductos(ctk.CTkToplevel):

    def __init__(self, master, con):
        super().__init__(master)
        self.con = con
        self.producto_id = None      # None = producto nuevo

        self.title("Productos")
        self.geometry("600x540")
        self.minsize(520, 460)
        self.transient(master)

        marco, self.tabla = estilo.tabla(self, COLUMNAS, alto=10)
        marco.pack(fill="both", expand=True, padx=16, pady=(16, 0))
        self.tabla.bind("<<TreeviewSelect>>", self._al_seleccionar)

        formulario = ctk.CTkFrame(self)
        formulario.pack(fill="x", padx=16, pady=(12, 0))
        self.modo = ctk.CTkLabel(formulario, font=ctk.CTkFont(weight="bold"))
        self.modo.grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=(8, 2))
        self.nombre = estilo.campo(formulario, "Nombre:", 1, 0, ancho=300)
        self.nombre.bind("<Return>", lambda _evento: self.guardar())

        botones = ctk.CTkFrame(self, fg_color="transparent")
        botones.pack(fill="x", padx=16, pady=16)
        ctk.CTkButton(botones, text="Nuevo", width=110, command=self.nuevo).pack(side="left")
        ctk.CTkButton(botones, text="Guardar", width=110,
                      command=self.guardar).pack(side="left", padx=8)
        self.aviso = ctk.CTkLabel(botones, text="", text_color=estilo.COLOR_AVISO)
        self.aviso.pack(side="left", padx=8)

        self.actualizar()
        self.nuevo()

    def actualizar(self):
        """Vuelve a leer los productos. Las otras pantallas cambian sus totales:
        una reserva en Reservas mueve Disponible y Reservado acá."""
        self.tabla.delete(*self.tabla.get_children())
        for p in bd.listar_productos(self.con):
            self.tabla.insert("", "end", iid=str(p["id"]),
                              values=(p["id"], p["nombre"], p["disponible"], p["reservado"]))
        if self.producto_id is not None and self.tabla.exists(str(self.producto_id)):
            self.tabla.selection_set(str(self.producto_id))

    def _al_seleccionar(self, _evento=None):
        seleccion = self.tabla.selection()
        if seleccion and int(seleccion[0]) != self.producto_id:
            self._cargar_formulario(int(seleccion[0]))
            self.aviso.configure(text="")

    def _cargar_formulario(self, producto_id):
        estilo.escribir(self.nombre, bd.obtener_producto(self.con, producto_id)["nombre"])
        self.producto_id = producto_id
        self.modo.configure(text=f"Modificando el producto Nº {producto_id}")

    def nuevo(self):
        self.tabla.selection_remove(*self.tabla.selection())
        estilo.escribir(self.nombre, "")
        self.producto_id = None
        self.aviso.configure(text="")
        self.modo.configure(text="Producto nuevo")
        self.nombre.focus_set()

    def guardar(self):
        try:
            if self.producto_id is None:
                guardado = negocio.agregar_producto(self.con, self.nombre.get())
            else:
                guardado = self.producto_id
                negocio.renombrar_producto(self.con, guardado, self.nombre.get())
        except ErrorNegocio as error:
            estilo.avisar(self, error)
            return

        self._cargar_formulario(guardado)
        self.actualizar()
        self.tabla.see(str(guardado))
        self.aviso.configure(text=f"Producto Nº {guardado} guardado.")
        self.master.datos_cambiaron(self)    # Lotes y Reservas muestran productos
