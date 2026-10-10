"""Formativa 1 de MCDI501: auditoría, descripción e inferencia por localidad.

El CSV se lee sin modificarlo. Las exclusiones son específicas de cada cálculo.
Los intervalos t son aproximaciones bajo un modelo de localidades comparables;
no establecen representatividad nacional ni independencia espacial.
"""
from __future__ import annotations

import hashlib
import json
import platform
import sys
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

SHA256_ESPERADO = "573fd715cd69fcacc4df32024d823b450ae3edaae7e8ff2eeb623adbed424014"
COLUMNAS = [
    "Date", "Location", "MinTemp", "MaxTemp", "Rainfall", "Evaporation",
    "Sunshine", "WindGustDir", "WindGustSpeed", "WindDir9am", "WindDir3pm",
    "WindSpeed9am", "WindSpeed3pm", "Humidity9am", "Humidity3pm", "Pressure9am",
    "Pressure3pm", "Cloud9am", "Cloud3pm", "Temp9am", "Temp3pm", "RainToday",
    "RainTomorrow",
]
NUMERICAS = [v for v in COLUMNAS if v not in (
    "Date", "Location", "WindGustDir", "WindDir9am", "WindDir3pm",
    "RainToday", "RainTomorrow")]
VARIABLES_IC = ["Humidity3pm", "MaxTemp", "MinTemp"]
ALFA = 0.05
SEMILLA = 50107  # Reservada; los cálculos de esta formativa son deterministas.
AZUL, NARANJA, GRIS = "#235789", "#CE6C39", "#64748B"

DEFINICIONES = {
    "Date": ("Temporal", "Fecha", "Fecha del registro", "Orden temporal; no es una medida continua meteorológica"),
    "Location": ("Cualitativa nominal", "Localidad", "Nombre de la localidad de observación", "Agrupación geográfica"),
    "MinTemp": ("Cuantitativa continua", "°C", "Temperatura mínima", "Descripción; disponibilidad depende del corte de predicción"),
    "MaxTemp": ("Cuantitativa continua", "°C", "Temperatura máxima", "Descripción; disponibilidad depende del corte de predicción"),
    "Rainfall": ("Cuantitativa continua", "mm", "Precipitación registrada", "Acumulación meteorológica; comprobar ventana temporal"),
    "Evaporation": ("Cuantitativa continua", "mm", "Evaporación de tanque Clase A", "Acumulación hasta las 9 am según Rattle"),
    "Sunshine": ("Cuantitativa continua", "h", "Horas de sol intenso", "Total diario; no se supone disponible a las 3 pm"),
    "WindGustDir": ("Cualitativa nominal circular", "16 direcciones", "Dirección de la ráfaga más intensa", "Dirección circular; el máximo diario no se supone disponible a las 3 pm"),
    "WindGustSpeed": ("Cuantitativa continua", "km/h", "Velocidad de la ráfaga máxima", "Máximo hasta medianoche según Rattle"),
    "WindDir9am": ("Cualitativa nominal circular", "16 direcciones", "Dirección del viento a las 9 am", "Medición de la mañana"),
    "WindDir3pm": ("Cualitativa nominal circular", "16 direcciones", "Dirección del viento a las 3 pm", "Medición de la tarde"),
    "WindSpeed9am": ("Cuantitativa continua", "km/h", "Velocidad del viento a las 9 am", "Medición de la mañana"),
    "WindSpeed3pm": ("Cuantitativa continua", "km/h", "Velocidad del viento a las 3 pm", "Medición de la tarde"),
    "Humidity9am": ("Cuantitativa continua", "%", "Humedad relativa a las 9 am", "Rango físico de 0 a 100"),
    "Humidity3pm": ("Cuantitativa continua", "%", "Humedad relativa a las 3 pm", "Variable principal de la comparación exploratoria"),
    "Pressure9am": ("Cuantitativa continua", "hPa", "Presión al nivel del mar a las 9 am", "Medición de la mañana"),
    "Pressure3pm": ("Cuantitativa continua", "hPa", "Presión al nivel del mar a las 3 pm", "Medición de la tarde"),
    "Cloud9am": ("Cuantitativa discreta codificada", "Octas y código", "Nubosidad a las 9 am", "0 a 8 octas; revisar significado del código 9"),
    "Cloud3pm": ("Cuantitativa discreta codificada", "Octas y código", "Nubosidad a las 3 pm", "0 a 8 octas; revisar significado del código 9"),
    "Temp9am": ("Cuantitativa continua", "°C", "Temperatura a las 9 am", "Medición de la mañana"),
    "Temp3pm": ("Cuantitativa continua", "°C", "Temperatura a las 3 pm", "Medición de la tarde"),
    "RainToday": ("Cualitativa nominal binaria", "No / Yes", "Lluvia en el día del registro", "Etiqueta observada; contrastada con Rainfall > 1 mm"),
    "RainTomorrow": ("Cualitativa nominal binaria", "No / Yes", "Lluvia al día siguiente", "Objetivo; nunca un predictor del mismo día"),
}


