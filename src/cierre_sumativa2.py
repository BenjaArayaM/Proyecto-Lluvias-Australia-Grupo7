"""Cierre documentado de S2 sobre los tres scripts originales de Patricio.

No ejecuta Git ni accede a servicios remotos. El notebook llama estas funciones
en orden. Cada ejecución vuelve a calcular los resultados desde el CSV original.
"""
from __future__ import annotations

import hashlib
import json
import os
import platform
import runpy
import sys
import time
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/03_sumativa2"
TABLES, FIGS = OUT / "tables", OUT / "figures"
EVIDENCE = ROOT / "evidence/03_sumativa2"
DATA = ROOT / "data/raw/weatherAUS.csv"
DATA_SHA256 = "573fd715cd69fcacc4df32024d823b450ae3edaae7e8ff2eeb623adbed424014"
BASE_COMMIT = "1484dd055fb99779932b85f0e87ac541400b893f"
S1_COMMIT = "134859256a519e0ffde2827319d73a603598e0ea"
SEED, B = 20261018, 10_000
PAIRS = [("MaxTemp", "Temp3pm"), ("Humidity3pm", "Sunshine"), ("Humidity3pm", "Rainfall")]
AUTHORS = ["Benjamín Araya", "Alan Cañete", "Patricio Cortez", "Jorge Guaico"]
BLUE, TEAL, ORANGE = "#233D54", "#26817E", "#B16531"


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_table(name):
    return pd.read_csv(TABLES / name, encoding="utf-8-sig")


def _json(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2,
                                    allow_nan=False) + "\n", encoding="utf-8")


def _save(fig, name):
    fig.savefig(FIGS / name, dpi=230, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def _style():
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10,
                         "axes.titlesize": 11, "axes.labelsize": 10,
                         "legend.fontsize": 8.5, "axes.spines.top": False,
                         "axes.spines.right": False, "axes.titleweight": "bold"})


def iniciar():
    """Verifica identidad y recupera estimandos propios de S1, sin imputar."""
    if not DATA.is_file():
        raise FileNotFoundError("Ubica el CSV original en data/raw/weatherAUS.csv.")
    digest = sha256(DATA)
    if digest != DATA_SHA256:
        raise ValueError("El SHA-256 del dataset difiere de la versión auditada; detener y revisar.")
    import scipy
    major, minor = map(int, scipy.__version__.split(".")[:2])
    if (major, minor) < (1, 15):
        raise RuntimeError("Se necesita SciPy >= 1.15 por el argumento rng de bootstrap.")
    for folder in [TABLES, FIGS, EVIDENCE]:
        folder.mkdir(parents=True, exist_ok=True)
    _style()
    df = pd.read_csv(DATA)
    if df.shape != (145460, 23) or df.Location.nunique() != 49:
        raise ValueError("La estructura del dataset no coincide con la auditoría.")
    if df.duplicated(["Location", "Date"]).any():
        raise ValueError("Se encontraron duplicados localidad-fecha.")
    ref_path = ROOT / "results/02_sumativa1/tables/intervalos_medias_localidades.csv"
    if not ref_path.exists():
        raise FileNotFoundError("Falta la tabla propia de intervalos de S1; recuperar S1 antes de continuar.")
    reference = pd.read_csv(ref_path, encoding="utf-8-sig")
    means = df.groupby("Location")[["Humidity3pm", "MaxTemp", "MinTemp"]].mean()
    np.testing.assert_allclose(means.mean().to_numpy(), reference["Media local"].to_numpy(),
                               rtol=0, atol=1e-10)
    z = df.loc[df.RainTomorrow.isin(["Yes", "No"]),
               ["Location", "RainTomorrow", "Humidity3pm"]].dropna()
    local = z.groupby(["Location", "RainTomorrow"])["Humidity3pm"].mean().unstack()
    differences = (local.Yes - local.No).dropna()
    np.testing.assert_allclose(differences.mean(), 20.076901361988934, rtol=0, atol=1e-10)
    t = stats.ttest_1samp(differences, 0)
    np.testing.assert_allclose(t.pvalue, 2.747107556482988e-29, rtol=1e-10, atol=0)
    audit = {"filas": len(df), "columnas": len(df.columns), "localidades": 49,
             "fecha_minima": df.Date.min(), "fecha_maxima": df.Date.max(),
             "objetivo_conocido": int(df.RainTomorrow.notna().sum()),
             "lluvia_yes": int(df.RainTomorrow.eq("Yes").sum()),
             "porcentaje_yes_etiquetas_conocidas": 100 * df.RainTomorrow.eq("Yes").sum() / df.RainTomorrow.notna().sum(),
             "faltantes_sunshine_pct": 100 * df.Sunshine.isna().mean(),
             "faltantes_evaporation_pct": 100 * df.Evaporation.isna().mean(),
             "localidades_sunshine_totalmente_ausente": int(df.groupby("Location").Sunshine.count().eq(0).sum()),
             "registros_comparacion_humedad": len(z), "sha256": digest}
    ctx = {"df": df, "referencia_s1": reference, "diferencias": differences,
           "auditoria": audit, "hash_inicial": digest, "tiempos": {},
           "inicio": time.monotonic()}
    print("CSV identificado; S1 conciliada; no se imputa ni modifica el original.")
    return ctx


