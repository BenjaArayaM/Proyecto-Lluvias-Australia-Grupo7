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

# Ficha de continuidad — Sumativa 3

Preparada el 24 de octubre de 2026. Ejecución Work verificada; reproducción Windows, revisión grupal, video y entrega Canvas pendientes de sus propias evidencias.

## Identidad y antecedentes

- Grupo 7: Benjamín Araya, Alan Cañete, Patricio Cortez y Jorge Guaico.
- Base consultada en GitHub: `28e3a8a0805e11fd1b93beb273db7ca4060aa557`.
- CSV: 145.460 × 23, 49 localidades; SHA-256 `573fd715cd69fcacc4df32024d823b450ae3edaae7e8ff2eeb623adbed424014`.
- Respuesta conocida: 142.193; train 99.535, test 42.658; semilla 42 y estratificación conservadas de F2.
- S1 aporta faltantes y matriz parcial; S2 aporta estabilidad, sensibilidad e IC; F2 aporta referencia reproducida. Los archivos anteriores permanecen sin modificación analítica.

## Resultados que deben conservarse

| Resultado | Valor | Archivo |
|---|---|---|
| Referencia F2 reproducida | Recall 39,82 %, AUC 0,8164, FN 5.755 | `tables/reproduccion_referencia_F2.csv` |
| Sunshine: RMSE mediana / regresión | 3,8216 / 2,2257 h; reducción 41,76 % | `tables/imputacion_diagnosticos_regresion.csv` |
| Modelo y umbral | M2 stepwise AIC; 0,6034295983 | `decision_congelada_entrenamiento.json` |
| AUC / PR-AUC prueba | 0,861933 / 0,687208 | `tables/metricas_tres_modelos.csv` |
| Accuracy / precision / recall / F1 | 81,79 % / 57,98 % / 68,26 % / 0,626999 | mismo archivo |
| Matriz prueba M2 | TN 28.363; FP 4.732; FN 3.035; TP 6.528 | mismo archivo |
| Bootstrap | 2.000 válidas, 0 fallos, 49 jackknife | `tables/bootstrap_*`, `tables/jackknife_*` |
| VIF máximo | 3,054 (Sunshine) | `tables/diagnostico_VIF.csv` |
| Eliminación | 18.234 test; 27 localidades; cobertura 42,74 % | `tables/impacto_imputacion_metricas.csv` |
| Monte Carlo: capacidad 95 % | 22 / 7 días de un escenario de 30 | `tables/montecarlo_decision_resumen.csv` |

Todas las rutas de la tabla se refieren a `results/05_sumativa3/`. Las cifras completas están en `resultados_validados_s3.json`. El aumento de recall frente a F2 (+28,44 pp) coexiste con menor accuracy (−1,09 pp) y más falsas alertas; no equivale a mejora universal.

## Predictores e intervalos reutilizables

Predictores M2: Humidity3pm, WindGustSpeed, Pressure3pm, Sunshine, log1p_Rainfall, Cloud3pm, MaxTemp y Humidity9am. Betas y OR corresponden a una DE de referencia del predictor transformado, con pesos de clase.

| Predictor | OR | IC bootstrap percentil 95 % | Frecuencia de signo |
|---|---:|---|---:|
| Humidity3pm | 2,465 | [2,234; 2,787] | 100,0 % |
| WindGustSpeed | 1,596 | [1,491; 1,729] | 100,0 % |
| Pressure3pm | 0,615 | [0,548; 0,679] | 100,0 % |
| Sunshine | 0,620 | [0,577; 0,670] | 100,0 % |
| log1p_Rainfall | 1,294 | [1,214; 1,360] | 100,0 % |
| Cloud3pm | 1,213 | [1,124; 1,297] | 100,0 % |
| MaxTemp | 1,099 | [0,966; 1,237] | 92,6 % |
| Humidity9am | 1,106 | [1,011; 1,213] | 98,5 % |

MaxTemp incluye OR=1 en bootstrap, aunque su IC Wald lo excluye. Humidity9am queda cerca del límite y merece cautela. Los IC BCa y de beta también están exportados. Las tres localidades con mayor cambio máximo de beta al omitirlas son MountGinini, Wollongong y Ballarat; los cambios máximos absolutos son 0,02803; 0,02330 y 0,02231. Influencia no implica error de medición.

## Decisiones y limitaciones vigentes

- Regresión elegida por reconstrucción en donantes de train y cobertura; los resultados de prueba son sensibilidad, no criterio retrospectivo de elección de imputador.
- Diecinueve estaciones sin Sunshine observado; MAR y transporte entre estaciones no demostrados. Mediana auxiliar y recortes físicos se cuentan.
- Listas de predictores fijas en bootstrap; la incertidumbre completa de selección no está incluida. Independencia espacial y generalización temporal no verificadas.
- Scores ponderados sin calibrar; forma lineal del logit no exacta según diagnósticos exploratorios. No se borraron observaciones por Cook ni lluvias extremas plausibles.
- Prueba ya observada en F2 y archivo explorado en fases previas: comparación académica, no validación externa nueva.
- Simulación binomial de capacidad: iid, p fija, 30 días y riesgo 5 % supuestos; sin costos inventados ni pronósticos por fecha.

## Archivos y evidencia

El notebook maestro contiene 16 celdas de código con salidas. `src/sumativa3.py` implementa el análisis; `src/generar_informe_sumativa3.py` actualiza tablas LaTeX desde resultados. El PDF usa diez páginas y portada institucional; su fuente es editable. Presentación de 12 diapositivas y guion: `presentations/05_sumativa3/`. Ver auditoría de 108 puntos en `evidence/05_sumativa3/auditoria_final_sumativa3.md`.

No repetir remuestreo por un cambio puramente editorial. Si se modifica metodología, datos o semillas, ejecutar notebook completo, regenerar datos del informe y conciliar también presentación/guion. Conservar evidencia por plataforma y revisar el manifiesto antes del commit.
