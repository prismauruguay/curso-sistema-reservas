# Entrega: del proyecto al programa instalado

> Resultado de la **clase 8**. RNF-01 pedía *"una aplicación de escritorio para
> Windows, que se instala sin Python"*. Esta clase arma ese programa y resuelve
> lo que cambia cuando el código deja de correr en la PC de quien lo escribió.

## 1. Lo que cambia al salir de la PC del programador

Mientras desarrollamos, todo vive en la carpeta del proyecto: el código, la
base y los mensajes de error en la terminal. En la PC de la importadora no hay
nada de eso:

| En desarrollo | Instalado | Qué hubo que resolver |
|---------------|-----------|-----------------------|
| Python instalado | No hay Python | Empaquetar con PyInstaller (§2). |
| La base, al lado del código | La carpeta del programa puede no admitir escritura, y se reemplaza al actualizar | Separar archivos del programa y datos del usuario (§3). |
| Los errores salen en la terminal | No hay terminal | Guardarlos en un archivo (§4). |
| "La versión que tengo abierta" | Varias PCs, cada una con la suya | Un número de versión visible (§5). |

Ninguno de estos problemas aparece mientras se programa. Por eso la entrega es
una etapa propia del proyecto y no "compilar al final".

## 2. Empaquetar con PyInstaller

PyInstaller junta el programa, Python y las librerías en una carpeta que se
puede copiar a cualquier PC con Windows.

```bash
pyinstaller SistemaReservas.spec --noconfirm
```

El resultado queda en `dist/SistemaReservas/`: el `SistemaReservas.exe` y una
carpeta `_internal` con todo lo que necesita.

### La receta se guarda en el proyecto

Las opciones no se escriben en la línea de comandos cada vez: van en
[`SistemaReservas.spec`](../SistemaReservas.spec), que se sube a git. Así
cualquiera arma **exactamente** el mismo programa, y si una opción cambia, queda
en la historia.

Lo que dice la receta:

- **`datos/esquema.sql`**: el programa lo lee de disco para crear la base en
  una PC nueva. PyInstaller solo incluye código Python por su cuenta, así que
  los demás archivos hay que nombrarlos.
- **Los temas de CustomTkinter**, por el mismo motivo.
- **`console=False`**: sin la ventana negra de la terminal detrás del programa.
- **Sin `pytest`**: se usa para desarrollar, no para correr el programa.

### Carpeta, no un solo archivo

PyInstaller también puede armar **un único `.exe`** (`onefile`). Lo descartamos:

- Ese `.exe` se descomprime en una carpeta temporal **cada vez** que se abre,
  así que el programa tarda más en arrancar.
- Los antivirus desconfían más de los programas que se descomprimen solos.
- Si el programa guardara algo "al lado del código", lo guardaría en esa
  carpeta temporal, **que se borra al cerrar**. Con la base como estaba hasta
  la clase 7, se perdían los datos en cada cierre.

Con una carpeta, para entregar alcanza con comprimirla en un `.zip`.

## 3. Archivos del programa y datos del usuario

Hasta la clase 7, `bd.py` guardaba `reservas.db` al lado del código. Al
empaquetar, eso deja de servir: los datos del usuario no pueden vivir dentro
de la carpeta del programa.

[`app/ubicaciones.py`](../app/ubicaciones.py) separa dos tipos de archivos:

| | Archivos del programa | Datos del usuario |
|-|-----------------------|-------------------|
| Ejemplos | `esquema.sql`, temas | `reservas.db`, `errores.log` |
| ¿Cambian al actualizar? | Sí, se reemplazan | **No: son lo valioso** |
| En desarrollo | Carpeta del proyecto | Carpeta del proyecto |
| Instalado | Junto al `.exe` | `%LOCALAPPDATA%\SistemaReservas` |

`%LOCALAPPDATA%` es la carpeta que Windows reserva para los datos de cada
programa y cada usuario (por ejemplo, `C:\Users\Ana\AppData\Local`). Siempre se
puede escribir ahí, y no se toca al reinstalar el programa.

Una variable de entorno, `RESERVAS_CARPETA`, permite elegir otra carpeta. La
usamos para **probar el `.exe` sin tocar la carpeta real**, y sirve también si
la importadora quiere los datos en una carpeta con copia de seguridad.

En `bd.py` cambiaron solo un par de líneas, porque desde la clase 3 la ruta de
la base estaba en un solo lugar y cada función recibe la conexión.

## 4. Errores sin terminal

Desde la clase 5, un error imprevisto le muestra al usuario un mensaje claro y
deja el detalle técnico en la terminal. Pero el `.exe` no tiene terminal: ese
detalle se perdería, y ante un "me apareció un error" nadie podría averiguar
qué pasó.

Ahora el detalle va a **`errores.log`**, en la carpeta de datos del usuario, con
fecha y hora. Durante el desarrollo sigue saliendo también en la terminal. El
archivo se crea recién con el primer error: **si no existe, no hubo errores**.

