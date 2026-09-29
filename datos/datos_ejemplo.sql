-- =====================================================================
--  Datos de ejemplo — TODOS FICTICIOS (nombres, teléfonos y emails
--  inventados). Sirven para practicar y para probar cada regla.
--
--  Cargar DESPUÉS de esquema.sql:
--      sqlite3 reservas.db < datos/esquema.sql
--      sqlite3 reservas.db < datos/datos_ejemplo.sql
-- =====================================================================

PRAGMA foreign_keys = ON;

INSERT INTO clientes (id, nombre, direccion, telefono, email) VALUES
    (1, 'Ferretería Norte',        'Av. Siempre Viva 742',   '099 123 456', 'norte@ejemplo.com'),
    (2, 'Casa Rodríguez',          'Calle Falsa 123',        '2400 1234',   NULL),
    (3, 'Herramientas El Tornillo', 'Rambla Sur 1500',       '098 765 432', 'ventas@eltornillo.ejemplo'),
    (4, 'Construcciones Pérez',    'Ruta 8 km 20',           '094 555 010', 'compras@perez.ejemplo'),
    (5, 'Bazar La Esquina',        'Esquina Central 45',     '2600 9999',   NULL);

INSERT INTO productos (id, nombre) VALUES
    (1, 'Taladro 650W'),
    (2, 'Amoladora 115mm'),
    (3, 'Set de destornilladores x12'),
    (4, 'Escalera de aluminio 6 peldaños'),
    (5, 'Lijadora orbital');           -- sin lotes todavía: debe mostrar 0 / 0

-- Numeramos los lotes desde 101 para que no se confundan con otros números.
INSERT INTO lotes (id, producto_id, cantidad_comprada, fecha_arribo, estado) VALUES
    (101, 1,  50, '2026-11-15', 'Activo'),    -- viene en camino
    (102, 2,  25, '2026-12-02', 'Activo'),    -- viene en camino, ya agotado
    (103, 1,  30, '2026-09-10', 'Activo'),    -- YA LLEGÓ: se puede entregar (RN-03)
    (104, 3, 100, '2026-10-20', 'Activo'),
    (105, 4,  20, '2026-10-05', 'Anulado');   -- la compra se cayó (RF-07)

INSERT INTO reservas (id, cliente_id, lote_id, cantidad, estado, fecha_reserva, fecha_entrega) VALUES
    -- Lote 101 (Taladro, 50): quedan 40 disponibles
    (1, 1, 101, 10, 'Reservado', '2026-09-01', NULL),
    -- Lote 102 (Amoladora, 25): reservado completo -> disponible 0
    (2, 2, 102, 25, 'Reservado', '2026-09-03', NULL),
    -- Lote 103 (Taladro, 30, ya llegó): una entregada, una pendiente, una cancelada
    (3, 3, 103, 12, 'Entregado', '2026-08-20', '2026-09-12'),
    (4, 4, 103,  8, 'Reservado', '2026-08-25', NULL),
    (5, 5, 103,  5, 'Cancelado', '2026-08-26', NULL),   -- RN-05: no descuenta
    -- Lote 104 (Destornilladores, 100)
    (6, 1, 104, 30, 'Reservado', '2026-09-15', NULL),
    -- Lote 105 anulado: su reserva pendiente pasó a Cancelado (RN-07)
    (7, 4, 105,  6, 'Cancelado', '2026-09-02', NULL);

-- Resultado esperado de  SELECT * FROM v_productos;
--   Taladro 650W                       disponible 50  reservado 18
--       (lote 101: 40 disp / 10 res  +  lote 103: 10 disp / 8 res)
--   Amoladora 115mm                    disponible  0  reservado 25
--   Set de destornilladores x12        disponible 70  reservado 30
--   Escalera de aluminio 6 peldaños    disponible  0  reservado  0   (lote anulado)
--   Lijadora orbital                   disponible  0  reservado  0   (sin lotes)
