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

El código llega recién en la clase 3. La historia de commits y las etiquetas
`clase-NN` muestran el proceso en orden.

## Cómo se trabaja

Cada clase termina en una **etiqueta de git** (`clase-01`, `clase-02`, …).
Si faltaste o te atrasaste, podés ponerte al día con:

```bash
git checkout clase-04
```

## Estructura

```
curso_reservas/
├── docs/       requisitos, bocetos, modelo de datos, lógica de negocio
├── datos/      script de creación de la base y datos de ejemplo
├── app/        el código de la aplicación
├── tests/      pruebas de la lógica de negocio
└── requirements.txt
```

## Plan del curso

| Clase | Tema | Resultado |
|-------|------|-----------|
| 1 | Del problema al diseño | `docs/requisitos.md`, `docs/bocetos.md` |
| 2 | Modelo de datos | `docs/modelo_er.md`, `datos/esquema.sql` |
| 3 | Proyecto y base de datos | entorno virtual, git, `app/bd.py` |
| 4 | Lógica de negocio | `app/negocio.py` + `tests/`, `docs/logica_negocio.md` |
| 5 | Interfaz I | ventana principal y pantalla de Clientes |
| 6 | Interfaz II | pantallas de Lotes y Reservas |
| 7 | Toques profesionales | exportar a Excel, validaciones |
| 8 | Entrega | ejecutable con PyInstaller, README final |

## Poner en marcha el proyecto (clase 3)

Desde una terminal en la carpeta `curso_reservas` (en VS Code: *Terminal → New Terminal*):

```bash
# 1. Crear el entorno virtual (una sola vez)
python -m venv .venv

# 2. Activarlo (cada vez que abrís una terminal nueva)
.venv\Scripts\activate          # Windows
source .venv/bin/activate       # macOS / Linux

# 3. Instalar las librerías del proyecto
pip install -r requirements.txt

# 4. Crear la base con los datos de ejemplo
python -m app.bd
```

El paso 4 crea `reservas.db`. Podés abrirla con DB Browser for SQLite para mirarla.
La base **no se sube a git**: cada uno la genera con este comando.

## Correr los tests (clase 4)

Con el entorno activado:

```bash
pytest
```

Prueban todas las reglas de negocio sobre una base en memoria. No hace falta
haber creado `reservas.db`, y si existe, no la tocan.

## Requisitos para instalar (antes de la clase 3)

- Python 3.12 o superior — <https://www.python.org/downloads/>
- Visual Studio Code — <https://code.visualstudio.com/>
- Git — <https://git-scm.com/downloads>
- DB Browser for SQLite — <https://sqlitebrowser.org/>

## Licencia

- **Documentos** (archivos `.md`, incluidos requisitos, bocetos y modelo de datos):
  [CC BY 4.0](LICENSE-DOCS.md). Podés usarlos y adaptarlos, también para tus
  propios cursos, siempre que cites la fuente.
- **Código** (`.py`, `.sql`): [MIT](LICENSE).
