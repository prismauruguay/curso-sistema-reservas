"""
Conversión entre lo que se ve en pantalla y lo que usa el programa (clase 6).

    Pantalla          Programa              Base
    "15/11/2026"  ->  date(2026, 11, 15) -> "2026-11-15"
    "12"          ->  12

Las cajas de texto siempre devuelven texto. negocio.py trabaja con fechas y
números de verdad (date, int). Convertir es trabajo de la interfaz, y se hace
acá, en un solo lugar, para que todas las pantallas lo hagan igual.
"""

import re
from datetime import date, datetime


class ErrorFormato(Exception):
    """Lo que escribió el usuario no se puede convertir. El mensaje se muestra
    tal cual, igual que el de ErrorNegocio."""


def fecha_a_texto(valor):
    """date o "2026-11-15" (como viene de la base) -> "15/11/2026"."""
    if not valor:
        return ""
    if isinstance(valor, str):
        valor = date.fromisoformat(valor)
    return valor.strftime("%d/%m/%Y")


def texto_a_fecha(texto):
    """"15/11/2026" -> date(2026, 11, 15). También acepta "5/1/2027"."""
    texto = (texto or "").strip()
    if not texto:
        raise ErrorFormato("Falta completar la fecha.")
    try:
        return datetime.strptime(texto, "%d/%m/%Y").date()
    except ValueError:
        # strptime también rechaza fechas que no existen, como 31/02/2026.
        raise ErrorFormato(
            f"La fecha «{texto}» no es válida. "
            "Tiene que ser día/mes/año, por ejemplo 15/11/2026."
        ) from None


def texto_a_entero(texto, que="La cantidad"):
    """"12" -> 12. `que` es el nombre del dato, para el mensaje de error."""
    texto = (texto or "").strip()
    # Ojo: int() acepta cosas raras como "1_000" o "²". Controlamos antes
    # que sean solo dígitos, con un signo menos opcional.
    if not re.fullmatch(r"-?[0-9]+", texto):
        raise ErrorFormato(f"{que} tiene que ser un número entero, por ejemplo 12.")
    # Un "-3" sí se convierte: que sea mayor que cero lo controla negocio.py
    # (RN-02), con su propio mensaje.
    return int(texto)
