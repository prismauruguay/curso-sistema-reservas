"""
Reglas del negocio (clase 4).

Este módulo decide QUÉ se puede hacer. No escribe SQL (eso es de bd.py) y no
muestra ventanas (eso es de la interfaz, clase 5). Por eso se puede probar
entero con tests, sin abrir nada.

Cómo avisa que algo no se puede: lanza ErrorNegocio con un mensaje pensado
para el usuario ("No hay stock suficiente: quedan 3"). La interfaz solo tiene
que mostrar ese texto (RNF-04).

Cada función sigue el mismo orden:
    1. Buscar lo que hace falta (el lote, la reserva…).
    2. Controlar las reglas, una por una, con su número (RN-xx).
    3. Recién entonces, guardar.

Comparar con el sistema original: cada operación tenía que acordarse de
actualizar a mano cantidad_disponible, cantidad_reservada, stock_disponible y
stock_reservado. Acá ninguna función toca un total: las vistas los calculan.
"""

from datetime import date

from app import bd


class ErrorNegocio(Exception):
    """Algo que el usuario intentó hacer y las reglas no permiten.

    El mensaje se muestra tal cual en pantalla: tiene que ser claro y no
    técnico.
    """


# ---------------------------------------------------------------------
#  Clientes (clase 5)
#
#  Por ahora solo lo que pide RF-01: nombre, dirección y teléfono son
#  obligatorios, el email no. Controlar formatos (email válido, teléfono)
#  queda para la clase 7.
# ---------------------------------------------------------------------

def agregar_cliente(con, nombre, direccion, telefono, email=""):
    """RF-01. Devuelve el id que le asignó la base."""
    datos = _datos_cliente(nombre, direccion, telefono, email)
    return bd.agregar_cliente(con, **datos)


def modificar_cliente(con, cliente_id, nombre, direccion, telefono, email=""):
    """RF-02."""
    if bd.obtener_cliente(con, cliente_id) is None:
        raise ErrorNegocio(f"No existe el cliente {cliente_id}.")
    datos = _datos_cliente(nombre, direccion, telefono, email)
    bd.modificar_cliente(con, cliente_id, **datos)


def _datos_cliente(nombre, direccion, telefono, email):
    """Limpia lo que escribió el usuario y controla que no falte nada."""
    datos = {
        "nombre": (nombre or "").strip(),
        "direccion": (direccion or "").strip(),
        "telefono": (telefono or "").strip(),
        "email": (email or "").strip() or None,     # vacío -> sin email
    }
    faltan = [campo for campo in ("nombre", "direccion", "telefono") if not datos[campo]]
    if faltan:
        nombres = {"nombre": "nombre", "direccion": "dirección", "telefono": "teléfono"}
        raise ErrorNegocio("Falta completar: " + ", ".join(nombres[c] for c in faltan) + ".")
    return datos


# ---------------------------------------------------------------------
#  Lotes
# ---------------------------------------------------------------------

def crear_lote(con, producto_id, cantidad, fecha_arribo):
    """RF-05. Registra un lote que viene en camino. Devuelve su id."""
    _controlar_cantidad(cantidad)
    if bd.obtener_producto(con, producto_id) is None:
        raise ErrorNegocio("El producto elegido no existe.")
    return bd.agregar_lote(con, producto_id, cantidad, fecha_arribo.isoformat())


def cambiar_fecha_lote(con, lote_id, nueva_fecha):
    """RF-06. El envío se atrasó (o se adelantó)."""
    lote = _buscar_lote(con, lote_id)
    if lote["estado"] == "Anulado":
        raise ErrorNegocio("El lote está anulado: no se puede cambiar su fecha.")
    # RN-09: regla que apareció al programar (ver docs/requisitos.md).
    if lote["entregado"] > 0:
        raise ErrorNegocio(
            "Este lote ya tiene entregas: la mercadería llegó, "
            "no se puede cambiar la fecha de arribo."
        )
    bd.cambiar_fecha_lote(con, lote_id, nueva_fecha.isoformat())


