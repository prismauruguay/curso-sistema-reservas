"""
Pantalla de Lotes (clase 6) — RF-05, RF-06 y RF-07.

Dos zonas, como en el boceto:
  - La tabla, con los botones que actúan sobre el lote ELEGIDO en ella:
    Cambiar fecha y Anular.
  - El formulario de abajo, que sirve solo para cargar un lote NUEVO.
"""

import customtkinter as ctk

from app import bd, negocio
from app.negocio import ErrorNegocio
from app.ui import estilo, formato
from app.ui.formato import ErrorFormato

COLUMNAS = [
    ("id",          "Lote",        60, "center"),
    ("producto",    "Producto",   200, "w"),
    ("arribo",      "Arribo",     100, "center"),
    ("comprada",    "Comprada",    90, "e"),
    ("reservado",   "Reservado",   90, "e"),
    ("entregado",   "Entregado",   90, "e"),
    ("disponible",  "Disponible", 100, "e"),
    ("estado",      "Estado",      90, "center"),
]


class VentanaLotes(ctk.CTkToplevel):

    def __init__(self, master, con):
        super().__init__(master)
        self.con = con

        self.title("Lotes")
        self.geometry("900x620")
        self.minsize(820, 540)
        self.transient(master)

        marco, self.tabla = estilo.tabla(self, COLUMNAS, alto=11)
        marco.pack(fill="both", expand=True, padx=16, pady=(16, 0))
        self.tabla.tag_configure("anulado", foreground=estilo.COLOR_APAGADO)

        acciones = ctk.CTkFrame(self, fg_color="transparent")
        acciones.pack(fill="x", padx=16, pady=(8, 0))
        ctk.CTkLabel(acciones, text="Lote elegido:").pack(side="left", padx=(0, 8))
        ctk.CTkButton(acciones, text="Cambiar fecha…", width=130,
                      command=self.cambiar_fecha).pack(side="left")
        ctk.CTkButton(acciones, text="Anular lote", width=130, fg_color="#C0392B",
                      hover_color="#962D22", command=self.anular).pack(side="left", padx=8)

        self._armar_formulario()
        self.actualizar()

    def _armar_formulario(self):
        marco = ctk.CTkFrame(self)
        marco.pack(fill="x", padx=16, pady=(12, 0))
        ctk.CTkLabel(marco, text="Nuevo lote", font=ctk.CTkFont(weight="bold")).grid(
            row=0, column=0, columnspan=6, sticky="w", padx=10, pady=(8, 2))

        ctk.CTkLabel(marco, text="Producto:").grid(row=1, column=0, sticky="e", padx=(10, 6), pady=8)
        self.producto = estilo.Selector(marco, vacio="(cargá productos primero)", width=240)
        self.producto.grid(row=1, column=1, sticky="w", pady=8)
        self.cantidad = estilo.campo(marco, "Cantidad:", 1, 2, ancho=80)
        self.arribo = estilo.campo(marco, "Arribo (dd/mm/aaaa):", 1, 4, ancho=120)
        for caja in (self.cantidad, self.arribo):
            caja.bind("<Return>", lambda _evento: self.crear())

        botones = ctk.CTkFrame(self, fg_color="transparent")
        botones.pack(fill="x", padx=16, pady=16)
        ctk.CTkButton(botones, text="Crear lote", width=130, command=self.crear).pack(side="left")
        self.aviso = ctk.CTkLabel(botones, text="", text_color=estilo.COLOR_AVISO)
        self.aviso.pack(side="left", padx=12)

    # -----------------------------------------------------------------

    def actualizar(self, seleccionar=None):
        seleccion = self.tabla.selection()
        if seleccionar is None and seleccion:
            seleccionar = int(seleccion[0])

        self.producto.cargar([(p["id"], p["nombre"]) for p in bd.listar_productos(self.con)])

        self.tabla.delete(*self.tabla.get_children())
        for l in bd.listar_lotes(self.con, incluir_anulados=True):
            self.tabla.insert(
                "", "end", iid=str(l["id"]),
                values=(l["id"], l["producto"], formato.fecha_a_texto(l["fecha_arribo"]),
                        l["cantidad_comprada"], l["reservado"], l["entregado"],
                        l["disponible"], l["estado"]),
                tags=("anulado",) if l["estado"] == "Anulado" else (),
            )
        if seleccionar is not None and self.tabla.exists(str(seleccionar)):
            self.tabla.selection_set(str(seleccionar))
            self.tabla.see(str(seleccionar))

    def _lote_elegido(self):
        """El lote marcado en la tabla, o None (y avisa) si no hay ninguno."""
        seleccion = self.tabla.selection()
        if not seleccion:
            estilo.avisar(self, "Primero elegí un lote en la tabla.")
            return None
        return bd.obtener_lote(self.con, int(seleccion[0]))

    def _listo(self, lote_id, mensaje):
        """Lo que se hace después de cualquier cambio."""
        self.actualizar(seleccionar=lote_id)
        self.aviso.configure(text=mensaje)
        self.master.datos_cambiaron(self)    # Productos y Reservas muestran lotes

    def crear(self):
        try:
            if self.producto.valor() is None:
                raise ErrorFormato("Primero cargá el producto en la pantalla Productos.")
            cantidad = formato.texto_a_entero(self.cantidad.get())
            arribo = formato.texto_a_fecha(self.arribo.get())
            lote_id = negocio.crear_lote(self.con, self.producto.valor(), cantidad, arribo)
        except (ErrorNegocio, ErrorFormato) as error:
            estilo.avisar(self, error)
            return
        estilo.escribir(self.cantidad, "")
        estilo.escribir(self.arribo, "")
        self._listo(lote_id, f"Lote {lote_id} creado.")

    def cambiar_fecha(self):
        lote = self._lote_elegido()
        if lote is None:
            return
        dialogo = ctk.CTkInputDialog(
            title="Cambiar fecha de arribo",
            text=f"Lote {lote['id']} — {lote['producto']}\n"
                 f"Arribo actual: {formato.fecha_a_texto(lote['fecha_arribo'])}\n\n"
                 "Nueva fecha (dd/mm/aaaa):",
        )
        texto = dialogo.get_input()
        if texto is None:            # tocó Cancelar o cerró el diálogo
            return
        try:
            negocio.cambiar_fecha_lote(self.con, lote["id"], formato.texto_a_fecha(texto))
        except (ErrorNegocio, ErrorFormato) as error:
            estilo.avisar(self, error)
            return
        self._listo(lote["id"], f"Lote {lote['id']}: nueva fecha de arribo {texto.strip()}.")

    def anular(self):
        lote = self._lote_elegido()
        if lote is None:
            return
        pregunta = f"¿Anular el lote {lote['id']} ({lote['producto']})?"
        if lote["reservado"]:
            # Que no sea una sorpresa: decir ANTES qué más va a pasar (RN-07).
            pregunta += (f"\n\nSus reservas pendientes ({lote['reservado']} unidades) "
                         "se van a cancelar.")
        pregunta += "\n\nEsto no se puede deshacer."
        if not estilo.confirmar(self, "Anular lote", pregunta):
            return
        try:
            canceladas = negocio.anular_lote(self.con, lote["id"])
        except ErrorNegocio as error:
            estilo.avisar(self, error)
            return
        self._listo(lote["id"], f"Lote {lote['id']} anulado. Reservas canceladas: {canceladas}.")
