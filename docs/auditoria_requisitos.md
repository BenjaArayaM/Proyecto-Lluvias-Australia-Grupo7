# Auditoría de requisitos — MCDI501 — Grupo 7

Actualización: 10 de octubre de 2026. Evaluación activa: **Formativa 1 — Informe 1**. Las otras evaluaciones no se han desarrollado.

## Fuentes y prioridad

1. Rúbrica oficial y enunciado específico.
2. Canvas y aclaraciones del profesor proporcionadas por el estudiante.
3. Sesiones y documentos didácticos.
4. Plantillas docentes.
5. Ejemplos y README docente.
6. Recomendaciones metodológicas propias, identificadas como tales.

Se inspeccionaron el Excel hoja por hoja en el diagnóstico global y, para esta evaluación, el enunciado B3, todos los niveles de las filas 42–69 y el total B70 de la hoja **Formativa 1**. Se revisaron la primera sesión, la plantilla Word/LaTeX de F1, el informe y notebook de ejemplo y los apuntes de Semana01. Los ejemplos se usaron como referencia; todas nuestras cifras provienen de weatherAUS.csv.

## Requisitos confirmados

- Ponderación: **0 %**. Rúbrica: **99 puntos máximos**, no 100.
- Trabajo grupal: **3 a 4 integrantes**. El Grupo 7 está integrado por **Benjamín Araya, Alan Cañete, Patricio Cortez y Jorge Guaico**. Los cuatro integrantes fueron confirmados por el estudiante el 10 de octubre de 2026.
- Ficha descriptiva: problema, variables, tipos y relaciones preliminares.
- Informe en **PDF**, en la sección Entrega de Canvas.
- Publicación del producto en el foro y comentarios a **por lo menos dos publicaciones de otros grupos**.
- **Un intento** según el enunciado. La fecha exacta se consulta en Canvas; no está confirmada aquí.
- No se identificó un máximo de páginas para F1. El PDF compilado desde LaTeX tiene 13 páginas, con portada e índice. El límite de ocho páginas mencionado para otra evaluación no se traslada a esta.

## Matriz completa

| Criterio | Puntaje máximo | Requisito para el nivel excelente | Evidencia requerida y preparada | Estado | Fuente |
|---|---:|---|---|---|---|
| Aplicación de estadística descriptiva (ID1.2) | 15 | Medidas de tendencia central y dispersión completas, correctas y gráficos pertinentes. | Informe LaTeX pp. 5–8; descriptivos de las 16 columnas numéricas, frecuencias, faltantes y gráficos; notebook ejecutado en Work y reproducción Windows acreditada. | Cumplido y verificado | Excel, Formativa 1, filas 42–45 |
| Estimación puntual e intervalos de confianza (ID1.3) | 15 | Métodos correctos e interpretación adecuada de los parámetros poblacionales. | Informe LaTeX pp. 9 y 11; tres estimadores, IC individuales al 95 %, fórmulas, diagnósticos y alcance poblacional explícito; medias_localidad.csv e intervalos_localidades.csv. | Cumplido parcialmente | Excel, Formativa 1, filas 46–49 |
| Aplicación de pruebas de hipótesis (ID1.4) | 15 | Una prueba básica pertinente para el tipo de variable, con significancia declarada e interpretación coherente. | Informe LaTeX pp. 10–11; H0/H1, t sobre 49 diferencias locales, α=0,05, IC, efecto y valor p; diferencias_localidad.csv. | Cumplido parcialmente | Excel, Formativa 1, filas 50–53 |
| Documentación de procedimientos y resultados | 15 | Procedimientos claros, ordenados, completos y trazables. | Informe LaTeX p. 12; notebook, módulo, 19 tablas, ocho gráficos, resultados.json y evidencias de Work y Windows. Registro local y equivalencia numérica revisados. | Cumplido y verificado | Excel, Formativa 1, filas 54–57 |
| Interpretación preliminar de resultados | 15 | Interpretaciones claras, coherentes y vinculadas con decisiones bajo incertidumbre. | Informe LaTeX pp. 7–12 y explicaciones del notebook: humedad, disponibilidad, desbalance, heterogeneidad y límites de decisiones. | Cumplido y verificado | Excel, Formativa 1, filas 58–61 |
| Presentación formal del informe técnico | 15 | Informe estructurado, redacción formal, lenguaje estadístico adecuado y formato solicitado. | Fuente LaTeX editable y PDF compilado de 13 páginas, con portada e índice; ficha descriptiva, tipos de todas las variables, metodología, resultados, limitaciones y referencias. Nómina de cuatro integrantes confirmada; resta revisar las instrucciones vigentes de Canvas. | Cumplido parcialmente | Excel, Formativa 1, filas 62–65 y B3 |
| Participación en foro: publicación y retroalimentación a pares | 9 | Publicación oportuna y al menos dos comentarios fundamentados, pertinentes, respetuosos y que promuevan diálogo. | Borrador publicacion_foro.md y guia_comentarios_foro.md. La evidencia debe ser de publicaciones reales en Canvas, con fecha y contenido. | No verificable por falta de evidencia | Excel, Formativa 1, filas 66–69 y B3 |