def huella(archivo: Path) -> str:
    """Calcular SHA-256 sin cargar el archivo completo en memoria."""
    h = hashlib.sha256()
    with archivo.open("rb") as f:
        for bloque in iter(lambda: f.read(1024 * 1024), b""):
            h.update(bloque)
    return h.hexdigest()


def cargar_datos(raiz: Path):
    archivo = raiz / "data/raw/weatherAUS.csv"
    if not archivo.is_file():
        raise FileNotFoundError(f"No se encontró {archivo}. Conserva el CSV original en data/raw/.")
    sha = huella(archivo)
    if sha != SHA256_ESPERADO:
        raise ValueError("El SHA-256 del CSV difiere de la copia auditada. Revisar la versión antes de continuar.")
    original = pd.read_csv(archivo)
    if original.shape != (145460, 23) or original.columns.tolist() != COLUMNAS:
        raise ValueError("Dimensiones o columnas diferentes de la versión verificada.")
    if not set(original.RainTomorrow.dropna().unique()).issubset({"No", "Yes"}):
        raise ValueError("Se encontraron etiquetas de RainTomorrow no previstas.")
    datos = original.copy(deep=True)
    datos["Date"] = pd.to_datetime(datos["Date"], format="%Y-%m-%d", errors="coerce")
    if datos.Date.isna().any():
        raise ValueError("Hay fechas no interpretables; deben revisarse antes de analizar.")
    datos["Mes"] = datos.Date.dt.month
    datos["Anio"] = datos.Date.dt.year
    datos["EstacionAustral"] = datos.Mes.map({
        12: "Verano", 1: "Verano", 2: "Verano", 3: "Otoño", 4: "Otoño", 5: "Otoño",
        6: "Invierno", 7: "Invierno", 8: "Invierno", 9: "Primavera", 10: "Primavera", 11: "Primavera",
    })
    return original, datos, {"archivo": "data/raw/weatherAUS.csv", "sha256": sha,
        "bytes": archivo.stat().st_size, "filas": len(original), "columnas": len(original.columns)}