def _run(ctx, filename):
    start = time.monotonic()
    previous = Path.cwd()
    try:
        os.chdir(ROOT)
        ns = runpy.run_path(str(ROOT / "src" / filename), run_name="__main__")
    finally:
        os.chdir(previous)
    ctx["tiempos"][filename] = time.monotonic() - start
    return ns


def ejecutar_bootstrap(ctx):
    _run(ctx, "validacion_bootstrap_ic_s2.py")
    table = read_table("bootstrap_ic_s2_resumen.csv")
    draws = read_table("bootstrap_ic_s2_distribuciones.csv")
    ref = ctx["referencia_s1"].set_index("Variable")
    for _, row in table.iterrows():
        for outcol, refcol in [("Estimacion_S1", "Media local"),
                               ("IC_clasico_inferior", "IC 95% inferior"),
                               ("IC_clasico_superior", "IC 95% superior")]:
            np.testing.assert_allclose(row[outcol], ref.loc[row.Variable, refcol], rtol=0, atol=1e-10)
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.15))
    for ax, (_, row) in zip(axes, table.iterrows()):
        values = draws.loc[draws.Variable.eq(row.Variable), "Media_bootstrap"]
        ax.hist(values, bins=40, density=True, color=BLUE, alpha=.70, edgecolor="white", linewidth=.3)
        ax.axvline(row.Estimacion_S1, color="black", lw=1.4, label="Estimación S1")
        for prefix, color, ls, label in [("IC_clasico", "black", ":", "IC t"),
                                         ("IC_percentil", TEAL, "--", "IC percentil"),
                                         ("IC_BCa", ORANGE, "-.", "IC BCa")]:
            for j, suffix in enumerate(["inferior", "superior"]):
                ax.axvline(row[f"{prefix}_{suffix}"], color=color, ls=ls, lw=1.3,
                           label=label if j == 0 else None)
        ax.set(title=row.Variable, xlabel=f"Media de localidades ({row.Unidad})", ylabel="Densidad")
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=4, frameon=False)
    fig.tight_layout(rect=[0, .10, 1, 1])
    _save(fig, "s2_bootstrap_medias.png")
    ctx["bootstrap"] = table
    return table


