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

> Estado actualizado al 24 de octubre de 2026: F1, S1, S2 y F2 entregadas y retroalimentadas, según lo informado por el estudiante y los materiales aportados. S3 desarrollada y validada en Work; Windows, revisión grupal, video y entrega pendientes. Las fichas siguientes se conservan como registro histórico; fichas vigentes: `continuidad_sumativa2.md` y `continuidad_sumativa3.md`.

# Fichas de continuidad — MCDI501 — Grupo 7

Actualización: 10 de octubre de 2026. Las cifras corresponden al CSV y a la ejecución Work documentada, conciliada con la reproducción Windows aportada por el estudiante. Los registros de ambos entornos se conservan. La evidencia de Canvas sigue pendiente.

## 01_formativa1 — Formativa 1 — Informe 1

**Estado:** trabajo técnico ejecutado en Work y reproducido en Windows con resultados conciliados. La evaluación no está cerrada: faltan revisión de Canvas, entrega y participación real. La nómina de cuatro integrantes está confirmada.

### Identidad y resultados principales

- CSV: 145.460 × 23, 14.094.055 bytes, 49 localidades; fechas 2007-11-01 a 2017-06-25.
- SHA-256: `573fd715cd69fcacc4df32024d823b450ae3edaae7e8ff2eeb623adbed424014`.
- Objetivo conocido: 142.193 registros; No=110.316 (77,58 %) y Yes=31.877 (22,42 %). Faltantes: 3.267 (2,25 % del total).
- Casos completos de las 23 variables: 56.420 (38,79 %); no se usan para una eliminación global.
- Faltantes estructurados: Sunshine 48,01 %, ausente en todas las filas de 19 localidades; evaporación 43,17 %.
- Duplicados exactos y localidad/fecha: cero. Los chequeos físicos implementados no encontraron valores incompatibles; no equivalen a una certificación de todos los mecanismos de medición.
- RainToday concuerda con Rainfall > 1 mm en 142.199 pares observados. RainTomorrow concuerda con esa regla del día siguiente en 142.017 pares consecutivos. No se reconstruyen etiquetas.
- Cloud9am=9: dos registros; Cloud3pm=9: uno. Conservados; codificación histórica pendiente.
- Mediana de autocorrelación lag 1 de Humidity3pm por localidad: 0,5023, calculada solo con fechas exactamente consecutivas.

### Variables y relaciones seleccionadas para exploración

Humidity3pm, Rainfall, Sunshine, Pressure3pm, MaxTemp y MinTemp se estudian por pertinencia meteorológica. RainToday, Location y Date aportan persistencia, heterogeneidad y cobertura. Esta lista **no es una selección de predictores finales**.

| Relación descriptiva con RainTomorrow (Yes=1) | Spearman | n pares |
|---|---:|---:|
| Humidity3pm | 0,4312 | 138.583 |
| Rainfall | 0,3318 | 140.787 |
| Sunshine | −0,4385 | 74.377 |
| Pressure3pm | −0,2154 | 128.212 |
| MaxTemp | −0,1588 | 141.871 |

Estos coeficientes son asociaciones agrupadas con exclusión por pares. Sus denominadores y composiciones difieren. No sustentan causalidad ni una comparación definitiva de utilidad predictiva.

### Parámetros que deben conservarse

**Estimando de F1:** promedio con igual peso de las 49 medias históricas observadas por localidad. No sustituirlo por la media de todas las filas sin cambiar explícitamente la pregunta. Los IC t son individuales y condicionales a un modelo de localidades comparables aproximadamente independientes.

| Variable | n registros válidos | L | Media con igual peso por localidad | IC 95 % | Media de todas las filas |
|---|---:|---:|---:|---|---:|
| Humidity3pm (%) | 140,953 | 49 | 51.24669260 | 48.02474745 a 54.46863776 | 51.53911588 |
| MaxTemp (°C) | 144,199 | 49 | 23.38834489 | 22.22329867 a 24.55339110 | 23.22134828 |
| MinTemp (°C) | 143,975 | 49 | 12.25871081 | 11.12390115 a 13.39352046 | 12.19403438 |

