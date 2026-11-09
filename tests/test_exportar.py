"""
Pruebas de la exportación a Excel (clase 7) — RF-12.

Se exporta a una carpeta temporal (tmp_path, la da pytest) y se vuelve a abrir
el archivo con openpyxl para revisar lo que quedó adentro.
"""

from datetime import date, datetime

from openpyxl import load_workbook

from app import exportar, negocio


def exportar_y_abrir(con, tmp_path):
    ruta = tmp_path / "prueba.xlsx"
    exportar.exportar_excel(con, ruta)
    return load_workbook(ruta)


def filas(hoja):
    return list(hoja.iter_rows(values_only=True))


def test_dos_hojas_con_todos_los_datos(con, tmp_path):
    libro = exportar_y_abrir(con, tmp_path)
    assert libro.sheetnames == ["Lotes", "Reservas"]
    # 5 lotes (incluido el anulado) y 7 reservas, más la fila de títulos.
    assert libro["Lotes"].max_row == 1 + 5
    assert libro["Reservas"].max_row == 1 + 7


def test_titulos(con, tmp_path):
    libro = exportar_y_abrir(con, tmp_path)
    assert filas(libro["Lotes"])[0] == (
        "Lote", "Producto", "Arribo", "Comprada", "Reservado", "Entregado", "Disponible", "Estado",
    )


def test_los_totales_son_los_de_la_pantalla(con, tmp_path):
    libro = exportar_y_abrir(con, tmp_path)
    por_lote = {f[0]: f for f in filas(libro["Lotes"])[1:]}
    # Lote 103: 30 comprados, 8 reservados, 12 entregados -> 10 disponibles
    assert por_lote[103][3:] == (30, 8, 12, 10, "Activo")
    assert por_lote[105][7] == "Anulado"


def test_las_fechas_son_fechas_y_no_texto(con, tmp_path):
    hoja = exportar_y_abrir(con, tmp_path)["Lotes"]
    celda = hoja["C2"]                      # Arribo del primer lote
    assert isinstance(celda.value, datetime)
    assert celda.number_format == "DD/MM/YYYY"


def test_reserva_sin_entregar_deja_la_fecha_vacia(con, tmp_path):
    hoja = exportar_y_abrir(con, tmp_path)["Reservas"]
    por_reserva = {f[0]: f for f in filas(hoja)[1:]}
    assert por_reserva[1][8] is None                          # pendiente
    assert por_reserva[3][8] == datetime(2026, 9, 12)         # entregada


def test_refleja_los_cambios(con, tmp_path):
    negocio.cancelar(con, 1)
    hoja = exportar_y_abrir(con, tmp_path)["Reservas"]
    assert {f[0]: f for f in filas(hoja)[1:]}[1][6] == "Cancelado"


def test_titulos_fijos_y_filtros(con, tmp_path):
    hoja = exportar_y_abrir(con, tmp_path)["Reservas"]
    assert hoja.freeze_panes == "A2"
    assert hoja.auto_filter.ref == "A1:I8"


def test_nombre_sugerido():
    assert exportar.nombre_sugerido(date(2026, 11, 9)) == "lotes_y_reservas_2026-11-09.xlsx"
