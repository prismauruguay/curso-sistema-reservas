"""
Pruebas de clientes: datos obligatorios (clase 5) y formato de teléfono y
email (clase 7).
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


# ---------------------------------------------------------------------
#  Formatos (clase 7). Importa tanto lo que se RECHAZA como lo que se
#  ACEPTA: una validación que rechaza datos reales es un error.
# ---------------------------------------------------------------------

@pytest.mark.parametrize("telefono", [
    "099 123 456", "2400 1234", "2400-1234", "+598 99 123 456", "(02) 400 1234", "099123456",
])
def test_telefonos_validos(con, telefono):
    cliente_id = negocio.agregar_cliente(con, "Bazar 18", "18 de Julio 1234", telefono)
    assert bd.obtener_cliente(con, cliente_id)["telefono"] == telefono


@pytest.mark.parametrize("telefono", ["099 123 45a", "12345", "tel: 2400 1234", "099/123/456"])
def test_telefonos_invalidos(con, telefono):
    with pytest.raises(ErrorNegocio, match="teléfono"):
        negocio.agregar_cliente(con, "Bazar 18", "18 de Julio 1234", telefono)


@pytest.mark.parametrize("email", [
    "ventas@empresa.com.uy", "juan.perez+compras@mail.com", "compras@ferretería.uy", "a@b.co",
])
def test_emails_validos(con, email):
    cliente_id = negocio.agregar_cliente(con, "Pérez & Hijos", "Ruta 8 km 20", "094 555 010", email)
    assert bd.obtener_cliente(con, cliente_id)["email"] == email


@pytest.mark.parametrize("email", [
    "ventas", "ventas@empresa", "ventas@@empresa.com", "ventas @empresa.com",
    "@empresa.com", "ventas@empresa.", "ventas@empresa.com.",
])
def test_emails_invalidos(con, email):
    with pytest.raises(ErrorNegocio, match="email"):
        negocio.agregar_cliente(con, "Pérez & Hijos", "Ruta 8 km 20", "094 555 010", email)


def test_los_datos_de_ejemplo_siguen_siendo_validos(con):
    # Si una validación nueva rechazara datos que ya están en la base, el
    # usuario no podría ni corregir otro campo del cliente sin "arreglar" ese.
    for c in bd.listar_clientes(con):
        negocio.modificar_cliente(con, c["id"], c["nombre"], c["direccion"],
                                  c["telefono"], c["email"])
