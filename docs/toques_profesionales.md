# Toques profesionales: validaciones y Excel

> Resultado de la **clase 7**. El programa ya funciona de punta a punta
> (clases 4 a 6). Esta clase cierra lo que separa "funciona" de "se puede
> entregar": mensajes claros donde había un *error inesperado*, datos con
> forma razonable y el informe en Excel que pide RF-12.

## 1. Un error inesperado que era previsible

Cargar un producto con un nombre que ya existe terminaba en *"Ocurrió un error
inesperado"*. La base hacía bien su trabajo y no guardaba el duplicado
(`UNIQUE`), pero el usuario no tenía forma de saber qué había pasado.

Si un error se puede prever, no es inesperado: le corresponde un mensaje claro.
Ahora `negocio.py` lo controla antes de guardar:

> Ya existe el producto «Taladro 650W» (Nº 1).

Y de paso apareció un caso que la base **no** atajaba: para SQLite,
"Taladro 650W" y "taladro 650w" son nombres distintos. Para el negocio son el
mismo producto. La comparación se hace con `casefold()`, que ignora mayúsculas.

> **La base es la última red, no la primera.** El `UNIQUE` sigue ahí y protege
> si algo se escapa. Pero los mensajes para el usuario y las reglas del negocio
> ("mayúsculas no cuentan") van en `negocio.py`.

## 2. Validar lo justo

### Lo que hacía el sistema original

| Campo | Regla del original | Rechazaba… |
|-------|--------------------|------------|
| Teléfono | Solo números | `099 123 456`, `2400-1234`, `+598 99 123 456` |
| Dirección | No puede empezar con un número | `18 de Julio 1234` |
| Nombre | Solo letras y espacios | `Bazar 18`, `Pérez & Hijos`, `Construcciones S.A.` |
| Email | Una expresión regular | (razonable) |

Las tres primeras rechazan **datos reales y correctos**. Cuando eso pasa, el
usuario no corrige el dato: lo deforma hasta que el sistema lo acepta
(`0991234567`, `Dieciocho de Julio`). La validación termina empeorando los datos
que tenía que cuidar.

### Lo que hacemos acá

| Campo | Regla | Por qué |
|-------|-------|---------|
| Nombre, dirección | Obligatorios, sin formato | Hay demasiadas formas válidas de escribirlos. |
| Teléfono | Números, espacios, `-`, `( )`, `+`, y al menos 6 números | Ataja errores de tipeo (`099 123 45a`) sin rechazar cómo la gente escribe los teléfonos. |
| Email | Opcional; si está, `algo@algo.algo` sin espacios | Ataja olvidos (`ventas@empresa`). Si un email *existe* solo se sabe mandándole un correo: no tiene sentido una regla más estricta. |

Los tests prueban **las dos caras**: lo que se tiene que rechazar y, con el
mismo cuidado, lo que se tiene que **aceptar** (ver
[`tests/test_clientes.py`](../tests/test_clientes.py)). Una validación que
rechaza un dato real es un error, aunque "funcione".

### Cuidado con los datos que ya están cargados

Al agregar las validaciones, uno de nuestros scripts de prueba de la clase 6
dejó de andar: daba de alta un cliente con teléfono `"099"`, que antes se
aceptaba y ahora no.

Lo mismo le puede pasar a una base real. Un cliente cargado antes con un
teléfono que hoy no pasa la validación obliga a corregirlo la próxima vez que
alguien modifique ese cliente, aunque quiera cambiar otra cosa. Por eso hay un
test que comprueba que **los datos de ejemplo siguen siendo válidos**. Con una
base en producción, antes de endurecer una regla, hay que revisar qué datos
quedarían afuera.

## 3. Exportar a Excel (RF-12)

El botón **Exportar a Excel** del menú pregunta dónde guardar y genera un libro
con dos hojas, **Lotes** y **Reservas**.

### Pensado para quien lo va a usar

Un informe en Excel no es para mirarlo: es para trabajar con él. Por eso:

- **Las fechas son fechas, no texto.** El original escribía `"15/11/2026"` como
  texto: Excel no lo puede ordenar ni filtrar por mes. Acá se escribe la fecha y
  se le da formato `DD/MM/YYYY`.
- **Los números son números**, así se pueden sumar.
- **Los títulos quedan fijos** al bajar, y cada columna tiene su **filtro**.
- **El nombre que sugiere** es `lotes_y_reservas_2026-11-09.xlsx`: con la fecha
  en formato ISO, los archivos de distintos días quedan ordenados en la carpeta.
- Si Excel tiene abierto el archivo, Windows no deja reemplazarlo. Es un
  problema previsible, así que tiene su propio mensaje: *"Si está abierto en
  Excel, cerralo y probá de nuevo."*

### Separado de la pantalla

La exportación vive en [`app/exportar.py`](../app/exportar.py). No abre
ventanas: recibe la conexión y la ruta del archivo. Lo único que hace el menú
es preguntar dónde guardar y ofrecer abrir el archivo.

Gracias a eso, la exportación **tiene tests**: se exporta a una carpeta
temporal, se vuelve a abrir el archivo y se revisa que las fechas sean fechas,
que los totales coincidan con los de la pantalla y que estén todas las filas.

El original tenía todo dentro de la pantalla de Lotes, y escribía título por
título y celda por celda (`hoja['A1'] = 'Nro. Lote'`, `hoja['B1'] = …`). Acá
cada hoja se describe **una vez**, como una lista de columnas (título, ancho y
dato), y la misma lista sirve para títulos, datos, anchos y formatos. Agregar
una columna es agregar una línea.

## 4. Lo que decidimos no hacer

Algunas mejoras quedaron afuera a propósito:

- **Buscar dentro de las listas desplegables.** Con decenas de clientes, la
  lista alcanza. Si un día son cientos, hay un solo lugar para cambiar,
  `estilo.Selector`, y todas las pantallas lo reciben.
- **Avisar si un cliente parece repetido** (mismo nombre y teléfono). Dos
  clientes con el mismo nombre pueden existir, y no queda claro qué regla
  quiere el negocio. Antes de programarla, habría que preguntarle al cliente,
  como pasó con RN-09.

Decidir qué **no** hacer, y dejarlo escrito, también es parte del trabajo.
