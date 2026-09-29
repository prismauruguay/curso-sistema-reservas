# Requisitos — Sistema de Reservas

> Resultado de la **clase 1**. Surge de "entrevistar al cliente" (la importadora)
> **antes de escribir una sola línea de código**.

## 1. El problema

La importadora compra mercadería al exterior. Entre que se hace la compra y que
la mercadería llega al depósito pasan semanas. Mientras tanto, los clientes
llaman para **apartar** unidades de lo que viene en camino.

Hoy eso se anota en papel y planillas sueltas. Consecuencias:

- Se reservan **más unidades de las que vienen** (sobreventa).
- No se sabe con certeza **cuánto queda libre** de cada producto.
- Cuando llega la mercadería, cuesta saber **a quién hay que entregarle qué**.

## 2. Quién usa el sistema

| Usuario | Qué hace |
|---------|----------|
| **Vendedor / administrativo** | Carga clientes, registra reservas, marca entregas. |
| **Encargado de compras** | Carga productos y los lotes que vienen en camino. |

(En la práctica puede ser la misma persona.)

## 3. Glosario

Acordar las palabras **antes** de programar evita malentendidos.

| Término | Significado |
|---------|-------------|
| **Producto** | Un artículo que vende la importadora (ej.: "Taladro 650W"). |
| **Lote** | Una compra concreta de un producto: *cuántas unidades* llegan y *en qué fecha*. Un producto puede tener varios lotes. |
| **Fecha de arribo** | Fecha en que el lote llega al depósito. |
| **Reserva** | Unidades de un lote apartadas para un cliente. |
| **Disponible** | Unidades de un lote que todavía nadie reservó. |
| **Reservado** | Unidades apartadas que todavía no se entregaron. |

## 4. Requisitos funcionales (qué debe hacer)

### Clientes
- **RF-01** Registrar un cliente: nombre, dirección, teléfono y email (opcional).
- **RF-02** Buscar, modificar y ver el listado de clientes.

### Productos
- **RF-03** Registrar un producto: nombre.
- **RF-04** Ver, por producto, el total **disponible** y **reservado** (sumando sus lotes).

### Lotes
- **RF-05** Registrar un lote: producto, cantidad comprada y fecha de arribo.
- **RF-06** Modificar la fecha de arribo de un lote (los envíos se atrasan).
- **RF-07** Anular un lote (la compra se cayó).

### Reservas
- **RF-08** Reservar unidades de un lote para un cliente.
- **RF-09** Entregar una reserva (el cliente retiró la mercadería).
- **RF-10** Cancelar una reserva.
- **RF-11** Listar reservas filtrando por cliente, producto o estado.

### Informes
- **RF-12** Exportar a Excel el listado de lotes y reservas.

## 5. Reglas de negocio (qué se puede y qué no)

- **RN-01** No se puede reservar más de lo **disponible** en el lote.
- **RN-02** La cantidad reservada debe ser mayor que cero.
- **RN-03** Solo se puede **entregar** a partir de la fecha de arribo del lote.
- **RN-04** Una reserva **entregada** no se puede cancelar (la mercadería ya salió).
- **RN-05** Una reserva **cancelada** devuelve sus unidades a *disponible*.
- **RN-06** Un lote con alguna reserva **entregada** no se puede anular.
- **RN-07** Al anular un lote, sus reservas pendientes pasan a **canceladas**.
- **RN-08** Nada se borra: reservas y lotes se **cancelan / anulan** para conservar la historia.

Estados de una reserva:

```
            crear
              │
              ▼
         ┌──────────┐   entregar    ┌───────────┐
         │ Reservado │ ────────────▶ │ Entregado │
         └──────────┘               └───────────┘
              │ cancelar
              ▼
         ┌───────────┐
         │ Cancelado │
         └───────────┘
```

## 6. Requisitos no funcionales (cómo debe ser)

- **RNF-01** Aplicación de escritorio para Windows, que se instala sin Python (un `.exe`).
- **RNF-02** Funciona sin internet. Los datos se guardan en un archivo local (SQLite).
- **RNF-03** Interfaz simple: la usa personal administrativo, no técnico.
- **RNF-04** Mensajes de error claros ("No hay stock suficiente: quedan 3"), nunca un error técnico.

## 7. Fuera de alcance (lo que NO hacemos en este curso)

Decir que *no* es parte del diseño. Estas funciones existen en el sistema real
pero quedan afuera para que el curso entre en 8 clases:

- Envío de emails al cliente.
- Impresión directa.
- Varias PCs usando la misma base al mismo tiempo.
- Usuarios y contraseñas.
- Copias de seguridad automáticas.
