# app/

Código de la aplicación.

- `bd.py` — conexión y consultas a la base (clase 3) ✔
- `negocio.py` — reglas del negocio, sin interfaz ni SQL (clase 4) ✔
- `main.py` — punto de entrada: `python -m app.main` (clase 5) ✔
- `ui/` — pantallas con CustomTkinter
  - `estilo.py` — apariencia común a todas las pantallas (clase 5) ✔
  - `principal.py` — menú principal (clase 5) ✔
  - `clientes.py` — pantalla de Clientes (clase 5) ✔
  - Productos, Lotes y Reservas (clase 6)

Reglas de la casa:

- **Solo `bd.py` escribe SQL.** El resto del programa llama a sus funciones.
- **Las pantallas no deciden qué es válido.** Para guardar llaman a
  `negocio.py`, y si algo no se puede, muestran su mensaje.
