# Interfaz II: Productos, Lotes y Reservas

> Resultado de la **clase 6**. Se completan las pantallas de los
> [bocetos](bocetos.md) con el mismo esquema que Clientes ([clase 5](interfaz.md)).
> Aparecen tres temas nuevos: convertir lo que escribe el usuario, mantener al
> día varias ventanas abiertas, y confirmar antes de lo que no tiene vuelta
> atrás.

## 1. Convertir lo que escribe el usuario

Una caja de texto siempre devuelve **texto**. `negocio.py` trabaja con datos de
verdad: una fecha es un `date` y una cantidad es un `int`. Hay que convertir en
el medio, en los dos sentidos:

```
    Pantalla           Programa                Base
    "15/11/2026"   ->  date(2026, 11, 15)  ->  "2026-11-15"
    "12"           ->  12
    "15/11/2026"   <-                      <-  "2026-11-15"
```

Todo eso vive en un solo archivo, [`app/ui/formato.py`](../app/ui/formato.py),
para que todas las pantallas conviertan igual. Si algo no se puede convertir,
lanza `ErrorFormato` con un mensaje para el usuario, que la pantalla muestra
igual que un `ErrorNegocio`.

Hay trampas que **solo aparecen al escribir los tests**:

- `int("1_000")` da `1000`, y `int("²")` también acepta ese carácter. Por eso
  primero se controla que el texto sean solo dígitos.
- `31/02/2026` tiene buena forma pero no existe. `strptime` lo rechaza, y el
  mensaje nombra la fecha que escribió el usuario: *"La fecha «31/02/2026» no
  es válida."*
- `"-3"` **sí** se convierte. Que sea mayor que cero es una regla (RN-02) y la
  controla `negocio.py`, con su propio mensaje. Cada capa controla lo suyo.

Son funciones que reciben texto y devuelven datos, sin base ni ventanas, así que
se prueban fácil: ver [`tests/test_formato.py`](../tests/test_formato.py).

## 2. Un mismo esquema para todas las pantallas

```
┌─ Lotes ──────────────────────────────────────────────┐
│ ┌──────────────────────────────────────────────────┐ │
│ │ tabla                                            │ │
│ └──────────────────────────────────────────────────┘ │
│ Lote elegido: [Cambiar fecha…] [Anular lote]         │  ← actúan sobre la fila marcada
│ ┌─ Nuevo lote ─────────────────────────────────────┐ │
│ │ Producto [▼]  Cantidad [__]  Arribo [__/__/__]   │ │  ← solo para cargar uno nuevo
│ └──────────────────────────────────────────────────┘ │
│ [Crear lote]   Lote 106 creado.                      │  ← aviso discreto
└──────────────────────────────────────────────────────┘
```

Lotes y Reservas siguen esta forma: los botones que actúan sobre **la fila
elegida** van pegados a la tabla, y el formulario de abajo sirve **solo** para
cargar algo nuevo. Así nunca hay duda sobre a qué se aplica cada botón.

Para elegir clientes, productos y lotes hay una lista desplegable,
`estilo.Selector`, que **muestra** un texto ("Ferretería Norte (Nº 1)") pero
**devuelve** el id (`1`). El número va en el texto porque puede haber dos
clientes con el mismo nombre.

## 3. Ventanas que se enteran de los cambios

Con Reservas y Lotes abiertas a la vez, una reserva nueva cambia el Disponible
del lote. Si la ventana de Lotes no se entera, muestra un número viejo, y el
usuario no tiene forma de saberlo.

La solución pasa por el menú, que es quien abrió todas las ventanas:

```
   Reservas ── guarda ──▶ menu.datos_cambiaron(self)
                                 │
                   ┌─────────────┼──────────────┐
                   ▼             ▼              ▼
          Lotes.actualizar() Productos.actualizar() Clientes.actualizar()
```