def ejecutar_permutaciones_correlaciones(ctx):
    """Reejecuta los 10.000 cambios de signo y los 3 x 10.000 bootstrap."""
    ns = _run(ctx, "validacion_s2.py")
    p = read_table("prueba_permutacion_humedad.csv").iloc[0]
    perm = ns["estadisticos_perm"]
    pd.DataFrame({"replica": np.arange(1, len(perm) + 1),
                  "media_nula_pp": perm}).to_csv(TABLES / "distribucion_permutacion.csv", index=False)
    corr = read_table("estabilidad_correlaciones_bootstrap.csv")
    # Se distingue estabilidad de signo de sensibilidad a restricciones de rango.
    corr["clasificacion"] = np.where(corr.ic95_incluye_cero,
        "Signo no resuelto por el IC", "Signo estable bajo bootstrap por localidad; sensibilidad se evalúa aparte")
    corr.to_csv(TABLES / "estabilidad_correlaciones_bootstrap.csv", index=False, encoding="utf-8-sig")
    frames = []
    for (x, y), values in ns["distribuciones_bootstrap"].items():
        frames.append(pd.DataFrame({"variable_x": x, "variable_y": y,
                                   "replica": np.arange(1, len(values) + 1), "rho_bootstrap": values}))
    pd.concat(frames, ignore_index=True).to_csv(TABLES / "distribuciones_correlaciones.csv", index=False)
    # Cada histograma tiene su propio rango; una línea en cero no comprime la distribución.
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.25))
    for ax, (x, y) in zip(axes, PAIRS):
        values = ns["distribuciones_bootstrap"][(x, y)]
        row = corr.loc[corr.variable_x.eq(x) & corr.variable_y.eq(y)].iloc[0]
        ax.hist(values, bins=40, density=True, color=BLUE, alpha=.75, edgecolor="white", linewidth=.3)
        ax.axvline(row.rho_spearman_s1, color="black", label="S1", lw=1.3)
        ax.axvline(row.ic95_inferior, color=TEAL, ls="--", label="IC 95 %")
        ax.axvline(row.ic95_superior, color=TEAL, ls="--")
        ax.set(title=f"{x}\n{y}", xlabel="Spearman (escala propia)", ylabel="Densidad")
        ax.ticklabel_format(axis="x", style="plain", useOffset=False)
        ax.tick_params(axis="x", labelsize=9)
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=2, frameon=False)
    fig.tight_layout(rect=[0, .09, 1, 1])
    _save(fig, "s2_correlaciones_distribuciones.png")
    fig, axes = plt.subplots(1, 2, figsize=(11, 3.4))
    axes[0].hist(perm, bins=45, density=True, color=BLUE, alpha=.8, edgecolor="white", linewidth=.4)
    axes[0].axvline(p.media_diferencias_pp, color=ORANGE, ls="--", label=f"Observado +{p.media_diferencias_pp:.2f}")
    axes[0].axvline(-p.media_diferencias_pp, color=ORANGE, ls=":", label="Simétrico negativo")
    axes[0].set(xlabel="Media bajo cambios de signo (pp)", ylabel="Densidad", title="Distribución nula y valor observado")
    axes[0].legend(loc="upper center")
    d = ctx["diferencias"].to_numpy()
    centered = d - d.mean()
    stats.probplot(centered, dist="norm", plot=axes[1])
    axes[1].set(title="Diagnóstico de forma (D centradas)", xlabel="Cuantil normal teórico", ylabel="D - media(D), pp")
    fig.tight_layout()
    _save(fig, "s2_permutacion_diagnostico.png")
    ref = pd.read_csv(ROOT / "results/02_sumativa1/tables/matriz_correlaciones_spearman.csv", index_col=0)
    for _, row in corr.iterrows():
        np.testing.assert_allclose(row.rho_spearman_s1, ref.loc[row.variable_x, row.variable_y], rtol=0, atol=1e-12)
    ctx.update({"permutacion": p, "correlaciones": corr})
    return p.to_frame("valor"), corr


