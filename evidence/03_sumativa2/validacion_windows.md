# Validación en Windows — Sumativa 2

## Ejecución local

- Evidencia primaria: `ejecucion_sumativa2_windows.json`.
- Fecha de ejecución UTC: 2026-10-18T22:24:20.445125+00:00.
- Python: 3.12.0.
- Notebook ejecutado mediante nbconvert desde un kernel limpio: `grupo7_mcdi501`.
- Celdas de código: 13, ejecutadas en orden.
- Errores guardados: 0.
- Controles numéricos: 10 de 10 correctos.
- CSV original intacto; SHA-256: `573fd715cd69fcacc4df32024d823b450ae3edaae7e8ff2eeb623adbed424014`.
- Las huellas de resultados y scripts coincidieron con el registro local.

## Concordancia con Work

Se cotejaron las salidas de Windows compartidas por Benjamín Araya con los
resultados de la ejecución documentada en Work:

- Tres estimaciones e intervalos clásicos, percentil y BCa.
- Diferencia de humedad, estadístico t y valores p.
- Tres correlaciones de Spearman e intervalos bootstrap.
- Media, desviación y cuantiles de Monte Carlo.
- Intervalos de la diferencia y rango jackknife.
- Influencia de Albany, AliceSprings y Cobar.
- Sensibilidad de Humidity3pm–Rainfall y proporción de registros excluidos.

Todas las cifras cotejadas coinciden hasta los dígitos mostrados.
La comparación corresponde a estas cifras; no certifica identidad binaria
de todos los archivos entre plataformas.

La correlación Humidity3pm–Rainfall pasa de 0,443635 a 0,307406 con el
filtro diagnóstico: conserva el signo positivo y su magnitud es sensible
al rango de precipitación.

## Alcance

La reproducción computacional está verificada. Los supuestos espaciales
y de intercambiabilidad conservan las limitaciones declaradas.
La compilación LaTeX y el PDF de siete páginas se verificaron en Work.
La revisión grupal, la publicación y la entrega en Canvas se acreditan
por separado.
