# MCDI501 — Lluvias en Australia — Grupo 7

Proyecto acumulativo de Estadística Computacional para la Toma de Decisiones, Magíster en Ciencia de Datos e Inteligencia Artificial, Universidad Andrés Bello.

**Integrantes del Grupo 7:** Benjamín Araya, Alan Cañete, Patricio Cortez y Jorge Guaico. Nómina de cuatro integrantes confirmada para MCDI501 por el estudiante el 10 de octubre de 2026.

**Repositorio:** https://github.com/BenjaArayaM/Proyecto-Lluvias-Australia-Grupo7

## Problema y datos

Exploramos la lluvia al día siguiente (`RainTomorrow`) usando información meteorológica de localidades de Australia. Unidad observada: localidad y fecha. Fuente: https://www.kaggle.com/datasets/jsphyg/weather-dataset-rattle-package/data

El archivo original se conserva en `data/raw/weatherAUS.csv`, fuera de Git y sin imputaciones ni modificaciones. La versión comprobada contiene **145.460 filas, 23 columnas, 49 localidades y 14.094.055 bytes**; cubre 2007-11-01 a 2017-06-25. SHA-256:

`573fd715cd69fcacc4df32024d823b450ae3edaae7e8ff2eeb623adbed424014`

El ZIP de la Formativa 1 no redistribuye el dataset. Cada integrante debe obtener el archivo legítimamente y comprobar su identidad antes de reproducir el análisis.

## Evaluaciones

| Identificador | Evaluación | Ponderación | Estado |
|---|---|---:|---|
| 01_formativa1 | Formativa 1 — Informe 1 | 0 % | Análisis ejecutado en Work y reproducido en Windows; resultados conciliados y nómina confirmada. Canvas pendiente. |
| 02_sumativa1 | Sumativa 1 — Informe técnico de avance | 20 % | Análisis estadístico desarrollado en la rama sumativa1-jorge; informe y entrega pendientes. |
| 03_sumativa2 | Sumativa 2 — Informe 3 | 20 % | Pendiente de autorización y desarrollo. |
| 04_formativa2 | Formativa 2 — Informe 4 | 0 % | Pendiente de autorización y desarrollo. |
| 05_sumativa3 | Sumativa 3 — Cierre y comunicación | 60 % | Pendiente de autorización y desarrollo. |

La preparación de las cinco carpetas permite continuidad; no significa que se hayan iniciado las otras evaluaciones.

## Organización del proyecto

| Ruta | Contenido |
|---|---|
| data/raw/ | CSV original, excluido de Git. |
| src/formativa1.py | Funciones de lectura, auditoría, análisis y exportación de F1. |
| notebooks/ | Un notebook por evaluación; F1 ya preparado. |
| results/<identificador>/ | Tablas, gráficos y resultados numéricos por fase. |
| reports/<identificador>/ | Fuentes editables del informe, PDF y materiales de comunicación. |
| evidence/<identificador>/ | Evidencias diferenciadas de preparación, ejecución y entrega. |
| presentations/05_sumativa3/ | Presentación final cuando se autorice. |
| docs/ | Requisitos, decisiones, continuidad e instalación de F1. |
| requirements.txt | Dependencias directas del proyecto. |
| requirements-lock-windows.txt | Versiones exactas instaladas en el computador del estudiante. |
| .venv/ | Entorno local no versionado; cada integrante prepara el suyo. |

## Formativa 1 preparada

- Notebook `notebooks/01_formativa1_eda_inferencia.ipynb`: 41 celdas, 19 de código, con explicaciones, salidas, interpretaciones y limitaciones.
- Módulo `src/formativa1.py`.
- 19 tablas CSV, ocho figuras y `results/01_formativa1/resultados.json`.
- Informe editable en LaTeX y PDF compilado de 13 páginas (portada e índice incluidos) en `reports/01_formativa1/`. El Word anterior se conserva como referencia.
- Borrador de foro y guía para dos comentarios; todavía no publicados.
- Matriz completa de siete criterios: máximo 99 puntos, según la rúbrica oficial.
- Evidencias diferenciadas Work/Windows, comparación de resultados y ficha de continuidad; no se declaran entregas realizadas.

