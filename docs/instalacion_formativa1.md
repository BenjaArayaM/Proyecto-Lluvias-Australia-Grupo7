# Incorporación y comprobación de la Formativa 1

Este ZIP es una **actualización para el proyecto existente**. No es necesario volver a clonar, crear otra carpeta raíz ni reinstalar el entorno ya comprobado.

## Estado actual y actualización de validación

El estudiante ya incorporó los archivos y ejecutó el notebook completo en Windows. La salida final, el registro del 10 de octubre de 2026 a las 18:02 UTC y la comparación independiente de las 19 tablas y resultados.json acreditan la reproducción y equivalencia numérica. Los pasos de instalación y ejecución de abajo se conservan como instrucciones para una reproducción futura; no indican que la ejecución actual esté pendiente.

## Actualización vigente: informe LaTeX

Extraer `formativa1_latex_grupo7.zip` en una carpeta temporal y copiar su contenido a la raíz existente del proyecto, combinando `reports/`, `docs/` y `evidence/`. Reemplazar el PDF y la documentación coincidentes. El paquete incorpora la fuente editable `.tex`, el logo y la validación de su compilación; también añade exclusiones de auxiliares LaTeX a `.gitignore`. Si ese archivo tiene cambios propios, conservarlos al incorporar el nuevo bloque.

El informe vigente tiene 13 páginas, incluida portada e índice. La página 12 documenta la reproducción Windows. El paquete no contiene notebook, módulo, resultados, dataset, entorno ni registros Windows del estudiante. No requiere repetir el análisis ya validado.

Consultar `docs/edicion_informe_latex.md` para modificar y compilar. Abrir el nuevo PDF y comprobar que la portada muestra a los cuatro integrantes, que el índice corresponde a los títulos y que las tablas son legibles. La revisión del estado de Git se solicita después de confirmar esa incorporación.

## Reproducción futura desde el paquete base

Los pasos siguientes documentan la instalación original desde `formativa1_completa_grupo7.zip` (F1-1.1, formato Word), ya realizada por el estudiante. No repetirlos para incorporar el formato LaTeX: ese paquete base puede contener el PDF anterior. En una instalación nueva, incorporar la actualización LaTeX al final y conservar los registros propios del nuevo entorno.

## Paso 1: copiar los archivos

1. En JupyterLab, guardar y cerrar la pestaña antigua `01_formativa1_eda_inferencia.ipynb` para evitar que una sesión abierta vuelva a guardar la versión anterior.
2. Descargar y extraer `formativa1_completa_grupo7.zip` en una carpeta temporal mediante el Explorador de Windows.
3. Copiar el contenido extraído a `C:\Users\benja\OneDrive\Escritorio\Proyecto-Lluvias-Australia-Grupo7`. Combinar las carpetas existentes y reemplazar únicamente los archivos coincidentes que incluye este paquete.
4. Comprobar que existan directamente `src/formativa1.py` y `notebooks/01_formativa1_eda_inferencia.ipynb` dentro del proyecto. Evitar una carpeta anidada adicional llamada `formativa1_completa_grupo7`.

El paquete no contiene ni reemplaza `.git/`, `.venv/`, `data/raw/weatherAUS.csv`, `requirements-lock-windows.txt`, `evidence/01_formativa1/entorno.json` ni `preparacion_entorno.md`. Tampoco elimina los archivos de las otras evaluaciones.

**Evidencia para el primer paso:** confirmar la copia y la ubicación del módulo y notebook. Los comandos Git y la preparación del commit se revisan después de la ejecución local.

## Paso 2: ejecutar en JupyterLab después de comprobar la copia

1. Abrir el notebook actualizado en `notebooks/`.
2. Elegir `Python (Grupo 7 - MCDI501)`.
3. En el menú Kernel, usar **Restart Kernel and Run All Cells…**, confirmar la acción y esperar a que termine.
4. Guardar el notebook. La última celda debe mostrar **FORMATIVA 1 — EJECUCIÓN COMPLETA: CORRECTA**. Deben ejecutarse 19 celdas de código sin errores.
5. Revisar las salidas: 145.460 × 23, 49 localidades, 142.193 etiquetas, Yes=31.877, diferencia local de humedad de aproximadamente 20,0769 y t≈25,1461.
6. Comprobar que se creó `evidence/01_formativa1/ejecucion_windows.json`; compartir su contenido y la salida de la última celda para revisar la evidencia.

Si aparece un error, detenerse y compartir el texto completo de la primera celda que falla. No continuar ejecutando celdas posteriores para ocultarlo. Los gráficos y tablas se regeneran al ejecutar el notebook; el informe está construido con la ejecución de referencia comprobada en Work y debe revisarse si cambian los resultados.

## Paso 3: revisar el informe y Canvas

La portada ya identifica a Benjamín Araya, Alan Cañete, Patricio Cortez y Jorge Guaico. Revisar los nombres y recompilar el PDF si se modifica la fuente LaTeX vigente. Revisar las instrucciones vigentes de Canvas, la fecha y el foro. Estudiar la sección inferencial y adaptar los borradores del foro al trabajo real del equipo y de los compañeros.

Las fases posteriores y las operaciones con Git se abordan por separado después de verificar esta evaluación. La asistencia no ejecuta comandos Git ni publica contenidos.