Los seis primeros criterios usan niveles 15/10/5/0; el foro usa 9/6/3/0. Las descripciones de excelencia se sintetizan fielmente arriba. **No se asigna un puntaje estimado ni se promete una calificación**: faltan instrucciones vigentes de Canvas y evidencia de entrega y participación real; la reproducción Windows está acreditada.

Los cálculos de intervalos y prueba están ejecutados y conciliados numéricamente. Su estado conservador es parcial porque la independencia espacial entre localidades no se ha establecido. El informe declara explícitamente el modelo hipotético y el alcance condicional; no transforma esta limitación en una afirmación de representatividad nacional.

## Diferencias documentales y decisiones de alcance

| Fuentes que difieren | Diferencia | Tratamiento |
|---|---|---|
| Enunciado Excel B3 y rúbrica del mismo Excel | El enunciado enfatiza la ficha y la identificación de variables; la rúbrica añade estimación, IC y una prueba. | Se integran ambas exigencias en el mismo producto. Una aclaración oficial posterior deberá registrarse. |
| Enunciado Excel y plantilla Word | Excel: equipos de 3–4 y Fase 1; plantilla: individual o grupal y alude a una fase distinta. | Se prioriza el Excel oficial: Grupo 7, Fase 1. Nómina de cuatro integrantes confirmada por el estudiante. |
| Excel y plantilla | La plantilla no incorpora el criterio de foro. | Se conserva la publicación y las dos intervenciones como obligación de la rúbrica. |

La elección de tres parámetros numéricos, las exportaciones, el notebook y las evidencias son recomendaciones de trazabilidad y continuidad. No se presentan como requisitos adicionales del enunciado de F1. Esta formativa requiere una prueba básica pertinente; no se importan el mínimo de dos pruebas ni otras condiciones de Sumativa 1.

## Documentos fuente

- `RUBRICAS(2).xlsx`, hoja `Formativa 1`, B3, filas 42–70.
- `Sesion01_MCDI501_06102026.pdf`.
- Repositorio docente: https://github.com/jpmaidana/MCDI501-202682
- Plantilla: `04-plantillas/word/plantilla_formativa1_eda_inferencia.docx` y su versión LaTeX.
- Ejemplo: `03-evaluaciones/formativa-1-eda-inferencia/Formativa1_GiveMeSomeCredit.pdf` y notebook asociado.
- Apuntes pertinentes: `01-apuntes/Semana01/` sobre variables, visualización, dispersión, inferencia, IC y prueba t.

## Evaluaciones posteriores

| Identificador | Estado |
|---|---|
| 02_sumativa1 | Auditoría específica y desarrollo pendientes de autorización. |
| 03_sumativa2 | Auditoría específica y desarrollo pendientes de autorización. |
| 04_formativa2 | Auditoría específica y desarrollo pendientes de autorización. |
| 05_sumativa3 | Auditoría específica y desarrollo pendientes de autorización. |

La existencia de sus carpetas no es evidencia de análisis ni de cumplimiento de sus rúbricas.
