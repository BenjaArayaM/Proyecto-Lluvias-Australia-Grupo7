# Reproducción y edición de Sumativa 2

## Alcance y procedencia

Esta actualización completa la documentación y los entregables sobre la rama
`sumativa2-patricio`, commit base `1484dd055fb99779932b85f0e87ac541400b893f`.
Conserva sin cambios los tres scripts de Patricio. El módulo `src/cierre_sumativa2.py`
los ejecuta, concilia S1, mejora las visualizaciones del informe y completa diagnósticos,
interpretación y continuidad. El informe no incorpora un modelo de Sumativa 3.

El paquete se aplica sobre esa base, preservando los archivos de las fases anteriores.
No incluye el dataset, entornos virtuales, credenciales, comandos ejecutados de Git,
auxiliares de LaTeX ni materiales privados de retroalimentación del profesor.
No debe extraerse sobre cambios locales sin revisar antes el estado del repositorio.
Los comandos de Git se revisarán de uno en uno con Benjamín antes de commit/push.

## Dependencias

Se utilizan pandas, NumPy, SciPy y matplotlib, además de Jupyter/ipykernel y las
herramientas habituales de notebooks. `requirements-sumativa2.txt` complementa
`requirements.txt`: requiere SciPy >= 1.15 por el argumento `rng=` utilizado por
Patricio en BCa. El lock de Windows de Formativa 1 se conserva como registro histórico;
no acredita las versiones con que se reproduzca S2.

El PDF se compila con **pdfLaTeX** (distribución TeX Live o MiKTeX); no se necesita
LaTeX para ejecutar el análisis estadístico. No se ha acreditado una compilación
en el computador del estudiante.

## Notebook completo

Archivo: `notebooks/03_sumativa2_validacion_remuestreo.ipynb`.

1. Verificar que exista `data/raw/weatherAUS.csv` con SHA-256
   `573fd715cd69fcacc4df32024d823b450ae3edaae7e8ff2eeb623adbed424014`.
2. Instalar las dependencias en el entorno `.venv` del proyecto cuando se verifique
   su estado. Seleccionar el kernel `Python (Grupo 7 - MCDI501)`.
3. Reiniciar el kernel y ejecutar todas las celdas desde el principio. Las correlaciones
   generan 30.000 réplicas en total y pueden tardar varios minutos; no interrumpir
   mientras muestran progreso.
4. Guardar el cuaderno y revisar todos los controles finales. Debe existir el registro
   `evidence/03_sumativa2/ejecucion_sumativa2_windows.json` si la ejecución fue Windows.
5. Compartir esa salida para comparar los valores numéricos con Work antes de preparar
   el commit. Los PNG pueden variar en bytes entre versiones de matplotlib; se cotejan
   sus datos, contenido y legibilidad, no solo la huella del archivo.

El notebook vuelve a ejecutar los tres scripts y no usa un modo de resultados en caché.
Las dos tablas nuevas de distribuciones guardan las 10.000 permutaciones y los
30.000 coeficientes bootstrap. Las salidas `s2_*.png` son las cinco figuras utilizadas
por el informe. Las siete figuras de los scripts originales se conservan también.

El punto de entrada alternativo es `src/cierre_sumativa2.py`, ejecutado con el Python
del entorno desde la raíz del proyecto. El notebook es el entregable de código
documentado y debe guardarse ejecutado para Canvas.

## Archivos de resultados

- `results/03_sumativa2/resultados_validados_s2.json`: resultados completos y unidades.
- `results/03_sumativa2/tables/sintesis_resultados_para_s3.csv`: diez entradas con
  intervalos, conclusiones, limitaciones y acciones posteriores.
- `docs/continuidad_sumativa2.md`: ficha de continuidad de lectura.
- `tables/diagnostico_convergencia_mc.csv`: error Monte Carlo y referencia teórica.
- `tables/diagnostico_supuestos_localidades.csv`: diagnóstico de forma y supuestos
  que no fueron demostrados.
- `tables/cercas_tukey_diagnostico.csv`: umbrales y conteos del filtro de sensibilidad.
- `tables/robustez_correlaciones_interpretada.csv`: signo y magnitud, con conclusiones.
- `tables/jackknife_diferencia_humedad.csv`: cambios al omitir cada una de 49 localidades.

Las rutas abreviadas `tables/` de esta lista corresponden a `results/03_sumativa2/tables/`.
Los dos resúmenes de texto y la tabla de clasificación se actualizan al finalizar el
notebook para evitar que la clasificación automática antigua se confunda con robustez
general. Ejecutar un script original aisladamente puede regenerar su resumen anterior:
el flujo vigente para el cierre es ejecutar todo el notebook o el módulo de cierre.

## Edición del informe en LaTeX

Fuente editable: `reports/03_sumativa2/informe_sumativa2_grupo7.tex`.
La portada editable está en `portada_unab.tex`, con el logotipo original de referencia
en `logo_unab.jpeg`. Conserva orden y posiciones de la portada de Sumativa 1: universidad,
programa, curso, evaluación, proyecto, integrantes, dataset, docente, fecha y repositorio.
La tipografía utiliza Times compatible (Nimbus Roman) para reproducir las métricas de la referencia.
Las cifras y tablas se cargan desde `datos_sumativa2.tex`, generado a partir de
`resultados_validados_s2.json` y tablas numéricas de S1/S2. El cuerpo del informe
puede editarse sin que el generador lo sobrescriba. No editar cifras a mano en el PDF.

Tras cambiar un cálculo, ejecutar primero el notebook completo y después el generador
`src/generar_informe_sumativa2.py`. La opción `--compilar` actualiza las macros y
compila dos veces con pdfLaTeX. El generador no ejecuta Git.
Si se modifica texto, comprobar de nuevo que el PDF conserve **como máximo siete
páginas totales**, contando identificación y referencias, y que no se corten tablas.

El ZIP autónomo de LaTeX suministrado lleva el informe, portada, logotipo y macros en la raíz,
y las cinco figuras en `figures/`; adapta solo esas rutas para compilar sin el proyecto.
En Overleaf se selecciona como documento principal `informe_sumativa2_grupo7.tex`
y se compila con pdfLaTeX.
El ZIP autónomo se usa para edición del informe y no reemplaza el paquete del proyecto.

## Estado de validación

La ejecución de Work se documenta con el entorno real y los controles numéricos.
En este entorno, la verificación de las celdas utiliza un kernel real ipykernel en
memoria porque los sockets TCP están restringidos; no se simula una ejecución Windows.
Los archivos `validacion_notebook_work.json` y `validacion_informe_work.json`
registran el alcance exacto de la comprobación.

La reproducción Windows de S2 fue acreditada el 18 de octubre de 2026 mediante
`ejecucion_sumativa2_windows.json`: 13 celdas sin errores y diez controles correctos.
Las cifras principales coinciden con Work; consultar
`evidence/03_sumativa2/validacion_windows.md`.
La revisión grupal y la entrega en Canvas siguen pendientes de evidencia.
La fecha límite y cualquier aclaración de Canvas deben verificarse en la plataforma.

## Organización S1/S2 solicitada por el enunciado

`S1/README.md` y `S2/README.md` son índices con enlaces relativos a los entregables de
cada sumativa. Cumplen la navegación por carpetas de fase conservando la organización
aprobada (`notebooks/`, `reports/`, `results/`, `evidence/`) sin duplicar notebooks o datos.
Esta equivalencia se declara de forma visible para revisión docente.
