# Guion de exposición — Sumativa 3 — Grupo 7

Propuesta de reparto: cuatro integrantes, 2 minutos 30 segundos cada uno; 12 diapositivas, 10 minutos en total. Los tiempos son una planificación y deben comprobarse mediante ensayo. No acreditan una grabación realizada.

| Integrante | Diapositivas | Tiempo |
|---|---|---|
| Benjamín Araya | 1–3 | 00:00–02:30 |
| Jorge Guaico | 4–6 | 02:30–05:00 |
| Alan Cañete | 7–9 | 05:00–07:30 |
| Patricio Cortez | 10–12 | 07:30–10:00 |

Cada sección está también en las notas del PPTX. AIC: «a-i-ce»; BIC: «bi-ce»; OOF: predicciones fuera de pliegue; OR: odds ratio, cociente de odds. Odds no equivale a probabilidad. La palabra «prueba» designa el conjunto 30 % ya usado en F2.

## 1. Del análisis a una decisión de lluvia

**Benjamín Araya · 00:00–00:40**

Presentamos el cierre del proyecto Rain in Australia, desarrollado por Benjamín Araya, Alan Cañete, Patricio Cortez y Jorge Guaico. Nuestra pregunta es cómo usar las condiciones meteorológicas disponibles para identificar lluvia al día siguiente. Integramos descripción, remuestreo y clasificación, manteniendo la trazabilidad entre las tres sumativas. El objetivo no es mostrar únicamente un indicador alto: también debemos explicar qué días dejamos sin detectar, qué información falta y cuánto cambian las conclusiones al considerar diferencias entre localidades. La propuesta final mejora la detección frente a la Formativa 2, pero conserva limitaciones que comunicaremos durante la exposición.

## 2. Cada fase modifica una decisión

**Benjamín Araya · 00:40–01:35**

La primera sumativa describió asociaciones y calidad del archivo. Identificó, por ejemplo, ausencia de Sunshine cercana al cuarenta y ocho por ciento. La segunda sumativa examinó estabilidad: MaxTemp y Temp3pm resultaron casi redundantes, por lo que conservamos una sola en la clasificación. También mostró que humedad y precipitación mantienen asociación positiva, aunque su magnitud cae al restringir el rango de lluvia. Por eso aquí conservamos extremos plausibles y evaluamos una transformación logarítmica. La Formativa 2 aportó cuatro predictores y una referencia reproducible. Estas evidencias se convierten ahora en decisiones concretas de imputación, selección y evaluación.

## 3. La referencia exige detectar mejor la lluvia

**Benjamín Araya · 01:35–02:30**

El archivo tiene ciento cuarenta y cinco mil cuatrocientas sesenta filas y cuarenta y nueve localidades. Excluimos únicamente las etiquetas futuras ausentes, sin inventarlas. Quedan ciento cuarenta y dos mil ciento noventa y tres respuestas conocidas; aproximadamente veintidós por ciento corresponden a lluvia. Reproducimos la partición estratificada setenta treinta y las métricas de la Formativa 2. Su recall era treinta y nueve coma ochenta y dos por ciento, con cinco mil setecientos cincuenta y cinco omisiones. Esto explica por qué accuracy aislada resulta insuficiente. El conjunto de prueba ya se utilizó en la Formativa 2; esta comparación académica no constituye una validación externa nueva.

## 4. Los faltantes tienen estructura geográfica

**Jorge Guaico · 02:30–03:20**

Retomamos explícitamente el análisis de faltantes de la Sumativa 1. Sunshine está ausente en todas las fechas de diecinueve localidades, lo que cuestiona una explicación completamente aleatoria. Comparamos eliminación de casos incompletos, mediana e imputación mediante regresión. La respuesta RainTomorrow nunca participa como predictor de imputación. La partición ocurre antes de ajustar cualquier mediana, regresión o escala. Suponer que relaciones aprendidas en estaciones con observaciones se transportan a estaciones sin Sunshine es una limitación fundamental: el algoritmo puede completar una tabla, pero no demostrar que recuperó la medición que faltaba.

## 5. La regresión mejora reconstrucción observada

**Jorge Guaico · 03:20–04:10**

Construimos dieciséis regresiones OLS, una por variable numérica incompleta, cada una con tres predictores. Priorizamos relaciones de S1 y pares estables de S2. Como la matriz exportada de S1 cubre siete variables, ampliamos las relaciones restantes únicamente con entrenamiento y lo documentamos. En donantes de entrenamiento retenidos para validación, el RMSE de Sunshine baja de tres coma ochenta y dos a dos coma veintitrés horas, una reducción de cuarenta y uno coma setenta y seis por ciento. La regla fijada exigía al menos cinco por ciento de reducción frente a mediana. Los residuos presentan desviaciones; este resultado apoya reconstrucción predictiva, no normalidad ni certeza sobre valores ausentes.

## 6. Seleccionamos procedimientos dentro de entrenamiento

**Jorge Guaico · 04:10–05:00**

Comparamos tres procedimientos logísticos. El primero conserva los cuatro predictores de la Formativa 2. El segundo aplica stepwise AIC a ocho candidatos, incorporando viento, presión, humedad matinal y nubosidad. El tercero busca un modelo reducido mediante BIC entre subconjuntos de uno a tres predictores del primero. Declaramos esa restricción: no representa el mínimo BIC de toda combinación imaginable. La validación tiene cinco pliegues dentro de entrenamiento y reajusta imputación, escala y selección en cada pliegue. Seleccionamos el mayor AUC fuera de pliegue y fijamos el umbral con F1 de entrenamiento, antes de evaluar prueba.

