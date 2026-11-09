"""
Preparación común a todos los tests.

pytest busca este archivo solo. La "fixture" `con` le da a cada test una base
NUEVA, en memoria, con los datos de ejemplo. Así cada test arranca igual y
ninguno ensucia al siguiente. La base real (reservas.db) no se toca nunca.
"""

import pytest

from app import bd


@pytest.fixture
def con():
    conexion = bd.conectar(":memory:")
    bd.crear_base(conexion, con_datos_ejemplo=True)
    yield conexion          # acá corre el test
    conexion.close()
