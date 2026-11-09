# app/

Código de la aplicación.

- `bd.py` — conexión y consultas a la base (clase 3) ✔
- `negocio.py` — reglas del negocio, sin interfaz ni SQL (clase 4) ✔
- `ui/` — pantallas con CustomTkinter (clases 5 y 6)
- `main.py` — punto de entrada (clase 5)

Regla de la casa: **solo `bd.py` escribe SQL.** El resto del programa llama a
sus funciones.