## 7. M2 detecta más lluvia, con más falsas alertas

**Alan Cañete · 05:00–05:50**

El procedimiento seleccionado es M2, con ocho predictores y umbral cero coma seis cero tres cuatro. Se reajusta con pesos balanceados: aproximadamente dos coma veintitrés para lluvia y cero coma sesenta y cuatro para ausencia. En prueba alcanza AUC cero coma ocho seis uno nueve, recall sesenta y ocho coma veintiséis por ciento y F1 cero coma seis dos siete. Detecta seis mil quinientos veintiocho días lluviosos y omite tres mil treinta y cinco. El recall mejora veintiocho coma cuarenta y cuatro puntos frente a la referencia. Sin embargo, hay cuatro mil setecientas treinta y dos falsas alertas y accuracy disminuye cerca de un punto porcentual. La mejora requiere valorar ese intercambio.

## 8. Discriminación favorable; calibración pendiente

**Alan Cañete · 05:50–06:40**

Las curvas ROC comparan discriminación a distintos umbrales. M2 presenta mayor AUC que las otras dos especificaciones, de acuerdo con la elección realizada dentro de entrenamiento. AUC no es el porcentaje de clasificaciones correctas ni garantiza probabilidades calibradas. Al ponderar clases cambiamos el objetivo del ajuste: el score permite ordenar y aplicar el umbral seleccionado, pero no debe comunicarse directamente como probabilidad meteorológica. Los diagnósticos muestran VIF máximo cercano a tres, sin la redundancia extrema descartada. También detectan desviaciones de linealidad del logit en algunas variables. Las reconocemos y distinguimos significancia con muestra grande de la magnitud práctica de esas desviaciones.

## 9. La cobertura cambia la comparación de imputaciones

**Alan Cañete · 06:40–07:30**

Para aislar el impacto de imputación mantenemos los mismos predictores y el mismo umbral. La eliminación deja solo dieciocho mil doscientos treinta y cuatro casos de prueba y veintisiete localidades: cubre cuarenta y dos coma setenta y cuatro por ciento. Su AUC aparentemente superior describe otra población. Al comparar exactamente los mismos casos completos, las tres estrategias tienen AUC muy cercanas, alrededor de cero coma ochenta y ocho. También publicamos coeficientes e intervalos en una escala común. Elegimos regresión por reconstrucción interna y cobertura, no porque una diferencia pequeña en prueba demuestre superioridad universal. La mediana permanece como referencia de sensibilidad.

## 10. El bootstrap cambia la lectura de MaxTemp

**Patricio Cortez · 07:30–08:20**

La estabilidad se evalúa mediante dos mil remuestras válidas de las cuarenta y nueve localidades de entrenamiento. Cada localidad conserva juntos todos sus registros, y se reajustan imputaciones, escala, pesos y regresión logística. Las listas de predictores quedan fijas, por lo que los intervalos son condicionales a esa selección. Para humedad vespertina, el odds ratio por una desviación de referencia es dos coma cuarenta y seis, con intervalo bootstrap aproximado entre dos coma veintitrés y dos coma setenta y nueve. MaxTemp es el contraste principal: el intervalo bootstrap incluye uno, aunque el convencional no. Independencia entre localidades y representatividad nacional continúan como supuestos no demostrados.

## 11. La simulación responde una decisión explícita

**Patricio Cortez · 08:20–09:10**

Atendemos además la retroalimentación de S2: una simulación debe relacionarse con una decisión. Formulamos un escenario hipotético de treinta días y una tolerancia de cinco por ciento a exceder la capacidad. Calibramos frecuencias de lluvia solo en entrenamiento para humedad al menos setenta por ciento y para humedad menor. Diez mil simulaciones por grupo entregan capacidades de referencia de veintidós y siete días lluviosos. Contrastamos medias con el cálculo binomial y publicamos error Monte Carlo y convergencia. El ejercicio supone días independientes y probabilidades fijas: orienta cómo traducir incertidumbre en reserva de recursos, pero no pronostica treinta fechas reales ni incorpora costos observados.

## 12. Recomendaciones y límites del cierre

**Patricio Cortez · 09:10–10:00**

Concluimos con tres decisiones. Primero, utilizar M2 como especificación académica de referencia y comunicar recall junto con falsas alertas. Segundo, conservar comparación de imputaciones y revisar especialmente estaciones sin Sunshine observado. Tercero, interpretar con cautela MaxTemp y revisar las localidades más influyentes del nuevo ajuste: MountGinini, Wollongong y Ballarat. La progresión es explícita: S1 caracteriza, S2 contrasta estabilidad y S3 integra decisiones predictivas e incertidumbre. El notebook se ejecutó completo dos veces, con veintidós controles correctos y resultados numéricos idénticos. Antes de una aplicación operativa se requiere calibración y validación temporal y geográfica. La reproducción Windows y la grabación grupal se acreditan por separado.

## Ensayo y entrega

- Ensayar con cronómetro y ajustar la velocidad de cada bloque; conservar 2:30 por persona. Evitar leer cifras en exceso.
- Revisar juntos la distinción entre OR y probabilidad; supuestos de imputación, remuestreo, pesos de clase y Monte Carlo.
- Abrir el PPTX en el programa de grabación y comprobar gráficos, tipografía y notas; la apertura local todavía requiere evidencia.
- Grabar a los cuatro integrantes y verificar duración, audio, coordinación y legibilidad del video. No se entrega este PPTX como si acreditara participación efectiva.
- Comprobar formato de video, fecha y canal vigentes en Canvas; entregar PDF, notebook, presentación/video y enlace según el instructivo oficial. No se inventa plazo ni se publica automáticamente.
