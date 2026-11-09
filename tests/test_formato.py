"""
Pruebas de las conversiones de pantalla (clase 6).
No usan la base: son funciones que reciben texto y devuelven datos.
"""

from datetime import date

import pytest

from app.ui.formato import ErrorFormato, fecha_a_texto, texto_a_entero, texto_a_fecha


def test_fecha_a_texto():
    assert fecha_a_texto("2026-11-15") == "15/11/2026"     # como viene de la base
    assert fecha_a_texto(date(2027, 1, 5)) == "05/01/2027"
    assert fecha_a_texto(None) == ""                       # sin fecha de entrega


@pytest.mark.parametrize("texto, esperado", [
    ("15/11/2026", date(2026, 11, 15)),
    ("  15/11/2026 ", date(2026, 11, 15)),
    ("5/1/2027", date(2027, 1, 5)),
    ("29/02/2028", date(2028, 2, 29)),                     # 2028 es bisiesto
])
def test_texto_a_fecha(texto, esperado):
    assert texto_a_fecha(texto) == esperado


@pytest.mark.parametrize("texto", ["", "   ", "2026-11-15", "15-11-2026",
                                   "31/02/2026", "29/02/2027", "15/13/2026", "mañana"])
def test_texto_a_fecha_rechaza(texto):
    with pytest.raises(ErrorFormato):
        texto_a_fecha(texto)


def test_la_fecha_que_no_existe_se_nombra_en_el_mensaje():
    with pytest.raises(ErrorFormato, match="31/02/2026"):
        texto_a_fecha("31/02/2026")


@pytest.mark.parametrize("texto, esperado", [("12", 12), (" 12 ", 12), ("0", 0), ("-3", -3)])
def test_texto_a_entero(texto, esperado):
    assert texto_a_entero(texto) == esperado


@pytest.mark.parametrize("texto", ["", "doce", "2.5", "1,000", "1_000", "²", "12a"])
def test_texto_a_entero_rechaza(texto):
    with pytest.raises(ErrorFormato, match="La cantidad tiene que ser un número entero"):
        texto_a_entero(texto)
