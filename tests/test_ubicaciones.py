"""
Pruebas de ubicaciones (clase 8): dónde van los archivos.
"""

from app import ubicaciones


def test_en_desarrollo_todo_esta_en_el_proyecto(monkeypatch):
    monkeypatch.delenv("RESERVAS_CARPETA", raising=False)
    proyecto = ubicaciones.carpeta_programa()
    assert (proyecto / "datos" / "esquema.sql").exists()
    assert ubicaciones.carpeta_usuario() == proyecto


def test_la_variable_elige_la_carpeta_de_datos_y_la_crea(monkeypatch, tmp_path):
    destino = tmp_path / "otra" / "carpeta"
    monkeypatch.setenv("RESERVAS_CARPETA", str(destino))
    assert ubicaciones.carpeta_usuario() == destino
    assert destino.is_dir()