def diccionario(original: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame([{"variable": v, "dtype_csv": str(original[v].dtype),
        "tipo_estadistico": DEFINICIONES[v][0], "unidad": DEFINICIONES[v][1],
        "definicion": DEFINICIONES[v][2], "papel_y_disponibilidad": DEFINICIONES[v][3],
        "n_validos": int(original[v].notna().sum()), "n_faltantes": int(original[v].isna().sum())}
        for v in COLUMNAS])


def estadistica_descriptiva(original: pd.DataFrame) -> pd.DataFrame:
    filas = []
    for v in NUMERICAS:
        x = original[v].dropna()
        q1, med, q3 = x.quantile([.25, .5, .75]).tolist()
        iqr = q3 - q1
        modas = x.mode()
        filas.append({"variable": v, "unidad": DEFINICIONES[v][1], "n": len(x),
            "faltantes": len(original)-len(x), "media": x.mean(), "mediana": med,
            "moda": modas.iloc[0] if len(modas) else np.nan, "n_modas": len(modas),
            "desviacion_estandar": x.std(ddof=1), "varianza": x.var(ddof=1),
            "minimo": x.min(), "q1": q1, "q3": q3, "maximo": x.max(),
            "rango": x.max()-x.min(), "iqr": iqr, "p99": x.quantile(.99),
            "asimetria": x.skew(), "fuera_tukey": int(((x < q1-1.5*iqr) | (x > q3+1.5*iqr)).sum())})
    return pd.DataFrame(filas)


def frecuencias_categoricas(original: pd.DataFrame) -> pd.DataFrame:
    filas = []
    for v in ["Location", "WindGustDir", "WindDir9am", "WindDir3pm", "RainToday", "RainTomorrow", "Cloud9am", "Cloud3pm"]:
        n_validos = int(original[v].notna().sum())
        for categoria, n in original[v].value_counts(dropna=False).items():
            falta = bool(pd.isna(categoria))
            filas.append({"variable": v, "categoria": "Faltante" if falta else str(categoria),
                "n": int(n), "porcentaje_total": 100*n/len(original),
                "porcentaje_validos": np.nan if falta else 100*n/n_validos})
    return pd.DataFrame(filas)


def calidad_y_cobertura(original: pd.DataFrame, datos: pd.DataFrame):
    faltantes = pd.DataFrame({"variable": COLUMNAS,
        "n_faltantes": original.isna().sum().reindex(COLUMNAS).values,
        "porcentaje": original.isna().mean().reindex(COLUMNAS).values*100})
    cobertura = datos.groupby("Location", sort=True).agg(
        n_registros=("Date", "size"), fecha_inicio=("Date", "min"), fecha_fin=("Date", "max"),
        n_objetivo=("RainTomorrow", "count"))
    cobertura["n_yes"] = datos.RainTomorrow.eq("Yes").groupby(datos.Location).sum()
    cobertura["porcentaje_yes_validos"] = cobertura.n_yes/cobertura.n_objetivo*100
    cobertura["dias_entre_extremos"] = (cobertura.fecha_fin-cobertura.fecha_inicio).dt.days+1
    cobertura["cobertura_fechas_pct"] = cobertura.n_registros/cobertura.dias_entre_extremos*100
    falt_loc = datos.groupby("Location")[NUMERICAS+["RainTomorrow"]].agg(lambda s: s.isna().mean()*100)
    cobertura = cobertura.reset_index()
    falt_loc = falt_loc.reset_index()
    ordenados = datos.sort_values(["Location", "Date"]).copy()
    salto = ordenados.groupby("Location").Date.diff().dt.days
    checks = [
        ("Duplicados exactos", int(original.duplicated().sum()), "Duplicados de las 23 columnas"),
        ("Duplicados localidad fecha", int(original.duplicated(["Location", "Date"]).sum()), "Clave de observación"),
        ("Fechas inválidas", int(datos.Date.isna().sum()), "Interpretación YYYY-MM-DD"),
        ("Mínima mayor que máxima", int((datos.MinTemp > datos.MaxTemp).sum()), "Solo pares observados"),
        ("Humedad fuera de 0 a 100", int(sum(((datos[v]<0)|(datos[v]>100)).sum() for v in ["Humidity9am", "Humidity3pm"])), "Solo valores observados"),
        ("Precipitación negativa", int((datos.Rainfall < 0).sum()), "Valor físico negativo"),
        ("Evaporación negativa", int((datos.Evaporation < 0).sum()), "Valor físico negativo"),
        ("Sol fuera de 0 a 24 horas", int(((datos.Sunshine<0)|(datos.Sunshine>24)).sum()), "Cota física general"),
        ("Velocidad de viento negativa", int(sum((datos[v]<0).sum() for v in ["WindGustSpeed", "WindSpeed9am", "WindSpeed3pm"])), "Valor físico negativo"),
        ("Cloud9am código 9", int(datos.Cloud9am.eq(9).sum()), "Posible código de niebla; no se elimina"),
        ("Cloud3pm código 9", int(datos.Cloud3pm.eq(9).sum()), "Posible código de niebla; no se elimina"),
        ("Saltos de más de un día", int((salto>1).sum()), "No interpolar fechas ausentes"),
    ]
    for v in ["WindGustDir", "WindDir9am", "WindDir3pm"]:
        validos = {"N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"}
        checks.append((f"Direcciones imprevistas {v}", int((datos[v].notna() & ~datos[v].isin(validos)).sum()), "Categorías de la rosa de 16 direcciones"))
    conocidos = datos.Rainfall.notna() & datos.RainToday.notna()
    clasif = datos.loc[conocidos, "Rainfall"].gt(1).map({True:"Yes", False:"No"})
    checks.append(("RainToday frente a Rainfall > 1", int((clasif != datos.loc[conocidos, "RainToday"]).sum()), f"Pares contrastados: {int(conocidos.sum())}"))
    siguiente = datos[["Location", "Date", "RainToday", "Rainfall"]].copy()
    siguiente["Date"] = siguiente.Date-pd.Timedelta(days=1)
    siguiente = siguiente.rename(columns={"RainToday":"RainToday_siguiente", "Rainfall":"Rainfall_siguiente"})
    pares = datos[["Location", "Date", "RainTomorrow"]].merge(siguiente, on=["Location", "Date"], how="inner", validate="one_to_one")
    p = pares.dropna(subset=["RainTomorrow", "RainToday_siguiente"])
    checks.append(("Objetivo frente a RainToday siguiente", int((p.RainTomorrow != p.RainToday_siguiente).sum()), f"Días consecutivos contrastados: {len(p)}"))
    p = pares.dropna(subset=["RainTomorrow", "Rainfall_siguiente"])
    esperado = p.Rainfall_siguiente.gt(1).map({True:"Yes", False:"No"})
    checks.append(("Objetivo frente a Rainfall siguiente > 1", int((p.RainTomorrow != esperado).sum()), f"Días consecutivos contrastados: {len(p)}"))
    # Estos valores del día siguiente se usan exclusivamente para esta auditoría.
    # No se añaden al dataframe de análisis ni se convierten en predictores.
    return faltantes, cobertura, falt_loc, pd.DataFrame(checks, columns=["comprobacion", "n", "alcance"])


def descriptivos_objetivo(datos: pd.DataFrame) -> pd.DataFrame:
    n = len(datos)
    n_validos = int(datos.RainTomorrow.notna().sum())
    return pd.DataFrame([{"clase": c, "n": int((datos.RainTomorrow.eq(c) if c != "Faltante" else datos.RainTomorrow.isna()).sum()),
        "denominador_total": n, "denominador_validos": n_validos,
        "porcentaje_total": 100*(datos.RainTomorrow.eq(c) if c != "Faltante" else datos.RainTomorrow.isna()).sum()/n,
        "porcentaje_validos": np.nan if c == "Faltante" else 100*datos.RainTomorrow.eq(c).sum()/n_validos}
        for c in ["No", "Yes", "Faltante"]])


def exploracion_bivariada(datos: pd.DataFrame):
    variables = ["Humidity3pm", "Pressure3pm", "MaxTemp", "Rainfall", "Sunshine"]
    filas = []
    for v in variables:
        for clase in ["No", "Yes"]:
            x = datos.loc[datos.RainTomorrow.eq(clase), v].dropna()
            filas.append({"variable":v, "clase":clase, "n":len(x), "media":x.mean(),
                "mediana":x.median(), "desviacion_estandar":x.std(ddof=1),
                "q1":x.quantile(.25), "q3":x.quantile(.75)})
    binarias = datos.RainTomorrow.map({"No":0, "Yes":1})
    filas_corr = []
    for v in NUMERICAS:
        x = datos[v]
        if v.startswith("Cloud"):
            x = x.where(x.between(0, 8))  # Vista temporal; no recodifica el CSV.
        par = pd.DataFrame({"x": x, "y": binarias}).dropna()
        filas_corr.append({"variable":v, "n_pares":len(par),
            "spearman_objetivo":par.x.corr(par.y, method="spearman")})
    matriz_vars = ["MinTemp", "MaxTemp", "Temp3pm", "Humidity3pm", "Pressure3pm", "Rainfall", "Sunshine"]
    matriz = datos[matriz_vars].corr(method="spearman")
    presentes = datos[matriz_vars].notna().astype("int64")
    n_pares = presentes.T.dot(presentes)
    return pd.DataFrame(filas), pd.DataFrame(filas_corr), matriz, n_pares


def patrones_temporales(datos: pd.DataFrame):
    conocido = datos.loc[datos.RainTomorrow.notna()].copy()
    conocido["lluvia"] = conocido.RainTomorrow.eq("Yes").astype("int8")
    mensual = conocido.groupby(["Location", "Mes"]).lluvia.agg(["size", "sum", "mean"]).reset_index()
    mensual = mensual.rename(columns={"size":"n", "sum":"n_yes", "mean":"proporcion_yes"})
    estacional = conocido.groupby("EstacionAustral").lluvia.agg(["size", "sum", "mean"]).reindex(["Verano", "Otoño", "Invierno", "Primavera"]).reset_index()
    estacional = estacional.rename(columns={"size":"n", "sum":"n_yes", "mean":"proporcion_yes"})
    anuales = datos.groupby("Anio").agg(n=("Date", "size"), n_localidades=("Location", "nunique")).reset_index()
    filas = []
    for loc, d in datos.groupby("Location", sort=True):
        d = d.sort_values("Date")
        actual = d.Humidity3pm
        anterior = actual.shift(1)
        mascara = d.Date.diff().dt.days.eq(1) & actual.notna() & anterior.notna()
        filas.append({"Location":loc, "n_pares_consecutivos":int(mascara.sum()),
            "correlacion_lag1_humedad":actual.loc[mascara].corr(anterior.loc[mascara])})
    return mensual, estacional, anuales, pd.DataFrame(filas)


def intervalo_t(x, nivel=0.95):
    x = np.asarray(x, dtype=float)
    if len(x) < 3 or not np.isfinite(x).all():
        raise ValueError("El intervalo requiere al menos tres unidades completas y finitas.")
    n, media = len(x), float(np.mean(x))
    sd = float(np.std(x, ddof=1))
    se = sd / np.sqrt(n)
    critico = float(stats.t.ppf((1+nivel)/2, df=n-1))
    return {"n_localidades":n, "media_localidades":media, "sd_localidades":sd,
        "error_estandar":se, "gl":n-1, "nivel":nivel,
        "t_critico":critico, "ic_inferior":media-critico*se, "ic_superior":media+critico*se}


def inferencia_localidades(datos: pd.DataFrame):
    medias = datos.groupby("Location", sort=True)[VARIABLES_IC].mean()
    conteos = datos.groupby("Location", sort=True)[VARIABLES_IC].count()
    filas = []
    for v in VARIABLES_IC:
        z = medias[v].dropna()
        r = intervalo_t(z)
        sh = stats.shapiro(z)
        q1, q3 = z.quantile([.25, .75])
        filas.append({"variable":v, "unidad":DEFINICIONES[v][1],
            "n_registros_validos":int(datos[v].notna().sum()),
            "media_agrupada_registros":float(datos[v].mean()), **r,
            "shapiro_w":float(sh.statistic), "shapiro_p":float(sh.pvalue),
            "localidades_fuera_tukey":int(((z<q1-1.5*(q3-q1)) | (z>q3+1.5*(q3-q1))).sum())})
    resumen = pd.DataFrame(filas)
    medias = medias.add_suffix("_media").join(conteos.add_suffix("_n")).reset_index()
    valido = datos.RainTomorrow.isin(["No", "Yes"]) & datos.Humidity3pm.notna()
    analisis = datos.loc[valido, ["Location", "RainTomorrow", "Humidity3pm"]]
    medias_grupo = analisis.groupby(["Location", "RainTomorrow"]).Humidity3pm.mean().unstack().reindex(columns=["No", "Yes"])
    n_grupo = analisis.groupby(["Location", "RainTomorrow"]).Humidity3pm.count().unstack().reindex(columns=["No", "Yes"])
    parejas = medias_grupo.dropna().copy()
    parejas["diferencia_pp"] = parejas.Yes-parejas.No
    parejas["n_no"] = n_grupo.loc[parejas.index, "No"]
    parejas["n_yes"] = n_grupo.loc[parejas.index, "Yes"]
    dif = parejas.diferencia_pp
    t = stats.ttest_1samp(dif.to_numpy(), popmean=0, alternative="two-sided")
    ci = intervalo_t(dif)
    sh = stats.shapiro(dif)
    q1, q3 = dif.quantile([.25, .75])
    prueba = {"variable":"Humidity3pm", "unidad_efecto":"puntos porcentuales",
        "unidad_inferencia":"localidad", "h0":"mu_D = 0", "h1":"mu_D != 0",
        "alfa":ALFA, "alternativa":"bilateral", "n_registros":len(analisis),
        "n_excluidos":len(datos)-len(analisis), **ci,
        "t":float(t.statistic), "p":float(t.pvalue),
        "rechazo_condicional":bool(t.pvalue < ALFA),
        "shapiro_w":float(sh.statistic), "shapiro_p":float(sh.pvalue),
        "d_z":float(dif.mean()/dif.std(ddof=1)),
        "media_no_igual_peso_localidades":float(parejas.No.mean()),
        "media_yes_igual_peso_localidades":float(parejas.Yes.mean()),
        "n_diferencias_positivas":int(dif.gt(0).sum()),
        "min_diferencia":float(dif.min()), "min_localidad":str(dif.idxmin()),
        "max_diferencia":float(dif.max()), "max_localidad":str(dif.idxmax()),
        "min_n_no":int(parejas.n_no.min()), "min_n_yes":int(parejas.n_yes.min()),
        "localidades_fuera_tukey":int(((dif<q1-1.5*(q3-q1)) | (dif>q3+1.5*(q3-q1))).sum()),
        "limitacion":"Inferencia exploratoria condicional a independencia aproximada entre localidades y al mecanismo de observación. No se valida independencia espacial ni representatividad nacional."}
    # Verificación independiente de la fórmula y del IC de SciPy.
    np.testing.assert_allclose(prueba["t"], dif.mean()/(dif.std(ddof=1)/np.sqrt(len(dif))), rtol=1e-12)
    ci_scipy = t.confidence_interval(confidence_level=.95)
    np.testing.assert_allclose([prueba["ic_inferior"], prueba["ic_superior"]], [ci_scipy.low, ci_scipy.high], rtol=1e-12)
    return resumen, medias, parejas.reset_index(), prueba


def guardar_csv(df: pd.DataFrame, ruta: Path, index=False):
    ruta.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(ruta, index=index, encoding="utf-8-sig", float_format="%.15g")


def generar_figuras(datos: pd.DataFrame, tablas: dict, ruta: Path):
    ruta.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.family":"DejaVu Sans", "font.size":10,
        "axes.spines.top":False, "axes.spines.right":False,
        "figure.dpi":110, "savefig.dpi":180})
    figuras = {}
    def guardar(fig, nombre):
        fig.savefig(ruta/nombre, bbox_inches="tight", facecolor="white")
        plt.close(fig)
        figuras[nombre] = str((ruta/nombre).name)
    obj = tablas["objetivo"]
    fig, ax = plt.subplots(1, 2, figsize=(10.5, 5.8), gridspec_kw={"width_ratios":[.9, 1.5]}, layout="constrained")
    ax[0].bar(["No", "Yes"], obj.loc[:1,"porcentaje_validos"], color=[AZUL,NARANJA])
    for i,r in obj.iloc[:2].iterrows():
        ax[0].text(i, r.porcentaje_validos+1.5, f"{r.porcentaje_validos:.2f}%\nn={int(r.n):,}", ha="center", fontsize=10)
    ax[0].set(ylim=(0,95), ylabel="Porcentaje de etiquetas observadas", title="RainTomorrow")
    ax[0].text(.5,-.17,f"Denominador: {int(obj.denominador_validos.iloc[0]):,}\nFaltantes: {int(obj.n.iloc[2]):,} (excluidos del porcentaje)", transform=ax[0].transAxes, ha="center", fontsize=9)
    f = tablas["faltantes"].sort_values("porcentaje").query("n_faltantes > 0")
    ax[1].barh(f.variable, f.porcentaje, color=AZUL)
    for i, v in enumerate(f.porcentaje):
        ax[1].text(v+.4,i,f"{v:.1f}", va="center", fontsize=8)
    ax[1].set(xlabel="Faltantes (% de 145 460 registros)", xlim=(0,55), title="Disponibilidad por variable")
    ax[1].tick_params(axis="y",labelsize=8)
    guardar(fig,"01_objetivo_faltantes.png")
    fig, ax = plt.subplots(2,2,figsize=(10,6.5),layout="constrained")
    for a, v, unidad in zip(ax.flat[:3], ["MinTemp","MaxTemp","Humidity3pm"], ["°C","°C","%"]):
        x = datos[v].dropna()
        a.hist(x,bins=35,color=AZUL,edgecolor="white",linewidth=.25)
        a.axvline(x.mean(),color=NARANJA,lw=1.5,label=f"Media {x.mean():.2f}")
        a.axvline(x.median(),color="#1E293B",ls="--",lw=1,label=f"Mediana {x.median():.2f}")
        a.set(xlabel=f"{v} ({unidad})",ylabel="Registros",title=f"n={len(x):,}")
        a.legend(fontsize=8)
    x=datos.Rainfall.dropna()
    ax[1,1].hist(np.log1p(x),bins=40,color=AZUL,edgecolor="white",linewidth=.25)
    ticks=np.array([0,1,5,20,100,371])
    ax[1,1].set(xticks=np.log1p(ticks),xticklabels=[str(i) for i in ticks],xlabel="Rainfall (mm; eje log(1+x))",ylabel="Registros",title=f"n={len(x):,}; ceros={(x==0).mean()*100:.1f}%")
    guardar(fig,"02_distribuciones.png")
    fig, ax=plt.subplots(1,2,figsize=(10,4.0),layout="constrained")
    for a,v,u in zip(ax,["Humidity3pm","Pressure3pm"],["%","hPa"]):
        grupos=[datos.loc[datos.RainTomorrow.eq(c),v].dropna() for c in ["No","Yes"]]
        b=a.boxplot(grupos, tick_labels=[f"No\nn={len(grupos[0]):,}",f"Yes\nn={len(grupos[1]):,}"],patch_artist=True,showfliers=False)
        for caja,color in zip(b["boxes"],[AZUL,NARANJA]): caja.set_facecolor(color); caja.set_alpha(.75)
        a.set(xlabel="RainTomorrow",ylabel=f"{v} ({u})",title="Valores observados por clase")
    guardar(fig,"03_relaciones_objetivo.png")
    mat=tablas["matriz_correlacion"]
    fig,ax=plt.subplots(figsize=(7.2,6.0),layout="constrained")
    im=ax.imshow(mat,vmin=-1,vmax=1,cmap="RdBu_r")
    ax.set(xticks=range(len(mat)),yticks=range(len(mat)),xticklabels=mat.columns,yticklabels=mat.index,title="Correlación de Spearman entre variables observadas")
    plt.setp(ax.get_xticklabels(),rotation=45,ha="right",fontsize=9)
    for i in range(len(mat)):
        for j in range(len(mat)):
            v=mat.iloc[i,j]
            ax.text(j,i,f"{v:.2f}",ha="center",va="center",fontsize=9,color="white" if abs(v)>.65 else "black")
    fig.colorbar(im,ax=ax,label="rho; eliminación por pares")
    guardar(fig,"04_correlaciones.png")
    mensual=tablas["mensual_localidad"]
    cobertura=tablas["cobertura_localidad"]
    fig,ax=plt.subplots(1,2,figsize=(10,4.2),layout="constrained")
    colors=[AZUL,NARANJA,"#27826D","#7851A9"]
    for loc,col in zip(["Darwin","Perth","Sydney","Hobart"],colors):
        d=mensual.loc[mensual.Location.eq(loc)].sort_values("Mes")
        ax[0].plot(d.Mes,d.proporcion_yes*100,marker="o",markersize=3,label=loc,color=col)
    ax[0].set(xticks=range(1,13),xlabel="Mes del registro (1=enero)",ylabel="RainTomorrow = Yes (%)",title="Cuatro localidades de referencia")
    ax[0].legend(fontsize=8,ncol=2)
    c=cobertura.sort_values("porcentaje_yes_validos")
    extremos=pd.concat([c.head(4),c.tail(4)])
    ax[1].barh(extremos.Location,extremos.porcentaje_yes_validos,color=AZUL)
    ax[1].set(xlabel="Yes entre etiquetas conocidas (%)",title="Extremos geográficos observados")
    guardar(fig,"05_geografia_estacionalidad.png")
    med=tablas["medias_localidad"].set_index("Location")
    dif=tablas["diferencias_localidad"].diferencia_pp
    fig,ax=plt.subplots(2,2,figsize=(9.5,6.8),layout="constrained")
    for a,v in zip(ax.flat[:3],VARIABLES_IC):
        stats.probplot(med[v+"_media"],dist="norm",plot=a)
        a.set(title=f"Q-Q de medias locales: {v}",xlabel="Cuantil normal teórico",ylabel=DEFINICIONES[v][1])
    stats.probplot(dif,dist="norm",plot=ax[1,1])
    ax[1,1].set(title="Q-Q de diferencias locales de humedad",xlabel="Cuantil normal teórico",ylabel="Diferencia (puntos porcentuales)")
    guardar(fig,"06_diagnostico_normalidad.png")
    d=tablas["diferencias_localidad"].sort_values("diferencia_pp")
    fig,ax=plt.subplots(figsize=(8,10),layout="constrained")
    ax.scatter(d.diferencia_pp,np.arange(len(d)),s=18,color=AZUL)
    ax.axvline(0,color=GRIS,lw=1)
    ax.axvline(d.diferencia_pp.mean(),color=NARANJA,ls="--",label="Media con igual peso por localidad")
    ax.set(yticks=range(len(d)),yticklabels=d.Location,xlabel="Humedad media con Yes menos con No (puntos porcentuales)",title="Diferencias de Humidity3pm dentro de cada localidad")
    ax.tick_params(axis="y",labelsize=8)
    ax.legend(fontsize=8,loc="lower right")
    guardar(fig,"07_diferencias_localidades.png")
    f=tablas["faltantes_localidad"].set_index("Location")
    vs=["Sunshine","Evaporation","Cloud9am","Cloud3pm","Pressure3pm","RainTomorrow"]
    fig,ax=plt.subplots(figsize=(8,10),layout="constrained")
    im=ax.imshow(f[vs],vmin=0,vmax=100,cmap="Blues",aspect="auto")
    ax.set(yticks=range(len(f)),yticklabels=f.index,xticks=range(len(vs)),xticklabels=vs,title="Porcentaje de faltantes por localidad")
    ax.tick_params(axis="y",labelsize=8)
    plt.setp(ax.get_xticklabels(),rotation=35,ha="right",fontsize=9)
    fig.colorbar(im,ax=ax,label="Faltantes (%)",shrink=.65)
    guardar(fig,"08_faltantes_localidades.png")
    return figuras


