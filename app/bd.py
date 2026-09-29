"""
Acceso a la base de datos (clase 3).

Este módulo es el ÚNICO que escribe SQL. El resto del programa llama a estas
funciones y recibe datos de Python; nunca arma consultas por su cuenta.

Tres reglas que seguimos en todo el archivo:

1. Nada de variables globales: cada función recibe la conexión (`con`).
   Así podemos probar con una base en memoria sin tocar la real.
2. Los valores SIEMPRE van como parámetros (`?`), nunca pegados al texto
   con f-strings. Así no hay inyección SQL ni problemas con comillas.
3. Este módulo no muestra ventanas ni mensajes. Si algo falla, lanza la
   excepción; decidir qué se le dice al usuario es trabajo de la interfaz.
"""

import sqlite3
from pathlib import Path

CARPETA_PROYECTO = Path(__file__).resolve().parent.parent
RUTA_BD = CARPETA_PROYECTO / "reservas.db"
CARPETA_DATOS = CARPETA_PROYECTO / "datos"


# ---------------------------------------------------------------------
#  Conexión y creación
# ---------------------------------------------------------------------

def conectar(ruta=RUTA_BD):
    """Abre la base y la deja lista para usar.

    `ruta` puede ser ":memory:" para una base temporal (la usan los tests).
    """
    con = sqlite3.connect(ruta)
    # SQLite no controla las claves foráneas si no se le pide, y hay que
    # pedírselo en CADA conexión.
    con.execute("PRAGMA foreign_keys = ON")
    # Las filas se pueden leer por nombre: fila["nombre"] en vez de fila[1].
    con.row_factory = sqlite3.Row
    return con


def crear_base(con, con_datos_ejemplo=False):
    """Crea las tablas y vistas (borra lo que hubiera). Opcionalmente carga
    los datos de ejemplo."""
    con.executescript(_leer_sql("esquema.sql"))
    if con_datos_ejemplo:
        con.executescript(_leer_sql("datos_ejemplo.sql"))


def base_creada(con):
    """True si la base ya tiene las tablas del sistema."""
    fila = con.execute(
        "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = 'reservas'"
    ).fetchone()
    return fila is not None


def _leer_sql(nombre):
    return (CARPETA_DATOS / nombre).read_text(encoding="utf-8")


# ---------------------------------------------------------------------
#  Clientes
# ---------------------------------------------------------------------

def listar_clientes(con, buscar=""):
    """Clientes ordenados por nombre. `buscar` filtra por nombre o teléfono."""
    patron = f"%{buscar.strip()}%"   # el % es parte del VALOR, no del SQL
    return con.execute(
        """SELECT id, nombre, direccion, telefono, email
           FROM clientes
           WHERE nombre LIKE ? OR telefono LIKE ?
           ORDER BY nombre""",
        (patron, patron),
    ).fetchall()


def obtener_cliente(con, cliente_id):
    """Un cliente, o None si no existe."""
    return con.execute(
        "SELECT id, nombre, direccion, telefono, email FROM clientes WHERE id = ?",
        (cliente_id,),
    ).fetchone()


def agregar_cliente(con, nombre, direccion, telefono, email=None):
    """Guarda un cliente nuevo y devuelve su id."""
    with con:   # transacción: si algo falla, no queda nada a medias
        cursor = con.execute(
            "INSERT INTO clientes (nombre, direccion, telefono, email) VALUES (?, ?, ?, ?)",
            (nombre, direccion, telefono, email or None),
        )
    return cursor.lastrowid


def modificar_cliente(con, cliente_id, nombre, direccion, telefono, email=None):
    with con:
        con.execute(
            """UPDATE clientes
               SET nombre = ?, direccion = ?, telefono = ?, email = ?
               WHERE id = ?""",
            (nombre, direccion, telefono, email or None, cliente_id),
        )


# ---------------------------------------------------------------------
#  Productos
# ---------------------------------------------------------------------

def listar_productos(con):
    """Productos con su disponible y reservado (calculados por la vista)."""
    return con.execute(
        "SELECT id, nombre, disponible, reservado FROM v_productos ORDER BY nombre"
    ).fetchall()


