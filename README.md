# Sistema de Reservas — Proyecto del curso

Proyecto que construimos **desde cero** a lo largo de 8 clases: una aplicación de
escritorio para que una importadora pueda **reservar mercadería a sus clientes
antes de que llegue** al depósito.

> Basado en un sistema real que funciona en una importadora. Acá lo rehacemos
> paso a paso, corrigiendo los errores de diseño que tuvo la primera versión.

## Cómo encaramos un proyecto

La idea central del curso: **no se empieza escribiendo código**. Primero se
entiende el problema, después se decide qué datos hacen falta, y recién entonces
se programa. Los documentos de [`docs/`](docs/) muestran ese recorrido, en este
orden:

1. **[Requisitos](docs/requisitos.md)**: el problema del cliente, quién usa el
   sistema, un glosario para acordar las palabras, requisitos funcionales, reglas
   de negocio y, también importante, lo que queda **fuera de alcance**.
2. **[Bocetos de pantallas](docs/bocetos.md)**: qué datos muestra y pide cada
   pantalla, dibujados antes de pensar en el diseño visual. De acá surgen las
   preguntas que se responden en el paso siguiente.
3. **[Modelo de datos](docs/modelo_er.md)**: de los sustantivos a las tablas.
   Cada decisión de diseño está explicada, junto con el error del sistema
   original que corrige: datos duplicados, totales guardados a mano, fechas como
   texto que no se ordenan bien y contraseñas dentro de la base.
4. **[Lógica de negocio y tests](docs/logica_negocio.md)**: cada regla pasa a
   código separado de la interfaz y de la base, y cada una tiene un test.
   Incluye una regla que apareció al programar y volvió a los requisitos.
5. **[Interfaz](docs/interfaz.md)**: los bocetos se convierten en ventanas. La
   pantalla solo muestra y pide datos, y los errores previstos e imprevistos
   tienen cada uno su tratamiento. También muestra qué cambió del boceto al
   programarlo, y un error que no se veía leyendo el código pero apareció al
   probar.
6. **[Interfaz II](docs/interfaz_2.md)**: convertir lo que escribe el usuario,
   mantener al día varias ventanas abiertas y confirmar lo que no tiene vuelta
   atrás. También muestra un filtro que el boceto olvidó, y que apareció al
   revisar la pantalla contra los requisitos.
7. **[Toques profesionales](docs/toques_profesionales.md)**: convertir un
   "error inesperado" previsible en un mensaje claro, validar lo justo sin
   rechazar datos reales, y un Excel pensado para quien lo va a usar. También
   deja escrito lo que se decidió no hacer.
8. **[Entrega](docs/entrega.md)**: lo que cambia cuando el programa sale de la
   PC de quien lo escribió (dónde van los datos, a dónde van los errores sin
   terminal), la lista de entrega y una mirada al recorrido completo.

El código llega recién en la clase 3. La historia de commits y las etiquetas
`clase-NN` muestran el proceso en orden. A lo largo del curso, cada vez que el
diseño cambió al programar, se volvió al documento y se dejó una nota de por
qué.

## Qué hace el programa

- **Clientes y productos**: alta, modificación y búsqueda.
- **Lotes**: la mercadería que viene en camino, con su fecha de arribo. Se
  puede cambiar la fecha si el envío se atrasa, o anular el lote si la compra
  se cae.
- **Reservas**: apartar unidades de un lote para un cliente, sin poder
  reservar más de lo que viene. Entregar cuando llega, o cancelar.
- **Totales al día**: disponible, reservado y entregado se calculan, nunca se
  cargan a mano.
- **Exportar a Excel** lotes y reservas, listo para filtrar y ordenar.

## Cómo se trabaja

Cada clase termina en una **etiqueta de git** (`clase-01` … `clase-08`).
Para ver el proyecto como quedó al final de una clase:

```bash
git checkout clase-04      # y para volver al final:  git checkout main
```