def analizar(original: pd.DataFrame, datos: pd.DataFrame, meta: dict, raiz: Path):
    faltantes,cobertura,faltloc,checks=calidad_y_cobertura(original,datos)
    biv,corr,mat,npairs=exploracion_bivariada(datos)
    mensual,estacion,anual,dependencia=patrones_temporales(datos)
    ic,medias,diferencias,prueba=inferencia_localidades(datos)
    tablas={"diccionario_variables":diccionario(original), "descriptivos":estadistica_descriptiva(original),
        "frecuencias":frecuencias_categoricas(original),"faltantes":faltantes,
        "objetivo":descriptivos_objetivo(datos),"calidad":checks,
        "cobertura_localidad":cobertura,"faltantes_localidad":faltloc,
        "bivariado":biv,"correlacion_objetivo":corr,"matriz_correlacion":mat,"n_pares_correlacion":npairs,
        "mensual_localidad":mensual,"estacional":estacion,"cobertura_anual":anual,
        "dependencia_lag1":dependencia,"intervalos_localidades":ic,
        "medias_localidad":medias,"diferencias_localidad":diferencias}
    resumen=exportar_resultados(original,datos,meta,tablas,prueba,raiz)
    return tablas,resumen


def exportar_resultados(original: pd.DataFrame, datos: pd.DataFrame, meta: dict,
                       tablas: dict, prueba: dict, raiz: Path):
    """Guardar las tablas ya calculadas, figuras y cifras de continuidad."""
    destino=raiz/"results/01_formativa1"
    for nombre,tabla in tablas.items():
        guardar_csv(tabla,destino/"tables"/(nombre+".csv"),index=nombre in ["matriz_correlacion","n_pares_correlacion"])
    figuras=generar_figuras(datos,tablas,destino/"figures")
    resumen={"version_analisis":"F1-1.0", "dataset":meta,
        "fecha_min":str(datos.Date.min().date()),"fecha_max":str(datos.Date.max().date()),
        "n_localidades":int(datos.Location.nunique()),"n_completos_23_variables":int(original.notna().all(axis=1).sum()),
        "n_etiquetados":int(datos.RainTomorrow.notna().sum()),
        "objetivo":tablas["objetivo"].replace({np.nan:None}).to_dict("records"),
        "intervalos":tablas["intervalos_localidades"].to_dict("records"),"prueba":prueba,
        "mediana_correlacion_lag1_humedad":float(tablas["dependencia_lag1"].correlacion_lag1_humedad.median()),
        "localidades_sin_sunshine":int(tablas["faltantes_localidad"].Sunshine.eq(100).sum()),
        "tablas":{k:"results/01_formativa1/tables/"+k+".csv" for k in tablas},
        "figuras":{k:"results/01_formativa1/figures/"+k for k in figuras}}
    (destino/"resultados.json").write_text(json.dumps(resumen,indent=2,ensure_ascii=False,allow_nan=False)+"\n",encoding="utf-8")
    return resumen


