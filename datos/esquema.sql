-- =====================================================================
--  Sistema de Reservas — esquema de la base (SQLite)
--  Clase 2. Ver docs/modelo_er.md para el porqué de cada decisión.
--
--  Uso (desde la carpeta del proyecto):
--      sqlite3 reservas.db < datos/esquema.sql
--  o en DB Browser for SQLite: "Ejecutar SQL" y pegar este archivo.
-- =====================================================================

-- SQLite NO controla las claves foráneas si no se le pide.
-- Hay que activarlo en CADA conexión (lo hará app/bd.py en la clase 3).
PRAGMA foreign_keys = ON;

DROP VIEW  IF EXISTS v_productos;
DROP VIEW  IF EXISTS v_lotes;
DROP TABLE IF EXISTS reservas;
DROP TABLE IF EXISTS lotes;
DROP TABLE IF EXISTS productos;
DROP TABLE IF EXISTS clientes;


-- ---------------------------------------------------------------------
--  Tablas
-- ---------------------------------------------------------------------

CREATE TABLE clientes (
    id        INTEGER PRIMARY KEY,
    nombre    TEXT NOT NULL CHECK (trim(nombre) <> ''),
    direccion TEXT NOT NULL,
    telefono  TEXT NOT NULL,
    email     TEXT                                   -- opcional (RF-01)
);

CREATE TABLE productos (
    id     INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL UNIQUE CHECK (trim(nombre) <> '')
);

CREATE TABLE lotes (
    id                INTEGER PRIMARY KEY,
    producto_id       INTEGER NOT NULL
                      REFERENCES productos (id) ON DELETE RESTRICT,
    cantidad_comprada INTEGER NOT NULL CHECK (cantidad_comprada > 0),
    fecha_arribo      TEXT    NOT NULL
                      CHECK (date(fecha_arribo) IS fecha_arribo),  -- AAAA-MM-DD
    estado            TEXT    NOT NULL DEFAULT 'Activo'
                      CHECK (estado IN ('Activo', 'Anulado'))
);

CREATE TABLE reservas (
    id            INTEGER PRIMARY KEY,
    cliente_id    INTEGER NOT NULL
                  REFERENCES clientes (id) ON DELETE RESTRICT,
    lote_id       INTEGER NOT NULL
                  REFERENCES lotes (id) ON DELETE RESTRICT,
    cantidad      INTEGER NOT NULL CHECK (cantidad > 0),            -- RN-02
    estado        TEXT    NOT NULL DEFAULT 'Reservado'
                  CHECK (estado IN ('Reservado', 'Entregado', 'Cancelado')),
    fecha_reserva TEXT    NOT NULL DEFAULT (date('now', 'localtime'))
                  CHECK (date(fecha_reserva) IS fecha_reserva),
    fecha_entrega TEXT
                  CHECK (date(fecha_entrega) IS fecha_entrega),
    -- Entregada <=> tiene fecha de entrega. Ni una sin la otra.
    CHECK ((estado = 'Entregado') = (fecha_entrega IS NOT NULL))
);

-- Índices para las búsquedas más comunes (RF-11: filtrar por cliente o lote).
CREATE INDEX ix_lotes_producto   ON lotes    (producto_id);
CREATE INDEX ix_reservas_cliente ON reservas (cliente_id);
CREATE INDEX ix_reservas_lote    ON reservas (lote_id);


-- ---------------------------------------------------------------------
--  Vistas: los números que NO guardamos, se calculan (modelo_er.md §4.2)
-- ---------------------------------------------------------------------

-- Un renglón por lote, con sus cantidades al día.
CREATE VIEW v_lotes AS
SELECT
    l.id,
    l.producto_id,
    p.nombre                AS producto,
    l.fecha_arribo,
    l.cantidad_comprada,
    l.estado,
    COALESCE(SUM(CASE WHEN r.estado = 'Reservado' THEN r.cantidad END), 0)
                            AS reservado,
    COALESCE(SUM(CASE WHEN r.estado = 'Entregado' THEN r.cantidad END), 0)
                            AS entregado,
    CASE WHEN l.estado = 'Anulado' THEN 0
         ELSE l.cantidad_comprada
              - COALESCE(SUM(CASE WHEN r.estado IN ('Reservado', 'Entregado')
                                  THEN r.cantidad END), 0)
    END                     AS disponible
FROM lotes l
JOIN productos p      ON p.id = l.producto_id
LEFT JOIN reservas r  ON r.lote_id = l.id      -- LEFT: incluye lotes sin reservas
GROUP BY l.id;

-- Un renglón por producto: suma de sus lotes activos (RF-04).
CREATE VIEW v_productos AS
SELECT
    p.id,
    p.nombre,
    COALESCE(SUM(v.disponible), 0) AS disponible,
    COALESCE(SUM(v.reservado),  0) AS reservado
FROM productos p
LEFT JOIN v_lotes v ON v.producto_id = p.id AND v.estado = 'Activo'
GROUP BY p.id;
