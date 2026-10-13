# Validación del informe LaTeX — Formativa 1

Fecha UTC: 2026-10-10T19:13:41.645528+00:00. Formato F1-1.2; análisis F1-1.0 sin cambios.

## Comprobaciones realizadas

- El informe validado se transcribió a una fuente `.tex` con texto, nueve tablas y tres ecuaciones editables. Las cinco figuras utilizadas se referencian mediante rutas relativas.
- Los 75 párrafos de contenido se localizaron en el PDF compilado, normalizando espacios y composición tipográfica. Las 275 celdas de las nueve tablas conservan sus textos y números; el valor p se presenta en notación científica LaTeX equivalente.
- Se comprobó por SHA-256 que el notebook de referencia, módulo, 19 CSV, ocho PNG, resumen JSON y Word anterior no cambiaron. No se ejecutó un nuevo análisis ni se modificó el dataset.
- Se compiló con pdfLaTeX en Work y se actualizaron índice y enlaces. PDF: 13 páginas A4, incluida portada con los cuatro integrantes e índice. No hay errores, desbordamientos ni referencias pendientes.
- Se renderizaron e inspeccionaron las 13 páginas. Se corrigió la distribución tipográfica de la huella del CSV. La única advertencia no crítica es una caja poco llena en la tabla descriptiva, que conserva alineación y legibilidad.
- Se extrajo el ZIP autónomo en otra carpeta y se compiló por separado. Sus siete archivos fuente y recursos están completos. El PDF obtenido conserva exactamente el mismo texto y paginación en Work.
- Las figuras del ZIP autónomo corresponden a la referencia Work ya validada. El `.tex` del proyecto lee las imágenes presentes en `results/01_formativa1/figures/`. La equivalencia numérica Windows está documentada; no se afirma igualdad visual píxel a píxel de sus PNG.

Los hashes y el detalle de las comprobaciones se conservan en `validacion_latex.json`. `manifiesto_latex.json` identifica los archivos de la actualización F1-1.2. El manifiesto anterior pertenece al paquete base F1-1.1 y se conserva como registro histórico.

## Alcance y pendientes

La compilación fue realizada en Work; no se ha ejecutado en el computador del estudiante ni en su cuenta de Overleaf. La incorporación local se verificará con su evidencia. La reproducción estadística Windows permanece acreditada por los registros previos y no requiere repetirse por esta conversión.

Una instalación con otros paquetes o separación silábica puede distribuir líneas de forma diferente: revisar el PDF después de recompilar y actualizar las referencias a páginas si cambian. La independencia espacial, el alcance inferencial condicional, las instrucciones vigentes de Canvas, la entrega y la participación real en el foro conservan su estado anterior. La conversión de formato no los resuelve.
