# Auditoría de cumplimiento - Sumativa 2, Grupo 7

## Fuentes y alcance

- `RUBRICAS(2).xlsx`, hoja **Sumativa 2**, B38-B66; máximo **87 puntos**.
- Enunciado de Fase 3 proporcionado por el estudiante: PDF máximo **7 páginas**, notebook
  ejecutable documentado, repositorio con S1/S2 y archivo de resultados validados.
- Plantilla docente `04-plantillas/latex/sumativa-2-validacion-simulacion-remuestreo/plantilla.tex`.
- Resultados propios de S1, commit `134859256a519e0ffde2827319d73a603598e0ea`.
- Código de Patricio, commit `1484dd055fb99779932b85f0e87ac541400b893f`.

El Word adjunto se titula "Objetivo de la actividad SUMATIVA 3", pero su cuerpo,
ponderación (20 %), RA2 y tabla indican **Sumativa 2, Fase 3**. Se aplica el contenido
específico de S2 y su rúbrica; no se importan requisitos de la evaluación final.
La hoja Excel contiene "sin info" en B3: los detalles de entrega se toman del enunciado.
No se ha confirmado aquí una fecha límite vigente de Canvas.

## Matriz completa de los seis criterios

| Criterio | Puntaje máximo | Requisito del nivel más alto | Evidencia preparada | Estado y límite | Fuente |
|---|---:|---|---|---|---|
| Validación bootstrap de IC | 18 | >=10.000 remuestras; percentil y BCa para >=3 parámetros de S1; comparación sistemática con clásicos; distribuciones; análisis de discrepancias y supuestos. | Notebook sección 2; informe sección 1, tabla 1 y figura 1; `bootstrap_ic_s2_resumen.csv`; tres grupos de 10.000 medias. | Cumplido y verificado en Work según registros de ejecución. Se explican independencia aproximada, cobertura y variación de remuestreo; no se acredita cobertura real del IC. | Excel C42-C45; enunciado punto 1. |
| Pruebas por permutación | 15 | >=10.000 permutaciones de al menos una prueba propia de S1; valor observado y p; comparación con p original; distribución e interpretación crítica. | Notebook sección 3; informe sección 2, tabla 2 y figura 2; `prueba_permutacion_humedad.csv`; `distribucion_permutacion.csv`. | Cumplido y verificado en Work, con validez inferencial explícitamente condicional. Se distingue media nula de invariancia ante cambios de signo; no se afirma aleatorización del estudio. | Excel C46-C49; enunciado punto 2. |
| Estabilidad de correlaciones | 6 | Entre 3 y 5 correlaciones de S1; IC bootstrap 95 %; distribuciones claras; clasificación fundamentada de estabilidad, cero y variabilidad. | Notebook sección 4; informe sección 3, tabla 3 y figura 3; `estabilidad_correlaciones_bootstrap.csv`; 30.000 coeficientes exportados. | Cumplido y verificado en Work. Escalas ajustadas a cada histograma; se distingue estabilidad de signo de sensibilidad. Sunshine usa 30 localidades, no 49. | Excel C50-C53; enunciado punto 3. |
| Simulación Monte Carlo | 24 | Escenario relevante con parámetros propios de S1; >=10.000 iteraciones; convergencia; estadísticas, figuras e interpretación contextual. | Notebook sección 5; informe sección 4, tabla 4 y figura 4; `monte_carlo_resumen.csv`, `monte_carlo_convergencia.csv`, `diagnostico_convergencia_mc.csv`. | Cumplido y verificado en Work. MCSE y referencia analítica cuantificados; rango central del escenario separado del IC del parámetro. Normalidad, independencia y parámetros fijos declarados. | Excel C54-C57; enunciado punto 4. |
| Robustez | 15 | Sensibilidad a outliers y supuestos; identificación de resultados robustos/sensibles; recomendaciones para S3. | Notebook sección 6; informe sección 5, tabla 5 y figura 5; jackknife de 49 localidades; comparación Spearman/Kendall; cercas de Tukey; diagnósticos de forma. | Cumplido y verificado en Work dentro del alcance declarado. Identifica Albany, AliceSprings y Cobar. Humedad/lluvia: signo estable y magnitud sensible al rango; no elimina lluvia plausible ni certifica errores. | Excel C58-C61; enunciado punto 5. |
| Documentación | 9 | Parámetros validados, correlaciones estables, observaciones/unidades influyentes y recomendaciones metodológicas concretas para S3. | Informe sección 6; `resultados_validados_s2.json`; síntesis de diez entradas; `docs/continuidad_sumativa2.md`; índices `S1/` y `S2/`. | Cumplido y verificado en Work. Se separan cálculos, supuestos no demostrados, reproducción Windows y entrega. No se inicia S3. | Excel C62-C65; enunciado punto 6. |

