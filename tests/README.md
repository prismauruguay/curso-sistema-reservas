# tests/

Pruebas que se corren sin abrir ninguna ventana.

- `conftest.py`: le da a cada test una base nueva **en memoria** con los datos
  de ejemplo. La base real no se toca.
- `test_negocio.py`: reservar, entregar, cancelar, crear y anular lotes, un
  test por caso, agrupados por regla (RN-01 a RN-09). Clase 4.
- `test_clientes.py`, `test_productos.py`: datos obligatorios. Clases 5 y 6.
- `test_formato.py`: conversión de fechas y números escritos por el usuario.
  Clase 6.

Para correrlos, desde la carpeta del proyecto y con el entorno activado:

```bash
pytest
```

Por qué están escritos así: [docs/logica_negocio.md](../docs/logica_negocio.md#3-los-tests).