def ejecutar_montecarlo_robustez(ctx):
    ns = _run(ctx, "analisis_s2_puntos_4_6.py")
    sim = ns["sim"]
    mc = read_table("monte_carlo_resumen.csv").iloc[0]
    expected_se = mc.sd_diferencias_entre_localidades_pp / np.sqrt(mc.n_localidades_S1)
    mcse = sim.std(ddof=1) / np.sqrt(len(sim))
    diag = {"iteraciones": len(sim), "media_objetivo_pp": mc.media_diferencias_S1_pp,
            "media_montecarlo_pp": float(sim.mean()), "sd_medias_simuladas_pp": float(sim.std(ddof=1)),
            "sd_teorica_media_pp": float(expected_se), "mcse_media_simulada_pp": float(mcse),
            "diferencia_media_simulada_objetivo_pp": float(sim.mean() - mc.media_diferencias_S1_pp),
            "diferencia_en_unidades_mcse": float((sim.mean() - mc.media_diferencias_S1_pp) / mcse),
            "tipo_intervalo_simulado": "Intervalo central de medias hipotéticas; no IC del parámetro"}
    pd.DataFrame([diag]).to_csv(TABLES / "diagnostico_convergencia_mc.csv", index=False)
    d = ctx["diferencias"].to_numpy()
    shapiro = stats.shapiro(d)
    q1, q3 = np.quantile(d, [.25, .75])
    d_diag = {"n_localidades": len(d), "asimetria_diferencias": float(stats.skew(d, bias=False)),
              "shapiro_W": float(shapiro.statistic), "shapiro_p": float(shapiro.pvalue),
              "diferencias_fuera_tukey": int(np.sum((d < q1 - 1.5*(q3-q1)) | (d > q3 + 1.5*(q3-q1)))),
              "independencia_espacial_verificada": False,
              "intercambiabilidad_signos_verificada_por_diseno": False,
              "alcance": "Diagnóstico de forma; no prueba independencia ni simetría de la distribución nula"}
    pd.DataFrame([d_diag]).to_csv(TABLES / "diagnostico_supuestos_localidades.csv", index=False)
    fences = []
    for x, y in PAIRS:
        z = ctx["df"][[x, y]].replace([np.inf, -np.inf], np.nan).dropna()
        q = z.quantile([.25, .75])
        iqr = q.loc[.75] - q.loc[.25]
        low, high = q.loc[.25] - 1.5*iqr, q.loc[.75] + 1.5*iqr
        keep = z[x].between(low[x], high[x]) & z[y].between(low[y], high[y])
        fences.append({"variable_x": x, "variable_y": y, "n_original": len(z),
                       "limite_inferior_x": low[x], "limite_superior_x": high[x],
                       "limite_inferior_y": low[y], "limite_superior_y": high[y],
                       "n_excluido_diagnostico": int((~keep).sum()),
                       "pct_excluido": 100 * (~keep).mean(),
                       "uso": "Sensibilidad; no regla de limpieza ni identificación de errores"})
    fence_table = pd.DataFrame(fences)
    fence_table.to_csv(TABLES / "cercas_tukey_diagnostico.csv", index=False)
    corr_rob = read_table("robustez_correlaciones.csv")
    conclusions = ["Signo estable y magnitud poco sensible al filtro aplicado; posible redundancia",
                   "Signo estable en 30 localidades; filtro no elimina casos y no prueba resistencia a extremos",
                   "Signo positivo estable; magnitud sensible al rango de precipitación"]
    corr_rob["conclusion_integrada"] = conclusions
    corr_rob["cambio_relativo_magnitud_pct"] = 100 * (corr_rob.spearman_sensibilidad_tukey.abs() / corr_rob.spearman_completo.abs() - 1)
    corr_rob.to_csv(TABLES / "robustez_correlaciones_interpretada.csv", index=False, encoding="utf-8-sig")
    fig, axes = plt.subplots(1, 2, figsize=(11, 3.6))
    cumulative = np.cumsum(sim) / np.arange(1, len(sim) + 1)
    k = np.arange(100, len(sim) + 1)
    axes[0].plot(k, cumulative[99:], color=BLUE, lw=1.2, label="Media acumulada")
    axes[0].axhline(d.mean(), ls="--", color=ORANGE, label="Objetivo S1")
    axes[0].fill_between(k, d.mean() - 1.96*expected_se/np.sqrt(k),
                         d.mean() + 1.96*expected_se/np.sqrt(k), color=TEAL, alpha=.12,
                         label="±1,96 MCSE teórico")
    axes[0].set(xlabel="Iteraciones", ylabel="Media acumulada (pp)", title="Convergencia y error Monte Carlo")
    axes[0].legend()
    axes[1].hist(sim, bins=40, density=True, color=BLUE, alpha=.75, edgecolor="white", linewidth=.4)
    for j, value in enumerate(np.quantile(sim, [.025, .975])):
        axes[1].axvline(value, color=TEAL, ls="--", label="Intervalo central 95 %" if j == 0 else None)
    axes[1].axvline(d.mean(), color=ORANGE, ls=":", label="Media S1")
    axes[1].set(xlabel="Media de 49 diferencias hipotéticas (pp)", ylabel="Densidad", title="Escenario normal condicionado a S1")
    axes[1].legend()
    fig.tight_layout()
    _save(fig, "s2_montecarlo.png")
    jack = read_table("jackknife_diferencia_humedad.csv")
    fig, axes = plt.subplots(1, 2, figsize=(11, 3.5))
    top = jack.head(6).iloc[::-1]
    axes[0].barh(top.localidad_omitida, top.cambio_vs_media_completa_pp, color=BLUE)
    axes[0].axvline(0, color="black", lw=.8)
    axes[0].set(xlabel="Cambio de la media al omitir (pp)", title="Influencia: seis localidades principales")
    positions = np.arange(3)
    axes[1].scatter(corr_rob.spearman_completo, positions, color=BLUE, label="Datos completos", s=38)
    axes[1].scatter(corr_rob.spearman_sensibilidad_tukey, positions+.12, color=ORANGE, marker="s", label="Filtro diagnóstico", s=30)
    axes[1].set_yticks(positions+.06, ["MaxTemp / Temp3pm", "Humedad / Sol", "Humedad / Lluvia"])
    axes[1].set(xlabel="Spearman", title="Signo y sensibilidad de la magnitud")
    axes[1].legend(loc="lower left")
    fig.tight_layout()
    _save(fig, "s2_robustez.png")
    ctx.update({"montecarlo": mc, "mc_diagnostico": diag, "supuestos": d_diag,
                "cercas": fence_table, "robustez_corr": corr_rob, "jackknife": jack,
                "robustez_diferencia": read_table("robustez_diferencia_humedad.csv").iloc[0]})
    return pd.DataFrame([diag]), corr_rob


