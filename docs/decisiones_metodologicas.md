# Registro de decisiones — MCDI501 — Grupo 7

Fecha de actualización: 10 de octubre de 2026. Los registros distinguen hechos técnicos verificados, decisiones estadísticas y cuestiones pendientes. La solicitud de preparar la Formativa 1 completa autoriza este desarrollo; no autoriza iniciar las demás evaluaciones.

## Preparación técnica

| ID | Decisión | Fundamento y evidencia | Estado |
|---|---|---|---|
| D001 | Usar el repositorio existente del Grupo 7. | URL proporcionada, clonación y origin comprobados en las salidas del estudiante. | Confirmado. |
| D002 | Guardar el proyecto en el Escritorio real de Windows. | Ruta OneDrive/Escritorio verificada mediante la salida del estudiante. | Confirmado. |
| D003 | Conservar la estructura aprobada para las cinco fases. | Archivos iniciales revisados por el estudiante y commit d5142a1. | Base local confirmada. |
| D004 | Usar .venv con Python 3.12.0 y kernel grupo7_mcdi501. | Ruta del intérprete, dependencias, pip check, kernel.json, JupyterLab y arranque de kernel evidenciados. | Entorno local preparado; ejecución F1 completa y equivalencia de resultados acreditadas. |
| D005 | Desarrollar únicamente F1. | Selección y solicitud expresa de la Formativa 1 completa. | Activo. |
| D006 | Mantener el CSV original sin modificaciones y fuera de Git. | Exclusiones .gitignore verificadas; CSV local auditado por el estudiante y en Work. | Confirmado. |
| D007 | Preservar requisitos exactos y evidencia de cada entorno. | Lock Windows y entorno.json del estudiante; archivos Work diferenciados. | Confirmado; no reemplazar los registros de Windows. |
| D008 | Trabajar en la rama local formativa1-benjamin. | Creación por el estudiante comprobada en su salida. | Confirmado localmente; no se ha verificado publicación remota. |

| D009 | Identificar a los cuatro integrantes: Benjamín Araya, Alan Cañete, Patricio Cortez y Jorge Guaico. | Confirmación explícita del estudiante el 10 de octubre de 2026. | Confirmado para MCDI501. |

## Formato del informe

| ID | Decisión | Fundamento y evidencia | Estado |
|---|---|---|---|
| D010 | Usar LaTeX como fuente editable del informe y generar el PDF con pdfLaTeX. | Solicitud expresa del estudiante antes del commit. Se transcribe el informe validado: nueve tablas, tres ecuaciones y cinco figuras utilizadas; portada con los cuatro integrantes e índice. Esta modificación no cambia el análisis F1-1.0. | Compilado y revisado en Work; incorporación local y compilación en Windows/Overleaf pendientes de evidencia. |

## Decisiones estadísticas de F1