def agregar_producto(con, nombre):
    with con:
        cursor = con.execute("INSERT INTO productos (nombre) VALUES (?)", (nombre,))
    return cursor.lastrowid


def renombrar_producto(con, producto_id, nombre):
    # Una sola línea. En el sistema original había que actualizar también la
    # tabla lotes, porque guardaba una copia del nombre (ver docs/modelo_er.md).
    with con:
        con.execute("UPDATE productos SET nombre = ? WHERE id = ?", (nombre, producto_id))


# ---------------------------------------------------------------------
#  Lotes (solo lectura: las altas y cambios con reglas llegan en la clase 4)
# ---------------------------------------------------------------------

def listar_lotes(con, incluir_anulados=False):
    """Lotes con sus cantidades al día, ordenados por fecha de arribo."""
    sql = """SELECT id, producto_id, producto, fecha_arribo, cantidad_comprada,
                    reservado, entregado, disponible, estado
             FROM v_lotes"""
    if not incluir_anulados:
        sql += " WHERE estado = 'Activo'"
    sql += " ORDER BY fecha_arribo, id"
    return con.execute(sql).fetchall()


def obtener_lote(con, lote_id):
    """Un lote con sus cantidades, o None si no existe."""
    return con.execute(
        """SELECT id, producto_id, producto, fecha_arribo, cantidad_comprada,
                  reservado, entregado, disponible, estado
           FROM v_lotes WHERE id = ?""",
        (lote_id,),
    ).fetchone()


# ---------------------------------------------------------------------
#  Reservas (solo lectura, por ahora)
# ---------------------------------------------------------------------

def listar_reservas(con, cliente_id=None, producto_id=None, estado=None):
    """Reservas con los datos que muestra la pantalla (RF-11).

    Producto y fecha de arribo NO están guardados en la reserva: se traen
    del lote con JOIN.
    """
    condiciones = []
    parametros = []
    if cliente_id is not None:
        condiciones.append("r.cliente_id = ?")
        parametros.append(cliente_id)
    if producto_id is not None:
        condiciones.append("l.producto_id = ?")
        parametros.append(producto_id)
    if estado is not None:
        condiciones.append("r.estado = ?")
        parametros.append(estado)

    # Lo que se agrega al texto son trozos FIJOS escritos por nosotros;
    # los valores que vienen de afuera siguen yendo como parámetros.
    donde = ("WHERE " + " AND ".join(condiciones)) if condiciones else ""

    return con.execute(
        f"""SELECT r.id, r.cliente_id, c.nombre AS cliente,
                   l.producto_id, p.nombre AS producto,
                   r.lote_id, l.fecha_arribo, r.cantidad, r.estado,
                   r.fecha_reserva, r.fecha_entrega
            FROM reservas r
            JOIN clientes  c ON c.id = r.cliente_id
            JOIN lotes     l ON l.id = r.lote_id
            JOIN productos p ON p.id = l.producto_id
            {donde}
            ORDER BY l.fecha_arribo, r.id""",
        parametros,
    ).fetchall()


# ---------------------------------------------------------------------
#  Uso directo:  python -m app.bd
#  Crea reservas.db con los datos de ejemplo y muestra un resumen.
# ---------------------------------------------------------------------

def _crear_base_de_ejemplo():
    if RUTA_BD.exists():
        respuesta = input(f"{RUTA_BD.name} ya existe. ¿Borrarla y crearla de nuevo? (s/n) ")
        if respuesta.strip().lower() != "s":
            print("No se hizo nada.")
            return

    con = conectar()
    crear_base(con, con_datos_ejemplo=True)
    print(f"Base creada en {RUTA_BD}\n")
    print(f"{'Producto':<34}{'Disponible':>11}{'Reservado':>11}")
    for p in listar_productos(con):
        print(f"{p['nombre']:<34}{p['disponible']:>11}{p['reservado']:>11}")
    con.close()


if __name__ == "__main__":
    _crear_base_de_ejemplo()
