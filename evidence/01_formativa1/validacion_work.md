# Validación técnica en Work — Formativa 1

Fecha: 10 de octubre de 2026. Esta evidencia corresponde al entorno aislado Work Linux, no al computador Windows del estudiante.

## Método real y alcance

Se ejecutó secuencialmente cada celda de código del notebook mediante `ipykernel.inprocess.InProcessKernel` e IPython `run_cell`. La ejecución fue real, con 19 celdas, cero errores y duración registrada de 7,836 segundos. El notebook entregado conserva las salidas de esa ejecución. Los sockets TCP e IPC para un servidor de kernel están bloqueados en Work; no se atribuye a esta prueba una ejecución mediante JupyterLab ni una validación del transporte de Windows.

Python Work: 3.12.14. Versiones de cálculo coincidentes con las compartidas desde Windows: NumPy 2.5.3, pandas 3.0.6, SciPy 1.18.1 y matplotlib 3.11.2. Windows usa Python 3.12.0 y conserva su propio lock, intérprete y kernel. La diferencia de versión de Python y del mecanismo de ejecución está declarada.

## Evidencias disponibles

- `ejecucion_work.json`: identidad de datos, versiones, verificaciones numéricas y salidas exportadas.
- `validacion_notebook_work.json`: secuencia real, conteo de celdas, cero errores, duración y limitación del transporte.
- Notebook: 41 celdas, 19 de código ejecutadas en orden, sin salidas de error.
- 19 tablas CSV y ocho PNG, más resultados.json.
- Versión inicial del PDF: 11 páginas, convertida desde Word y revisada visualmente. La versión vigente se compila desde LaTeX y tiene 13 páginas, con portada e índice; su comprobación específica consta en validacion_latex.md.
- `manifiesto_paquete.json`: identidad de los archivos entregados como referencia, cuando se incorpora al paquete final.

Los resúmenes originales se conciliaron con conteos de etiquetas y faltantes; las medias por filas con medias locales ponderadas; los IC y el estadístico t con fórmulas y resultados de SciPy. Se comprobó integridad del CSV y del dataframe original. Los números del informe Word original se generaron leyendo los CSV y resultados.json de esta misma ejecución. La conversión a LaTeX conserva esos números; no reestima parámetros.

## Qué permanece pendiente

La ejecución Windows fue acreditada posteriormente por el estudiante mediante la salida final correcta y `ejecucion_windows.json`, registrado el 10 de octubre de 2026 a las 18:02 UTC. Los archivos adjuntados permitieron conciliar las 19 tablas y resultados.json; consultar `validacion_windows.md` y `validacion_windows.json`. Se conserva este registro de Work sin atribuirle la ejecución en el computador del estudiante. Sigue pendiente la evidencia de entrega y participación en Canvas.

No se ha validado independencia espacial, representatividad nacional ni desempeño predictivo. La ejecución correcta de código no demuestra esos supuestos.
