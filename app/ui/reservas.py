"""
Pantalla de Reservas (clase 6) — RF-08 a RF-11.

Tres zonas, como en el boceto:
  - Filtros arriba (RF-11).
  - La tabla, con Entregar y Cancelar para la reserva ELEGIDA en ella.
  - El formulario de abajo, para una reserva NUEVA.

Producto y fecha de arribo se muestran, pero no están guardados en la
reserva: bd.listar_reservas los trae del lote (modelo_er.md §4.1).
"""

import customtkinter as ctk

from app import bd, negocio
from app.negocio import ErrorNegocio
from app.ui import estilo, formato
from app.ui.formato import ErrorFormato

COLUMNAS = [
    ("id",        "Nº",         50, "center"),
    ("cliente",   "Cliente",   190, "w"),
    ("producto",  "Producto",  180, "w"),
    ("lote",      "Lote",       60, "center"),
    ("arribo",    "Arribo",    100, "center"),
    ("cantidad",  "Cant.",      60, "e"),
    ("estado",    "Estado",    100, "center"),
]

TODOS = (None, "Todos")


class VentanaReservas(ctk.CTkToplevel):

    def __init__(self, master, con):
        super().__init__(master)
        self.con = con

        self.title("Reservas")
        self.geometry("960x660")
        self.minsize(900, 580)
        self.transient(master)

        self._armar_filtros()
        marco, self.tabla = estilo.tabla(self, COLUMNAS, alto=11)
        marco.pack(fill="both", expand=True, padx=16)
        self.tabla.tag_configure("Cancelado", foreground=estilo.COLOR_APAGADO)

        acciones = ctk.CTkFrame(self, fg_color="transparent")
        acciones.pack(fill="x", padx=16, pady=(8, 0))
        ctk.CTkLabel(acciones, text="Reserva elegida:").pack(side="left", padx=(0, 8))
        ctk.CTkButton(acciones, text="Entregar", width=130,
                      command=self.entregar).pack(side="left")
        ctk.CTkButton(acciones, text="Cancelar reserva", width=130, fg_color="#C0392B",
                      hover_color="#962D22", command=self.cancelar).pack(side="left", padx=8)

        self._armar_formulario()
        self.actualizar()

    # -----------------------------------------------------------------
    #  Armado
    # -----------------------------------------------------------------

    def _armar_filtros(self):
        fila = ctk.CTkFrame(self, fg_color="transparent")
        fila.pack(fill="x", padx=16, pady=(16, 8))
        recargar = self.actualizar_tabla

        ctk.CTkLabel(fila, text="Cliente:").pack(side="left", padx=(0, 6))
        self.filtro_cliente = estilo.Selector(fila, width=210, al_cambiar=recargar)
        self.filtro_cliente.pack(side="left")
        # El boceto no tenía este filtro, pero RF-11 lo pide (ver docs/interfaz_2.md).
        ctk.CTkLabel(fila, text="Producto:").pack(side="left", padx=(14, 6))
        self.filtro_producto = estilo.Selector(fila, width=210, al_cambiar=recargar)
        self.filtro_producto.pack(side="left")
        ctk.CTkLabel(fila, text="Estado:").pack(side="left", padx=(14, 6))
        self.filtro_estado = estilo.Selector(fila, width=130, al_cambiar=recargar)
        self.filtro_estado.pack(side="left")
        # Para el estado, el "id" es el mismo texto que se guarda en la base.
        self.filtro_estado.cargar([TODOS] + [(e, e) for e in ("Reservado", "Entregado", "Cancelado")])

    def _armar_formulario(self):
        marco = ctk.CTkFrame(self)
        marco.pack(fill="x", padx=16, pady=(12, 0))
        ctk.CTkLabel(marco, text="Nueva reserva", font=ctk.CTkFont(weight="bold")).grid(
            row=0, column=0, columnspan=6, sticky="w", padx=10, pady=(8, 2))

        ctk.CTkLabel(marco, text="Cliente:").grid(row=1, column=0, sticky="e", padx=(10, 6), pady=8)
        self.cliente = estilo.Selector(marco, vacio="(no hay clientes)", width=220)
        self.cliente.grid(row=1, column=1, sticky="w", pady=8)

        ctk.CTkLabel(marco, text="Lote:").grid(row=1, column=2, sticky="e", padx=(14, 6), pady=8)
        self.lote = estilo.Selector(marco, vacio="(no hay lotes con disponible)", width=330,
                                    al_cambiar=self._mostrar_disponible)
        self.lote.grid(row=1, column=3, sticky="w", pady=8)

        self.cantidad = estilo.campo(marco, "Cantidad:", 1, 4, ancho=70)
        self.cantidad.bind("<Return>", lambda _evento: self.reservar())

        self.disponible = ctk.CTkLabel(marco, text="", text_color="gray40")
        self.disponible.grid(row=2, column=3, sticky="w", pady=(0, 8))

        botones = ctk.CTkFrame(self, fg_color="transparent")
        botones.pack(fill="x", padx=16, pady=16)
        ctk.CTkButton(botones, text="Reservar", width=130, command=self.reservar).pack(side="left")
        self.aviso = ctk.CTkLabel(botones, text="", text_color=estilo.COLOR_AVISO)
        self.aviso.pack(side="left", padx=12)

    # -----------------------------------------------------------------
    #  Datos
    # -----------------------------------------------------------------

    def actualizar(self, seleccionar=None):
        """Recarga listas desplegables y tabla. La llaman esta pantalla y el
        menú, cuando otra pantalla cambió clientes, productos o lotes."""
        clientes = [(c["id"], f"{c['nombre']} (Nº {c['id']})") for c in bd.listar_clientes(self.con)]
        productos = [(p["id"], p["nombre"]) for p in bd.listar_productos(self.con)]
        self.filtro_cliente.cargar([TODOS] + clientes)
        self.filtro_producto.cargar([TODOS] + productos)
        self.cliente.cargar(clientes)

        # Solo se ofrecen lotes de los que se puede reservar algo. La regla
        # RN-01 la sigue controlando negocio.py: esto es comodidad, no control.
        self.lote.cargar([
            (l["id"], f"{l['id']} · {l['producto']} · arribo {formato.fecha_a_texto(l['fecha_arribo'])}")
            for l in bd.listar_lotes(self.con) if l["disponible"] > 0
        ])
        self._mostrar_disponible()
        self.actualizar_tabla(seleccionar)

    def actualizar_tabla(self, seleccionar=None):
        seleccion = self.tabla.selection()
        if seleccionar is None and seleccion:
            seleccionar = int(seleccion[0])

        self.tabla.delete(*self.tabla.get_children())
        for r in bd.listar_reservas(self.con, cliente_id=self.filtro_cliente.valor(),
                                    producto_id=self.filtro_producto.valor(),
                                    estado=self.filtro_estado.valor()):
            self.tabla.insert(
                "", "end", iid=str(r["id"]),
                values=(r["id"], r["cliente"], r["producto"], r["lote_id"],
                        formato.fecha_a_texto(r["fecha_arribo"]), r["cantidad"], r["estado"]),
                tags=(r["estado"],),
            )
        if seleccionar is not None and self.tabla.exists(str(seleccionar)):
            self.tabla.selection_set(str(seleccionar))
            self.tabla.see(str(seleccionar))

    def _mostrar_disponible(self):
        lote_id = self.lote.valor()
        texto = ""
        if lote_id is not None:
            texto = f"Disponible en el lote: {bd.obtener_lote(self.con, lote_id)['disponible']}"
        self.disponible.configure(text=texto)

    # -----------------------------------------------------------------
    #  Acciones
    # -----------------------------------------------------------------

    def _listo(self, reserva_id, mensaje):
        self.actualizar(seleccionar=reserva_id)
        self.aviso.configure(text=mensaje)
        self.master.datos_cambiaron(self)    # Productos y Lotes muestran totales

    def reservar(self):
        try:
            if self.cliente.valor() is None:
                raise ErrorFormato("Elegí un cliente.")
            if self.lote.valor() is None:
                raise ErrorFormato("Elegí un lote.")
            cantidad = formato.texto_a_entero(self.cantidad.get())
            reserva_id = negocio.reservar(self.con, self.cliente.valor(),
                                          self.lote.valor(), cantidad)
        except (ErrorNegocio, ErrorFormato) as error:
            estilo.avisar(self, error)
            return
        estilo.escribir(self.cantidad, "")
        self._listo(reserva_id, f"Reserva Nº {reserva_id} registrada.")

    def _reserva_elegida(self):
        """(id, descripción) de la reserva marcada, o None si no hay."""
        seleccion = self.tabla.selection()
        if not seleccion:
            estilo.avisar(self, "Primero elegí una reserva en la tabla.")
            return None
        valores = self.tabla.item(seleccion[0], "values")
        # valores: (id, cliente, producto, lote, arribo, cantidad, estado)
        descripcion = f"Nº {valores[0]}: {valores[5]} × {valores[2]} para {valores[1]}"
        return int(valores[0]), descripcion

    def entregar(self):
        elegida = self._reserva_elegida()
        if elegida is None:
            return
        reserva_id, descripcion = elegida
        if not estilo.confirmar(self, "Entregar", f"¿Entregar la reserva {descripcion}?"):
            return
        try:
            negocio.entregar(self.con, reserva_id)
        except ErrorNegocio as error:
            estilo.avisar(self, error)
            return
        self._listo(reserva_id, f"Reserva Nº {reserva_id} entregada.")

    def cancelar(self):
        elegida = self._reserva_elegida()
        if elegida is None:
            return
        reserva_id, descripcion = elegida
        pregunta = (f"¿Cancelar la reserva {descripcion}?\n\n"
                    "Las unidades vuelven a quedar disponibles. Esto no se puede deshacer.")
        if not estilo.confirmar(self, "Cancelar reserva", pregunta):
            return
        try:
            negocio.cancelar(self.con, reserva_id)
        except ErrorNegocio as error:
            estilo.avisar(self, error)
            return
        self._listo(reserva_id, f"Reserva Nº {reserva_id} cancelada.")
