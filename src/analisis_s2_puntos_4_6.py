from pathlib import Path
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

SEED = 20261018
N_MC = 10_000
N_BOOT = 10_000
ALPHA = 0.05
DATA = Path("data/raw/weatherAUS.csv")
OUT = Path("results/03_sumativa2")
TABLES, FIGS = OUT / "tables", OUT / "figures"
TABLES.mkdir(parents=True, exist_ok=True)
FIGS.mkdir(parents=True, exist_ok=True)
rng = np.random.default_rng(SEED)

if not DATA.exists():
    raise FileNotFoundError(f"No se encontró {DATA}; ejecuta desde la raíz del repositorio.")
df = pd.read_csv(DATA, low_memory=False)
required = {"Location", "RainTomorrow", "Humidity3pm", "MaxTemp", "Temp3pm", "Sunshine", "Rainfall"}
missing = required - set(df.columns)
if missing:
    raise ValueError(f"Faltan columnas: {sorted(missing)}")
df["RainTomorrow"] = df["RainTomorrow"].astype("string").str.strip()

# PUNTO 4: Monte Carlo basado en la media y SD de las 49 diferencias locales S1.
h = df.loc[df.RainTomorrow.isin(["Yes", "No"]), ["Location", "RainTomorrow", "Humidity3pm"]].copy()
h["Humidity3pm"] = pd.to_numeric(h["Humidity3pm"], errors="coerce")
h = h.dropna(subset=["Location", "RainTomorrow", "Humidity3pm"])
means = h.groupby(["Location", "RainTomorrow"])["Humidity3pm"].mean().unstack().dropna(subset=["Yes", "No"])
d = (means["Yes"] - means["No"]).astype(float)
nloc, mu, sd = len(d), float(d.mean()), float(d.std(ddof=1))
if nloc < 2 or not np.isfinite(sd) or sd <= 0:
    raise ValueError("Diferencias locales insuficientes para la simulación.")

# Escenario: medias de muestras hipotéticas de nloc localidades comparables.
# No es simulación del clima ni pronóstico de lluvia.
sim = rng.normal(mu, sd, size=(N_MC, nloc)).mean(axis=1)
mc_summary = pd.DataFrame([{
    "escenario": "Media de diferencias locales en muestras hipotéticas de localidades comparables",
    "distribucion": "Normal(mu_hat, sd_hat), estimados de las diferencias locales S1",
    "n_localidades_S1": nloc, "media_diferencias_S1_pp": mu,
    "sd_diferencias_entre_localidades_pp": sd, "localidades_por_muestra": nloc,
    "iteraciones": N_MC, "media_simulada_pp": sim.mean(), "sd_medias_simuladas_pp": sim.std(ddof=1),
    "p2_5_pp": np.quantile(sim, .025), "p97_5_pp": np.quantile(sim, .975), "semilla": SEED
}])
mc_summary.to_csv(TABLES / "monte_carlo_resumen.csv", index=False)
checkpoints = sorted(set([100, 500, 1000, 2500, 5000, N_MC]))
conv = []
cummean = np.cumsum(sim) / np.arange(1, N_MC + 1)
for k in checkpoints:
    qlo, qhi = np.quantile(sim[:k], [.025, .975])
    conv.append({"iteraciones": k, "media_acumulada": cummean[k-1],
                 "p2_5": qlo, "p97_5": qhi, "ancho_intervalo": qhi-qlo})
conv = pd.DataFrame(conv)
conv.to_csv(TABLES / "monte_carlo_convergencia.csv", index=False)

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(np.arange(1, N_MC+1), cummean, linewidth=1)
ax.axhline(mu, linestyle="--", label=f"Media observada S1 = {mu:.2f} pp")
ax.set(xlabel="Iteraciones Monte Carlo", ylabel="Media acumulada simulada (pp)",
       title="Convergencia de la media simulada")
ax.legend(); fig.tight_layout()
fig.savefig(FIGS / "monte_carlo_convergencia.png", dpi=180); plt.close(fig)

fig, ax = plt.subplots(figsize=(10, 5))
ax.hist(sim, bins=45, density=True, alpha=.8, edgecolor="white")
ax.axvline(np.quantile(sim,.025), linestyle="--", label="Percentil 2,5")
ax.axvline(np.quantile(sim,.975), linestyle="--", label="Percentil 97,5")
ax.axvline(mu, linestyle=":", linewidth=2, label=f"Media S1 = {mu:.2f} pp")
ax.set(xlabel="Media simulada de la diferencia de humedad (pp)", ylabel="Densidad",
       title="Monte Carlo: escenario de medias entre localidades")
ax.legend(); fig.tight_layout()
fig.savefig(FIGS / "monte_carlo_distribucion.png", dpi=180); plt.close(fig)

