# Decisiones metodológicas — Sumativa 3

Fecha de preparación: 24 de octubre de 2026. Grupo 7: Benjamín Araya, Alan Cañete, Patricio Cortez y Jorge Guaico.

## Fuentes y alcance

Prevalecen la rúbrica vigente aportada por Benjamín (108 puntos), `INSTRUCCIONES SUMATIVA 3.docx` y las aclaraciones docentes entregadas en las retroalimentaciones de S2 y F2. La plantilla antigua asignaba seis puntos a presentación; la rúbrica vigente asigna nueve. No se usa la hoja antigua «AUN NO DISPONIBLE» para inventar requisitos de S3.

El enunciado específico solicita video de diez minutos; la caracterización general menciona video o presentación en vivo. Se prepara el material para video, conforme a la instrucción específica y al nivel «No cumple» de la rúbrica. Si el docente autoriza exposición en vivo, conservar esa aclaración. No hay fecha de entrega verificable en los materiales revisados.

El adjunto `Objetivo de la actividad SUMATIVA 3.docx` tiene nombre discordante: su contenido describe S2/Fase 3, 20 %, siete páginas y rúbrica de 87 puntos. Fue leído y se clasifica por ese contenido como antecedente S2. No se mezcla con el enunciado de cierre S3 ni se trasladan automáticamente sus 10.000 remuestras a bootstrap del modelo final. Esta discrepancia queda visible y el rótulo puede confirmarse en Canvas.

## 1. Antecedentes y etiquetas

- Se mantiene el SHA-256 del CSV, su orden e índices originales: 145.460 × 23, 49 localidades.
- Se excluyen las 3.267 etiquetas RainTomorrow ausentes. No se imputan ni se reconstruyen etiquetas con información futura.
- S1 y S2 estudiaron el archivo completo y F2 ya utilizó el conjunto 30 %. Se conserva la división estratificada 70/30, semilla 42, solicitada en el curso; se declara que no es una prueba externa nueva.
- Date y Location se conservan para trazabilidad y remuestreo. Los tres clasificadores usan predictores numéricos disponibles en el día registrado; no se impone una hora de emisión que el dataset no certifica.
- No hay variables categóricas en esos modelos. RainTomorrow se codifica No=0/Yes=1; las direcciones del viento y RainToday no se introducen sin justificación adicional.

## 2. Imputación por regresión

Se recupera directamente la auditoría de faltantes de S1. Para las 16 variables numéricas incompletas se ajusta OLS con tres predictores en donantes completos de entrenamiento. La selección prioriza pares estables de S2 y limita redundancia. La matriz exportada de S1 cubre siete variables: las relaciones adicionales se calculan únicamente en entrenamiento y se rotulan «ampliación S3». No se presenta esa ampliación como resultado previo de S1.

La evaluación de reconstrucción retiene 20 % de donantes de entrenamiento y compara regresión con mediana, con RMSE, MAE y R². Se examinan normalidad, heterocedasticidad y VIF; se publican los diagnósticos de las 16 regresiones y sus coeficientes. Las desviaciones de supuestos no se ocultan. La reconstrucción predictiva no certifica inferencia OLS ni mediciones recuperadas.

Al aplicar OLS puede faltar una covariable: se usa su mediana auxiliar aprendida en entrenamiento. Esta operación no utiliza etiquetas. Se cuentan esos usos y los recortes físicos aplicados exclusivamente a valores imputados. Ningún valor originalmente observado se altera. Los límites de humedad, sol, precipitación y nubosidad son controles de plausibilidad; no hacen verdadera la imputación.

La regla de elección se fija antes de evaluar prueba: usar regresión si reduce al menos 5 % el RMSE de Sunshine frente a mediana en donantes retenidos. Es una recomendación metodológica, no un umbral impuesto por la rúbrica. El resultado fue 41,76 %. Mediana y eliminación se conservan para sensibilidad del modelo final. La regla centrada en Sunshine se justifica por su elevada ausencia y patrón geográfico; no garantiza que regresión sea mejor para toda variable.

El patrón por estación cuestiona MCAR. MAR condicionado a covariables es un supuesto de trabajo; MNAR no se descarta. Diecinueve localidades carecen de Sunshine observado: transportar la relación de otras estaciones requiere un supuesto adicional no comprobado. Imputación determinista reduce variabilidad y no incorpora la incertidumbre completa del valor ausente.

## 3. Modelos y criterios

M1 conserva Humidity3pm, Sunshine, Rainfall y MaxTemp de F2, informados por S1/S2. M2 aplica stepwise bidireccional AIC a ocho candidatos; sustituye Rainfall por log1p(Rainfall) y añade WindGustSpeed, Pressure3pm, Humidity9am y Cloud3pm. M3 minimiza BIC entre los 14 subconjuntos de uno a tres predictores de M1. Esta restricción responde a la recomendación docente de un modelo reducido; no es búsqueda global de BIC ni prueba de que la selección sea única.

