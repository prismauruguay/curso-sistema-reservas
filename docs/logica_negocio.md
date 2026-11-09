# Lógica de negocio y tests

> Resultado de la **clase 4**. Las reglas de los [requisitos](requisitos.md#5-reglas-de-negocio-qué-se-puede-y-qué-no)
> pasan a código, y cada regla tiene un test que la comprueba.
> Todavía no hay ventanas: todo se prueba sin interfaz.

## 1. Tres capas, tres responsabilidades

```
┌──────────────────────┐
│ Interfaz (clase 5)   │  muestra y pide datos. Ni reglas ni SQL.
└──────────┬───────────┘
           │ llama a…            ▲ si algo no se puede: ErrorNegocio("mensaje claro")
┌──────────▼───────────┐
│ app/negocio.py       │  decide QUÉ se puede hacer (RN-01 a RN-09).
└──────────┬───────────┘
           │ llama a…
┌──────────▼───────────┐
│ app/bd.py            │  sabe CÓMO se guarda. Único archivo con SQL.
└──────────┬───────────┘
           ▼
       reservas.db
```

El sistema original ya separaba las reglas en un `negocio.py`, y eso estaba
bien. Pero la separación quedó a medias:

- **La pantalla repetía reglas.** El botón "Reservar" comparaba la cantidad con
  el disponible *que mostraba el formulario* antes de llamar a `negocio`. Cuando
  una regla vive en dos lugares, tarde o temprano los dos dicen cosas distintas.
- **Las reglas y el SQL estaban juntos.** Cada función de `negocio.py` armaba
  sus propios `UPDATE`. Para leer una regla había que leer también el SQL.
- **Usaba una conexión global**, abierta una sola vez para todo el programa. No
  había forma de darle a `negocio` una base de prueba: para probar una regla
  había que usar la base real.

Acá cada capa hace una sola cosa, y por eso cada una se puede cambiar o probar
sin tocar las otras.

## 2. Cómo está escrita cada operación

Todas las funciones de `negocio.py` siguen el mismo orden:

1. **Buscar** lo que hace falta: el lote, la reserva.
2. **Controlar** las reglas una por una, con su número (`# RN-01`).
3. Recién entonces, **guardar**.

Si una regla no se cumple, la función lanza `ErrorNegocio` con un mensaje para
el usuario, como *"No hay stock suficiente en el lote 101: quedan 40."* (RNF-04).
La interfaz no tiene que interpretar nada: muestra ese texto.

### Lo que ya no hay que programar

Ninguna función de `negocio.py` actualiza un total. En el sistema original,
reservar, entregar, cancelar y anular tenían que acordarse de modificar a mano
`cantidad_disponible`, `cantidad_reservada`, `stock_disponible` y
`stock_reservado`: hasta tres `UPDATE` extra por operación. Acá las vistas
calculan los totales (ver [modelo de datos §4.2](modelo_er.md#42-disponible-y-reservado-se-calculan-no-se-guardan)),
y por eso, por ejemplo:

- **RN-05** ("cancelar devuelve las unidades") no tiene ni una línea de código:
  la reserva cancelada deja de sumar.
- **Cambiar la fecha de un lote** es un único `UPDATE` sobre una fila.

### Una transacción donde hace falta

Anular un lote (RN-07) cambia **varias filas**: el lote y sus reservas
pendientes. `bd.anular_lote` hace las dos cosas dentro de un mismo `with con:`.
Si algo falla a la mitad, no se guarda nada: nunca queda un lote anulado con
reservas que siguen vivas.

## 3. Los tests

Un test es un caso concreto escrito en código: *"si reservo 41 unidades de un
lote que tiene 40, tiene que dar error y no guardar nada"*.

```python
def test_rn01_no_se_puede_reservar_mas_de_lo_disponible(con):
    with pytest.raises(ErrorNegocio, match="quedan 40"):
        negocio.reservar(con, cliente_id=2, lote_id=101, cantidad=41, hoy=HOY)
    assert disponible(con, 101) == 40          # no se guardó nada
```

Decisiones que hacen posibles estos tests:

| Decisión | Para qué |
|----------|----------|
| Cada función recibe la conexión (`con`) | Los tests usan una base **en memoria**, nueva para cada test. La base real no se toca. |
| La fecha de hoy entra como parámetro (`hoy=`) | Un test sobre RN-03 da el mismo resultado hoy, mañana y el año que viene. |
| Los datos de ejemplo tienen un caso de cada cosa | Lote por llegar, lote que ya llegó, lote agotado, lote anulado, reservas en los tres estados. |
| Los nombres de los tests llevan el número de regla | Si falla `test_rn04_…`, se sabe qué regla se rompió sin abrir el archivo. |

No se prueba solo "que funcione": también que **falle cuando tiene que
fallar** y que, al fallar, **no deje nada a medias**.

Para correrlos, desde la carpeta del proyecto y con el entorno activado:

```bash
pytest
```

## 4. Una regla que apareció al programar

Al escribir `cambiar_fecha_lote` surgió una pregunta que no estaba en los
requisitos: **¿qué pasa si el lote ya llegó y ya se entregaron unidades?**
Cambiarle la fecha de arribo dejaría entregas hechas *antes* de que la
mercadería "llegara".

Eso **no se decide en el código**: se le pregunta al cliente. La respuesta pasó
a ser una regla nueva, **RN-09**, y quedó escrita en los
[requisitos](requisitos.md#5-reglas-de-negocio-qué-se-puede-y-qué-no) con la
nota de dónde salió.

> Los requisitos no se escriben una vez y se olvidan. Programar obliga a ser
> preciso y aparecen casos que nadie pensó. Cuando pasa, se vuelve al documento,
> no se resuelve en silencio en el código.

## 5. Qué quedó para más adelante

- Validar los datos de clientes y productos (campos vacíos, nombres repetidos):
  **clase 7**.
- Convertir lo que escribe el usuario (`"15/11/2026"`, `"12"`) a `date` e `int`
  antes de llamar a `negocio`: **clase 5**, en la interfaz.
- Dos PCs reservando del mismo lote al mismo tiempo: fuera de alcance (una sola
  PC). Con varias, controlar el disponible y guardar la reserva tendrían que ser
  un único paso atómico.
