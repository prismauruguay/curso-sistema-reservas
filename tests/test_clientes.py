"""
Pruebas de clientes (clase 5): lo mínimo que pide RF-01.
Los formatos (email, teléfono) se controlan en la clase 7.
"""

import pytest

from app import bd, negocio
from app.negocio import ErrorNegocio


def test_agregar_cliente_limpia_espacios_y_devuelve_el_id(con):
    cliente_id = negocio.agregar_cliente(
        con, "  Ferretería Sur ", " Av. Italia 100", " 099 000 111 ", "  "
    )
    cliente = bd.obtener_cliente(con, cliente_id)
    assert cliente["nombre"] == "Ferretería Sur"
    assert cliente["direccion"] == "Av. Italia 100"
    assert cliente["telefono"] == "099 000 111"
    assert cliente["email"] is None             # email vacío = sin email


def test_faltan_datos_obligatorios(con):
    with pytest.raises(ErrorNegocio, match="Falta completar: dirección, teléfono."):
        negocio.agregar_cliente(con, "Ferretería Sur", "", "   ")


def test_un_cliente_con_datos_faltantes_no_se_guarda(con):
    antes = len(bd.listar_clientes(con))
    with pytest.raises(ErrorNegocio):
        negocio.agregar_cliente(con, "", "Av. Italia 100", "099 000 111")
    assert len(bd.listar_clientes(con)) == antes


def test_modificar_cliente(con):
    negocio.modificar_cliente(con, 2, "Casa Rodríguez e Hijos", "Calle Falsa 123",
                              "2400 1234", "rodriguez@ejemplo.com")
    cliente = bd.obtener_cliente(con, 2)
    assert cliente["nombre"] == "Casa Rodríguez e Hijos"
    assert cliente["email"] == "rodriguez@ejemplo.com"


def test_modificar_no_acepta_borrar_un_dato_obligatorio(con):
    with pytest.raises(ErrorNegocio, match="nombre"):
        negocio.modificar_cliente(con, 2, "", "Calle Falsa 123", "2400 1234")
    assert bd.obtener_cliente(con, 2)["nombre"] == "Casa Rodríguez"


def test_modificar_un_cliente_que_no_existe(con):
    with pytest.raises(ErrorNegocio, match="No existe el cliente 999"):
        negocio.modificar_cliente(con, 999, "X", "Y", "Z")
