# tests/

Pruebas de las reglas de negocio (**clase 4**): reservar, entregar, cancelar,
crear y anular lotes, sin abrir ninguna ventana.

- `conftest.py`: le da a cada test una base nueva **en memoria** con los datos
  de ejemplo. La base real no se toca.
- `test_negocio.py`: un test por caso, agrupados por regla (RN-01 a RN-09).

Para correrlos, desde la carpeta del proyecto y con el entorno activado:

```bash
pytest
```

Por qué están escritos así: [docs/logica_negocio.md](../docs/logica_negocio.md#3-los-tests).