También se cubrió un caso que antes no tenía red: que **la base no se pueda
abrir** al arrancar. Todavía no hay menú donde mostrar el error, así que se
avisa con una ventana suelta que dice dónde quedó el detalle.

Lo probamos con el `.exe` real: pusimos una carpeta donde tenía que ir el
archivo `reservas.db`, y el error quedó en `errores.log` con el detalle
completo.

## 5. Número de versión

El título del menú dice **Sistema de Reservas 1.0**. Cuando alguien llama por un
problema, lo primero es saber qué versión tiene. El número está en un solo
lugar, [`app/__init__.py`](../app/__init__.py), y se sube con cada entrega.

## 6. Cómo se probó el programa armado

Correr el `.exe` en la misma PC donde se programó **no alcanza**: ahí Python y
las librerías ya están instalados, y pueden tapar algo que falte. Igual hay
cosas que se pueden comprobar acá:

1. Arranca, y el título muestra la versión.
2. La base se crea en la carpeta de datos, **no** junto al programa.
3. Un error al abrir la base queda en `errores.log`.
4. El informe de PyInstaller no reporta módulos faltantes que el programa use.

La prueba que de verdad cuenta es en **una PC limpia**, sin Python. Va en la
lista de entrega.

## 7. Lista de entrega

Antes de darle el programa al cliente:

- [ ] `pytest` pasa completo.
- [ ] Se subió el número de versión en `app/__init__.py`.
- [ ] `pyinstaller SistemaReservas.spec --noconfirm` termina sin errores.
- [ ] El `.exe` abre en **una PC sin Python** (o una máquina virtual limpia).
- [ ] En esa PC: cargar un cliente, un producto, un lote y una reserva;
      cerrar, volver a abrir, y verificar que los datos siguen ahí.
- [ ] Exportar a Excel y abrir el archivo.
- [ ] Comprimir `dist/SistemaReservas` en `SistemaReservas-1.0.zip`.
- [ ] Explicarle al cliente cómo hacer una copia de la base (§8).

## 8. Para la importadora

- **Instalar:** descomprimir el `.zip` en una carpeta (por ejemplo,
  `C:\SistemaReservas`) y crear un acceso directo a `SistemaReservas.exe` en el
  escritorio.
- **Actualizar:** reemplazar esa carpeta por la de la versión nueva. Los datos
  no se tocan, porque están en otra carpeta (§3).
- **Copia de seguridad:** copiar `reservas.db` de
  `%LOCALAPPDATA%\SistemaReservas` (escribir eso en la barra del Explorador de
  archivos lleva directo) a un pendrive o a la nube, **con el programa
  cerrado**.

## 9. Lo que queda afuera

Quedó escrito desde la clase 1, en los
[requisitos](requisitos.md#7-fuera-de-alcance-lo-que-no-hacemos-en-este-curso):
varias PCs con la misma base, usuarios y contraseñas, copias automáticas, envío
de emails. A eso se suma un tema que aparece en cuanto haya una versión 2.0:
**cambiar la estructura de una base que ya tiene datos**. Hoy `esquema.sql`
crea la base de cero. Una versión nueva que agregue una columna necesitaría
modificar las bases existentes sin perder lo que tienen (lo que se llama
*migraciones*).

---

## Mirando el recorrido completo

| Clase | Documento | La idea que se lleva |
|-------|-----------|----------------------|
| 1 | [Requisitos](requisitos.md), [bocetos](bocetos.md) | Entender el problema y acordar las palabras antes de programar. Decir qué queda afuera. |
| 2 | [Modelo de datos](modelo_er.md) | Cada dato en un solo lugar. Lo que se puede calcular no se guarda. |
| 3 | `app/bd.py` | Un solo lugar escribe SQL. Cada función recibe la conexión. |
| 4 | [Lógica de negocio](logica_negocio.md) | Las reglas, separadas de la pantalla y probadas con tests. |
| 5 | [Interfaz](interfaz.md) | La pantalla muestra y pide datos; no decide qué es válido. |
| 6 | [Interfaz II](interfaz_2.md) | Revisar cada pantalla contra los requisitos que dice cumplir. |
| 7 | [Toques profesionales](toques_profesionales.md) | Validar lo justo. Un error previsible merece un mensaje claro. |
| 8 | Este documento | El programa tiene que funcionar donde no está quien lo escribió. |

Hay algo que se repitió en casi todas las clases: **el diseño cambió al
programar**. Apareció RN-09, "Nuevo" y "Limpiar" resultaron ser lo mismo, al
boceto de Reservas le faltaba un filtro, y la base tuvo que mudarse de carpeta.
Cada vez se volvió al documento y se corrigió ahí, con una nota de por qué.

Planificar no sirve para acertar todo de entrada. Sirve para tener dónde
anotar lo que se aprende, y para que el próximo que lea el proyecto entienda
no solo **qué** se hizo, sino **por qué**.
