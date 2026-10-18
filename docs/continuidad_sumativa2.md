# Continuidad Sumativa 2 hacia Sumativa 3

Resultados calculados desde el CSV original; sin entrenamiento predictivo.

Base de Patricio: `1484dd055fb99779932b85f0e87ac541400b893f`. Fuente S1: `134859256a519e0ffde2827319d73a603598e0ea`.

## Resultados y decisiones

### Media local: Humidity3pm
Estimación: 51.246693 %; IC95% [48.04160, 54.25606].
Evidencia: t=[48.0247, 54.4686]; percentil=[48.0451, 54.3491].
Conclusión: Estimación concordante entre métodos bajo modelo de localidades comparables.
Límite: Sin representatividad nacional ni independencia espacial comprobada; medias históricas observadas.
Acción posterior: Conservar estimando y unidades; no usar este promedio para imputar fuera del entrenamiento.

### Media local: MaxTemp
Estimación: 23.388345 °C; IC95% [22.29971, 24.57146].
Evidencia: t=[22.2233, 24.5534]; percentil=[22.2751, 24.5142].
Conclusión: Estimación concordante entre métodos bajo modelo de localidades comparables.
Límite: Sin representatividad nacional ni independencia espacial comprobada; medias históricas observadas.
Acción posterior: Conservar estimando y unidades; no usar este promedio para imputar fuera del entrenamiento.

### Media local: MinTemp
Estimación: 12.258711 °C; IC95% [11.26024, 13.47981].
Evidencia: t=[11.1239, 13.3935]; percentil=[11.1883, 13.3759].
Conclusión: Estimación concordante entre métodos bajo modelo de localidades comparables.
Límite: Sin representatividad nacional ni independencia espacial comprobada; medias históricas observadas.
Acción posterior: Conservar estimando y unidades; no usar este promedio para imputar fuera del entrenamiento.

### Diferencia local de humedad Yes-No
Estimación: 20.076901 pp; IC95% [18.51720, 21.61670].
Evidencia: 49/49 positivas; p_t=2.7471076e-29; p_signos=9.9990001e-05; jackknife [19.8007, 20.3584]; Albany: +0.2815 pp; AliceSprings: -0.2762 pp; Cobar: -0.1961 pp.
Conclusión: Asociación descriptiva consistente; estable al retirar una localidad.
Límite: La prueba de signos aleatorios requiere simetría bajo H0 e independencia; no es efecto causal ni cambio de probabilidad.
Acción posterior: Evaluar Humidity3pm disponible a la hora de emisión; comprobar estabilidad por fecha y localidad.

### Spearman: MaxTemp / Temp3pm
Estimación: 0.984476 coeficiente; IC95% [0.98123, 0.98682].
Evidencia: n=141589; Kendall=0.9117; Tukey=0.9842; excluye 0.55%.
Conclusión: Signo estable y magnitud poco sensible al filtro aplicado; posible redundancia.
Límite: Asociación agrupada; tamaños y cobertura por par distintos; IC condicional al remuestreo de localidades.
Acción posterior: Examinar redundancia MaxTemp/Temp3pm mediante diagnóstico y comparación dentro del entrenamiento; verificar hora de disponibilidad.

### Spearman: Humidity3pm / Sunshine
Estimación: -0.620349 coeficiente; IC95% [-0.65953, -0.58031].
Evidencia: n=74497; Kendall=-0.4492; Tukey=-0.6203; excluye 0.00%.
Conclusión: Signo estable en 30 localidades; filtro no elimina casos y no prueba resistencia a extremos.
Límite: Asociación agrupada; tamaños y cobertura por par distintos; IC condicional al remuestreo de localidades.
Acción posterior: Evaluar cobertura por localidad/periodo y comparar modelos con/sin Sunshine dentro del entrenamiento; no extrapolar el IC a las 49 localidades.

### Spearman: Humidity3pm / Rainfall
Estimación: 0.443635 coeficiente; IC95% [0.41072, 0.47392].
Evidencia: n=138569; Kendall=0.3403; Tukey=0.3074; excluye 17.89%.
Conclusión: Signo positivo estable; magnitud sensible al rango de precipitación.
Límite: Asociación agrupada; tamaños y cobertura por par distintos; IC condicional al remuestreo de localidades.
Acción posterior: Conservar lluvia plausible en el análisis principal; estudiar transformaciones y sensibilidad con umbrales aprendidos solo en entrenamiento.

### Dependencia temporal
Estimación: 0.502285 mediana lag-1.
Evidencia: Pares diarios consecutivos calculados en S1.
Conclusión: Dependencia diaria apreciable.
Límite: Conservar localidades completas retiene sus registros; no simula futuros temporales ni elimina dependencia espacial.
Acción posterior: Separar prueba por fechas completas; dentro de entrenamiento usar validación temporal y, si procede, geográfica.

### Desbalance RainTomorrow
Estimación: 22.418122 % Yes.
Evidencia: 142.193 etiquetas conocidas.
Conclusión: La exactitud aislada puede ocultar errores en lluvia.
Límite: Archivo completo ya explorado; evitar presentar la prueba futura como totalmente ajena a decisiones exploratorias previas.
Acción posterior: Priorizar métricas de rúbrica: matriz de confusión, precision, recall, F1 y ROC-AUC; PR-AUC como complemento; fijar umbral con validación de entrenamiento.

### Faltantes Sunshine
Estimación: 48.009762 % faltante.
Evidencia: 19 localidades sin Sunshine observado.
Conclusión: La composición de casos observados limita generalización.
Límite: No se comprobó mecanismo MCAR/MAR/MNAR.
Acción posterior: Ajustar imputación, selección y escalado dentro del entrenamiento; comparar estrategias con la misma partición.

## Archivos de referencia

- `results/03_sumativa2/resultados_validados_s2.json`: parámetros e intervalos completos.
- `results/03_sumativa2/tables/sintesis_resultados_para_s3.csv`: síntesis con decisiones.
- `results/03_sumativa2/tables/jackknife_diferencia_humedad.csv`: 49 localidades.
- `results/03_sumativa2/figures/s2_*.png`: cinco figuras utilizadas por el informe.
- `notebooks/03_sumativa2_validacion_remuestreo.ipynb`: cálculo e interpretación.
- `evidence/03_sumativa2/`: distinguir ejecución Work de reproducción Windows.

Antes de iniciar S3 se revisarán sus instrucciones y rúbrica; estas recomendaciones no autorizan su desarrollo.