### Prueba y magnitud del efecto

Para cada localidad, D = media de Humidity3pm en Yes − media en No. Prueba bilateral de una muestra sobre D: H0 μD=0, H1 μD≠0, α=0,05. Se usan 138.583 registros completos en humedad y objetivo; se excluyen 6.877 solo de esta comparación.

- L=49; gl=48; diferencia media=20.0769013620 puntos porcentuales.
- IC 95 %: 18.4715891616 a 21.6822135624 puntos porcentuales.
- t=25.1460841663; p=2.747107556483e-29.
- Las 49 diferencias son positivas. Mínima: Albany (6,57); máxima: AliceSprings (33,34).
- Menor n dentro de una localidad/clase: No=618; Yes=115.
- Shapiro de las diferencias: W≈0,9884 y p≈0,9059. No prueba normalidad ni independencia. No hay diferencias fuera de las cercas de Tukey.
- d_z≈3,5923 usa variabilidad entre diferencias locales; no interpretarlo como efecto estandarizado de días individuales.

El rechazo de H0 se expresa **bajo los supuestos del modelo**. La diferencia de humedad no es un aumento de 20,08 puntos en probabilidad de lluvia. Independencia espacial, representatividad nacional y ajuste por mezcla estacional no están comprobados.

### Gráficos y archivos conservados

| Archivo o conjunto | Evidencia que conserva |
|---|---|
| notebooks/01_formativa1_eda_inferencia.ipynb | 41 celdas con métodos, 19 celdas de código ejecutadas y salidas. |
| src/formativa1.py | Funciones y verificaciones. |
| results/01_formativa1/resultados.json | Identidad, parámetros completos, prueba y rutas de exportación. |
| results/01_formativa1/tables/medias_localidad.csv | Tres variables con conteos y medias de las 49 localidades. |
| results/01_formativa1/tables/diferencias_localidad.csv | Dos medias y conteos por clase/localidad; diferencias usadas en la prueba. |
| results/01_formativa1/tables/intervalos_localidades.csv | Estimadores, errores estándar, IC y diagnósticos. |
| results/01_formativa1/tables/matriz_correlacion.csv y n_pares_correlacion.csv | Asociaciones y denominadores por par. |
| results/01_formativa1/tables/faltantes_localidad.csv y cobertura_localidad.csv | Ausencias y cobertura geográfica. |
| results/01_formativa1/figures/01_objetivo_faltantes.png | Desbalance y calidad. |
| results/01_formativa1/figures/05_geografia_estacionalidad.png | Heterogeneidad y estacionalidad descriptiva. |
| results/01_formativa1/figures/06_diagnostico_normalidad.png | Q-Q de las unidades inferenciales. |
| results/01_formativa1/figures/07_diferencias_localidades.png | Magnitud de la diferencia en cada localidad. |
| results/01_formativa1/figures/08_faltantes_localidades.png | Patrón espacial de datos ausentes. |
| reports/01_formativa1/ | Informe LaTeX/PDF vigente, Word anterior como referencia y borradores de comunicación. |
| evidence/01_formativa1/ | Registros Work, preparación y ejecución Windows, comparación de resultados, validación LaTeX y auditoría final. |

Los 19 CSV y ocho gráficos se identifican en resultados.json. Consultar `docs/decisiones_metodologicas.md` para la justificación de cada elección.

### Hallazgos pendientes de validar y límites conocidos

- Independencia espacial entre localidades; el archivo no incorpora un diseño probabilístico nacional.
- Sensibilidad de medias y contrastes al período, estacionalidad y faltantes; las localidades no tienen cobertura idéntica.
- Significado histórico definitivo de Cloud=9.
- Disponibilidad real de predictores en la hora de emisión de una predicción.
- La reproducción Windows y la equivalencia de las 19 tablas y resultados.json están acreditadas; conservar el notebook local guardado y el registro de ejecución. Los nombres en sus celdas Markdown se revisan por separado.
- Entrega y foro en Canvas. La identidad de los cuatro integrantes fue confirmada.