El análisis incluye ficha de variables, calidad, descripción, relaciones bivariadas, cobertura, faltantes, tres IC individuales y una prueba básica. La inferencia usa **49 resúmenes por localidad**, con igual peso, y un modelo exploratorio condicionado a independencia aproximada entre localidades. No se ha validado independencia espacial ni representatividad nacional. No se imputa, elimina globalmente ni modela la variable objetivo.

## Entornos y ejecución comprobada

En Windows se verificaron Python 3.12.0, `.venv`, importaciones, `pip check`, versiones exactas, kernel `grupo7_mcdi501`, apertura de JupyterLab y arranque de un kernel. El estudiante comprobó además el CSV, el commit inicial **d5142a1** y la creación local de la rama **formativa1-benjamin**. No hay evidencia de una publicación remota del proyecto.

Las 19 celdas de análisis se ejecutaron en Work con Python 3.12.14, un kernel real ipykernel en memoria y las mismas versiones de NumPy (2.5.3), pandas (3.0.6), SciPy (1.18.1) y matplotlib (3.11.2) registradas en Windows. Se verificaron identidad del CSV, integridad de datos, conteos, medias, intervalos y prueba. Los sockets de kernel están bloqueados en Work. El estudiante acreditó posteriormente la ejecución completa en JupyterLab Windows con su registro del 10 de octubre de 2026 a las 18:02 UTC y la salida final correcta. Se conciliaron las 19 tablas y resultados.json: 17 tablas coinciden tras adaptar los saltos de línea y las demás diferencias numéricas son del orden de 1e-14, sin cambiar las cifras publicadas.

`evidence/01_formativa1/ejecucion_work.json` y `validacion_notebook_work.json` describen la comprobación Work. `ejecucion_windows.json` conserva el registro aportado por el estudiante y `validacion_windows.json`/`validacion_windows.md` documentan la comparación independiente. Los registros locales del estudiante `entorno.json`, `preparacion_entorno.md` y `requirements-lock-windows.txt` se conservan y no son reemplazados por este paquete.

## Reproducción en el proyecto local

Para reproducir el análisis desde cero, consultar `docs/instalacion_formativa1.md`, abrir el notebook y seleccionar **Python (Grupo 7 - MCDI501)**. Reiniciar el kernel y ejecutar todas las celdas, guardar, revisar los resultados y comprobar `evidence/01_formativa1/ejecucion_windows.json`. La celda final debe indicar **FORMATIVA 1 — EJECUCIÓN COMPLETA: CORRECTA**.

Las rutas son relativas. La semilla registrada es 50107; no se realiza remuestreo aleatorio en F1. Los CSV se exportan con codificación UTF-8 con BOM para facilitar su lectura en Excel. Cada cálculo conserva sus conteos y sus exclusiones. Si cambia el archivo de datos, el notebook detiene la ejecución al no coincidir su identidad; antes de analizar otra versión se revisa la metodología y la trazabilidad.

## Edición del informe

La fuente vigente es `reports/01_formativa1/informe_formativa1_grupo7.tex`. Sus nueve tablas, tres ecuaciones, texto y referencias son editables. El logo permanece junto al `.tex` y las cinco figuras utilizadas se leen desde `results/01_formativa1/figures/`, conservando la estructura aprobada. `docs/edicion_informe_latex.md` explica la edición, la compilación con pdfLaTeX y el uso del ZIP autónomo para Overleaf.

La compilación y la revisión de las 13 páginas se realizaron en Work; el ZIP autónomo también se compiló fuera del árbol del proyecto. La comprobación del análisis Windows continúa acreditada y esta actualización no requiere ejecutarlo otra vez. La compilación en el computador del estudiante o en su cuenta de Overleaf aún no se ha acreditado. La evidencia del formato se registra en `evidence/01_formativa1/validacion_latex.json` y `validacion_latex.md`.

