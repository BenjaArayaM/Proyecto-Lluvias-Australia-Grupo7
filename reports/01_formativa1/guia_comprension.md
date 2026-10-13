# Guía de comprensión y defensa de F1

Esta guía acompaña al notebook y al informe. No reemplaza leerlos ni acreditar participación en Canvas.

## Qué estamos describiendo

Cada fila es un registro meteorológico de una localidad y fecha. Hay 145.460 filas, pero no 145.460 experimentos independientes. La repetición temporal y los climas de cada localidad afectan las relaciones. El 22,42 % de Yes usa únicamente las 142.193 etiquetas conocidas; no se convierte un objetivo ausente en No.

## Por qué no imputamos ni eliminamos todo

F1 busca comprender los datos. Sunshine falta completamente en 19 localidades y los casos completos son solo el 38,79 % del archivo. Eliminar globalmente o imputar sin una metodología podría cambiar la composición. Por eso se excluyen faltantes para cada cálculo, se registra n y se conserva el original.

## Por qué existen dos medias

La media de todas las filas da más peso a las localidades que tienen más mediciones. La media de 49 medias locales da igual peso a cada localidad. Por ejemplo, Humidity3pm es 51,54 % por filas y 51,25 % con peso igual por localidad. Ambas se calculan correctamente; responden preguntas distintas.

## Qué significa nuestro intervalo

Para las 49 localidades fijas del CSV, su resumen no es desconocido. El IC agrega un modelo hipotético de localidades comparables e independencia aproximada. El 95 % corresponde a la cobertura del procedimiento al repetir ese modelo, no al porcentaje de días dentro del intervalo ni a una probabilidad del parámetro fijo. No hay evidencia de muestreo aleatorio nacional y no se ha probado independencia espacial. Los tres intervalos son individuales; no se afirma que todos cubran simultáneamente con probabilidad 95 %.

## Qué compara la prueba

En cada localidad se calcula la humedad media observada en filas con Yes y la humedad media en filas con No. Se restan y se obtiene una diferencia por localidad. La t usa esas 49 diferencias, con 48 grados de libertad. El emparejamiento es entre dos medias de la misma localidad, no entre dos días arbitrarios. La normalidad relevante es la de las diferencias; Shapiro no demuestra normalidad ni independencia.

## Cómo explicar el resultado sin exagerarlo

La diferencia media local es 20,08 puntos porcentuales de humedad. Bajo el modelo, su IC es 18,47–21,68 y el contraste encuentra incompatibilidad con H0. El valor p no indica la probabilidad de H0. La diferencia no significa que la probabilidad de lluvia aumente 20,08 puntos, ni que la humedad cause lluvia. Las 49 diferencias positivas y su tamaño sugieren pertinencia exploratoria; la utilidad predictiva debe evaluarse posteriormente con validación apropiada.

## Cómo defender las limitaciones

Un resultado pequeño de p no resuelve dependencia espacial, mezcla estacional, años desiguales o faltantes no aleatorios. Estos límites se declaran y se conservan para revisión. No se presenta un clasificador ni se usa una medición futura como predictor. El desplazamiento de Rainfall al día siguiente se emplea solo para auditar las etiquetas observadas.

## Relación con la rúbrica

La ficha y el diccionario cubren identificación y tipos de variables. Tablas y gráficos cubren descripción. Los tres IC y la t cubren inferencia básica con sus supuestos y límites. El notebook, módulo, exportaciones y evidencias permiten trazabilidad. La interpretación conecta los hallazgos con decisiones sensibles a la lluvia. La fuente LaTeX editable y su PDF compilado preparan la presentación formal; el Word anterior permanece como referencia. El foro requiere acciones reales del estudiante y del equipo, que el paquete no acredita.
