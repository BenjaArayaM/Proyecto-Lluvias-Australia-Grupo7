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

# Auditoría de cumplimiento — Sumativa 3 — Grupo 7

Preparación: 24 de octubre de 2026. Alcance de esta revisión: artefactos generados y ejecutados en Work. **No acredita todavía reproducción Windows, grabación grupal, push ni entrega en Canvas.**

## Fuentes vigentes y diferencias documentales

1. Rúbrica «Sumativa 3 fase 4» transcrita por el estudiante: seis criterios, **108 puntos**.
2. `INSTRUCCIONES SUMATIVA 3.docx`: cinco partes, PDF máximo diez páginas, notebook maestro, presentación de diez minutos y repositorio con las tres sumativas; un intento en Canvas. Se revisó el contenido completo del archivo.
3. Retroalimentaciones de S2 y F2 aportadas por el estudiante y revisadas: fortalecer la decisión Monte Carlo; conservar 70/30 estratificado dentro del alcance del curso; comparar imputaciones, incluir pesos de clase y evaluar estabilidad del modelo.
4. Repositorio docente y plantilla S3: referencias didácticas, subordinadas a rúbrica/enunciado vigentes. La plantilla antigua atribuye seis puntos a presentación; se aplica el máximo vigente de nueve.
5. Resultados previos del grupo consultados contra el commit `28e3a8a0805e11fd1b93beb273db7ca4060aa557`, mediante API de lectura. Sus archivos y huellas se identifican en `fuentes_base.json`.

La sección específica pide video; la ficha general menciona video o en vivo. Se prepara para video según el requisito específico. No se inventa una fecha de entrega. El máximo de diez páginas se aplica conservadoramente a portada y referencias incluidas.

**Adjunto con nombre discordante:** `Objetivo de la actividad SUMATIVA 3.docx` contiene Fase 3, validación de S1, 20 %, PDF de siete páginas y la rúbrica «Sumativa 2 fase 3» de 87 puntos. Se revisó íntegramente y se identifica como material de S2 por su contenido; no se importa a S3 su mínimo de 10.000 remuestras ni su límite de siete páginas. `INSTRUCCIONES SUMATIVA 3.docx` y la rúbrica vigente aportada por el estudiante coinciden en el alcance de cierre/modelamiento. Conviene confirmar el rótulo de aquel adjunto al consultar Canvas; no se interpreta su nombre como una modificación oficial de S3.

## Matriz de seis criterios

| Criterio | Puntaje máximo | Requisito para Excelente | Evidencia requerida y disponible | Estado | Fuente |
|---|---:|---|---|---|---|
| Imputación y manejo de datos faltantes, parte 1 | 21 | Usar explícitamente faltantes de S1; regresión correcta; comparación sistemática de las tres estrategias; justificación sólida. | Notebook, celdas de código 1 y 3; 16 OLS con tres predictores; donantes completos de train, evaluación retenida y diagnósticos; conteos/recortes/medianas auxiliares; distribuciones y correlaciones; comparación final de tres estrategias. Informe pp. 3 y 8. | **Cumplido y verificado en Work**, con límites MAR/MNAR y transporte de estaciones declarados. Windows pendiente. | Rúbrica criterio 1; instructivo P10–P12. |
| Clasificación mediante regresión logística, parte 2 | 30 | Tres modelos solicitados; selección informada por S1/S2; interpretación rigurosa de coeficientes/OR; decisión final fundamentada. | Celdas 2, 4, 5 y 8; resúmenes GLM y CSV de coeficientes/IC de los tres modelos; dominio, stepwise AIC y BIC reducido; 70/30; cinco pliegues con ajustes internos; pesos balanceados; umbrales OOF; matrices train/test, métricas y ROC; VIF, linealidad, residuos e influencia. Informe pp. 4–5 y 7. | **Cumplido y verificado en Work**. BIC restringido y prueba previamente utilizada se explican. Windows pendiente. | Rúbrica criterio 2; instructivo P14–P23; retroalimentación F2. |
| Estabilidad y bootstrap del modelo | 30 | Bootstrap del modelo seleccionado; IC para beta y OR; parámetros inestables; comparación con intervalos tradicionales. | Celda 7 y visualización 13; 2.000 réplicas válidas por localidad, 0 fallos; reajuste de imputación/escala/pesos/logit, equivalencia numérica con duplicación; IC percentil y BCa, Wald, distribuciones, convergencia y 49 jackknife. MaxTemp inestable frente a Wald. Informe p. 6. | **Cumplido y verificado en Work**, condicional a listas de predictores; independencia espacial no demostrada. Windows pendiente. | Rúbrica criterio 3; instructivo P21. |
| Impacto comparativo de imputación, parte 3 | 9 | Tres datasets; impacto en coeficientes, IC y desempeño; recomendaciones fundamentadas. | Celda 6 y visualización 14; tamaño, cobertura/localidades, distribuciones, correlaciones; mismo modelo/umbral; coeficientes/IC con misma DE; AUC/accuracy y otras métricas en población propia y casos comunes. Informe p. 8. | **Cumplido y verificado en Work**. La cobertura explica por qué AUC en muestras distintas no basta para elegir. Windows pendiente. | Rúbrica criterio 4; instructivo P25. |
| Informe final integrado, parte 4 | 9 | Narrativa S1→S2→S3 cohesiva; metodología integrada; comunicación clara; conclusiones accionables. | PDF de diez páginas incluidas portada y referencias; fuente LaTeX editable con cifras desde resultados; tabla inicial de decisiones; discusión, recomendaciones y límites; extensión de decisión Monte Carlo responde al feedback de S2. | **Cumplido y verificado en Work** en contenido, compilación y diagramación. Revisión grupal y comprobación de la versión a entregar pendientes. | Rúbrica criterio 5; instructivo P27. |
| Presentación del proyecto, parte 5 | 9 | Exposición sintética y precisa del problema/métodos/resultados/conclusiones; progresión S1/S2/S3; cuatro integrantes con participación equitativa y dominio; diez minutos. | PPTX de 12 diapositivas, gráficos/tablas nativos editables, notas y guion de diez minutos repartidos 2:30 por persona. Faltan video/ensayo real y evidencia de apertura local. | **Cumplido parcialmente**: material preparado y revisado en Work; participación, dominio, coordinación y tiempo reales **no verificables** hasta grabar. | Rúbrica criterio 6; instructivo P29, P49–P50. |

