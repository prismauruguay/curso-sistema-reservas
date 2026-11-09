# Interfaz: menú y pantalla de Clientes

> Resultado de la **clase 5**. Los [bocetos](bocetos.md) de la clase 1 se
> convierten en ventanas con CustomTkinter. Las reglas ya están en
> `negocio.py` y probadas (clase 4): la pantalla solo **muestra y pide**.

## 1. Qué hace la pantalla y qué no

```
                    lee (listar, obtener)
   Pantalla ──────────────────────────────▶ bd.py
      │
      │  guarda (agregar, modificar…)
      ▼
   negocio.py ──── controla las reglas ───▶ bd.py
      │
      └─ si algo no se puede: ErrorNegocio("Falta completar: dirección.")
                                     │
   Pantalla ◀── muestra el mensaje ──┘
```

- **Para leer**, la pantalla le pide los datos a `bd.py`. Leer no tiene reglas.
- **Para guardar**, siempre pasa por `negocio.py`. La pantalla nunca decide si
  un dato es válido: si `negocio` dice que no, muestra el mensaje tal cual.
- **Nunca escribe SQL.**

Compará con el sistema original: su pantalla de clientes controlaba ella misma
los campos vacíos, el formato del teléfono y del email, y después armaba el
`INSERT`. Cualquier otra pantalla que cargara clientes tendría que repetir todo
eso.

Para la clase 5 alcanzó con agregar a `negocio.py` lo mínimo de clientes:
nombre, dirección y teléfono son obligatorios (RF-01). Controlar formatos queda
para la clase 7.

## 2. Cómo está armado el código

```
app/
├── main.py           punto de entrada: abre la base y muestra el menú
└── ui/
    ├── estilo.py     colores, letras y la tabla: se deciden una vez para todas las pantallas
    ├── principal.py  el menú
    └── clientes.py   la pantalla de Clientes
```

Cada pantalla es una **clase** con dos partes:

- **Armado** (`_armar_busqueda`, `_armar_tabla`…): crea los controles. Se
  ejecuta una sola vez.
- **Comportamiento** (`nuevo`, `guardar`, `actualizar_tabla`…): lo que pasa al
  tocar un botón o elegir una fila.

Los controles se guardan como atributos de la ventana (`self.tabla`,
`self.campos["nombre"]`). El original los guardaba en variables `global`, con
dos problemas: cualquier parte del programa podía cambiarlos, y no se podían
abrir dos ventanas del mismo tipo sin que se pisaran.

### Una sola ventana de cada pantalla

El menú guarda las ventanas que abrió. Si se toca "Clientes" con la ventana ya
abierta, la trae al frente en lugar de abrir otra.

El original deshabilitaba el botón del menú y llamaba a `mainloop()` otra vez
por cada ventana. Un programa de tkinter tiene que tener **un solo**
`mainloop()`, el de la ventana principal. Cada `mainloop()` de más es un bucle
de eventos dentro de otro, y eso trae comportamientos raros al cerrar ventanas.

## 3. Del boceto a la pantalla

La pantalla sigue el boceto: búsqueda arriba, listado en el medio, formulario
abajo, **todo en una misma ventana**. El original abría una ventana aparte para
agregar, otra para modificar y otra para buscar.

El formulario tiene dos modos, y un título los indica:

| Modo | Cuándo | Guardar hace… |
|------|--------|---------------|
| **Cliente nuevo** | Al abrir la pantalla o al tocar *Nuevo* | `negocio.agregar_cliente` |
| **Modificando el cliente Nº 3** | Al elegir un cliente en la tabla | `negocio.modificar_cliente` |

Detalles que salieron al programarla:

- **Nuevo y Limpiar hacían lo mismo.** Quedó solo *Nuevo*, y la nota volvió al
  [boceto](bocetos.md#clientes-rf-01-rf-02). Es lo mismo que pasó con RN-09 en
  la clase 4: si el diseño cambia al programar, se corrige el documento.
- **El número de cliente no se muestra antes de guardar.** Lo asigna la base al
  hacer el `INSERT`. El original lo calculaba de antemano para mostrarlo y, si
  el usuario cancelaba, corregía a mano la tabla interna `sqlite_sequence`.
  Mucho trabajo y muchos riesgos para mostrar un número un rato antes.
- **Confirmar sin interrumpir.** Al guardar aparece *"Cliente Nº 6 guardado."*
  al lado de los botones, sin una ventanita que haya que cerrar. Las ventanitas
  quedan para los problemas.
- **Enter guarda.** Quien carga muchos clientes no tiene que ir al mouse.

### Un error que encontró la prueba

Al guardar, la pantalla vuelve a marcar en la tabla el cliente guardado. Eso
dispara el evento "se eligió una fila", que limpiaba el aviso *"guardado"*.
Pero tkinter procesa el evento **después**, cuando el programa vuelve a esperar
al usuario. Resultado: el aviso aparecía y desaparecía al instante.

No se veía leyendo el código. Apareció al probar la pantalla con un script
que hacía clic por nosotros. La solución: borrar el aviso solo si se eligió
**otro** cliente.

## 4. Errores: dos tipos, dos tratamientos

| Tipo | Ejemplo | Qué ve el usuario |
|------|---------|-------------------|
| **Previsto** (`ErrorNegocio`) | Falta el teléfono | Un aviso con el mensaje de `negocio`: *"Falta completar: teléfono."* |
| **Imprevisto** (un error de programación, la base bloqueada…) | Un `sqlite3.OperationalError` | *"Ocurrió un error inesperado y la operación no se completó."* |

Los imprevistos se atrapan en un solo lugar, `report_callback_exception`, en
el menú: tkinter lo llama cuando cualquier botón de cualquier ventana termina
en un error no atrapado. El usuario nunca ve un error técnico (RNF-04), y el
programador sí lo ve completo en la terminal.

## 5. Correr el programa

Desde la carpeta del proyecto, con el entorno activado:

```bash
python -m app.main
```

Si no existe `reservas.db`, el programa la crea **vacía**. Para practicar con
los datos de ejemplo, primero hay que correr `python -m app.bd`.

## 6. Qué quedó para la clase 6

- Pantallas de **Productos, Lotes y Reservas**. Sus botones del menú están
  grises hasta entonces.
- **Convertir lo que escribe el usuario** (`"15/11/2026"`, `"12"`) a `date` e
  `int` antes de llamar a `negocio`. En Clientes no hizo falta, porque todos
  los datos son texto.
