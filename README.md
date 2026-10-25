<!-- ESTADO_S3_WINDOWS -->
> **Estado S3 actualizado al 25 de octubre de 2026:** reproducción Windows
> verificada: 16 celdas en orden, ningún error y 22 controles correctos.
> Los resultados cotejados coinciden con Work dentro de tolerancia 1e-7.
> Benjamín confirmó que PDF y PowerPoint abren en su computador.
> Evidencias: `evidence/05_sumativa3/validacion_windows.json` y
> `evidence/05_sumativa3/validacion_windows.md`.
> Permanecen pendientes revisión académica grupal, ensayo/grabación,
> revisión para commit, publicación y entrega en Canvas.
>
> Los registros originales de Work y las menciones de pendientes en los
> materiales preparados entonces se conservan como antecedentes históricos.
> Esta actualización acredita reproducción y apertura; no acredita por sí
> sola revisión visual exhaustiva, participación grupal ni entrega.
<!-- FIN_ESTADO_S3_WINDOWS -->

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
| 01_formativa1 | Formativa 1 — Informe 1 | 0 % | Entregada; retroalimentación del profesor recibida. |
| 02_sumativa1 | Sumativa 1 — Informe técnico de avance | 20 % | Entregada e integrada en main; retroalimentación del profesor recibida. |
| 03_sumativa2 | Sumativa 2 — Informe 3 | 20 % | Entregada y retroalimentada por el profesor, según actualización del estudiante; resultados conservados para S3. |
| 04_formativa2 | Formativa 2 — Informe 4 | 0 % | Entregada y retroalimentada por el profesor; referencia predictiva reproducida en S3. |
| 05_sumativa3 | Sumativa 3 — Cierre y comunicación | 60 % | Validada en Work y Windows; PDF/PPTX abiertos localmente. Revisión grupal, video, publicación y entrega pendientes. |

La preparación y ejecución de S3 fueron autorizadas por el estudiante. Los estados de entrega se distinguen de la existencia de archivos.

## Organización del proyecto

| Ruta | Contenido |
|---|---|
| data/raw/ | CSV original, excluido de Git. |
| src/formativa1.py | Funciones de lectura, auditoría, análisis y exportación de F1. |
| notebooks/ | Un notebook por evaluación; maestro S3 ejecutado en Work. |
| results/<identificador>/ | Tablas, gráficos y resultados numéricos por fase. |
| reports/<identificador>/ | Fuentes editables del informe, PDF y materiales de comunicación. |
| evidence/<identificador>/ | Evidencias diferenciadas de preparación, ejecución y entrega. |
| presentations/05_sumativa3/ | PPTX editable, notas, guion de diez minutos y datos de gráficos. |
| docs/ | Requisitos, decisiones, continuidad e instalación de F1. |
| requirements.txt | Dependencias directas del proyecto. |
| requirements-lock-windows.txt | Versiones exactas instaladas en el computador del estudiante. |
| .venv/ | Entorno local no versionado; cada integrante prepara el suyo. |

## Formativa 1 preparada

- Notebook `notebooks/01_formativa1_eda_inferencia.ipynb`: 41 celdas, 19 de código, con explicaciones, salidas, interpretaciones y limitaciones.
- Módulo `src/formativa1.py`.
- 19 tablas CSV, ocho figuras y `results/01_formativa1/resultados.json`.
- Informe editable en LaTeX y PDF compilado de 13 páginas (portada e índice incluidos) en `reports/01_formativa1/`. El Word anterior se conserva como referencia.
- Material del foro y guía de comentarios conservados como antecedentes de la evaluación entregada.
- Matriz completa de siete criterios: máximo 99 puntos, según la rúbrica oficial.
- Evidencias diferenciadas Work/Windows, comparación de resultados y ficha de continuidad. La entrega y retroalimentación fueron informadas por el estudiante el 18 de octubre de 2026.

El análisis incluye ficha de variables, calidad, descripción, relaciones bivariadas, cobertura, faltantes, tres IC individuales y una prueba básica. La inferencia usa **49 resúmenes por localidad**, con igual peso, y un modelo exploratorio condicionado a independencia aproximada entre localidades. No se ha validado independencia espacial ni representatividad nacional. No se imputa, elimina globalmente ni modela la variable objetivo.

## Entornos y ejecución comprobada

En Windows se verificaron Python 3.12.0, `.venv`, importaciones, `pip check`, versiones exactas, kernel `grupo7_mcdi501`, apertura de JupyterLab y arranque de un kernel. El estudiante comprobó además el CSV, el commit inicial **d5142a1** y la creación local de la rama **formativa1-benjamin**. La publicación de F1 y la integración posterior de S1 se verificaron en GitHub el 18 de octubre de 2026; las evidencias iniciales se conservan como registro histórico.

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
- `results/02_sumativa1/tables/`: once tablas CSV.
- `docs/entorno_sumativa1_jorge.md`: documentación del entorno.