Cada pantalla tiene un método `actualizar()` que vuelve a leer sus datos sin
perder la fila elegida. Las pantallas no se conocen entre sí: solo le avisan al
menú. Agregar una pantalla nueva no obliga a tocar las demás.

En el sistema original cada pantalla se actualizaba solo a sí misma
(`traer_data()`). Lo que mostraban las otras ventanas abiertas quedaba viejo
hasta cerrarlas y volver a abrirlas.

## 4. Confirmar lo que no tiene vuelta atrás

Anular un lote, entregar y cancelar una reserva **no se pueden deshacer**
(RN-04, RN-08). Antes de hacerlos, la pantalla pregunta, y la pregunta dice
**qué va a pasar**, no solo "¿Está seguro?":

> ¿Anular el lote 104 (Set de destornilladores x12)?
>
> Sus reservas pendientes (30 unidades) se van a cancelar.
>
> Esto no se puede deshacer.

Lo que hace RN-07 por detrás (cancelar las reservas del lote) se avisa **antes**.
Que no sea una sorpresa.

Crear y modificar no preguntan: un dato mal cargado se corrige.

## 5. Comodidad no es control

En "Nueva reserva", la lista de lotes muestra **solo** los que tienen
disponible. Eso evita que el usuario elija un lote agotado, pero **no** es lo que
hace cumplir RN-01: `negocio.reservar` lo sigue controlando. La pantalla puede
ayudar, pero la regla no puede depender de ella. Si mañana otra pantalla
reserva, o el lote se agota mientras la ventana está abierta, la regla sigue
protegiendo.

## 6. Del boceto a la pantalla

Lo que cambió al programar, y por qué:

| Pantalla | Cambio | Por qué |
|----------|--------|---------|
| Lotes | *Cambiar fecha* abre un cuadro que pide la fecha nueva, en lugar de usar el formulario | El formulario queda solo para lotes nuevos (ver §2). |
| Lotes | Columnas *Reservado* y *Entregado* | Explican el *Disponible*: sin ellas, "Comprada 30, Disponible 10" no se entiende. |
| Reservas | Filtro por **Producto** | **RF-11 lo pide y el boceto se lo olvidó.** Apareció al revisar la pantalla contra los requisitos. |
| Reservas | Columna *Arribo* | La pregunta que dejó abierta el boceto: se **muestra**, pero no se guarda en la reserva (modelo_er.md §4.1). |

El filtro por producto es la lección de esta clase: **antes de dar una pantalla
por terminada, se revisa contra los requisitos que dice cumplir.** El boceto
decía "RF-08 a RF-11" en el título, pero no cumplía todo RF-11.

Las notas volvieron a [bocetos.md](bocetos.md), debajo de cada boceto.

## 7. Cómo se probó

- **Tests** (`pytest`): las conversiones de `formato.py` y las reglas mínimas
  de productos. En total son 67.
- **Un script que usa las pantallas**: crea productos, lotes y reservas, carga
  datos mal escritos, anula, entrega y cancela, y comprueba que las *otras*
  ventanas abiertas se actualizan.
- **Capturas de pantalla**: mostraron que la tabla estiraba la última columna
  (Estado) en lugar de los nombres, y cortaba textos como "Escalera de aluminio
  6 pe…". Ahora se estiran las columnas de texto y los números quedan pegados
  a su título. Un test no encuentra eso: hay que **mirar** la pantalla.

## 8. Qué quedó para la clase 7

- **Nombres de producto repetidos.** La base no los deja guardar (`UNIQUE`),
  así que no se rompe nada, pero hoy el usuario ve *"Ocurrió un error
  inesperado"*. El mensaje claro se agrega en la clase 7, junto con los formatos
  de email y teléfono.
- **Exportar a Excel** (RF-12): el último botón gris del menú.
- **Buscar en las listas desplegables.** Con cientos de clientes, elegir de una
  lista larga se vuelve incómodo.