def comprobar_resultados(original: pd.DataFrame, datos: pd.DataFrame, tablas: dict, resumen: dict, raiz: Path):
    """Controles de integridad y conciliación, sin prometer validez de supuestos."""
    if huella(raiz/"data/raw/weatherAUS.csv") != SHA256_ESPERADO:
        raise AssertionError("El CSV original cambió durante la ejecución.")
    pd.testing.assert_frame_equal(original,pd.read_csv(raiz/"data/raw/weatherAUS.csv"))
    assert int(tablas["objetivo"].n.sum())==len(original)
    assert int(tablas["cobertura_localidad"].n_registros.sum())==len(original)
    assert int(tablas["faltantes"].n_faltantes.sum())==int(original.isna().sum().sum())
    assert len(tablas["diccionario_variables"])==23
    assert len(tablas["descriptivos"])==16
    assert len(tablas["intervalos_localidades"])==3
    assert resumen["prueba"]["n_localidades"]==len(tablas["diferencias_localidad"])==49
    assert resumen["prueba"]["n_registros"]==int(tablas["diferencias_localidad"][["n_no","n_yes"]].sum().sum())
    med=tablas["medias_localidad"].set_index("Location")
    for r in tablas["intervalos_localidades"].to_dict("records"):
        v=r["variable"]
        x=med[v+"_media"].to_numpy()
        ref=stats.ttest_1samp(x,0).confidence_interval(confidence_level=.95)
        np.testing.assert_allclose([r["ic_inferior"],r["ic_superior"]],[ref.low,ref.high],rtol=1e-12)
        # Con pesos por n se recupera la media agrupada de los registros.
        np.testing.assert_allclose(np.average(x,weights=med[v+"_n"]),datos[v].mean(),rtol=1e-12)
    paquetes=["numpy","pandas","scipy","matplotlib","ipykernel","nbformat","nbclient"]
    versiones={}
    for paquete in paquetes:
        try: versiones[paquete]=version(paquete)
        except Exception: versiones[paquete]="No instalado"
    entorno="windows" if sys.platform=="win32" else "work"
    archivos=[raiz/p for p in list(resumen["tablas"].values())+list(resumen["figuras"].values())+["results/01_formativa1/resultados.json","src/formativa1.py"]]
    evidencia={"fecha_utc":datetime.now(timezone.utc).isoformat(),"entorno":entorno,
        "python":platform.python_version(),"sistema":platform.system(),"versiones":versiones,
        "kernel_ejecuta_desde_venv_del_proyecto":Path(sys.prefix).resolve()==(raiz/".venv").resolve(),
        "dataset_sha256":SHA256_ESPERADO,"controles_numericos":"correctos",
        "csv_original_sin_modificaciones":True,"metodologia":"CI t y comparación de medias locales; independencia espacial no verificada",
        "archivos_resultados_sha256":{str(p.relative_to(raiz)).replace("\\","/"):huella(p) for p in archivos}}
    ruta=raiz/"evidence/01_formativa1"/("ejecucion_"+entorno+".json")
    ruta.parent.mkdir(parents=True,exist_ok=True)
    ruta.write_text(json.dumps(evidencia,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    return evidencia