La suma de máximos es 21 + 30 + 30 + 9 + 9 + 9 = **108**. No se asigna una calificación estimada a estos artefactos mientras falten evidencias humanas y revisión final de la versión a entregar.

## Escalas de desempeño completas

| Criterio | Excelente | Bueno | Deficiente | No cumple |
|---|---|---|---|---|
| Imputación | 21: uso explícito S1, regresión y comparación sólida de tres estrategias. | 14: implementación y comparación con justificación parcial o incompleta. | 7: imputación incompleta, comparación superficial o conexión débil con S1. | 0: sin análisis S1 o sin imputación adecuada. |
| Clasificación | 30: tres modelos, S1/S2 efectivos, coeficientes/OR y decisión rigurosos. | 20: modelos con interpretación general o selección parcialmente justificada. | 10: modelos incompletos, errores o interpretación débil. | 0: sin modelos solicitados o sin resultados S1/S2. |
| Bootstrap | 30: IC beta/OR, inestabilidad y contraste con IC tradicional. | 20: estabilidad parcial o comparación limitada. | 10: implementación incompleta o superficial. | 0: no aplica bootstrap al modelo final. |
| Impacto imputación | 9: comparación sistemática de tres datasets, coeficientes/IC/desempeño y recomendaciones. | 6: comparación adecuada pero general o incompleta. | 3: comparación limitada o conclusiones poco claras. | 0: no compara. |
| Informe | 9: cohesión e integración explícita S1/S2/S3, comunicación y acciones. | 6: buena estructura con integración parcial. | 3: escasa cohesión o articulación. | 0: incompleto, desarticulado o no entregado. |
| Presentación | 9: exposición precisa, sintética e integrada, participación equitativa, dominio/coord. y diez minutos. | 6: exposición adecuada con menor articulación, participación desigual leve o imprecisiones/tiempo. | 3: fragmentada, progresión superficial, concentración de intervenciones o debilidades técnicas. | 0: sin video pertinente ni participación grupal efectiva. |

## Verificación computacional y entregables

- **Generado:** módulo estadístico, notebook, tablas/figuras/JSON, PDF/LaTeX, PPTX/guion y documentación.
- **Ejecutado:** notebook completo dos veces, 16 celdas en orden, sin errores; 2.000 remuestras y cinco pliegues en cada ejecución. No se usan pilotos como si fueran ejecución final.
- **Validado en Work:** 22 controles, identidad del CSV, fuentes analíticas anteriores intactas, reproducción F2, conciliación de métricas desde predicciones, intervalos/OR, reajustes bootstrap y concordancia exacta de los 32 archivos numéricos cotejados entre ejecuciones.
- **Pendiente Windows:** kernel/rutas/dependencias reales del estudiante, ejecución S3 desde cero y conciliación de cifras. La evidencia de Windows S2 no se reutiliza como S3.
- **Pendiente grupal/Canvas:** revisión conceptual de los cuatro integrantes, ensayo, video con participación y diez minutos, comprobación de formato/plazo vigente y entrega por el estudiante.

## Riesgos que podrían reducir la evaluación y correcciones previstas

1. **Video ausente:** grabar a los cuatro integrantes y comprobar reparto y duración. El PPTX no demuestra participación.
2. **Cambios locales sin conciliación:** ejecutar S3 en Windows antes del commit y cotejar indicadores/IC con PDF y diapositivas; regenerar cifras si cambian.
3. **Defensa débil de supuestos:** estudiar `docs/decisiones_sumativa3.md`. Poder explicar por qué remuestrear localidades conserva registros pero no demuestra independencia espacial, y por qué validar donantes no demuestra MAR.
4. **Comparación incorrecta de imputadores:** mantener la tabla de casos comunes y la cobertura. No concluir superioridad por AUC de eliminación sobre otra población.
5. **Interpretación de OR/score:** explicar DE y transformación de Rainfall; no confundir odds, probabilidad y causalidad. Conservar la advertencia de calibración.
6. **Entrega/formato:** usar el PDF actual de diez páginas, notebook completo, presentación/video y enlace de la rama publicada por el estudiante. Verificar Canvas antes del único intento.

La revisión estadística reconoce desviaciones de supuestos y límites de generalización; no los convierte en comprobaciones aprobadas por el mero hecho de ejecutar código.