Se conservan precipitaciones extremas plausibles. El filtro de S2 cambia ρ de 0,444 a 0,307 y restringe la muestra a precipitación ≤ 2 mm; no autoriza eliminar automáticamente lluvias intensas. Log1p modera asimetría sin borrar registros. Temp3pm no entra en clasificadores por su redundancia con MaxTemp; sí puede servir como covariable de imputación dentro del día.

AIC/BIC de selección se calculan sin pesos, sobre idénticas observaciones de entrenamiento. Luego se reajustan los clasificadores con pesos balanceados `n/(2*n_clase)`: 2,2303 para Yes y 0,6445 para No. No se mezclan IC de selección sin ponderar con inferencia del ajuste ponderado.

Cinco pliegues estratificados, semilla 50102, reajustan imputación, estandarización y selección dentro de cada entrenamiento interno. Se elige el mayor AUC fuera de pliegue (OOF); diferencias ≤0,002 favorecen menos predictores. El umbral de cada procedimiento maximiza F1 OOF. Se congela la decisión antes de predecir prueba. La estimación OOF se usa para elegir procedimientos: no sustituye validación externa ni equivale a un estimador sin sesgo tras selección.

## 4. Estabilidad e interpretación

El bootstrap sortea 49 localidades de entrenamiento con reemplazo y conserva todos sus registros. Se reajustan regresiones de imputación, medianas auxiliares, escalas, pesos de clase y logística. Permanecen fijas las listas de predictores del modelo y de los imputadores; por ello los intervalos son condicionales a esas elecciones. Se usan 2.000 remuestras válidas y 49 omisiones jackknife; el número es una decisión del plan aprobado, no un mínimo inventado del enunciado.

La implementación rápida usa multiplicidades y estadísticos OLS por conglomerado. Se cotejó contra duplicación material de filas y un GLM de statsmodels independiente. Los coeficientes bootstrap se convierten a una misma desviación de referencia, evitando mezclar escalas. Los intervalos de OR son la exponencial de los límites de beta, no «OR ± error».

La independencia aproximada entre localidades no se demuestra por remuestrearlas. La dependencia diaria se conserva dentro de cada conglomerado, pero puede persistir dependencia espacial entre estaciones. Los intervalos describen ese esquema condicional; no prueban representatividad nacional. La frecuencia de signo conservado es descriptiva, no una probabilidad posterior.

Los IC Wald son la referencia convencional del ajuste ponderado y no corrigen selección, imputación ni dependencia espacial. La discrepancia para MaxTemp se comunica expresamente. Odds ratio multiplica odds bajo la parametrización del ajuste ponderado, no probabilidad ni efecto causal. Los scores ponderados requieren calibración antes de interpretarse como probabilidades meteorológicas.

## 5. Comparaciones y diagnósticos

Para el modelo final se comparan eliminación, mediana y regresión con idénticos predictores y umbral congelado. Se publican tamaño, localidades, cobertura, distribuciones, correlaciones, coeficientes/IC en una escala común, AUC y accuracy. Se distinguen prueba propia de cada estrategia y los mismos casos comunes: comparar muestras distintas como si fueran idénticas confundiría cobertura con desempeño.

VIF, extensiones exploratorias Box–Tidwell, residuos de deviance/Pearson, Cook y leverage son diagnósticos. La logística no requiere residuos normales. Los valores p de forma funcional son exploratorios bajo ponderación; se acompaña el cambio relativo de deviance. No se eliminan automáticamente los registros con Cook >4/n. Las localidades más influyentes en S3 se recalculan; no se importan Albany, AliceSprings y Cobar de otro estimando de S2.

## 6. Decisión Monte Carlo y comunicación

Se añade una extensión S3 para responder a la retroalimentación de S2: capacidad para atender días lluviosos en un escenario hipotético de 30 días, aceptando 5 % de excedencia. Se estiman frecuencias en entrenamiento con Humidity3pm observado ≥70 % y <70 %. Se simulan 10.000 binomiales por grupo y se contrastan medias, colas y error Monte Carlo con cálculo analítico.

Los días iid, la probabilidad fija, el horizonte y la tolerancia son supuestos declarados, no datos de un cliente ni requisitos docentes. No es un pronóstico de fechas, ni un análisis de costos inexistentes. Cero excedencias simuladas no significa probabilidad cero.

El informe tiene diez páginas totales, incluida portada y referencias, porque el instructivo no especifica exclusiones. El PPTX y el guion distribuyen 2:30 a cada integrante; el tiempo real, la participación y el dominio conceptual deben demostrarse mediante ensayo y video. No se declara el proyecto entregado por existir archivos.