`manifiesto_paquete.json` conserva las huellas del paquete anterior F1-1.1. `manifiesto_latex.json` identifica esta actualización de formato F1-1.2; ambos mantienen el análisis F1-1.0.

## Rúbrica y continuidad

La rúbrica exige PDF en Canvas, publicación del producto y al menos dos comentarios fundamentados a otros grupos. Hay un intento y la fecha se consulta en Canvas. La nómina confirmada tiene cuatro integrantes y cumple el tamaño grupal de 3–4 indicado en el enunciado. No se confirmó un máximo de páginas para F1; no se importan condiciones de otra evaluación.

`docs/auditoria_requisitos.md` y `evidence/01_formativa1/auditoria_final.md` distinguen requisitos, recomendaciones, evidencia y pendientes. `docs/continuidad.md` conserva estimandos y resultados reutilizables. No se estima calificación mientras faltan evidencias.

El archivo completo ya fue explorado: este antecedente se declarará en las fases de modelamiento. Imputación, escalamiento, selección y cualquier ajuste predictivo deberán aprenderse dentro del entrenamiento, con validación temporal o geográfica justificada en la evaluación correspondiente.

## Git y fuentes

Todos los comandos Git los ejecuta el estudiante desde Git Bash. La asistencia mantiene GitHub en modo de lectura. Antes de cada commit se revisan la lista y el contenido; no se incluyen datos originales, entorno, credenciales ni temporales.

Fuentes principales: `RUBRICAS(2).xlsx` (Formativa 1, B3 y filas 42–70), `Sesion01_MCDI501_06102026.pdf`, plantillas y apuntes de https://github.com/jpmaidana/MCDI501-202682. La bibliografía verificable de Rattle, Bureau of Meteorology y SciPy figura en el informe y notebook.


## Sumativa 1 — Avance de análisis (Jorge)

El análisis de la Sumativa 1 se desarrolla en la rama `sumativa1-jorge`, tomando como base la metodología y los resultados de la Formativa 1.

### Archivos principales

- `notebooks/02_sumativa1_analisis.ipynb`: notebook de análisis.
- `results/02_sumativa1/figures/`: cinco figuras.
- `results/02_sumativa1/tables/`: nueve tablas CSV.
- `docs/entorno_sumativa1_jorge.md`: documentación del entorno.

### Análisis realizados

- Carga y verificación del dataset Weather Australia.
- Estadística descriptiva, asimetría y datos faltantes.
- Visualizaciones y correlaciones de Spearman.
- Intervalos de confianza para medias y proporciones.
- Prueba t sobre diferencias de humedad por localidad.
- Prueba chi-cuadrado entre RainToday y RainTomorrow.
- Verificación de supuestos estadísticos.
- Dependencia temporal de la humedad.
- Análisis de sensibilidad por localidad.

### Resultados principales

- Dataset: 145.460 registros y 49 localidades.
- Proporción de lluvia posterior: 22,42 %.
- Diferencia media de humedad por localidad: 20,08 puntos porcentuales.
- Chi-cuadrado de Pearson: 13.801,29.
- V de Cramér: 0,3131.
- Diferencia media en sensibilidad por localidad: 29,11 puntos porcentuales.

### Entorno y reproducibilidad

El notebook fue ejecutado en Windows con Python 3.13.0, utilizando temporalmente el kernel MCDI500 Grupo 7.

El dataset original debe ubicarse en `data/raw/weatherAUS.csv`. No se incorpora al repositorio.

Para reproducir el análisis, instalar las dependencias del proyecto, abrir el notebook, seleccionar un kernel compatible y ejecutar todas las celdas desde el inicio.

Se comprobó la generación de cinco figuras y nueve tablas. La independencia espacial y temporal continúa siendo una limitación para la interpretación inferencial.

### Estado

- Análisis estadístico: desarrollado.
- Validación básica: completada.
- Informe técnico: pendiente.
- Entrega de Sumativa 1: pendiente.

