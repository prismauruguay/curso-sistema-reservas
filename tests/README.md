# tests/

Pruebas que se corren sin abrir ninguna ventana.

- `conftest.py`: le da a cada test una base nueva **en memoria** con los datos
  de ejemplo. La base real no se toca.
- `test_negocio.py`: reservar, entregar, cancelar, crear y anular lotes, un
  test por caso, agrupados por regla (RN-01 a RN-09). Clase 4.
- `test_clientes.py`, `test_productos.py`: datos obligatorios (clases 5 y 6),
  formatos de teléfono y email, y nombres repetidos (clase 7).
- `test_formato.py`: conversión de fechas y números escritos por el usuario.
  Clase 6.
- `test_exportar.py`: el Excel se genera en una carpeta temporal y se vuelve a
  abrir para revisarlo. Clase 7.
- `test_ubicaciones.py`: dónde van los archivos del programa y los datos del
  usuario. Clase 8.

Para correrlos, desde la carpeta del proyecto y con el entorno activado:

```bash
pytest
```

Por qué están escritos así: [docs/logica_negocio.md](../docs/logica_negocio.md#3-los-tests).