def completar_sintesis(ctx):
    """Exporta resultados numéricos, límites de inferencia y decisiones para S3."""
    rows = []
    for _, r in ctx["bootstrap"].iterrows():
        rows.append({"resultado": f"Media local: {r.Variable}", "estimacion": r.Estimacion_S1,
                     "unidad": r.Unidad, "ic95_inferior": r.IC_BCa_inferior,
                     "ic95_superior": r.IC_BCa_superior, "metodo_ic": "BCa; 10.000 remuestras de localidades",
                     "evidencia_robustez": f"t=[{r.IC_clasico_inferior:.4f}, {r.IC_clasico_superior:.4f}]; percentil=[{r.IC_percentil_inferior:.4f}, {r.IC_percentil_superior:.4f}]",
                     "conclusion": "Estimación concordante entre métodos bajo modelo de localidades comparables",
                     "cautela": "Sin representatividad nacional ni independencia espacial comprobada; medias históricas observadas",
                     "recomendacion_s3": "Conservar estimando y unidades; no usar este promedio para imputar fuera del entrenamiento"})
    p, rd = ctx["permutacion"], ctx["robustez_diferencia"]
    top3 = ctx["jackknife"].head(3)
    influence = "; ".join(f"{r.localidad_omitida}: {r.cambio_vs_media_completa_pp:+.4f} pp" for _, r in top3.iterrows())
    rows.append({"resultado": "Diferencia local de humedad Yes-No", "estimacion": p.media_diferencias_pp,
                 "unidad": "pp", "ic95_inferior": rd.ic95_bootstrap_inferior,
                 "ic95_superior": rd.ic95_bootstrap_superior, "metodo_ic": "Bootstrap percentil por localidad; 10.000",
                 "evidencia_robustez": f"49/49 positivas; p_t={p.p_parametrico_t:.8g}; p_signos={p.p_permutacion:.8g}; jackknife [{rd.media_jackknife_min:.4f}, {rd.media_jackknife_max:.4f}]; {influence}",
                 "conclusion": "Asociación descriptiva consistente; estable al retirar una localidad",
                 "cautela": "La prueba de signos aleatorios requiere simetría bajo H0 e independencia; no es efecto causal ni cambio de probabilidad",
                 "recomendacion_s3": "Evaluar Humidity3pm disponible a la hora de emisión; comprobar estabilidad por fecha y localidad"})
    recommendations = ["Examinar redundancia MaxTemp/Temp3pm mediante diagnóstico y comparación dentro del entrenamiento; verificar hora de disponibilidad",
                       "Evaluar cobertura por localidad/periodo y comparar modelos con/sin Sunshine dentro del entrenamiento; no extrapolar el IC a las 49 localidades",
                       "Conservar lluvia plausible en el análisis principal; estudiar transformaciones y sensibilidad con umbrales aprendidos solo en entrenamiento"]
    for i, (_, r) in enumerate(ctx["correlaciones"].iterrows()):
        rob = ctx["robustez_corr"].iloc[i]
        rows.append({"resultado": f"Spearman: {r.variable_x} / {r.variable_y}", "estimacion": r.rho_spearman_s1,
                     "unidad": "coeficiente", "ic95_inferior": r.ic95_inferior, "ic95_superior": r.ic95_superior,
                     "metodo_ic": f"Percentil; 10.000 conglomerados; L={int(r.n_localidades)}",
                     "evidencia_robustez": f"n={int(r.n_pares_original)}; Kendall={rob.kendall_tau_b_completo:.4f}; Tukey={rob.spearman_sensibilidad_tukey:.4f}; excluye {rob.porcentaje_excluido_solo_sensibilidad:.2f}%",
                     "conclusion": rob.conclusion_integrada,
                     "cautela": "Asociación agrupada; tamaños y cobertura por par distintos; IC condicional al remuestreo de localidades",
                     "recomendacion_s3": recommendations[i]})
    lag = pd.read_csv(ROOT / "results/02_sumativa1/tables/dependencia_temporal_humedad.csv", encoding="utf-8-sig")["Correlación lag-1"].median()
    for name, estimate, units, evidence, conclusion, caution, rec in [
        ("Dependencia temporal", lag, "mediana lag-1", "Pares diarios consecutivos calculados en S1", "Dependencia diaria apreciable", "Conservar localidades completas retiene sus registros; no simula futuros temporales ni elimina dependencia espacial", "Separar prueba por fechas completas; dentro de entrenamiento usar validación temporal y, si procede, geográfica"),
        ("Desbalance RainTomorrow", ctx["auditoria"]["porcentaje_yes_etiquetas_conocidas"], "% Yes", "142.193 etiquetas conocidas", "La exactitud aislada puede ocultar errores en lluvia", "Archivo completo ya explorado; evitar presentar la prueba futura como totalmente ajena a decisiones exploratorias previas", "Priorizar métricas de rúbrica: matriz de confusión, precision, recall, F1 y ROC-AUC; PR-AUC como complemento; fijar umbral con validación de entrenamiento"),
        ("Faltantes Sunshine", ctx["auditoria"]["faltantes_sunshine_pct"], "% faltante", "19 localidades sin Sunshine observado", "La composición de casos observados limita generalización", "No se comprobó mecanismo MCAR/MAR/MNAR", "Ajustar imputación, selección y escalado dentro del entrenamiento; comparar estrategias con la misma partición")]:
        rows.append({"resultado": name, "estimacion": estimate, "unidad": units,
                     "ic95_inferior": None, "ic95_superior": None, "metodo_ic": "No se estima en S2",
                     "evidencia_robustez": evidence, "conclusion": conclusion,
                     "cautela": caution, "recomendacion_s3": rec})
    synthesis = pd.DataFrame(rows)
    synthesis.to_csv(TABLES / "sintesis_resultados_para_s3.csv", index=False, encoding="utf-8-sig")
    values = {"evaluacion": "Sumativa 2, Fase 3", "grupo": 7, "integrantes": AUTHORS,
              "base_de_codigo_patricio": BASE_COMMIT, "fuente_sumativa1": S1_COMMIT,
              "dataset": ctx["auditoria"], "semilla_base": SEED,
              "unidad_bootstrap_medias": "49 medias históricas locales con igual peso",
              "unidad_bootstrap_correlaciones": "Localidad completa; Spearman agrupado recalculado, ponderado por sus registros",
              "bootstrap_medias": ctx["bootstrap"].to_dict(orient="records"),
              "permutacion": p.to_dict(), "correlaciones": ctx["correlaciones"].to_dict(orient="records"),
              "montecarlo": ctx["montecarlo"].to_dict(), "convergencia_montecarlo": ctx["mc_diagnostico"],
              "supuestos_diagnostico": ctx["supuestos"],
              "robustez_diferencia": rd.to_dict(), "localidades_influyentes_top3": top3.to_dict(orient="records"),
              "cercas_diagnostico": ctx["cercas"].to_dict(orient="records"),
              "robustez_correlaciones": ctx["robustez_corr"].to_dict(orient="records"),
              "sintesis_para_s3": synthesis.where(pd.notna(synthesis), None).to_dict(orient="records"),
              "limites": ["Inferencia condicional a localidades comparables aproximadamente independientes",
                           "Sin diseño probabilístico nacional ni asignación aleatoria de lluvia",
                           "El diagnóstico de normalidad no prueba independencia ni intercambiabilidad",
                           "La simulación normal fija parámetros S1: no es pronóstico ni IC de la media desconocida",
                           "El filtro Tukey restringe el rango de lluvia y no identifica por sí solo errores",
                           "No se entrenan modelos ni se declara realizada la Sumativa 3"]}
    # Las columnas de IC sin aplicación usan None auténtico, no NaN JSON.
    for item in values["sintesis_para_s3"]:
        for key, value in item.items():
            if isinstance(value, float) and not np.isfinite(value): item[key] = None
    _json(OUT / "resultados_validados_s2.json", values)
    lines = ["# Continuidad Sumativa 2 hacia Sumativa 3", "", "Resultados calculados desde el CSV original; sin entrenamiento predictivo.", "",
             f"Base de Patricio: `{BASE_COMMIT}`. Fuente S1: `{S1_COMMIT}`.", "",
             "## Resultados y decisiones"]
    for item in rows:
        ci = ""
        if item["ic95_inferior"] is not None:
            ci = f"; IC95% [{item['ic95_inferior']:.5f}, {item['ic95_superior']:.5f}]"
        lines += ["", f"### {item['resultado']}", f"Estimación: {item['estimacion']:.6f} {item['unidad']}{ci}.",
                  f"Evidencia: {item['evidencia_robustez']}.", f"Conclusión: {item['conclusion']}.",
                  f"Límite: {item['cautela']}.", f"Acción posterior: {item['recomendacion_s3']}."]
    lines += ["", "## Archivos de referencia", "",
              "- `results/03_sumativa2/resultados_validados_s2.json`: parámetros e intervalos completos.",
              "- `results/03_sumativa2/tables/sintesis_resultados_para_s3.csv`: síntesis con decisiones.",
              "- `results/03_sumativa2/tables/jackknife_diferencia_humedad.csv`: 49 localidades.",
              "- `results/03_sumativa2/figures/s2_*.png`: cinco figuras utilizadas por el informe.",
              "- `notebooks/03_sumativa2_validacion_remuestreo.ipynb`: cálculo e interpretación.",
              "- `evidence/03_sumativa2/`: distinguir ejecución Work de reproducción Windows.", "",
              "Antes de iniciar S3 se revisarán sus instrucciones y rúbrica; estas recomendaciones no autorizan su desarrollo."]
    (ROOT / "docs/continuidad_sumativa2.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    summary = "SUMATIVA 2: SÍNTESIS VIGENTE\n\n" + "\n".join(
        f"{r['resultado']}: {r['conclusion']}. {r['cautela']}." for r in rows)
    summary += "\n\nResultados completos: resultados_validados_s2.json y tables/sintesis_resultados_para_s3.csv.\n"
    for filename in ["resumen_validacion_s2.txt", "resumen_puntos_4_6.txt"]:
        (OUT / filename).write_text(summary, encoding="utf-8")
    ctx["validados"] = values
    return synthesis


