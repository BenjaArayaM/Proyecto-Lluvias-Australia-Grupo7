# Auditoría final de la Formativa 1

Fecha: 10 de octubre de 2026. **Trabajo técnico ejecutado en Work y reproducido en Windows con resultados conciliados; evaluación aún no cerrada.** Esta auditoría no certifica entregas en Canvas ni operaciones remotas de GitHub.

| Criterio | Puntaje máximo | Requisito para el nivel excelente | Evidencia requerida y preparada | Estado | Fuente |
|---|---:|---|---|---|---|
| Aplicación de estadística descriptiva (ID1.2) | 15 | Medidas de tendencia central y dispersión completas, correctas y gráficos pertinentes. | Informe LaTeX pp. 5–8; descriptivos de las 16 columnas numéricas, frecuencias, faltantes y gráficos; notebook ejecutado en Work y reproducción Windows acreditada. | Cumplido y verificado | Excel, Formativa 1, filas 42–45 |
| Estimación puntual e intervalos de confianza (ID1.3) | 15 | Métodos correctos e interpretación adecuada de los parámetros poblacionales. | Informe LaTeX pp. 9 y 11; tres estimadores, IC individuales al 95 %, fórmulas, diagnósticos y alcance poblacional explícito; medias_localidad.csv e intervalos_localidades.csv. | Cumplido parcialmente | Excel, Formativa 1, filas 46–49 |
| Aplicación de pruebas de hipótesis (ID1.4) | 15 | Una prueba básica pertinente para el tipo de variable, con significancia declarada e interpretación coherente. | Informe LaTeX pp. 10–11; H0/H1, t sobre 49 diferencias locales, α=0,05, IC, efecto y valor p; diferencias_localidad.csv. | Cumplido parcialmente | Excel, Formativa 1, filas 50–53 |
| Documentación de procedimientos y resultados | 15 | Procedimientos claros, ordenados, completos y trazables. | Informe LaTeX p. 12; notebook, módulo, 19 tablas, ocho gráficos, resultados.json y evidencias de Work y Windows. Registro local y equivalencia numérica revisados. | Cumplido y verificado | Excel, Formativa 1, filas 54–57 |
| Interpretación preliminar de resultados | 15 | Interpretaciones claras, coherentes y vinculadas con decisiones bajo incertidumbre. | Informe LaTeX pp. 7–12 y explicaciones del notebook: humedad, disponibilidad, desbalance, heterogeneidad y límites de decisiones. | Cumplido y verificado | Excel, Formativa 1, filas 58–61 |
| Presentación formal del informe técnico | 15 | Informe estructurado, redacción formal, lenguaje estadístico adecuado y formato solicitado. | Fuente LaTeX editable y PDF compilado de 13 páginas, con portada e índice; ficha descriptiva, tipos de todas las variables, metodología, resultados, limitaciones y referencias. Nómina de cuatro integrantes confirmada; resta revisar las instrucciones vigentes de Canvas. | Cumplido parcialmente | Excel, Formativa 1, filas 62–65 y B3 |
| Participación en foro: publicación y retroalimentación a pares | 9 | Publicación oportuna y al menos dos comentarios fundamentados, pertinentes, respetuosos y que promuevan diálogo. | Borrador publicacion_foro.md y guia_comentarios_foro.md. La evidencia debe ser de publicaciones reales en Canvas, con fecha y contenido. | No verificable por falta de evidencia | Excel, Formativa 1, filas 66–69 y B3 |

## Comprobaciones efectivamente realizadas

- Identidad del CSV: 145.460 × 23, 14.094.055 bytes y SHA-256 esperado.
- Las 19 celdas de código se ejecutaron en orden en un kernel real ipykernel en memoria, sin errores.
- Integridad del dataframe original y del CSV después del análisis.
- Conciliación de clases, faltantes y conteos; exclusiones por cálculo con denominadores registrados.
- Medias por filas conciliadas con medias locales ponderadas por sus conteos.
- Fórmulas de errores estándar, intervalos t y prueba conciliadas con las funciones de SciPy.
- Diagnósticos Q-Q y Shapiro de las 49 unidades inferenciales; valores extremos señalados y conservados.
- Tablas y gráficos revisados; coeficientes y denominadores consistentes con el informe.
- Informe convertido a fuente LaTeX editable; compilación con pdfLaTeX, índice actualizado y 13 páginas inspeccionadas visualmente. El ZIP autónomo se compiló por separado y produjo el mismo texto y paginación en Work.
- Reproducción Windows acreditada por el registro y los archivos aportados; 19 tablas y resumen JSON conciliados con Work. La mayor diferencia absoluta observada es aproximadamente 1,01e-14.
- Archivo original no redistribuido y evidencias del computador del estudiante preservadas.

Las inferencias no validan independencia espacial ni un muestreo probabilístico nacional. El código y los valores están comprobados; la generalización depende del modelo declarado. El análisis de todo el archivo es exploratorio y queda registrado para evitar atribuir independencia a una evaluación predictiva futura.

## Pendientes antes de recomendar la entrega

1. Conservar el notebook guardado con sus salidas Windows y `ejecucion_windows.json`. La ejecución completa y la equivalencia de resultados fueron acreditadas; actualizar únicamente sus textos de identificación si aún muestran una nómina pendiente.
2. Revisar los cuatro nombres confirmados en el informe actualizado antes de entregar: Benjamín Araya, Alan Cañete, Patricio Cortez y Jorge Guaico.
3. Consultar Canvas para fecha, sección de entrega, foro y cualquier instrucción posterior. Si aparece un límite o formato diferente, ajustar antes de enviar.
4. Revisar y publicar el producto; comentar al menos dos trabajos reales de otros grupos y guardar evidencia de fecha y contenido. Los borradores no acreditan participación.
5. Revisar personalmente el informe y comprender el estimando por localidad y las limitaciones de la inferencia. Si el profesor exige otro alcance poblacional, reformular el análisis antes de la entrega.
6. Una vez verificados los archivos locales, revisar con el estudiante el estado de Git y la lista exacta que integrará su commit.

## Aspectos con mayor riesgo de descuento

- Omitir el foro o producir comentarios genéricos que no analicen el trabajo de los compañeros.
- Entregar sin todos los integrantes o fuera de la fecha de Canvas.
- Interpretar el IC como rango de días o el valor p como probabilidad de H0.
- Presentar la diferencia de humedad como cambio en probabilidad de lluvia o como efecto causal.
- Tratar 145.460 registros diarios como observaciones independientes o generalizar los intervalos a Australia sin justificar el muestreo.
- Entregar una versión distinta del notebook validado o desactualizar el informe después de cambiar resultados.

No se calcula puntaje: el máximo de la rúbrica es 99 y varios criterios necesitan evidencia adicional. La valoración conservadora figura en la matriz.