| ID | Decisión y motivo | Evidencia y consecuencias |
|---|---|---|
| F1-D01 | Comprobar SHA-256, tamaño, dimensiones y columnas antes de analizar. | cargar_datos detiene versiones incompatibles. La referencia es 573fd715cd69fcacc4df32024d823b450ae3edaae7e8ff2eeb623adbed424014. |
| F1-D02 | Conservar el original y trabajar sobre una copia con Date interpretada y agrupaciones temporales. | No se imputa ni modifica el CSV; se verifica igualdad del original y hash al finalizar. |
| F1-D03 | Clasificar cada columna por significado estadístico, no solo dtype. | Temperaturas continuas, fecha temporal, direcciones nominales circulares, nubosidad codificada y objetivo binario. |
| F1-D04 | Excluir faltantes por cálculo y registrar denominadores. | No se reduce globalmente a casos completos. Las proporciones del objetivo usan 142.193 etiquetas; los faltantes se informan aparte. |
| F1-D05 | Señalar extremos por Tukey sin eliminarlos automáticamente. | Se conservan valores meteorológicos plausibles y se distinguen inconsistencias físicas. Los tres códigos Cloud=9 se mantienen. |
| F1-D06 | Interpretar físicamente Cloud=0–8 y mantener el código 9 como significado histórico pendiente. | BoM documenta 9 como niebla en otro producto; no se presume equivalencia definitiva. Solo se excluye 9 de la vista de correlación ordinal. |
| F1-D07 | Auditar RainToday y RainTomorrow contra Rainfall > 1 mm sin reconstruir objetivos. | Coincidencias en pares observados y días exactamente consecutivos. El desplazamiento de Rainfall se usa únicamente para auditoría, nunca como predictor. |
| F1-D08 | Presentar bivariado y Spearman como relaciones exploratorias. | Se conservan n por par. Los tamaños distintos, faltantes y composición geográfica limitan comparaciones de magnitud. |
| F1-D09 | Usar meses del registro y estaciones australes como agrupaciones descriptivas. | Verano: dic–feb; otoño: mar–may; invierno: jun–ago; primavera: sep–nov. Una frecuencia agrupada puede mezclar años y localidades. |
| F1-D10 | Verificar dependencia temporal con pares de Humidity3pm exactamente consecutivos por localidad. | Mediana de correlación lag 1: 0,5023. No se contabilizan como consecutivos saltos de fecha; se conserva cobertura desigual. |
| F1-D11 | Estimar humedad y temperaturas con 49 medias históricas por localidad y peso igual. | Reduce pseudorreplicación diaria y define un estimando diferente de la media por filas. No elimina posible dependencia espacial. |
| F1-D12 | Formular IC t individuales al 95 % bajo un modelo hipotético de localidades comparables. | Parámetro: media de medias históricas observadas del modelo. El resumen de las 49 localidades fijas es exacto; no se afirma inferencia nacional ni conjunta de tres IC. |
| F1-D13 | Comparar la humedad de Yes y No dentro de cada localidad, usando una t sobre las 49 diferencias. | H0: μD=0; H1: μD≠0; α=0,05. Equivale a una t pareada de medias locales; no empareja días ni exige igualdad de varianzas diarias. |
| F1-D14 | Diagnosticar la forma de los resúmenes mediante Q-Q, Shapiro y Tukey, manteniendo todos los valores. | Shapiro no prueba normalidad ni independencia. Se declara independencia aproximada entre localidades como supuesto no comprobado espacialmente. |
| F1-D15 | Conservar la magnitud en puntos porcentuales y una conclusión condicional. | Diferencia local de humedad 20,08; no es cambio de probabilidad de lluvia, efecto causal ni evidencia de clasificación validada. |
| F1-D16 | Declarar que la selección y comparación son exploratorias. | El archivo completo ya fue revisado. No se presenta preregistro ni evaluación externa ciega; futuras decisiones predictivas se ajustarán en entrenamiento. |
| F1-D17 | Separar evidencia Work y Windows. | Work: 19 celdas reales en ipykernel en memoria, cero errores. Reproducción JupyterLab Windows acreditada por el estudiante; versiones coincidentes y 19 tablas/resumen conciliados. Las huellas de cada entorno se conservan. |
| F1-D18 | Exportar estadísticas y conservar estimandos para continuidad. | results/01_formativa1/resultados.json, tablas, figuras y ficha. Las fases futuras deben citar estas versiones y recalcular si cambian datos o criterios. |

## Decisiones que siguen pendientes

- Conservar los registros Work y Windows, la comparación numérica y las salidas locales ya validadas. El estado de ejecución no sustituye la revisión académica de Canvas.
- Fijar el momento de emisión de una futura predicción y comprobar cada ventana de medición. Los totales diarios y ráfagas hasta medianoche no se consideran automáticamente disponibles a las 3 pm.
- Seleccionar un esquema de partición y validación conforme a la rúbrica de la fase correspondiente. Considerar tiempo, localidades, desbalance y el antecedente de EDA sobre el archivo completo.
- Revisar dependencia espacial, mezcla de períodos y sensibilidad antes de generalizar inferencias.
- Resolver imputación, escalamiento, selección de predictores y modelamiento en su evaluación, aprendiendo todos los ajustes con entrenamiento.

Este registro no declara que una limitación esté resuelta por haber sido documentada. Las decisiones futuras se incorporan cuando se autorice y se disponga de evidencia.
