"""
Exportar a Excel (clase 7) — RF-12.

Un libro con dos hojas, Lotes y Reservas, listo para que alguien lo abra y
trabaje: fechas que Excel reconoce como fechas, números como números, títulos
fijos al bajar y filtros en cada columna.

Este módulo no abre ventanas ni pregunta dónde guardar: recibe la ruta. Por
eso se puede probar con un test, y la pantalla solo tiene que elegir el
archivo.
"""

from datetime import date

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

from app import bd

# Cada columna: (título, ancho, clave en la fila que devuelve bd).
COLUMNAS_LOTES = [
    ("Lote",        8,  "id"),
    ("Producto",   34,  "producto"),
    ("Arribo",     12,  "fecha_arribo"),
    ("Comprada",   11,  "cantidad_comprada"),
    ("Reservado",  11,  "reservado"),
    ("Entregado",  11,  "entregado"),
    ("Disponible", 11,  "disponible"),
    ("Estado",     10,  "estado"),
]

COLUMNAS_RESERVAS = [
    ("Reserva",       9,  "id"),
    ("Cliente",      30,  "cliente"),
    ("Producto",     30,  "producto"),
    ("Lote",          8,  "lote_id"),
    ("Arribo",       12,  "fecha_arribo"),
    ("Cantidad",     10,  "cantidad"),
    ("Estado",       11,  "estado"),
    ("Reservada el", 13,  "fecha_reserva"),
    ("Entregada el", 13,  "fecha_entrega"),
]

# Columnas que en la base son texto "AAAA-MM-DD" y en Excel tienen que ser
# fechas de verdad (para ordenar, filtrar por mes, restar días…).
FECHAS = {"fecha_arribo", "fecha_reserva", "fecha_entrega"}
FORMATO_FECHA = "DD/MM/YYYY"

TITULO_LETRA = Font(bold=True, color="FFFFFF")
TITULO_FONDO = PatternFill("solid", start_color="3B8ED0")   # el azul de la app


def exportar_excel(con, ruta):
    """Guarda en `ruta` (.xlsx) todos los lotes y todas las reservas.

    Si el archivo está abierto en Excel, Windows no deja reemplazarlo y se
    lanza PermissionError: lo atiende la pantalla.
    """
    libro = Workbook()
    hoja_lotes = libro.active
    hoja_lotes.title = "Lotes"
    _llenar(hoja_lotes, COLUMNAS_LOTES, bd.listar_lotes(con, incluir_anulados=True))
    _llenar(libro.create_sheet("Reservas"), COLUMNAS_RESERVAS, bd.listar_reservas(con))
    libro.save(ruta)


def nombre_sugerido(hoy=None):
    """lotes_y_reservas_2026-11-09.xlsx: con la fecha en formato ISO, los
    archivos de distintos días quedan ordenados en la carpeta."""
    return f"lotes_y_reservas_{(hoy or date.today()).isoformat()}.xlsx"


def _llenar(hoja, columnas, filas):
    # Una sola descripción de columnas (arriba) sirve para títulos, datos,
    # anchos y formatos. El original escribía celda por celda: 'A1', 'B1'…
    hoja.append([titulo for titulo, _, _ in columnas])
    for celda in hoja[1]:
        celda.font = TITULO_LETRA
        celda.fill = TITULO_FONDO
        celda.alignment = Alignment(horizontal="center")

    for fila in filas:
        hoja.append([_valor(fila, clave) for _, _, clave in columnas])

    for numero, (_, ancho, clave) in enumerate(columnas, start=1):
        hoja.column_dimensions[get_column_letter(numero)].width = ancho
        if clave in FECHAS:
            for (celda,) in hoja.iter_rows(min_row=2, min_col=numero, max_col=numero):
                celda.number_format = FORMATO_FECHA

    hoja.freeze_panes = "A2"                 # los títulos quedan fijos al bajar
    hoja.auto_filter.ref = hoja.dimensions   # flechitas de filtro en cada título


def _valor(fila, clave):
    valor = fila[clave]
    if clave in FECHAS and valor:
        return date.fromisoformat(valor)     # fecha de verdad, no texto
    return valor