### Recomendaciones para fases posteriores, cuando se autoricen

En Sumativa 1, revisar el alcance de sus parámetros y sus pruebas según su propia rúbrica antes de reutilizar resultados. Si se conserva un estimando, citar la versión de F1 y sus n; si se cambia, justificar y guardar ambas versiones. En las fases de remuestreo y simulación, estudiar estabilidad usando unidades y bloques compatibles con la dependencia, conservando el parámetro definido. En modelamiento, resolver horizonte, partición, faltantes y métricas dentro del entrenamiento y declarar que todo el archivo fue explorado en F1.

No se inicia ninguna de esas fases en este paquete.

## 02_sumativa1 — Sumativa 1 — Informe técnico de avance

**Actualización del 18 de octubre de 2026:** trabajo de Jorge entregado y retroalimentado por el profesor, integrado en main. S2 concilia sus tres medias e IC con `results/02_sumativa1/tables/intervalos_medias_localidades.csv`, sus correlaciones con `matriz_correlaciones_spearman.csv` y recalcula la diferencia de humedad con la misma definición. Consultar la ficha de continuidad S2 para resultados validados y limitaciones actuales.

## 03_sumativa2 — Sumativa 2 — Informe 3

**Actualización del 18 de octubre de 2026:** desarrollo autorizado y cierre preparado sobre el código de Patricio. La ficha vigente y completa está en [continuidad_sumativa2.md](continuidad_sumativa2.md). Incluye tres parámetros con IC clásicos, percentil y BCa; contraste mediante cambios de signo; tres correlaciones con IC; Monte Carlo; jackknife; sensibilidad al rango de lluvia y decisiones para S3. La reproducción Windows fue verificada el 18 de octubre de 2026: 13 celdas sin errores, diez controles correctos y cifras principales coincidentes con Work. Consultar `evidence/03_sumativa2/validacion_windows.md`. La entrega en Canvas sigue pendiente de evidencia.

## 04_formativa2 — Formativa 2 — Informe 4

**Estado:** pendiente de autorización, auditoría específica y desarrollo. Sin resultados generados. Al iniciar, revisar la ficha de F1, los vacíos pendientes y la rúbrica correspondiente. Rutas reservadas: `results/04_formativa2/`, `reports/04_formativa2/` y `evidence/04_formativa2/`.

## 05_sumativa3 — Sumativa 3 — Cierre y comunicación

**Estado:** pendiente de autorización, auditoría específica y desarrollo. Sin resultados generados. Al iniciar, revisar la ficha de F1, los vacíos pendientes y la rúbrica correspondiente. Rutas reservadas: `results/05_sumativa3/`, `reports/05_sumativa3/` y `evidence/05_sumativa3/`.


## 04_formativa2 — Referencia para el cierre

F2 fue entregada y retroalimentada por el profesor. S3 reproduce su partición 70/30 estratificada (99.535 / 42.658), métricas y matriz antes de modificar procedimientos. Referencia: recall 39,82 %, AUC 0,8164 y 5.755 falsos negativos. La prueba ya utilizada se declara en toda interpretación de S3. Los archivos originales se conservan.

## 05_sumativa3 — Cierre integrado

La ficha vigente está en [continuidad_sumativa3.md](continuidad_sumativa3.md). Conserva predictores, coeficientes/OR e intervalos, influencia por localidad, métricas, imputación, simulación, decisiones y rutas de evidencia. Notebook completo verificado en Work con 16 celdas, 22 controles y 2.000 remuestras; Windows, revisión grupal, video y entrega no se infieren de esa ejecución. Ver [reproduccion_sumativa3.md](reproduccion_sumativa3.md) antes de incorporar la actualización a una nueva rama creada por el estudiante.
