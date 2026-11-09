"""
Pruebas de las reglas de negocio (clase 4).

Cada test es un caso concreto: "si hago ESTO, tiene que pasar AQUELLO".
Están agrupados por regla, con el mismo número que en docs/requisitos.md.

Los datos de partida son los de datos/datos_ejemplo.sql:

    Lote 101  Taladro          50 u.  arriba 15/11/2026  reserva 1: 10 pendientes
    Lote 102  Amoladora        25 u.  arriba 02/12/2026  reserva 2: 25 pendientes (agotado)
    Lote 103  Taladro          30 u.  llegó  10/09/2026  reserva 3: 12 entregadas
                                                         reserva 4:  8 pendientes
                                                         reserva 5:  5 canceladas
    Lote 104  Destornilladores 100 u. llegó  20/10/2026  reserva 6: 30 pendientes
    Lote 105  Escalera         ANULADO                   reserva 7: cancelada

Correrlos (desde la carpeta del proyecto, con el entorno activado):
    pytest
"""

from datetime import date

import pytest

from app import bd, negocio
from app.negocio import ErrorNegocio

# "Hoy", fijo: el lote 103 ya llegó, el 101 todavía no.
HOY = date(2026, 11, 1)


def disponible(con, lote_id):
    return bd.obtener_lote(con, lote_id)["disponible"]


def estado_reserva(con, reserva_id):
    return bd.obtener_reserva(con, reserva_id)["estado"]


# ---------------------------------------------------------------------
#  Reservar (RF-08)
# ---------------------------------------------------------------------

def test_reservar_descuenta_del_disponible(con):
    reserva_id = negocio.reservar(con, cliente_id=2, lote_id=101, cantidad=15, hoy=HOY)

    assert disponible(con, 101) == 40 - 15
    reserva = bd.obtener_reserva(con, reserva_id)
    assert reserva["estado"] == "Reservado"
    assert reserva["fecha_reserva"] == "2026-11-01"


def test_rn01_no_se_puede_reservar_mas_de_lo_disponible(con):
    with pytest.raises(ErrorNegocio, match="quedan 40"):
        negocio.reservar(con, cliente_id=2, lote_id=101, cantidad=41, hoy=HOY)
    assert disponible(con, 101) == 40          # no se guardó nada


def test_rn01_se_puede_reservar_exactamente_lo_disponible(con):
    negocio.reservar(con, cliente_id=2, lote_id=101, cantidad=40, hoy=HOY)
    assert disponible(con, 101) == 0


def test_rn01_lote_agotado(con):
    with pytest.raises(ErrorNegocio, match="quedan 0"):
        negocio.reservar(con, cliente_id=1, lote_id=102, cantidad=1, hoy=HOY)


# Un mismo test, probado con varios valores malos.
@pytest.mark.parametrize("cantidad", [0, -3, 2.5, "5", None, True])
def test_rn02_la_cantidad_tiene_que_ser_un_entero_positivo(con, cantidad):
    with pytest.raises(ErrorNegocio):
        negocio.reservar(con, cliente_id=1, lote_id=101, cantidad=cantidad, hoy=HOY)


def test_no_se_reserva_en_un_lote_anulado(con):
    with pytest.raises(ErrorNegocio, match="anulado"):
        negocio.reservar(con, cliente_id=1, lote_id=105, cantidad=1, hoy=HOY)


def test_no_se_reserva_en_un_lote_que_no_existe(con):
    with pytest.raises(ErrorNegocio, match="No existe el lote 999"):
        negocio.reservar(con, cliente_id=1, lote_id=999, cantidad=1, hoy=HOY)


def test_no_se_reserva_para_un_cliente_que_no_existe(con):
    with pytest.raises(ErrorNegocio, match="cliente"):
        negocio.reservar(con, cliente_id=999, lote_id=101, cantidad=1, hoy=HOY)


# ---------------------------------------------------------------------
#  Entregar (RF-09)
# ---------------------------------------------------------------------

def test_entregar_pasa_de_reservado_a_entregado(con):
    negocio.entregar(con, reserva_id=4, hoy=HOY)

    reserva = bd.obtener_reserva(con, 4)
    assert reserva["estado"] == "Entregado"
    assert reserva["fecha_entrega"] == "2026-11-01"

    lote = bd.obtener_lote(con, 103)
    assert lote["reservado"] == 0
    assert lote["entregado"] == 12 + 8
    assert lote["disponible"] == 10            # entregar no cambia lo disponible


def test_rn03_no_se_entrega_antes_de_que_llegue_el_lote(con):
    # Reserva 1 es del lote 101, que arriba el 15/11/2026.
    with pytest.raises(ErrorNegocio, match="15/11/2026"):
        negocio.entregar(con, reserva_id=1, hoy=HOY)
    assert estado_reserva(con, 1) == "Reservado"


