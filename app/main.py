"""
Punto de entrada del programa (clase 5).

Correr desde la carpeta del proyecto, con el entorno activado:
    python -m app.main
"""

from app import bd
from app.ui import estilo
from app.ui.principal import VentanaPrincipal


def main():
    con = bd.conectar()
    if not bd.base_creada(con):
        # Primera vez en una PC nueva: base vacía, sin datos de ejemplo.
        bd.crear_base(con)

    estilo.preparar()
    try:
        VentanaPrincipal(con).mainloop()
    finally:
        # Se cierre como se cierre la ventana (Salir, la X o un error),
        # la base se cierra bien.
        con.close()


if __name__ == "__main__":
    main()
