"""
Pruebas de productos (clase 6): lo mínimo de RF-03.
Los nombres repetidos se tratan en la clase 7.
"""

import pytest

from app import bd, negocio
from app.negocio import ErrorNegocio


def test_agregar_producto_empieza_en_cero(con):
    producto_id = negocio.agregar_producto(con, "  Sierra circular ")
    producto = bd.obtener_producto(con, producto_id)
    assert producto["nombre"] == "Sierra circular"
    assert producto["disponible"] == 0
    assert producto["reservado"] == 0


def test_producto_sin_nombre(con):
    with pytest.raises(ErrorNegocio, match="nombre"):
        negocio.agregar_producto(con, "   ")


def test_renombrar_se_ve_en_los_lotes(con):
    # El nombre vive solo en productos (modelo_er.md §4.1).
    negocio.renombrar_producto(con, 1, "Taladro percutor 650W")
    assert bd.obtener_lote(con, 101)["producto"] == "Taladro percutor 650W"


def test_renombrar_un_producto_que_no_existe(con):
    with pytest.raises(ErrorNegocio, match="No existe el producto 999"):
        negocio.renombrar_producto(con, 999, "X")
