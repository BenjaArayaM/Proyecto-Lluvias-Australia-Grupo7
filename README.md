# MCDI501 — Lluvias en Australia — Grupo 7

Proyecto acumulativo de Estadística Computacional para la Toma de Decisiones, del Magíster en Ciencia de Datos e Inteligencia Artificial de la Universidad Andrés Bello.

**Estudiante:** Benjamín Araya. Los demás integrantes se incorporarán cuando se confirme su identificación para este curso.

**Repositorio de trabajo:** https://github.com/BenjaArayaM/Proyecto-Lluvias-Australia-Grupo7

## Problema y dataset

El problema general es estudiar la ocurrencia de lluvia al día siguiente en localidades de Australia a partir de información meteorológica. La variable objetivo es `RainTomorrow`.

- Dataset: Rain in Australia.
- Fuente: https://www.kaggle.com/datasets/jsphyg/weather-dataset-rattle-package/data
- Archivo esperado: `data/raw/weatherAUS.csv`.
- Unidad de observación: un registro meteorológico de una localidad en una fecha.

El dataset original se conserva sin modificaciones, una sola vez y fuera del versionamiento. Su copia local se comprobará antes de comenzar el análisis. No se redistribuye el CSV en este paquete; las condiciones de redistribución deben verificarse antes de cualquier publicación de datos.

## Evaluaciones y estado

| Identificador | Evaluación | Ponderación | Estado |
|---|---|---:|---|
| `01_formativa1` | Formativa 1 — Informe 1 | 0 % | Pendiente de desarrollo |
| `02_sumativa1` | Sumativa 1 — Informe técnico de avance | 20 % | Pendiente de desarrollo |
| `03_sumativa2` | Sumativa 2 — Informe 3 | 20 % | Pendiente de desarrollo |
| `04_formativa2` | Formativa 2 — Informe 4 | 0 % | Pendiente de desarrollo |
| `05_sumativa3` | Sumativa 3 — Cierre y comunicación | 60 % | Pendiente de desarrollo |

La evaluación activa es la Formativa 1. La estructura de todas las evaluaciones está preparada para conservar continuidad; cada fase se desarrolla cuando el estudiante la autoriza.

## Organización

| Ruta | Uso |
|---|---|
| `.venv/` | Entorno virtual local, excluido de Git. Se crea en cada computador. |
| `data/raw/` | Dataset original, excluido de Git. |
| `src/` | Funciones comunes, cuando sea necesario reutilizar código. |
| `notebooks/` | Notebooks identificados por evaluación. |
| `results/<identificador>/` | Tablas, gráficos y resultados estadísticos exportados. |
| `reports/<identificador>/` | Informes editables y PDF. |
| `evidence/<identificador>/` | Evidencias de ejecución y entrega. |
| `presentations/05_sumativa3/` | Presentación final y materiales asociados. |
| `docs/` | Requisitos, decisiones metodológicas y continuidad. |
| `requirements.txt` | Dependencias directas y versiones mínimas del proyecto. |
| `requirements-lock-windows.txt` | Versiones exactas instaladas en el entorno Windows del estudiante. |

Los archivos `.gitkeep` permiten conservar directorios inicialmente vacíos en Git; no representan análisis realizados. `data/raw/` se crea localmente y permanece excluido.

Nombres previstos para los notebooks:

- `01_formativa1_eda_inferencia.ipynb`
- `02_sumativa1_analisis_exploratorio_inferencial.ipynb`
- `03_sumativa2_validacion_simulacion_remuestreo.ipynb`
- `04_formativa2_modelamiento_predictivo.ipynb`
- `05_sumativa3_modelamiento_integrado.ipynb`

Los notebooks todavía no han sido generados. No hay resultados estadísticos ni informes de evaluación dentro de esta base.

## Entorno y dependencias

En el computador del estudiante se comprobaron el 2026-10-10:

- Python 3.12.0, la activación de `.venv` y la ruta del intérprete activo.
- Instalación de las dependencias de `requirements.txt` y comprobación con `python -m pip check`: `No broken requirements found.`
- Importación correcta de las diez bibliotecas principales; sus versiones se detallan en `evidence/01_formativa1/preparacion_entorno.md`.
- Registro del kernel `grupo7_mcdi501`, con nombre visible **Python (Grupo 7 - MCDI501)** y ruta al intérprete de `.venv` comprobada en `kernel.json`.
- Registro de versiones mediante `pip freeze --all` en `requirements-lock-windows.txt` y generación de `evidence/01_formativa1/entorno.json` con fecha, plataforma, intérprete, configuración del kernel y SHA-256 del archivo de dependencias.

`requirements.txt` define las dependencias directas y sus mínimos; `requirements-lock-windows.txt` conserva la instalación exacta observada, incluidas las dependencias transitivas y pip. Este registro corresponde a Windows y debe revisarse para reproducir el entorno en otro sistema operativo.

Estas comprobaciones verifican la preparación y las importaciones. La apertura de JupyterLab, el arranque del kernel y la ejecución completa del notebook de la Formativa 1 siguen pendientes.

## Reproducción

La preparación local se guía y verifica paso a paso con el estudiante. Otro integrante deberá crear su propio entorno, instalar las dependencias verificadas y disponer del mismo CSV en `data/raw/`. En Windows, las versiones exactas de referencia están en `requirements-lock-windows.txt`; cada integrante registra su propio intérprete y kernel.

Todos los análisis utilizarán rutas relativas al proyecto. Se documentarán semillas, versiones, hash del dataset y transformaciones. La reproducción de resultados se describirá cuando exista un notebook ejecutado y validado; todavía no hay un procedimiento de análisis terminado.

## Continuidad y metodología

Los resultados exportados de una evaluación permanecen en su directorio y las fases posteriores los consultan mediante rutas relativas. Cada ficha de continuidad identifica los archivos y la versión de los resultados reutilizados.

La estructura temporal y geográfica exige revisar dependencia entre observaciones, heterogeneidad por localidad, faltantes y alcance de las inferencias. Las imputaciones y transformaciones definitivas se decidirán para la evaluación correspondiente. El preprocesamiento y la selección de variables para modelamiento se ajustarán usando únicamente datos de entrenamiento, con un esquema de validación justificado.

## Trabajo con Git

El estudiante ejecuta todos los comandos Git desde Git Bash. La asistencia mantiene GitHub en modo de lectura. Antes de cada commit se revisa la lista de archivos; el dataset original, las credenciales, el entorno y los temporales quedan excluidos.

El repositorio se clonó estando vacío. El primer commit de la base, su publicación y la creación de la rama `formativa1-benjamin` siguen pendientes de ejecución y verificación por el estudiante.

## Fuentes

- Rúbricas oficiales: `RUBRICAS(2).xlsx`; las referencias de hoja y filas se conservan en `docs/auditoria_requisitos.md`.
- Primera sesión: `Sesion01_MCDI501_06102026.pdf`.
- Repositorio docente: https://github.com/jpmaidana/MCDI501-202682
- Plantilla de Formativa 1: `04-plantillas/word/plantilla_formativa1_eda_inferencia.docx` del repositorio docente.
- Documentación de entornos virtuales: https://docs.python.org/3.12/library/venv.html
- Formato de dependencias de pip: https://pip.pypa.io/en/stable/reference/requirements-file-format/
- Registro de kernels: https://ipython.readthedocs.io/en/stable/install/kernel_install.html

Los ejemplos docentes se usan como referencia metodológica; los resultados del proyecto deben calcularse con `weatherAUS.csv`.
