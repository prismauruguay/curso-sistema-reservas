# Receta de PyInstaller para armar el programa (clase 8).
#
#   pyinstaller SistemaReservas.spec --noconfirm
#
# Resultado: dist/SistemaReservas/SistemaReservas.exe (y su carpeta _internal).
# Ver docs/entrega.md para el porqué de cada decisión.

from PyInstaller.utils.hooks import collect_data_files

a = Analysis(
    ["app/main.py"],
    pathex=["."],                  # para que encuentre el paquete `app`
    datas=[
        # Lo que el programa lee de disco y no es código Python:
        ("datos/esquema.sql", "datos"),        # para crear la base en una PC nueva
        *collect_data_files("customtkinter"),  # temas y fuentes de CustomTkinter
    ],
    # Lo que se usa para desarrollar, no para correr el programa.
    excludes=["pytest"],
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,         # modo carpeta (onedir): ver docs/entrega.md
    name="SistemaReservas",
    console=False,                 # sin la ventana negra de la terminal
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    name="SistemaReservas",
)