### Análisis realizados

- Carga y verificación del dataset Weather Australia.
- Estadística descriptiva, asimetría, curtosis y datos faltantes.
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

Se comprobó la generación de cinco figuras y once tablas. La independencia espacial y temporal continúa siendo una limitación para la interpretación inferencial.

### Estado

- Análisis estadístico: desarrollado.
- Validación básica: completada.
- Informe técnico: publicado en `reports/02_sumativa1/informe_sumativa1_grupo7.pdf`.
- Entrega de Sumativa 1: informada y retroalimentada por el profesor.


## Sumativa 2 - Validación, simulación y remuestreo

Base de Patricio: `1484dd055fb99779932b85f0e87ac541400b893f`. Se conservan sus tres
scripts originales y se añade `src/cierre_sumativa2.py` para completar interpretación,
controles, visualización y continuidad. Los índices [S1](S1/README.md) y
[S2](S2/README.md) enlazan los entregables sin duplicarlos.

- Notebook: `notebooks/03_sumativa2_validacion_remuestreo.ipynb`.
- Informe PDF y LaTeX editable: `reports/03_sumativa2/`. Máximo siete páginas totales.
- Archivo reutilizable: `results/03_sumativa2/resultados_validados_s2.json`.
- Síntesis con intervalos y localidades influyentes: `results/03_sumativa2/tables/sintesis_resultados_para_s3.csv`.
- Decisiones y límites: `docs/continuidad_sumativa2.md`.
- Instrucciones de reproducción y edición: `docs/reproduccion_sumativa2.md`.
- Dependencias adicionales: `requirements-sumativa2.txt`, incluido SciPy >= 1.15.
- Evidencia: `evidence/03_sumativa2/`, con archivos separados por entorno.

Se ejecutan 10.000 remuestras por parámetro y método, 10.000 cambios de signo,
10.000 remuestras por correlación y 10.000 iteraciones Monte Carlo. Se mantienen
los estimandos de S1 y el CSV original. Los IC son condicionales a los supuestos;
los rangos simulados no son pronósticos. La correlación humedad/lluvia conserva
signo positivo y tiene magnitud sensible a restringir el rango de precipitación.

La reproducción Windows de S2 está verificada; consultar `evidence/03_sumativa2/validacion_windows.md`. El estudiante informó posteriormente la entrega y compartió la retroalimentación del profesor; S3 conserva sus resultados como antecedentes.
La asistencia no ejecuta Git ni publica cambios; Benjamín revisa y realiza esas operaciones.


## Sumativa 3 — Cierre y comunicación

La actualización se preparó contra main en `28e3a8a0805e11fd1b93beb273db7ca4060aa557`; no crea una rama ni publica cambios. El índice [S3](S3/README.md) enlaza los productos sin duplicarlos.

- Notebook: `notebooks/05_sumativa3_modelamiento_integrado.ipynb`.
- Código: `src/sumativa3.py`; verificador de ejecución: `src/verificar_entrega_sumativa3.py`.
- PDF de diez páginas y LaTeX editable con portada UNAB: `reports/05_sumativa3/`.
- Presentación PPTX de 12 diapositivas, notas y guion para cuatro integrantes: `presentations/05_sumativa3/`.
- Resultados completos y distribuciones: `results/05_sumativa3/`.
- Reproducción: `docs/reproduccion_sumativa3.md`; dependencias: `requirements-sumativa3.txt`.
- Decisiones: `docs/decisiones_sumativa3.md`; ficha de continuidad: `docs/continuidad_sumativa3.md`.
- Matriz de los seis criterios (108 puntos) y evidencias: `evidence/05_sumativa3/`.

Se reprodujo la referencia F2 y se compararon 16 regresiones de imputación, tres procedimientos logísticos, tres estrategias de faltantes para la especificación final y 2.000 remuestras por localidad. M2 obtiene AUC 0,8619, recall 68,26 %, precision 57,98 % y accuracy 81,79 % en la prueba ya usada en F2. El IC bootstrap de OR para MaxTemp incluye uno. La elección y los umbrales se basan en validación dentro de entrenamiento; los scores ponderados no se presentan como probabilidades calibradas.

El notebook se ejecutó dos veces en un kernel real nuevo de Work: 16 celdas, ningún error, 22 controles correctos y concordancia exacta de los 32 archivos numéricos cotejados. La reproducción Windows de S3 todavía requiere ejecución y evidencia local. La presentación/guion no acredita el video ni la participación; revisión grupal y Canvas siguen pendientes. No se ha ejecutado ninguna operación Git por la asistencia.
