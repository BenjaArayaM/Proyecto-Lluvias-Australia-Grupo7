"""Actualiza macros numéricas del informe desde resultados validados de S2.

El cuerpo .tex es editable y no se sobrescribe. Con --compilar usa pdfLaTeX
si está instalado. No ejecuta Git ni consulta fuentes remotas.
"""
import argparse
import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports/03_sumativa2"


def fmt(x, digits=4, signed=False):
    return format(float(x), f"{'+' if signed else ''}.{digits}f").replace(".", ",")


def interval(lo, hi, digits=3):
    return f"[{fmt(lo,digits)}; {fmt(hi,digits)}]"


def generar(compilar=False):
    data = json.loads((ROOT / "results/03_sumativa2/resultados_validados_s2.json").read_text(encoding="utf-8"))
    b = {x["Variable"]: x for x in data["bootstrap_medias"]}
    corr = {x["variable_y"]: x for x in data["correlaciones"]}
    rob = {x["variable_y"]: x for x in data["robustez_correlaciones"]}
    p, m, md = data["permutacion"], data["montecarlo"], data["convergencia_montecarlo"]
    d, s = data["robustez_diferencia"], data["supuestos_diagnostico"]
    j = {x["localidad_omitida"]: x for x in data["localidades_influyentes_top3"]}
    f = next(x for x in data["cercas_diagnostico"] if x["variable_y"] == "Rainfall")
    macros = {"PorcentajeLluvia": fmt(data["dataset"]["porcentaje_yes_etiquetas_conocidas"],2),
              "FaltantesSol": fmt(data["dataset"]["faltantes_sunshine_pct"],2),
              "DMedia": fmt(p["media_diferencias_pp"]), "DSd": fmt(m["sd_diferencias_entre_localidades_pp"]),
              "DIntervaloT": interval(p["ic95_t_inferior"],p["ic95_t_superior"]),
              "TValor": fmt(p["estadistico_t"]),
              "PValorSignos": fmt(p["p_permutacion"],8),
              "AsimetriaD": fmt(s["asimetria_diferencias"]), "ShapiroW": fmt(s["shapiro_W"]),
              "ShapiroP": fmt(s["shapiro_p"]), "MediaMC": fmt(m["media_simulada_pp"],5),
              "SdMC": fmt(m["sd_medias_simuladas_pp"],5), "SdTeorica": fmt(md["sd_teorica_media_pp"],5),
              "IntervaloMC": interval(m["p2_5_pp"],m["p97_5_pp"]),
              "ErrorMC": fmt(md["mcse_media_simulada_pp"],5),
              "DiferenciaMC": fmt(md["diferencia_media_simulada_objetivo_pp"],5),
              "ErrorUnidadesMC": fmt(md["diferencia_en_unidades_mcse"],2),
              "DIntervaloBootstrap": interval(d["ic95_bootstrap_inferior"],d["ic95_bootstrap_superior"]),
              "JackMin": fmt(d["media_jackknife_min"]), "JackMax": fmt(d["media_jackknife_max"]),
              "JackAlbany": fmt(j["Albany"]["cambio_vs_media_completa_pp"],4,True),
              "JackAlice": fmt(j["AliceSprings"]["cambio_vs_media_completa_pp"],4,True),
              "JackCobar": fmt(j["Cobar"]["cambio_vs_media_completa_pp"],4,True),
              "JackCambioMax": fmt(d["max_cambio_absoluto_jackknife_pp"]),
              "JackCambioRel": fmt(100*d["max_cambio_absoluto_jackknife_pp"]/p["media_diferencias_pp"],2),
              "RhoLluvia": fmt(corr["Rainfall"]["rho_spearman_s1"]),
              "RhoTemp": fmt(corr["Temp3pm"]["rho_spearman_s1"]),
              "RhoSol": fmt(corr["Sunshine"]["rho_spearman_s1"]),
              "RhoLluviaFiltro": fmt(rob["Rainfall"]["spearman_sensibilidad_tukey"]),
              "CambioRhoLluvia": fmt(rob["Rainfall"]["cambio_spearman"]),
              "ReduccionRhoLluvia": fmt(-rob["Rainfall"]["cambio_relativo_magnitud_pct"],2),
              "ExcluidosLluvia": format(f["n_excluido_diagnostico"],",").replace(",","."),
              "PorcentajeExcluidoLluvia": fmt(f["pct_excluido"],2),
              "CercaLluvia": fmt(f["limite_superior_y"],2)}
    mantissa, exponent = format(p["p_parametrico_t"], ".4e").split("e")
    macros["PValorT"] = mantissa.replace(".", "{,}") + r"\times10^{" + str(int(exponent)) + "}"
    import pandas as pd
    lag = pd.read_csv(ROOT / "results/02_sumativa1/tables/dependencia_temporal_humedad.csv",encoding="utf-8-sig")
    macros["LagMediana"] = fmt(lag["Correlación lag-1"].median())
    convergence = pd.read_csv(ROOT / "results/03_sumativa2/tables/monte_carlo_convergencia.csv").set_index("iteraciones")
    macros["MediaMCmil"] = fmt(convergence.loc[1000,"media_acumulada"],5)
    macros["MediaMCcincomil"] = fmt(convergence.loc[5000,"media_acumulada"],5)
    for variable, suffix in [("Humidity3pm","Hum"),("MaxTemp","Max"),("MinTemp","Min")]:
        r=b[variable]
        macros["CambioPercentil"+suffix] = fmt(100*(r["Ancho_percentil"]/r["Ancho_clasico"]-1),2)
        macros["CambioBca"+suffix] = fmt(100*(r["Ancho_BCa"]/r["Ancho_clasico"]-1),2)
    macros["DesplazaBcaHum"] = fmt(b["Humidity3pm"]["Diferencia_sup_BCa_vs_clasico"],3)
    macros["DesplazaBcaMin"] = fmt(b["MinTemp"]["Diferencia_inf_BCa_vs_clasico"],3,True)
    for variable, suffix in [("Temp3pm","Temp"),("Sunshine","Sol"),("Rainfall","Lluvia")]:
        macros["AnchoCorr"+suffix]=fmt(corr[variable]["amplitud_ic95"])
    rows = []
    names = {"Humidity3pm":r"Humidity3pm (\%)", "MaxTemp":r"MaxTemp ($^{\circ}$C)", "MinTemp":r"MinTemp ($^{\circ}$C)"}
    for variable in ["Humidity3pm","MaxTemp","MinTemp"]:
        r=b[variable]
        rows.append(names[variable]+" & "+fmt(r["Estimacion_S1"],3)+" & "+" & ".join(interval(r[f"IC_{prefix}_inferior"],r[f"IC_{prefix}_superior"]) for prefix in ["clasico","percentil","BCa"])+r"\\")
    macros["TablaBootstrap"] = (r"\begin{tabular}{@{}lrrrr@{}}\toprule Variable & Media S1 & IC t & IC percentil & IC BCa\\\midrule"+"\n"+"\n".join(rows)+"\n"+r"\bottomrule\end{tabular}")
    rows=[]
    for r in data["correlaciones"]:
        name={"Temp3pm":"MaxTemp / Temp3pm", "Sunshine":"Humedad / Sunshine", "Rainfall":"Humedad / Rainfall"}[r["variable_y"]]
        n=format(r["n_pares_original"],",").replace(",",".")
        rows.append(f"{name} & {n} & {r['n_localidades']} & {fmt(r['rho_spearman_s1'])} & {interval(r['ic95_inferior'],r['ic95_superior'],4)}"+r"\\")
    macros["TablaCorrelaciones"]=(r"\begin{tabular}{@{}lrrrr@{}}\toprule Par & $n$ pares & Localidades & $\rho$ S1 & IC bootstrap\\\midrule"+"\n"+"\n".join(rows)+"\n"+r"\bottomrule\end{tabular}")
    rows=[]
    for r in data["robustez_correlaciones"]:
        name={"Temp3pm":"MaxTemp / Temp3pm", "Sunshine":"Humedad / Sunshine", "Rainfall":"Humedad / Rainfall"}[r["variable_y"]]
        vals=[fmt(r[k]) for k in ["spearman_completo","kendall_tau_b_completo","spearman_sensibilidad_tukey"]]
        rows.append(name+" & "+" & ".join(vals)+" & "+fmt(r["porcentaje_excluido_solo_sensibilidad"],2)+r"\,\%\\")
    macros["TablaRobustez"]=(r"\begin{tabular}{@{}lrrrr@{}}\toprule Par & Spearman & Kendall $\tau_b$ & Spearman filtro & Excluidos\\\midrule"+"\n"+"\n".join(rows)+"\n"+r"\bottomrule\end{tabular}")
    REPORT.mkdir(parents=True,exist_ok=True)
    target=REPORT/"datos_sumativa2.tex"
    target.write_text("% Generado desde resultados_validados_s2.json; no editar cifras a mano.\n"+
        "\n".join("\\newcommand{\\"+key+"}{"+value+"}" for key,value in macros.items())+"\n",encoding="utf-8")
    if compilar:
        executable=shutil.which("pdflatex")
        if executable is None:
            raise RuntimeError("pdfLaTeX no está instalado. Las fuentes pueden compilarse en Overleaf con la estructura indicada en docs/reproduccion_sumativa2.md.")
        for _ in range(2):
            p=subprocess.run([executable,"-interaction=nonstopmode","-halt-on-error","-file-line-error",
                              "informe_sumativa2_grupo7.tex"],cwd=REPORT,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
            if p.returncode:
                raise RuntimeError(p.stdout[-6000:])
        print("PDF compilado:", REPORT/"informe_sumativa2_grupo7.pdf")
    print("Macros numéricas actualizadas:",target)
    return target


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--compilar",action="store_true")
    args=parser.parse_args()
    generar(args.compilar)