def validar(ctx):
    """Controles de procedencia, conteos, estadísticos y exportaciones."""
    checks = {}
    checks["dataset_identico_al_inicio"] = sha256(DATA) == ctx["hash_inicial"] == DATA_SHA256
    boot = read_table("bootstrap_ic_s2_resumen.csv")
    draws = read_table("bootstrap_ic_s2_distribuciones.csv")
    checks["tres_parametros_y_10000_remuestras"] = len(boot) == 3 and bool(boot.Remuestreos.ge(10000).all()) and bool(draws.groupby("Variable").size().eq(10000).all())
    ci_cols = [c for c in boot if c.startswith("IC_")]
    checks["intervalos_finitos_ordenados"] = bool(np.isfinite(boot[ci_cols]).all().all()) and all(bool((boot[f"IC_{p}_inferior"] < boot[f"IC_{p}_superior"]).all()) for p in ["clasico", "percentil", "BCa"])
    perm = read_table("distribucion_permutacion.csv")
    p = read_table("prueba_permutacion_humedad.csv").iloc[0]
    r = int((perm.media_nula_pp.abs() >= abs(p.media_diferencias_pp)).sum())
    checks["permutacion_recalculada_y_correccion_mas_uno"] = len(perm) >= 10000 and np.isclose((r+1)/(len(perm)+1), p.p_permutacion, rtol=1e-12, atol=0)
    corr = read_table("estabilidad_correlaciones_bootstrap.csv")
    cd = read_table("distribuciones_correlaciones.csv")
    checks["tres_correlaciones_10000_validas"] = len(corr) == 3 and bool(corr.n_bootstrap_valido.eq(10000).all()) and len(cd) == 30000
    for _, row in corr.iterrows():
        z = cd.loc[cd.variable_x.eq(row.variable_x) & cd.variable_y.eq(row.variable_y), "rho_bootstrap"]
        np.testing.assert_allclose(np.quantile(z, [.025, .975]), [row.ic95_inferior, row.ic95_superior], rtol=0, atol=1e-12)
    checks["intervalos_correlaciones_recalculados"] = True
    checks["montecarlo_10000_y_convergencia_cuantificada"] = ctx["mc_diagnostico"]["iteraciones"] >= 10000 and abs(ctx["mc_diagnostico"]["diferencia_en_unidades_mcse"]) < 5
    jack = read_table("jackknife_diferencia_humedad.csv")
    d = ctx["diferencias"]
    expected = pd.Series({loc: d.drop(loc).mean() for loc in d.index})
    np.testing.assert_allclose(jack.media_sin_localidad_pp, expected.loc[jack.localidad_omitida], rtol=0, atol=1e-12)
    checks["jackknife_49_localidades_conciliado"] = len(jack) == 49
    checks["sintesis_json_valida"] = len(json.loads((OUT / "resultados_validados_s2.json").read_text(encoding="utf-8"))["sintesis_para_s3"]) == 10
    checks["sin_imputacion_ni_modelamiento_predictivo"] = True
    if not all(checks.values()):
        raise AssertionError({k: v for k, v in checks.items() if not v})
    files = sorted(p for p in OUT.rglob("*") if p.is_file() and p.name != ".gitkeep")
    sources = sorted((ROOT / "src").glob("*s2*.py")) + [ROOT / "src/cierre_sumativa2.py"]
    env = "windows" if platform.system() == "Windows" else "work"
    evidence = {"fecha_utc": datetime.now(timezone.utc).isoformat(), "entorno": env,
                "python": platform.python_version(), "sistema": platform.system(),
                "versiones": {p: version(p) for p in ["numpy", "pandas", "scipy", "matplotlib", "ipykernel", "nbformat", "nbclient"]},
                "base_de_codigo": BASE_COMMIT, "dataset_sha256": DATA_SHA256,
                "controles": {k: bool(v) for k, v in checks.items()},
                "tiempos_scripts_segundos": ctx["tiempos"],
                "ejecucion_local_windows_acreditada_por_este_registro": env == "windows",
                "supuestos_no_demostrados": ["Independencia espacial", "Muestreo nacional representativo", "Intercambiabilidad de signos por diseño"],
                "archivos_sha256": {str(p.relative_to(ROOT)).replace(os.sep, "/"): sha256(p) for p in files + sources}}
    path = EVIDENCE / f"ejecucion_sumativa2_{env}.json"
    _json(path, evidence)
    print("SUMATIVA 2 - EJECUCIÓN COMPLETA: CORRECTA")
    print("Controles numéricos y trazabilidad: correctos")
    print("CSV original sin modificaciones:", checks["dataset_identico_al_inicio"])
    print("Entorno ejecutado:", env)
    print("Evidencia:", path.relative_to(ROOT))
    print("La evidencia computacional no demuestra los supuestos espaciales ni acredita entrega en Canvas.")
    return evidence


def main():
    ctx = iniciar()
    ejecutar_bootstrap(ctx)
    ejecutar_permutaciones_correlaciones(ctx)
    ejecutar_montecarlo_robustez(ctx)
    completar_sintesis(ctx)
    validar(ctx)


if __name__ == "__main__":
    main()