def test_rn03_se_entrega_el_mismo_dia_que_llega(con):
    negocio.entregar(con, reserva_id=1, hoy=date(2026, 11, 15))
    assert estado_reserva(con, 1) == "Entregado"


def test_no_se_entrega_dos_veces(con):
    with pytest.raises(ErrorNegocio, match="ya fue entregada"):
        negocio.entregar(con, reserva_id=3, hoy=HOY)


def test_no_se_entrega_una_reserva_cancelada(con):
    with pytest.raises(ErrorNegocio, match="cancelada"):
        negocio.entregar(con, reserva_id=5, hoy=HOY)


# ---------------------------------------------------------------------
#  Cancelar (RF-10)
# ---------------------------------------------------------------------

def test_rn05_cancelar_devuelve_las_unidades(con):
    negocio.cancelar(con, reserva_id=1)

    assert estado_reserva(con, 1) == "Cancelado"
    assert disponible(con, 101) == 50          # volvieron las 10


def test_rn04_no_se_cancela_una_reserva_entregada(con):
    with pytest.raises(ErrorNegocio, match="ya fue entregada"):
        negocio.cancelar(con, reserva_id=3)
    assert estado_reserva(con, 3) == "Entregado"


def test_no_se_cancela_dos_veces(con):
    with pytest.raises(ErrorNegocio, match="ya estaba cancelada"):
        negocio.cancelar(con, reserva_id=5)


def test_no_se_cancela_una_reserva_que_no_existe(con):
    with pytest.raises(ErrorNegocio, match="No existe la reserva 999"):
        negocio.cancelar(con, reserva_id=999)


# ---------------------------------------------------------------------
#  Lotes (RF-05, RF-06, RF-07)
# ---------------------------------------------------------------------

def test_crear_lote_queda_todo_disponible(con):
    lote_id = negocio.crear_lote(con, producto_id=5, cantidad=12,
                                 fecha_arribo=date(2027, 1, 10))
    lote = bd.obtener_lote(con, lote_id)
    assert lote["producto"] == "Lijadora orbital"
    assert lote["fecha_arribo"] == "2027-01-10"
    assert lote["disponible"] == 12


def test_crear_lote_de_un_producto_que_no_existe(con):
    with pytest.raises(ErrorNegocio, match="producto"):
        negocio.crear_lote(con, producto_id=999, cantidad=12, fecha_arribo=date(2027, 1, 10))


def test_crear_lote_con_cantidad_cero(con):
    with pytest.raises(ErrorNegocio, match="mayor que cero"):
        negocio.crear_lote(con, producto_id=1, cantidad=0, fecha_arribo=date(2027, 1, 10))


def test_cambiar_fecha_se_ve_en_las_reservas(con):
    # La fecha vive SOLO en el lote (modelo_er.md §4.1): al cambiarla ahí,
    # todas sus reservas la ven cambiada, sin tocarlas.
    negocio.cambiar_fecha_lote(con, 101, date(2026, 12, 20))

    reservas_del_lote = [r for r in bd.listar_reservas(con) if r["lote_id"] == 101]
    assert reservas_del_lote
    assert all(r["fecha_arribo"] == "2026-12-20" for r in reservas_del_lote)


def test_rn09_no_se_cambia_la_fecha_de_un_lote_con_entregas(con):
    with pytest.raises(ErrorNegocio, match="ya tiene entregas"):
        negocio.cambiar_fecha_lote(con, 103, date(2026, 12, 20))


def test_rn07_anular_lote_cancela_sus_reservas_pendientes(con):
    canceladas = negocio.anular_lote(con, 101)

    assert canceladas == 1
    assert bd.obtener_lote(con, 101)["estado"] == "Anulado"
    assert estado_reserva(con, 1) == "Cancelado"


def test_rn07_el_lote_anulado_no_suma_al_producto(con):
    # Taladro: lote 101 (40 disp / 10 res) + lote 103 (10 disp / 8 res)
    negocio.anular_lote(con, 101)

    taladro = bd.obtener_producto(con, 1)
    assert taladro["disponible"] == 10
    assert taladro["reservado"] == 8


def test_rn06_no_se_anula_un_lote_con_entregas(con):
    with pytest.raises(ErrorNegocio, match="ya se entregaron 12"):
        negocio.anular_lote(con, 103)
    assert bd.obtener_lote(con, 103)["estado"] == "Activo"
    assert estado_reserva(con, 4) == "Reservado"   # no quedó nada a medias


def test_no_se_anula_dos_veces(con):
    with pytest.raises(ErrorNegocio, match="ya estaba anulado"):
        negocio.anular_lote(con, 105)


def test_rn08_nada_se_borra(con):
    antes = len(bd.listar_reservas(con))
    negocio.anular_lote(con, 104)
    negocio.cancelar(con, 1)
    assert len(bd.listar_reservas(con)) == antes