# PUNTO 5A: bootstrap y jackknife de las diferencias locales.
dv = d.to_numpy()
boot = np.array([rng.choice(dv, size=nloc, replace=True).mean() for _ in range(N_BOOT)])
boot_ci = np.quantile(boot, [.025, .975])
jack = np.array([np.delete(dv, i).mean() for i in range(nloc)])
locs = d.index.astype(str).to_numpy()
jack_table = pd.DataFrame({
    "localidad_omitida": locs, "media_sin_localidad_pp": jack,
    "cambio_vs_media_completa_pp": jack - mu, "cambio_absoluto_pp": np.abs(jack-mu)
}).sort_values("cambio_absoluto_pp", ascending=False)
jack_table.to_csv(TABLES / "jackknife_diferencia_humedad.csv", index=False)
t_ci = stats.t.interval(.95, df=nloc-1, loc=mu, scale=stats.sem(dv))
robust_d = pd.DataFrame([{
    "n_localidades": nloc, "media_diferencia_pp": mu,
    "ic95_t_inferior": t_ci[0], "ic95_t_superior": t_ci[1],
    "ic95_bootstrap_inferior": boot_ci[0], "ic95_bootstrap_superior": boot_ci[1],
    "media_jackknife_min": jack.min(), "media_jackknife_max": jack.max(),
    "diferencias_locales_positivas": int((dv > 0).sum()),
    "max_cambio_absoluto_jackknife_pp": np.abs(jack-mu).max(),
    "bootstrap_replicas": N_BOOT, "semilla": SEED
}])
robust_d.to_csv(TABLES / "robustez_diferencia_humedad.csv", index=False)

fig, ax = plt.subplots(figsize=(10, 6))
show = jack_table.head(15).sort_values("cambio_absoluto_pp")
ax.barh(show.localidad_omitida, show.cambio_vs_media_completa_pp)
ax.axvline(0, linestyle="--")
ax.set(xlabel="Cambio al omitir localidad (pp)", ylabel="Localidad omitida",
       title="Jackknife: localidades más influyentes")
fig.tight_layout(); fig.savefig(FIGS / "jackknife_influencia_localidades.png", dpi=180); plt.close(fig)

# PUNTO 5B: Spearman vs Kendall y sensibilidad diagnóstica a cercas de Tukey.
# El análisis principal conserva todos los valores plausibles; el filtro solo diagnostica sensibilidad.
pairs = [("MaxTemp","Temp3pm"), ("Humidity3pm","Sunshine"), ("Humidity3pm","Rainfall")]
corr_rows = []
for x, y in pairs:
    z = df[[x,y]].copy()
    z[x] = pd.to_numeric(z[x], errors="coerce"); z[y] = pd.to_numeric(z[y], errors="coerce")
    z = z.replace([np.inf,-np.inf], np.nan).dropna()
    if len(z) < 3: continue
    rho = float(stats.spearmanr(z[x],z[y]).statistic)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        tau = float(stats.kendalltau(z[x],z[y], variant="b").statistic)
    xq1,xq3 = z[x].quantile([.25,.75]); yq1,yq3 = z[y].quantile([.25,.75])
    xi,yi = xq3-xq1,yq3-yq1
    keep = z[x].between(xq1-1.5*xi,xq3+1.5*xi) & z[y].between(yq1-1.5*yi,yq3+1.5*yi)
    zf = z.loc[keep]
    rhof = float(stats.spearmanr(zf[x],zf[y]).statistic) if len(zf)>=3 else np.nan
    corr_rows.append({
        "variable_x":x,"variable_y":y,"n_completo":len(z),"spearman_completo":rho,
        "kendall_tau_b_completo":tau,"n_dentro_cercas_tukey":len(zf),
        "porcentaje_excluido_solo_sensibilidad":100*(1-len(zf)/len(z)),
        "spearman_sensibilidad_tukey":rhof,"cambio_spearman":rhof-rho,
        "signo_spearman_kendall_coincide":bool(np.sign(rho)==np.sign(tau))
    })
corr = pd.DataFrame(corr_rows)
corr.to_csv(TABLES / "robustez_correlaciones.csv", index=False)

