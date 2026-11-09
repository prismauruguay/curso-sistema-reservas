# app/

Código de la aplicación.

- `bd.py` — conexión y consultas a la base (clase 3) ✔
- `negocio.py` — reglas del negocio, sin interfaz ni SQL (clase 4) ✔
- `main.py` — punto de entrada: `python -m app.main` (clase 5) ✔
- `ui/` — pantallas con CustomTkinter
  - `estilo.py` — apariencia común, tablas y listas desplegables (clases 5 y 6) ✔
  - `formato.py` — convierte fechas y números entre pantalla y programa (clase 6) ✔
  - `principal.py` — menú; avisa a las ventanas abiertas cuando cambian los datos ✔
  - `clientes.py` (clase 5), `productos.py`, `lotes.py`, `reservas.py` (clase 6) ✔

Reglas de la casa:

- **Solo `bd.py` escribe SQL.** El resto del programa llama a sus funciones.
- **Las pantallas no deciden qué es válido.** Para guardar llaman a
  `negocio.py`, y si algo no se puede, muestran su mensaje.
- **Convertir texto a fechas y números se hace en `ui/formato.py`**, en un solo
  lugar.
