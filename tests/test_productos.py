"""
Pruebas de productos: nombre obligatorio (clase 6) y sin repetir (clase 7).
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


@pytest.mark.parametrize("nombre", ["Taladro 650W", "taladro 650w", "  TALADRO 650W "])
def test_no_se_repite_un_nombre(con, nombre):
    antes = len(bd.listar_productos(con))
    with pytest.raises(ErrorNegocio, match="Ya existe el producto «Taladro 650W» \\(Nº 1\\)"):
        negocio.agregar_producto(con, nombre)
    assert len(bd.listar_productos(con)) == antes


def test_no_se_renombra_con_el_nombre_de_otro(con):
    with pytest.raises(ErrorNegocio, match="Ya existe el producto «Amoladora 115mm»"):
        negocio.renombrar_producto(con, 1, "amoladora 115MM")
    assert bd.obtener_producto(con, 1)["nombre"] == "Taladro 650W"


def test_renombrar_corrigiendo_solo_mayusculas(con):
    # "Se repite" consigo mismo: no cuenta.
    negocio.renombrar_producto(con, 1, "TALADRO 650W")
    assert bd.obtener_producto(con, 1)["nombre"] == "TALADRO 650W"


def test_renombrar_un_producto_que_no_existe(con):
    with pytest.raises(ErrorNegocio, match="No existe el producto 999"):
        negocio.renombrar_producto(con, 999, "X")