# PUNTO 6: síntesis de resultados y recomendaciones para S3.
synthesis = [{
    "resultado":"Diferencia de Humidity3pm Yes-No por localidad",
    "estimacion":f"{mu:.2f} pp",
    "evidencia_robustez":f"IC bootstrap [{boot_ci[0]:.2f}, {boot_ci[1]:.2f}]; rango jackknife [{jack.min():.2f}, {jack.max():.2f}]; {int((dv>0).sum())}/{nloc} localidades positivas",
    "conclusion":"Asociación descriptiva consistente en las localidades observadas",
    "cautela":"No implica causalidad ni cambio de probabilidad; puede persistir dependencia espacial y temporal",
    "recomendacion_s3":"Fijar hora de emisión y usar solo predictores disponibles en ese momento"
}]
for _, r in corr.iterrows():
    synthesis.append({
        "resultado":f"Correlación {r['variable_x']} vs {r['variable_y']}",
        "estimacion":f"Spearman={r['spearman_completo']:.3f}; Kendall tau-b={r['kendall_tau_b_completo']:.3f}",
        "evidencia_robustez":f"Spearman sensibilidad Tukey={r['spearman_sensibilidad_tukey']:.3f}; cambio={r['cambio_spearman']:.3f}",
        "conclusion":"Comparar signo y magnitud entre métodos antes de considerar su uso",
        "cautela":"La exclusión Tukey es solo diagnóstico; no recomienda eliminar extremos meteorológicos",
        "recomendacion_s3":"Validar estabilidad por tiempo y localidad y comprobar disponibilidad del predictor"
    })
synthesis.extend([
    {"resultado":"Dependencia temporal","estimacion":"Mediana de correlación lag-1 Humidity3pm = 0.5023 en S1",
     "evidencia_robustez":"Las filas diarias no deben suponerse independientes automáticamente",
     "conclusion":"La dependencia temporal afecta la incertidumbre y validación",
     "cautela":"El bootstrap por localidad no conserva explícitamente dependencia diaria",
     "recomendacion_s3":"Validación temporal o por bloques de fecha/localidad; ajustar preprocesamiento solo con entrenamiento"},
    {"resultado":"Desbalance RainTomorrow","estimacion":"Yes ≈ 22.42%; No ≈ 77.58% entre etiquetas conocidas",
     "evidencia_robustez":"La exactitud sola puede ocultar mal desempeño en la clase Yes",
     "conclusion":"El desbalance debe considerarse en evaluación",
     "cautela":"No balancear usando validación o prueba",
     "recomendacion_s3":"Reportar recall, precisión, F1, PR-AUC y matriz de confusión por clase"},
    {"resultado":"Datos faltantes","estimacion":"Sunshine ≈ 48.01% faltante; Evaporation ≈ 43.17%",
     "evidencia_robustez":"Cobertura desigual entre variables, localidades y periodos",
     "conclusion":"La eliminación global de filas puede cambiar la composición de la muestra",
     "cautela":"Imputar o escalar antes de dividir puede filtrar información",
     "recomendacion_s3":"Ajustar imputación y escalado solo dentro del entrenamiento"}
])
synthesis = pd.DataFrame(synthesis)
synthesis.to_csv(TABLES / "sintesis_resultados_para_s3.csv", index=False)

with open(OUT / "resumen_puntos_4_6.txt","w",encoding="utf-8") as f:
    f.write("SUMATIVA 2 — PUNTOS 4, 5 Y 6\n"+"="*70+"\n\n")
    f.write("PUNTO 4 — MONTE CARLO\n"+mc_summary.to_string(index=False)+"\n\n")
    f.write("CONVERGENCIA\n"+conv.to_string(index=False)+"\n\n")
    f.write("PUNTO 5 — ROBUSTEZ DE DIFERENCIA DE HUMEDAD\n"+robust_d.to_string(index=False)+"\n\n")
    f.write("PUNTO 5 — ROBUSTEZ DE CORRELACIONES\n"+corr.to_string(index=False)+"\n\n")
    f.write("PUNTO 6 — SÍNTESIS PARA SUMATIVA 3\n"+synthesis.to_string(index=False)+"\n\n")
    f.write("LIMITACIONES\n- Monte Carlo depende de Normal(mu_hat, sd_hat) para diferencias entre localidades comparables.\n- No es un pronóstico meteorológico.\n- Las localidades pueden no ser independientes.\n- El bootstrap por localidad no modela dependencia temporal diaria.\n- Tukey se usa solo como sensibilidad; el análisis principal conserva valores extremos plausibles.\n- Asociación no implica causalidad ni valida por sí sola un predictor.\n")

print("\nPUNTO 4: Monte Carlo")
print(mc_summary.to_string(index=False))
print("\nConvergencia:")
print(conv.to_string(index=False))
print("\nPUNTO 5: Robustez de la diferencia")
print(robust_d.to_string(index=False))
print("\nPUNTO 5: Robustez de correlaciones")
print(corr.to_string(index=False))
print("\nPUNTO 6: Síntesis guardada en", TABLES / "sintesis_resultados_para_s3.csv")
print("Análisis de puntos 4–6 completado.")
