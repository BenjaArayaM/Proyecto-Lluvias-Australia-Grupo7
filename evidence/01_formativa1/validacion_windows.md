# Validación de la reproducción Windows de Formativa 1

Revisión: 10 de octubre de 2026. Ejecución Windows registrada: `2026-10-10T18:02:15.855957+00:00` (15:02:15 del 10 de octubre en Chile continental).

## Procedencia de la evidencia

El estudiante ejecutó el notebook en su computador y compartió la salida final de ejecución completa, los controles correctos y `ejecucion_windows.json`. Posteriormente adjuntó `dependencia_lag1.csv`, `intervalos_localidades.csv` y `resultados.json`. La asistencia revisó esos archivos en Work; no ejecutó comandos ni código en el computador del estudiante.

## Comprobaciones realizadas

| Comprobación | Resultado | Evidencia |
|---|---|---|
| Entorno Windows y Python del proyecto | Python 3.12.0; kernel desde la .venv, verdadero | Registro Windows y comprobaciones previas del intérprete/kernel |
| Identidad e integridad del CSV | SHA-256 esperado; original sin modificaciones | Registro de ejecución y controles implementados |
| Código fuente usado | Identidad exacta de src/formativa1.py | Hash Windows idéntico al módulo entregado |
| Versiones científicas | Las siete bibliotecas del registro coinciden entre entornos | Registros Work y Windows |
| 17 tablas CSV | Coinciden exactamente al adaptar LF a CRLF | Hash de la referencia convertido comparado con el registro Windows |
| Dos tablas CSV restantes | Estructura, categorías, conteos y cifras equivalentes | Comparación completa de los archivos adjuntados |
| resultados.json | Estructura y contenido equivalentes | Comparación recursiva completa del archivo adjuntado |
| Autenticidad de los tres adjuntos | Sus hashes coinciden con la ejecución Windows | SHA-256 calculado independientemente |
| Estimaciones, intervalos y contraste principal | Coinciden; las cifras publicadas se conservan | Tablas y resumen JSON comparados |

Python Work fue 3.12.14 y Python Windows 3.12.0; esa diferencia está registrada. La comparación numérica usó tolerancia relativa `1e-12`, tolerancia absoluta cero, y coincidencia exacta para enteros, etiquetas, claves y nulos. La diferencia absoluta máxima fue 1.010302952408892e-14 y la relativa máxima 1.124710840470972e-14. Las pequeñas diferencias se encuentran en autocorrelaciones y diagnósticos Shapiro, en los últimos decimales; no cambian los resultados presentados ni las conclusiones. Los hashes de los PNG difieren entre entornos: este registro conserva sus huellas, pero no acredita una comparación visual de los PNG de Windows.

Las 19 tablas y el resumen quedan conciliados con la referencia. La evidencia detallada permanece en `validacion_windows.json`. Los resultados locales, el notebook guardado y los registros originales del estudiante se conservan. El módulo y las celdas de análisis no fueron modificados para obtener esta validación.

## Límites y pendientes académicos

La validación computacional no comprueba independencia espacial, muestreo probabilístico nacional ni desempeño predictivo. Los intervalos y la prueba mantienen su interpretación condicional. Sigue pendiente verificar la fecha e instrucciones vigentes de Canvas, revisar el informe con los cuatro integrantes, entregar el PDF y registrar publicación y comentarios fundamentados a al menos dos grupos. No se declara una entrega realizada ni se estima calificación.