def anular_lote(con, lote_id):
    """RF-07. La compra se cayó. Devuelve cuántas reservas se cancelaron."""
    lote = _buscar_lote(con, lote_id)
    if lote["estado"] == "Anulado":
        raise ErrorNegocio("El lote ya estaba anulado.")
    # RN-06
    if lote["entregado"] > 0:
        raise ErrorNegocio(
            f"No se puede anular el lote {lote_id}: ya se entregaron "
            f"{lote['entregado']} unidades."
        )
    # RN-07: bd.anular_lote cancela las reservas pendientes en la misma
    # transacción.
    return bd.anular_lote(con, lote_id)


# ---------------------------------------------------------------------
#  Reservas
# ---------------------------------------------------------------------

def reservar(con, cliente_id, lote_id, cantidad, hoy=None):
    """RF-08. Aparta unidades de un lote para un cliente. Devuelve el id."""
    hoy = hoy or date.today()
    _controlar_cantidad(cantidad)                                   # RN-02
    if bd.obtener_cliente(con, cliente_id) is None:
        raise ErrorNegocio("El cliente elegido no existe.")
    lote = _buscar_lote(con, lote_id)
    if lote["estado"] == "Anulado":
        raise ErrorNegocio(f"El lote {lote_id} está anulado: no se puede reservar.")
    # RN-01
    if cantidad > lote["disponible"]:
        raise ErrorNegocio(
            f"No hay stock suficiente en el lote {lote_id}: "
            f"quedan {lote['disponible']}."
        )
    return bd.agregar_reserva(con, cliente_id, lote_id, cantidad, hoy.isoformat())


def entregar(con, reserva_id, hoy=None):
    """RF-09. El cliente retiró la mercadería."""
    hoy = hoy or date.today()
    reserva = _buscar_reserva(con, reserva_id)
    if reserva["estado"] == "Entregado":
        raise ErrorNegocio(f"La reserva {reserva_id} ya fue entregada.")
    if reserva["estado"] == "Cancelado":
        raise ErrorNegocio(f"La reserva {reserva_id} está cancelada: no se puede entregar.")
    # RN-03
    arribo = date.fromisoformat(reserva["fecha_arribo"])
    if hoy < arribo:
        raise ErrorNegocio(
            f"La mercadería todavía no llegó: el lote arriba el {_mostrar(arribo)}."
        )
    bd.marcar_entregada(con, reserva_id, hoy.isoformat())


def cancelar(con, reserva_id):
    """RF-10. El cliente ya no la quiere.

    RN-05 (devolver las unidades a disponible) no necesita código: la vista
    v_lotes deja de contar las reservas canceladas.
    """
    reserva = _buscar_reserva(con, reserva_id)
    # RN-04
    if reserva["estado"] == "Entregado":
        raise ErrorNegocio(
            f"La reserva {reserva_id} ya fue entregada: la mercadería salió, "
            "no se puede cancelar."
        )
    if reserva["estado"] == "Cancelado":
        raise ErrorNegocio(f"La reserva {reserva_id} ya estaba cancelada.")
    bd.marcar_cancelada(con, reserva_id)


# ---------------------------------------------------------------------
#  Ayudantes (el _ adelante indica que son de uso interno del módulo)
# ---------------------------------------------------------------------

def _controlar_cantidad(cantidad):
    # bool es un tipo de int en Python (True == 1): lo excluimos a propósito.
    if not isinstance(cantidad, int) or isinstance(cantidad, bool):
        raise ErrorNegocio("La cantidad tiene que ser un número entero.")
    if cantidad <= 0:
        raise ErrorNegocio("La cantidad tiene que ser mayor que cero.")


def _buscar_lote(con, lote_id):
    lote = bd.obtener_lote(con, lote_id)
    if lote is None:
        raise ErrorNegocio(f"No existe el lote {lote_id}.")
    return lote


def _buscar_reserva(con, reserva_id):
    reserva = bd.obtener_reserva(con, reserva_id)
    if reserva is None:
        raise ErrorNegocio(f"No existe la reserva {reserva_id}.")
    return reserva


def _mostrar(fecha):
    """La base guarda 2026-11-15; al usuario le mostramos 15/11/2026."""
    return fecha.strftime("%d/%m/%Y")
