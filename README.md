# Sistema de Reservas — Proyecto del curso

Proyecto que construimos **desde cero** a lo largo de 8 clases: una aplicación de
escritorio para que una importadora pueda **reservar mercadería a sus clientes
antes de que llegue** al depósito.

> Basado en un sistema real que funciona en una importadora. Acá lo rehacemos
> paso a paso, corrigiendo los errores de diseño que tuvo la primera versión.

## Cómo se trabaja

Cada clase termina en una **etiqueta de git** (`clase-01`, `clase-02`, …).
Si faltaste o te atrasaste, podés ponerte al día con:

```bash
git checkout clase-03
```

## Estructura

```
curso_reservas/
├── docs/       requisitos, modelo de datos, bocetos de pantallas
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
| 4 | Lógica de negocio | `app/negocio.py` + `tests/` |
| 5 | Interfaz I | ventana principal y pantalla de Clientes |
| 6 | Interfaz II | pantallas de Lotes y Reservas |
| 7 | Toques profesionales | exportar a Excel, validaciones |
| 8 | Entrega | ejecutable con PyInstaller, README final |

## Requisitos para instalar (antes de la clase 3)

- Python 3.12 o superior — <https://www.python.org/downloads/>
- Visual Studio Code — <https://code.visualstudio.com/>
- Git — <https://git-scm.com/downloads>
- DB Browser for SQLite — <https://sqlitebrowser.org/>