## Poner en marcha el proyecto

Requisitos: **Python 3.12 o superior** y **Git**. Para seguir el curso también:
Visual Studio Code y DB Browser for SQLite (ver al final).

Desde una terminal en la carpeta del proyecto (en VS Code: *Terminal → New Terminal*):

```bash
# 1. Crear el entorno virtual (una sola vez)
python -m venv .venv

# 2. Activarlo (cada vez que abrís una terminal nueva)
.venv\Scripts\activate          # Windows
source .venv/bin/activate       # macOS / Linux

# 3. Instalar las librerías del proyecto
pip install -r requirements.txt

# 4. Crear la base con los datos de ejemplo (opcional)
python -m app.bd
```

El paso 4 crea `reservas.db` con clientes, productos, lotes y reservas
**ficticios**. Podés abrirla con DB Browser for SQLite para mirarla. La base
**no se sube a git**: cada uno la genera con este comando.

### Abrir el programa

```bash
python -m app.main
```

Si todavía no existe `reservas.db`, se crea vacía.

### Correr los tests

```bash
pytest
```

Prueban reglas de negocio, conversiones y la exportación a Excel sobre una base
en memoria. No hace falta haber creado `reservas.db`, y si existe, no la tocan.

### Armar el programa para Windows

```bash
pyinstaller SistemaReservas.spec --noconfirm
```

El resultado queda en `dist/SistemaReservas/`. Para entregarlo, se comprime esa
carpeta. El programa instalado guarda sus datos en
`%LOCALAPPDATA%\SistemaReservas`. Antes de entregar, revisá la
[lista de entrega](docs/entrega.md#7-lista-de-entrega).

## Estructura

```
curso_reservas/
├── docs/                   un documento por etapa: de los requisitos a la entrega
├── datos/                  script de creación de la base y datos de ejemplo
├── app/                    el código (ver app/README.md)
│   ├── bd.py               el único archivo con SQL
│   ├── negocio.py          las reglas: qué se puede hacer y qué no
│   ├── exportar.py         el libro de Excel
│   ├── ubicaciones.py      dónde va cada archivo, en desarrollo e instalado
│   ├── main.py             punto de entrada
│   └── ui/                 las pantallas
├── tests/                  pruebas que corren sin abrir ventanas
├── SistemaReservas.spec    la receta de PyInstaller
└── requirements.txt
```

## Las 8 clases

| Clase | Tema | Resultado |
|-------|------|-----------|
| 1 | Del problema al diseño | `docs/requisitos.md`, `docs/bocetos.md` |
| 2 | Modelo de datos | `docs/modelo_er.md`, `datos/esquema.sql` |
| 3 | Proyecto y base de datos | entorno virtual, git, `app/bd.py` |
| 4 | Lógica de negocio | `app/negocio.py` + `tests/`, `docs/logica_negocio.md` |
| 5 | Interfaz I | ventana principal y pantalla de Clientes, `docs/interfaz.md` |
| 6 | Interfaz II | pantallas de Productos, Lotes y Reservas, `docs/interfaz_2.md` |
| 7 | Toques profesionales | exportar a Excel, validaciones, `docs/toques_profesionales.md` |
| 8 | Entrega | ejecutable con PyInstaller, `docs/entrega.md`, este README |

## Herramientas para seguir el curso

- Python 3.12 o superior — <https://www.python.org/downloads/>
- Visual Studio Code — <https://code.visualstudio.com/>
- Git — <https://git-scm.com/downloads>
- DB Browser for SQLite — <https://sqlitebrowser.org/>

## Licencia

- **Documentos** (archivos `.md`, incluidos requisitos, bocetos y modelo de datos):
  [CC BY 4.0](LICENSE-DOCS.md). Podés usarlos y adaptarlos, también para tus
  propios cursos, siempre que cites la fuente.
- **Código** (`.py`, `.sql`): [MIT](LICENSE).
