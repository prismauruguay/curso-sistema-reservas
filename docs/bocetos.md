# Bocetos de pantallas

> Resultado de la **clase 1**. Dibujados en papel primero; acá quedan pasados en limpio.
> El objetivo **no** es que sean lindos: es decidir **qué datos** muestra y pide
> cada pantalla, y **qué botones** necesita. El diseño visual viene en la clase 5.

## Menú principal

```
┌──────────────────────────────┐
│      SISTEMA DE RESERVAS     │
│                              │
│   [       Clientes       ]   │
│   [       Productos      ]   │
│   [         Lotes        ]   │
│   [       Reservas       ]   │
│   [   Exportar a Excel   ]   │
│                              │
│   [         Salir        ]   │
└──────────────────────────────┘
```

## Clientes (RF-01, RF-02)

```
┌─ Clientes ──────────────────────────────────────────────────┐
│ Buscar: [______________]                                    │
│                                                             │
│ ┌────┬──────────────────┬───────────────┬──────────────────┐│
│ │ Nº │ Nombre           │ Teléfono      │ Email            ││
│ ├────┼──────────────────┼───────────────┼──────────────────┤│
│ │  1 │ Ferretería Norte │ 099 123 456   │ norte@mail.com   ││
│ │  2 │ Casa Rodríguez   │ 2400 1234     │                  ││
│ └────┴──────────────────┴───────────────┴──────────────────┘│
│                                                             │
│ Nombre:    [____________________]                           │
│ Dirección: [____________________]                           │
│ Teléfono:  [____________]   Email: [____________________]   │
│                                                             │
│ [ Nuevo ]  [ Guardar ]  [ Limpiar ]                         │
└─────────────────────────────────────────────────────────────┘
```

## Productos (RF-03, RF-04)

```
┌─ Productos ──────────────────────────────────────────┐
│ ┌────┬────────────────────┬────────────┬───────────┐ │
│ │ Nº │ Producto           │ Disponible │ Reservado │ │
│ ├────┼────────────────────┼────────────┼───────────┤ │
│ │  1 │ Taladro 650W       │         40 │        10 │ │
│ │  2 │ Amoladora 115mm    │          0 │        25 │ │
│ └────┴────────────────────┴────────────┴───────────┘ │
│                                                      │
│ Nombre: [____________________]                       │
│ [ Nuevo ]  [ Guardar ]                               │
└──────────────────────────────────────────────────────┘
```

> Disponible y Reservado **no se escriben**: se calculan a partir de los lotes.

## Lotes (RF-05, RF-06, RF-07)

```
┌─ Lotes ─────────────────────────────────────────────────────────────┐
│ ┌──────┬─────────────────┬────────────┬─────────┬──────┬─────────┐  │
│ │ Lote │ Producto        │ Arribo     │ Comprada│ Disp.│ Estado  │  │
│ ├──────┼─────────────────┼────────────┼─────────┼──────┼─────────┤  │
│ │  101 │ Taladro 650W    │ 15/11/2026 │      50 │   40 │ Activo  │  │
│ │  102 │ Amoladora 115mm │ 02/12/2026 │      25 │    0 │ Activo  │  │
│ └──────┴─────────────────┴────────────┴─────────┴──────┴─────────┘  │
│                                                                     │
│ Producto: [ Taladro 650W   ▼]  Cantidad: [____]  Arribo: [__/__/__] │
│ [ Nuevo lote ]  [ Cambiar fecha ]  [ Anular lote ]                  │
└─────────────────────────────────────────────────────────────────────┘
```

## Reservas (RF-08 a RF-11)

```
┌─ Reservas ──────────────────────────────────────────────────────────┐
│ Filtrar: Cliente [__________▼]  Estado [ Todos ▼]                   │
│                                                                     │
│ ┌────┬──────────────────┬──────────────┬──────┬──────┬───────────┐  │
│ │ Nº │ Cliente          │ Producto     │ Lote │ Cant.│ Estado    │  │
│ ├────┼──────────────────┼──────────────┼──────┼──────┼───────────┤  │
│ │  1 │ Ferretería Norte │ Taladro 650W │  101 │   10 │ Reservado │  │
│ │  2 │ Casa Rodríguez   │ Amoladora    │  102 │   25 │ Reservado │  │
│ └────┴──────────────────┴──────────────┴──────┴──────┴───────────┘  │
│                                                                     │
│ Cliente: [__________▼]   Lote: [__________▼]   Cantidad: [____]     │
│ (Disponible en el lote: 40)                                         │
│                                                                     │
│ [ Reservar ]   [ Entregar ]   [ Cancelar reserva ]                  │
└─────────────────────────────────────────────────────────────────────┘
```

> Observación para la clase 2: en esta pantalla mostramos **Producto** y la
> **fecha de arribo** de cada reserva… ¿hace falta *guardarlos* en la reserva,
> o alcanza con saber el **lote**?
