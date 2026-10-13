# Edición y compilación del informe de Formativa 1

## Archivo que se modifica

La fuente vigente es `reports/01_formativa1/informe_formativa1_grupo7.tex`. El PDF se genera a partir de esa fuente; editar el PDF o el Word anterior no actualiza el LaTeX. La conversión corresponde al formato F1-1.2 y conserva el análisis validado F1-1.0.

El `.tex` contiene todo el texto, las nueve tablas, tres ecuaciones y referencias. Las cinco figuras son PNG generados por el análisis; para cambiar sus resultados debe revisarse el notebook y la correspondencia con el informe. No se reconstruyen gráficos manualmente.

En el bloque **DATOS DEL GRUPO** se encuentran título, cuatro integrantes, dataset, fecha del análisis y repositorio. La fecha de entrega se verifica en Canvas y no se deduce de esa portada. Los títulos se editan dentro de `\section{...}` y `\subsection{...}`. Cada tabla tiene sus filas de texto en `tabularx`: `&` separa columnas y `\\` termina una fila. Las fórmulas están escritas en matemáticas LaTeX.

Al escribir texto, escapar caracteres reservados: porcentaje `\%`, guion bajo `\_`, ampersand `\&` y numeral `\#`. Para enlaces usar `\url{...}`; para rutas, `\path{...}`. Los acentos se guardan en UTF-8. La bibliografía está en la última sección del propio `.tex`; no se necesita Biber ni un archivo `.bib`.

## Incorporación al proyecto existente

**Paso:** incorporar la actualización de formato antes del commit.

**Objetivo:** conservar una fuente modificable y el PDF que corresponde a ella.

**Directorio:** `C:\Users\benja\OneDrive\Escritorio\Proyecto-Lluvias-Australia-Grupo7`.

**Acción en Windows:** descargar `formativa1_latex_grupo7.zip`, extraerlo en una carpeta temporal y copiar su contenido a esa raíz, combinando las carpetas existentes. Reemplazar los archivos coincidentes del paquete. No crear otra carpeta raíz. El `.gitignore` incluye un bloque final para auxiliares LaTeX; si se personalizó el archivo local, conservar esas modificaciones al incorporar el bloque.

**Resultado esperado:** la fuente `.tex`, `logo_unab.png` y el PDF quedan directamente en `reports/01_formativa1/`. Las tablas y gráficos ya ejecutados permanecen en `results/01_formativa1/`. La documentación describe el formato vigente.

**Evidencia:** confirmar la copia y que se puede abrir el PDF nuevo, de 13 páginas, con los cuatro nombres y el índice. La compilación en Work está comprobada; la compilación en Windows o una cuenta de Overleaf se acredita después de realizarla.

**Siguiente paso:** revisar el estado local de Git y los archivos exactos antes de indicar `git add` o un commit. Todos los comandos Git los ejecuta el estudiante. La actualización no realiza operaciones de GitHub ni incluye el notebook, CSV, módulo, resultados o entorno.

## Opción recomendada para editar: Overleaf

1. Descargar `formativa1_overleaf_grupo7.zip`. Es una copia autónoma para edición, distinta del ZIP que actualiza el proyecto local.
2. En Overleaf, elegir **New Project → Upload Project** y seleccionar ese ZIP. No se requiere importar desde GitHub ni activar una sincronización Git.
3. Abrir `informe_formativa1_grupo7.tex` y elegirlo como documento principal si no se selecciona automáticamente. Compilador: **pdfLaTeX**.
4. Pulsar **Recompile**, revisar errores y recorrer el PDF. El ZIP contiene la fuente, logo y `figures/` con las cinco imágenes utilizadas; no contiene un PDF con el mismo nombre que la fuente principal.
5. Editar el texto o los metadatos necesarios y recompilar. Una edición de cifras requiere contrastarla con los resultados validados. Revisar portada, índice, tablas y numeración después de cada cambio.
6. Descargar el código fuente y el PDF por separado. Copiar el `.tex` modificado y el PDF al directorio local `reports/01_formativa1/`, conservando los nombres. Si se agregan o cambian gráficos, documentar la modificación y mantenerlos en `results/01_formativa1/figures/` dentro del proyecto.

La compilación del ZIP autónomo se comprobó con pdfLaTeX en Work, no en una sesión del estudiante en Overleaf. Los paquetes y la separación silábica de la instalación pueden cambiar la distribución de líneas; después de compilar, revisar la paginación y actualizar las referencias a páginas en las auditorías si cambia. Las cifras del análisis no dependen del compilador.

Documentación oficial consultada:
- https://www.overleaf.com/learn/latex/Kb/Uploading_a_project
- https://docs.overleaf.com/getting-started/recompiling-your-project/the-main-document
- https://docs.overleaf.com/managing-projects-and-files/downloading-a-project

## Compilación local opcional

Requiere una distribución LaTeX instalada en Windows; no se ha comprobado que exista en el computador del estudiante. Python y Jupyter no instalan pdfLaTeX. Si se elige esta opción, primero verificar su disponibilidad con acompañamiento, antes de recomendar instalación o ejecución.

El directorio de compilación es `reports/01_formativa1/`. El comando de referencia es `pdflatex -interaction=nonstopmode -halt-on-error informe_formativa1_grupo7.tex`; se ejecuta dos veces cuando el índice o las referencias requieren actualización. El PDF queda junto a la fuente. El usuario ejecuta todos los comandos en Git Bash y comparte la salida para acreditar la compilación. Los auxiliares `.aux`, `.log` y `.toc` quedan fuera de Git por `.gitignore`.

La fuente busca imágenes primero en `figures/` (copia autónoma) y después en las rutas relativas del proyecto. En el repositorio no se crea una segunda copia de los gráficos. El español se activa con Babel si está instalado; una distribución mínima conserva las etiquetas españolas mediante la alternativa incluida en el preámbulo.

## Coherencia antes de versionar o entregar

Conservar la fuente `.tex`, su logo y los gráficos referenciados junto con el PDF correspondiente. No reemplazar el notebook Windows ejecutado por una copia de referencia. El Word anterior puede conservarse como antecedente; para nuevas modificaciones del informe se utiliza LaTeX. Verificar las instrucciones vigentes de Canvas, el informe con el equipo y las actividades reales de foro. La conversión de formato no cambia los supuestos inferenciales ni acredita una entrega.