La clasificación se refiere a la evidencia técnica comprobada en Work. No promete el
nivel de desempeño que asignará el profesor. No se convierte automáticamente en 87/87
ni se estima nota: la revisión académica, el entorno local y la entrega son evidencias distintas.

## Entregables y comprobaciones

| Producto o control | Evidencia | Alcance |
|---|---|---|
| Informe de máximo siete páginas totales | `reports/03_sumativa2/informe_sumativa2_grupo7.pdf`; `validacion_informe_work.json`. | Compilación y revisión visual en Work, incluyendo identificación y referencias dentro del límite. |
| Fuente editable | `.tex` principal y `datos_sumativa2.tex`. | Texto editable; cifras generadas desde resultados actuales. ZIP autónomo disponible para edición externa. |
| Notebook completo | `notebooks/03_sumativa2_validacion_remuestreo.ipynb`; `validacion_notebook_work.json`. | Celdas ejecutadas desde un kernel limpio en Work; no se usa caché de resultados para sustituir el análisis. |
| Trazabilidad de datos y resultados | `ejecucion_sumativa2_work.json`. | Identidad del CSV, conciliación S1, réplicas, intervalos, valor p, jackknife y hashes. |
| Organización de fases | `S1/README.md`, `S2/README.md`. | Índices con enlaces a la estructura aprobada; no duplican datos ni notebooks. |
| Reproducción Windows de S2 | `ejecucion_sumativa2_windows.json` y `validacion_windows.md`. | **Cumplido y verificado:** ejecución local de S2 con 13 celdas sin errores, diez controles correctos y cifras principales coincidentes con Work. |
| Publicación de esta actualización | Evidencia futura de commit y push del estudiante. | **Pendiente:** la asistencia no ejecuta Git ni escribe en GitHub. |
| Entrega Canvas | PDF + notebook + enlace; un intento según enunciado. | **No verificable todavía:** confirmar plazo/instrucciones vigentes, revisión del grupo y entrega real. |

## Límites estadísticos que deben mantenerse visibles

- El estimando de medias da igual peso a cada localidad; las correlaciones agrupadas
  se calculan sobre sus filas disponibles. No son parámetros intercambiables.
- El bootstrap de localidades completas mantiene juntos los registros de cada estación;
  no supone independencia de sus días, pero tampoco genera nuevos futuros ni elimina
  dependencia entre estaciones. Remuestrear medias locales condiciona a sus historias.
- La prueba mediante cambios de signo requiere un modelo nulo invariante ante esos
  cambios; no se justifica solo porque H0 diga media cero. El diagnóstico observado
  no demuestra esa propiedad ni la independencia espacial.
- Los IC de correlaciones excluyen cero bajo ese remuestreo. No prueban robustez ante
  toda transformación, faltante, selección geográfica o periodo futuro.
- La cerca de Rainfall es 2 mm en el par analizado y retira 17,89 % de pares del diagnóstico;
  modifica el rango. Esas observaciones no se declaran erróneas ni se borran del original.
- La simulación normal calibra un escenario con parámetros de S1; su intervalo central
  no es un IC del parámetro desconocido y no constituye predicción meteorológica.
- El archivo completo ya fue explorado. En modelamiento debe documentarse este antecedente,
  proteger la prueba final y ajustar todo preprocesamiento dentro del entrenamiento.

## Requisitos y recomendaciones

Las seis filas de la matriz y los productos de entrega proceden del enunciado/rúbrica.
El MCSE, exportar distribuciones, las huellas de archivos, los índices de navegación
y el ZIP autónomo son apoyos de reproducibilidad; no se les atribuyen puntos adicionales.
PR-AUC se recomienda como complemento futuro, sin sustituir métricas exigidas en S3.

La evaluación cuenta con ejecución comprobada en Work y Windows y cifras principales
conciliadas. Antes de recomendar la entrega se deben revisar integrantes/formato/plazo
vigentes, comprobar el contenido a versionar y acreditar la revisión grupal,
la publicación y la entrega por el estudiante.
