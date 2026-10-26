"""MCDI501, Grupo 7: análisis reproducible de Sumativa 3.

El CSV se lee y se identifica por SHA-256; nunca se modifica. Los ajustes,
la imputación, la selección y los umbrales utilizan entrenamiento. Las
correlaciones adicionales a la matriz parcial de S1 se identifican como S3.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import os
import platform
import time
import warnings
from dataclasses import dataclass
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats as st
from scipy.special import expit
import statsmodels.api as sm
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.metrics import (
    accuracy_score, average_precision_score, confusion_matrix, f1_score,
    mean_absolute_error, mean_squared_error, precision_recall_curve,
    precision_score, r2_score, recall_score, roc_auc_score, roc_curve,
)
from sklearn.model_selection import StratifiedKFold, train_test_split
from threadpoolctl import threadpool_limits

# Evita que matrices pequeñas lancen decenas de hilos BLAS en cada réplica.
_THREAD_LIMIT = threadpool_limits(limits=1)
ROOT = Path(__file__).resolve().parents[1]
DATA_SHA256 = "573fd715cd69fcacc4df32024d823b450ae3edaae7e8ff2eeb623adbed424014"
BASE_COMMIT = "28e3a8a0805e11fd1b93beb273db7ca4060aa557"
DOMAIN = ["Humidity3pm", "Sunshine", "Rainfall", "MaxTemp"]
CANDIDATES = ["Humidity3pm", "Sunshine", "log1p_Rainfall", "MaxTemp",
              "WindGustSpeed", "Pressure3pm", "Humidity9am", "Cloud3pm"]
ALL_FEATURES = list(dict.fromkeys(DOMAIN + CANDIDATES))
MODEL_NAMES = ["M1_dominio", "M2_stepwise_AIC", "M3_reducido_BIC"]
STABLE_PAIRS = {frozenset(p) for p in [
    ("MaxTemp", "Temp3pm"), ("Humidity3pm", "Sunshine"),
    ("Humidity3pm", "Rainfall")]}
BOUNDS = {"Sunshine": (0, 24), "Rainfall": (0, np.inf),
          "Evaporation": (0, np.inf), "Humidity9am": (0, 100),
          "Humidity3pm": (0, 100), "WindGustSpeed": (0, np.inf),
          "WindSpeed9am": (0, np.inf), "WindSpeed3pm": (0, np.inf),
          "Cloud9am": (0, 9), "Cloud3pm": (0, 9)}
BLUE, TEAL, ORANGE, RED = "#153B5B", "#167D8D", "#C77C27", "#AA4054"
plt.rcParams.update({"font.size": 10, "axes.spines.top": False,
                     "axes.spines.right": False, "figure.dpi": 110,
                     "savefig.dpi": 210, "axes.titleweight": "bold"})


@dataclass
class Config:
    semilla_particion: int = 42
    semilla_imputacion: int = 50101
    semilla_cv: int = 50102
    semilla_bootstrap: int = 50103
    semilla_mc: int = 50104
    bootstrap_replicas: int = 2000
    folds: int = 5
    montecarlo_iteraciones: int = 10000


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _clean(x):
    if isinstance(x, dict): return {str(k): _clean(v) for k, v in x.items()}
    if isinstance(x, (list, tuple, np.ndarray)): return [_clean(v) for v in x]
    if isinstance(x, (np.integer,)): return int(x)
    if isinstance(x, (np.floating, float)): return float(x) if np.isfinite(x) else None
    if isinstance(x, (np.bool_,)): return bool(x)
    if isinstance(x, Path): return str(x)
    return x


def write_json(path, obj):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(_clean(obj), ensure_ascii=False, indent=2,
                               allow_nan=False) + "\n", encoding="utf-8")


def table(ctx, name, data):
    frame = data if isinstance(data, pd.DataFrame) else pd.DataFrame(data)
    frame.to_csv(ctx["tables"] / (name + ".csv"), index=False,
                 encoding="utf-8-sig", float_format="%.15g")
    return frame


def _savefig(ctx, name, fig):
    fig.savefig(ctx["figures"] / (name + ".png"), bbox_inches="tight")
    plt.close(fig)


def _design(X, features):
    return np.column_stack([np.ones(len(X)), X.loc[:, features].to_numpy(float)])


def class_weights(y, freq=None):
    y = np.asarray(y, float)
    freq = np.ones(len(y)) if freq is None else np.asarray(freq, float)
    counts = np.bincount(y.astype(int), weights=freq, minlength=2)
    if counts.min() <= 0: raise ValueError("La remuestra no contiene ambas clases")
    values = counts.sum() / (2 * counts)
    return freq * values[y.astype(int)], values


def logit_fast(X, y, weights=None, start=None, tol=1e-9, maxiter=80):
    """MLE binomial por Newton y búsqueda de paso, sin penalización.

    Las frecuencias enteras equivalen a duplicar registros. Los pesos de clase
    multiplican la log-verosimilitud. La equivalencia con GLM se verifica.
    """
    X, y = np.asarray(X, float), np.asarray(y, float)
    w = np.ones(len(y)) if weights is None else np.asarray(weights, float)
    beta = np.zeros(X.shape[1]) if start is None else np.array(start, float).copy()
    def loss(b):
        eta = X @ b
        return float(np.dot(w, np.logaddexp(0, eta) - y * eta))
    current = loss(beta)
    for it in range(maxiter):
        p = expit(X @ beta)
        grad = X.T @ (w * (y - p))
        hess = X.T @ (X * (w * p * (1 - p))[:, None])
        try: step = np.linalg.solve(hess, grad)
        except np.linalg.LinAlgError: step = np.linalg.lstsq(hess, grad, rcond=None)[0]
        rate = 1.0
        while rate >= 2**-24:
            candidate = beta + rate * step
            value = loss(candidate)
            if value <= current + 1e-9: break
            rate /= 2
        if rate < 2**-24: raise RuntimeError("Newton no encontró un paso descendente")
        beta = candidate
        if np.max(np.abs(rate * step)) < tol:
            if not np.isfinite(beta).all(): raise RuntimeError("Coeficiente no finito")
            return beta, -value, it + 1
        current = value
    raise RuntimeError("El ajuste logístico no convergió")


def metrics(y, p, threshold=.5):
    y, p = np.asarray(y, int), np.asarray(p, float)
    keep = np.isfinite(p); y, p = y[keep], p[keep]
    pred = (p >= threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(y, pred, labels=[0, 1]).ravel()
    return {"n": len(y), "umbral": threshold,
            "accuracy": accuracy_score(y, pred),
            "precision": precision_score(y, pred, zero_division=0),
            "recall": recall_score(y, pred, zero_division=0),
            "f1": f1_score(y, pred, zero_division=0),
            "auc": roc_auc_score(y, p), "pr_auc": average_precision_score(y, p),
            "tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp)}


def best_threshold(y, p):
    """Maximiza F1 solo con predicciones fuera de pliegue de entrenamiento."""
    y, p = np.asarray(y, int), np.asarray(p, float)
    mask = np.isfinite(p)
    precision, recall, thresholds = precision_recall_curve(y[mask], p[mask])
    f1 = 2 * precision[:-1] * recall[:-1] / np.maximum(
        precision[:-1] + recall[:-1], 1e-15)
    pos = int(np.argmax(f1))
    return float(thresholds[pos])


class ImputationBank:
    """OLS por variable sobre casos completos y estadísticos por localidad.

    La base afín fija de cada regresión sirve para acondicionamiento numérico.
    Reponderar X'X y X'y por localidad reproduce exactamente su reajuste OLS.
    Los predictores auxiliares ausentes se rellenan temporalmente por mediana
    de entrenamiento; no se modifica un valor meteorológico observado.
    """
    def __init__(self, frame, numeric, prior, cfg, diagnostics=False):
        self.numeric, self.cfg = list(numeric), cfg
        self.raw = frame[self.numeric].to_numpy(float)
        self.locations, self.codes = np.unique(frame["Location"].astype(str), return_inverse=True)
        self.L = len(self.locations)
        self.models, self.diagnostics, self.selection, self.clips = {}, [], [], []
        current_corr = frame[self.numeric].corr(method="spearman")
        self.sorted = []
        for j in range(len(numeric)):
            idx = np.flatnonzero(np.isfinite(self.raw[:, j]))
            idx = idx[np.argsort(self.raw[idx, j], kind="stable")]
            self.sorted.append((self.raw[idx, j], self.codes[idx]))
        self.medians = np.nanmedian(self.raw, axis=0)
        for j, target in enumerate(self.numeric):
            if not frame[target].isna().any(): continue
            ranked = []
            for predictor in self.numeric:
                if predictor == target: continue
                in_s1 = target in prior.index and predictor in prior.columns
                corr = prior.loc[target, predictor] if in_s1 else current_corr.loc[target, predictor]
                stable = frozenset((target, predictor)) in STABLE_PAIRS
                ranked.append((100 * stable + abs(float(corr)), predictor, in_s1, corr, stable))
            ranked.sort(reverse=True)
            chosen = []
            for item in ranked:
                predictor = item[1]
                if chosen and any(abs(current_corr.loc[predictor, q[1]]) > .85 for q in chosen):
                    continue
                chosen.append(item)
                if len(chosen) == 3: break
            if len(chosen) < 3:
                chosen += [r for r in ranked if r[1] not in {x[1] for x in chosen}][:3-len(chosen)]
            pred = [r[1] for r in chosen]
            positions = [self.numeric.index(p) for p in pred]
            valid = np.isfinite(self.raw[:, [j] + positions]).all(axis=1)
            if valid.sum() < 100: raise ValueError("Insuficientes casos completos: " + target)
            xp = self.raw[valid][:, positions]; yt = self.raw[valid, j]
            center, scale = xp.mean(axis=0), xp.std(axis=0)
            scale = np.where(scale > 1e-10, scale, 1)
            Z = np.column_stack([np.ones(len(xp)), (xp-center)/scale])
            codes = self.codes[valid]
            A = np.zeros((self.L, 4, 4)); b = np.zeros((self.L, 4))
            for loc in range(self.L):
                z, yy = Z[codes == loc], yt[codes == loc]
                A[loc] = z.T @ z; b[loc] = z.T @ yy
            beta = np.linalg.solve(A.sum(axis=0), b.sum(axis=0))
            self.models[target] = {"j": j, "positions": positions, "predictors": pred,
                "center": center, "scale": scale, "A": A, "b": b, "beta": beta,
                "donors": int(valid.sum())}
            for rank, (_, predictor, in_s1, corr, stable) in enumerate(chosen, 1):
                self.selection.append({"variable_imputada": target, "predictor": predictor,
                    "orden": rank, "rho_referencia": corr,
                    "origen_correlacion": "S1" if in_s1 else "Ampliación S3: entrenamiento",
                    "par_validado_S2": stable})
            if diagnostics:
                tr, va = train_test_split(np.arange(len(yt)), test_size=.2,
                    random_state=cfg.semilla_imputacion+j)
                beta_cv = np.linalg.lstsq(Z[tr], yt[tr], rcond=None)[0]
                prediction = self._bound(target, Z[va] @ beta_cv)
                med = np.repeat(np.median(yt[tr]), len(va))
                fitted = sm.OLS(yt, Z).fit()
                resid = fitted.resid
                rng = np.random.default_rng(cfg.semilla_imputacion+j)
                sample = resid[rng.choice(len(resid), min(5000, len(resid)), replace=False)]
                vif = max(variance_inflation_factor(Z, k) for k in range(1, 4))
                bp = het_breuschpagan(resid, Z)
                self.diagnostics.append({"variable": target, "predictores": "; ".join(pred),
                    "n_ajuste_completos": len(yt), "n_validacion_interna": len(va),
                    "r2_ajuste": fitted.rsquared, "r2_validacion": r2_score(yt[va], prediction),
                    "rmse_regresion": np.sqrt(mean_squared_error(yt[va], prediction)),
                    "rmse_mediana": np.sqrt(mean_squared_error(yt[va], med)),
                    "mae_regresion": mean_absolute_error(yt[va], prediction),
                    "shapiro_p_muestra_5000": st.shapiro(sample).pvalue,
                    "breusch_pagan_p": bp[1], "vif_max": vif,
                    "rango_predicho_min": prediction.min(), "rango_predicho_max": prediction.max()})
                if target == "Sunshine":
                    self.sunshine_diagnostic = {"actual": yt[va], "prediction": prediction,
                        "residual": yt[va]-prediction, "fitted": fitted.fittedvalues,
                        "resid_fit": resid}

    @staticmethod
    def _bound(target, values):
        lo, hi = BOUNDS.get(target, (-np.inf, np.inf))
        return np.clip(values, lo, hi)

    def weighted_medians(self, multipliers):
        result = []
        for values, codes in self.sorted:
            weights = multipliers[codes].astype(np.int64)
            cum = weights.cumsum(); total = int(cum[-1])
            if total == 0: raise ValueError("Variable completamente ausente en remuestra")
            left = np.searchsorted(cum, (total-1)//2, side="right")
            right = np.searchsorted(cum, total//2, side="right")
            result.append((values[left]+values[right])/2)
        return np.array(result)

    def transform(self, frame, strategy, multipliers=None, columns=None, record=False):
        raw = frame[self.numeric].to_numpy(float)
        result = raw.copy()
        medians = self.medians if multipliers is None else self.weighted_medians(multipliers)
        active = self.numeric if columns is None else columns
        for target in active:
            j = self.numeric.index(target); missing = ~np.isfinite(raw[:, j])
            if not missing.any(): continue
            if strategy == "mediana": result[missing, j] = medians[j]; continue
            m = self.models[target]
            beta = m["beta"] if multipliers is None else np.linalg.solve(
                np.einsum("l,lij->ij", multipliers, m["A"]),
                np.einsum("l,li->i", multipliers, m["b"]))
            xp = raw[missing][:, m["positions"]].copy()
            aux_missing = ~np.isfinite(xp)
            xp = np.where(aux_missing, medians[m["positions"]], xp)
            prediction = beta[0] + ((xp-m["center"])/m["scale"]) @ beta[1:]
            bounded = self._bound(target, prediction)
            result[missing, j] = bounded
            if record:
                self.clips.append({"variable": target, "n_imputados": int(missing.sum()),
                    "n_recorte_solo_imputados": int((prediction != bounded).sum()),
                    "filas_con_predictores_auxiliares_imputados": int(aux_missing.any(axis=1).sum())})
        return pd.DataFrame(result, index=frame.index, columns=self.numeric)


def raw_dependencies(features):
    return list(dict.fromkeys("Rainfall" if p == "log1p_Rainfall" else p for p in features))


def engineer(raw):
    result = raw.copy()
    if "Rainfall" in result:
        result["log1p_Rainfall"] = np.log1p(np.maximum(result["Rainfall"], 0))
    return result


class Prepared:
    def __init__(self, frame, numeric, prior, cfg, strategy, features=ALL_FEATURES,
                 bank=None):
        self.strategy, self.features, self.numeric = strategy, list(features), list(numeric)
        self.bank = bank or (ImputationBank(frame, numeric, prior, cfg) if strategy != "eliminacion" else None)
        self.raw = frame
        if strategy == "eliminacion":
            selected = frame.dropna(subset=raw_dependencies(self.features))
            raw = selected[self.numeric]
        else:
            selected = frame
            raw = self.bank.transform(frame, strategy)
        eng = engineer(raw)[self.features]
        self.mean = eng.mean().to_numpy(float)
        self.scale = eng.std(ddof=0).to_numpy(float)
        self.scale = np.where(self.scale > 1e-12, self.scale, 1)
        self.fit_index = selected.index

    def transform(self, frame):
        if self.strategy == "eliminacion":
            selected = frame.dropna(subset=raw_dependencies(self.features))
            raw = selected[self.numeric]
        else:
            selected = frame; raw = self.bank.transform(frame, self.strategy)
        eng = engineer(raw)[self.features]
        return pd.DataFrame((eng.to_numpy(float)-self.mean)/self.scale,
                             index=selected.index, columns=self.features)


def select_features(X, y, kind, trace=None):
    """AIC/BIC no ponderados en idénticas filas, antes del reajuste balanceado."""
    cache = {}
    def score(features):
        key = tuple(sorted(features))
        if key not in cache:
            beta, ll, _ = logit_fast(_design(X, list(key)), y)
            k = len(key)+1; n = len(y)
            cache[key] = (2*k-2*ll, np.log(n)*k-2*ll)
        return cache[key]
    if kind == "M1_dominio": return DOMAIN.copy(), score(DOMAIN)
    if kind == "M3_reducido_BIC":
        choices = [(score(list(s))[1], list(s)) for k in range(1, 4)
                   for s in itertools.combinations(DOMAIN, k)]
        _, chosen = min(choices, key=lambda z: z[0])
        return chosen, score(chosen)
    selected = []; current = score(selected)[0]
    for iteration in range(30):
        proposals = []
        for p in CANDIDATES:
            if p not in selected:
                cand = selected+[p]; proposals.append((score(cand)[0], cand, "agrega", p))
        for p in selected:
            cand = [q for q in selected if q != p]
            proposals.append((score(cand)[0], cand, "retira", p))
        if not proposals: break
        value, cand, action, p = min(proposals, key=lambda z: z[0])
        if value >= current-1e-7: break
        selected, current = cand, value
        if trace is not None:
            trace.append({"paso": iteration+1, "accion": action, "variable": p,
                          "aic": current, "bic": score(selected)[1],
                          "predictores": "; ".join(selected), "n": len(y)})
    if not selected: raise RuntimeError("Stepwise seleccionó solo el intercepto")
    return selected, score(selected)


def cv_predictions(ctx, strategy, model_kinds=MODEL_NAMES, fixed_features=None):
    train, cfg = ctx["train"], ctx["cfg"]
    splitter = StratifiedKFold(cfg.folds, shuffle=True, random_state=cfg.semilla_cv)
    oof = {name: pd.Series(np.nan, index=train.index) for name in model_kinds}
    records = []
    for fold, (ii, vv) in enumerate(splitter.split(train, train.y), 1):
        fit, val = train.iloc[ii], train.iloc[vv]
        features = ALL_FEATURES if fixed_features is None else fixed_features
        prep = Prepared(fit, ctx["numeric"], ctx["prior"], cfg, strategy, features)
        Xfit, Xval = prep.transform(fit), prep.transform(val)
        yf, yv = fit.loc[Xfit.index, "y"], val.loc[Xval.index, "y"]
        for name in model_kinds:
            chosen = fixed_features or select_features(Xfit, yf.to_numpy(), name)[0]
            weights, _ = class_weights(yf)
            beta, _, _ = logit_fast(_design(Xfit, chosen), yf, weights)
            pp = expit(_design(Xval, chosen) @ beta)
            oof[name].loc[Xval.index] = pp
            records.append({"modelo": name, "estrategia": strategy, "fold": fold,
                "n_train": len(yf), "n_validacion": len(yv),
                "auc": roc_auc_score(yv, pp), "predictores": "; ".join(chosen)})
        print(f"CV {strategy}: pliegue {fold}/{cfg.folds} terminado", flush=True)
    return oof, pd.DataFrame(records)


def iniciar(cfg=None, output=None):
    cfg = cfg or Config()
    output = Path(output) if output else ROOT / "results/05_sumativa3"
    for d in (output, output/"tables", output/"figures", ROOT/"evidence/05_sumativa3"):
        d.mkdir(parents=True, exist_ok=True)
    path = ROOT / "data/raw/weatherAUS.csv"
    if not path.is_file(): raise FileNotFoundError("Falta data/raw/weatherAUS.csv")
    if sha256(path) != DATA_SHA256: raise ValueError("El CSV difiere del original auditado")
    raw = pd.read_csv(path, parse_dates=["Date"])
    if raw.shape != (145460, 23): raise ValueError("Dimensiones inesperadas del CSV")
    if raw.duplicated(["Date", "Location"]).any(): raise ValueError("Clave localidad/fecha duplicada")
    df = raw.loc[raw.RainTomorrow.isin(["No", "Yes"])].copy()
    df["y"] = df.RainTomorrow.map({"No": 0, "Yes": 1}).astype(int)
    ii, jj = train_test_split(df.index, test_size=.3,
        random_state=cfg.semilla_particion, stratify=df.y)
    train, test = df.loc[ii].copy(), df.loc[jj].copy()
    assert train.index.intersection(test.index).empty
    assert (len(df), len(train), len(test)) == (142193, 99535, 42658)
    numeric = raw.select_dtypes(include=np.number).columns.tolist()
    prior_path = ROOT / "results/02_sumativa1/tables/matriz_correlaciones_spearman.csv"
    prior = pd.read_csv(prior_path, index_col=0, encoding="utf-8-sig")
    s2_path = ROOT / "results/03_sumativa2/resultados_validados_s2.json"
    s2 = json.loads(s2_path.read_text(encoding="utf-8-sig"))
    if s2["dataset"]["sha256"] != DATA_SHA256: raise ValueError("S2 usa otro CSV")
    for r in s2["correlaciones"]:
        x, y = r["variable_x"], r["variable_y"]
        assert np.isclose(prior.loc[x, y], r["rho_spearman_s1"], atol=1e-12)
    ctx = {"cfg": cfg, "raw": raw, "df": df, "train": train, "test": test,
        "numeric": numeric, "prior": prior, "s2": s2, "data_path": path,
        "start": time.monotonic(), "output": output,
        "tables": output/"tables", "figures": output/"figures", "checks": {},
        "source_hashes": {str(p.relative_to(ROOT)): sha256(p)
            for p in (prior_path, s2_path, ROOT/"results/04_formativa2_jorge/metricas_test.csv")}}
    table(ctx, "particion", [{"conjunto": label, "n": len(a),
        "n_lluvia": int(a.y.sum()), "lluvia_pct": a.y.mean()*100,
        "localidades": a.Location.nunique()} for label, a in (("train", train), ("test", test))])
    table(ctx, "indices_particion", pd.DataFrame({"indice_original": df.index,
        "conjunto": np.where(df.index.isin(train.index), "train", "test")}))
    old = pd.read_csv(ROOT/"results/02_sumativa1/tables/auditoria_calidad_datos.csv", encoding="utf-8-sig")
    missing = old.loc[old.Variable.isin(numeric)].rename(columns={
        "Variable": "variable", "Faltantes": "faltantes_S1", "Porcentaje faltante": "porcentaje_S1"})
    missing = missing[["variable", "faltantes_S1", "porcentaje_S1"]].copy()
    missing["faltantes_respuesta_conocida"] = missing.variable.map(df[numeric].isna().sum())
    missing["porcentaje_respuesta_conocida"] = missing.variable.map(df[numeric].isna().mean()*100)
    missing["faltantes_train"] = missing.variable.map(train[numeric].isna().sum())
    missing["faltantes_test"] = missing.variable.map(test[numeric].isna().sum())
    table(ctx, "faltantes_S1_actualizacion_muestra", missing)
    table(ctx, "matriz_correlaciones_ampliacion_S3_train",
          train[numeric].corr(method="spearman").rename_axis("variable").reset_index())
    ctx["checks"].update({"dataset_original_identificado": True,
        "particion_70_30_estratificada_sin_solapamiento": True,
        "S2_conciliada_con_matriz_S1": True})
    print(f"Datos: {len(raw):,} filas; {len(df):,} respuestas conocidas; {len(numeric)} numéricas.")
    print(f"Train={len(train):,}; test={len(test):,}; semilla={cfg.semilla_particion}.")
    return ctx


def reproducir_f2(ctx):
    from sklearn.impute import SimpleImputer
    from sklearn.preprocessing import StandardScaler
    tr, te = ctx["train"], ctx["test"]
    imputer = SimpleImputer(strategy="median")
    scaler = StandardScaler()
    xtr = scaler.fit_transform(imputer.fit_transform(tr[DOMAIN]))
    xte = scaler.transform(imputer.transform(te[DOMAIN]))
    fit = sm.Logit(tr.y.to_numpy(), np.column_stack([np.ones(len(tr)), xtr])).fit(
        method="newton", maxiter=100, tol=1e-10, disp=False)
    p = fit.predict(np.column_stack([np.ones(len(te)), xte]))
    result = metrics(te.y, p)
    expected = pd.read_csv(ROOT/"results/04_formativa2_jorge/metricas_test.csv")
    mapping = {"Accuracy": "accuracy", "Precision": "precision", "Recall": "recall",
               "F1-score": "f1", "ROC-AUC": "auc"}
    comparisons = []
    for _, row in expected.iterrows():
        if row["Métrica"] not in mapping: continue
        key = mapping[row["Métrica"]]
        comparisons.append({"metrica": key, "F2_entregada": row.Valor,
            "reproducida_S3": result[key], "diferencia": result[key]-row.Valor})
        np.testing.assert_allclose(result[key], row.Valor, rtol=0, atol=1e-10)
    assert [result[k] for k in ("tn", "fp", "fn", "tp")] == [31549, 1546, 5755, 3808]
    ctx["f2"] = result
    table(ctx, "reproduccion_referencia_F2", comparisons)
    ctx["checks"]["F2_reproducida_metricas_y_matriz"] = True
    print("F2 reproducida: AUC", round(result["auc"], 6), "recall", round(result["recall"], 6))
    return pd.DataFrame(comparisons)


def estudiar_imputacion(ctx):
    tr, cfg = ctx["train"], ctx["cfg"]
    print("Ajustando regresiones de imputación sobre casos completos de entrenamiento...", flush=True)
    bank = ImputationBank(tr, ctx["numeric"], ctx["prior"], cfg, diagnostics=True)
    diag = pd.DataFrame(bank.diagnostics)
    sunshine = diag.set_index("variable").loc["Sunshine"]
    improvement = 1-sunshine.rmse_regresion/sunshine.rmse_mediana
    primary = "regresion" if improvement >= .05 else "mediana"
    ctx.update({"bank": bank, "primary": primary, "imputer_diagnostics": diag,
                "imputer_rmse_improvement": improvement})
    table(ctx, "imputacion_diagnosticos_regresion", diag)
    table(ctx, "imputacion_seleccion_predictores", bank.selection)
    counts = []
    for strategy in ("mediana", "regresion"):
        for label, frame in (("train", ctx["train"]), ("test", ctx["test"])):
            bank.clips = []
            completed = bank.transform(frame, strategy, record=strategy == "regresion")
            assert np.isfinite(completed.to_numpy()).all()
            observed = frame[ctx["numeric"]].notna().to_numpy()
            assert np.array_equal(completed.to_numpy()[observed],
                                  frame[ctx["numeric"]].to_numpy()[observed])
            for col in ctx["numeric"]:
                detail = next((z for z in bank.clips if z["variable"] == col), {})
                counts.append({"estrategia": strategy, "conjunto": label, "variable": col,
                    "n_imputados": int(frame[col].isna().sum()),
                    "n_recorte_solo_imputados": detail.get("n_recorte_solo_imputados", 0),
                    "n_fallback_auxiliar_mediana": detail.get("filas_con_predictores_auxiliares_imputados", 0)})
    table(ctx, "imputacion_conteos", counts)
    coef = []
    for target, m in bank.models.items():
        for p, b in zip(["const"]+m["predictors"], m["beta"]):
            coef.append({"variable_imputada": target, "termino": p,
                "coeficiente_base_estandarizada": b, "n_casos_completos": m["donors"]})
    table(ctx, "imputacion_coeficientes_OLS", coef)
    ctx["checks"]["16_regresiones_imputacion_y_observados_intactos"] = len(bank.models) == 16
    ctx["checks"]["imputadores_sin_RainTomorrow_ni_y"] = all(
        set(m["predictors"]).isdisjoint({"RainTomorrow", "y"}) for m in bank.models.values())
    write_json(ctx["output"]/"regla_imputacion.json", {
        "criterio_predefinido": "Regresión si reduce >=5% RMSE de reconstrucción de Sunshine frente a mediana en validación interna de donantes; de otro modo mediana",
        "reduccion_rmse_Sunshine": improvement, "estrategia": primary,
        "ajuste_con_datos": "solo entrenamiento; ninguna métrica de RainTomorrow de prueba interviene",
        "limitacion": "La validación de donantes observados no valida las 19 estaciones sin Sunshine; imputación determinista condicionada a covariables"})
    print(f"Imputación principal: {primary}; reducción RMSE Sunshine={improvement:.2%}.")
    return diag


def _coef_table(model, reference_mean=None, reference_scale=None):
    features = model["features"]
    beta, cov = np.asarray(model["fit"].params), np.asarray(model["fit"].cov_params())
    mean, scale = model["mean"], model["scale"]
    refmean = mean if reference_mean is None else reference_mean
    refscale = scale if reference_scale is None else reference_scale
    T = np.eye(len(features)+1)
    T[0, 1:] = (refmean-mean)/scale
    T[np.arange(1, len(features)+1), np.arange(1, len(features)+1)] = refscale/scale
    br = T @ beta; se = np.sqrt(np.diag(T @ cov @ T.T))
    rows = []
    for j, name in enumerate(["const"]+features):
        lo, hi = br[j]-st.norm.ppf(.975)*se[j], br[j]+st.norm.ppf(.975)*se[j]
        rows.append({"modelo": model["name"], "estrategia": model["strategy"], "termino": name,
            "coeficiente": br[j], "error_estandar_convencional": se[j],
            "ic_wald_beta_inf": lo, "ic_wald_beta_sup": hi,
            "odds_ratio": np.exp(br[j]), "ic_wald_OR_inf": np.exp(lo),
            "ic_wald_OR_sup": np.exp(hi), "p_convencional": 2*st.norm.sf(abs(br[j]/se[j])),
            "coeficiente_unidad_original_o_log1p": beta[j]/scale[j-1] if j else beta[0]-np.dot(beta[1:]/scale, mean),
            "DE_referencia": refscale[j-1] if j else np.nan})
    return pd.DataFrame(rows)


def _fit_full(ctx, prep, features, name, threshold):
    X = prep.transform(ctx["train"])
    y = ctx["train"].loc[X.index, "y"]
    design = pd.DataFrame(_design(X, features), index=X.index, columns=["const"]+features)
    weights, values = class_weights(y)
    fit = sm.GLM(y, design, family=sm.families.Binomial(), freq_weights=weights).fit(
        maxiter=100, tol=1e-10)
    fast, _, it = logit_fast(design, y, weights)
    np.testing.assert_allclose(fast, fit.params, rtol=0, atol=2e-7)
    idx = [prep.features.index(f) for f in features]
    return {"name": name, "features": list(features), "prep": prep,
        "strategy": prep.strategy, "threshold": threshold, "fit": fit,
        "mean": prep.mean[idx], "scale": prep.scale[idx],
        "class_weights": values, "X": X, "y": y, "design": design,
        "n_train": len(y), "newton_iter": it}


def ajustar_modelos(ctx):
    strategy = ctx["primary"]
    oof, cv = cv_predictions(ctx, strategy)
    table(ctx, "validacion_cruzada_procedimientos", cv)
    prep = Prepared(ctx["train"], ctx["numeric"], ctx["prior"], ctx["cfg"],
                    strategy, bank=ctx["bank"])
    X = prep.transform(ctx["train"])
    models, rows, trace = {}, [], []
    for name in MODEL_NAMES:
        features, (aic, bic) = select_features(X, ctx["train"].y.to_numpy(), name,
                                             trace if name == MODEL_NAMES[1] else None)
        threshold = best_threshold(ctx["train"].y, oof[name])
        model = _fit_full(ctx, prep, features, name, threshold)
        model["oof"] = oof[name]
        models[name] = model
        cvmetrics = metrics(ctx["train"].y, oof[name], threshold)
        rows.append({"modelo": name, "n_predictores": len(features),
            "predictores": "; ".join(features), "AIC_seleccion_no_ponderado": aic,
            "BIC_seleccion_no_ponderado": bic, "umbral_F1_OOF": threshold,
            **{"oof_"+k: v for k, v in cvmetrics.items()}})
    summary = pd.DataFrame(rows)
    maximum = summary.oof_auc.max()
    tied = summary.loc[summary.oof_auc >= maximum-.002].sort_values(
        ["n_predictores", "oof_auc"], ascending=[True, False])
    best = models[tied.iloc[0].modelo]
    ctx.update({"models": models, "best": best, "cv_summary": summary, "oof": oof})
    table(ctx, "seleccion_modelos_entrenamiento", summary)
    table(ctx, "trayectoria_stepwise_AIC", trace)
    table(ctx, "coeficientes_tres_modelos", pd.concat([_coef_table(m) for m in models.values()], ignore_index=True))
    # Evidencia de que el modelo y los umbrales se fijan antes de predecir prueba.
    frozen = {"criterio": "Mayor AUC OOF; diferencia <=0.002 favorece menos predictores",
        "modelo": best["name"], "estrategia": strategy,
        "predictores_finales": best["features"], "umbral_final": best["threshold"],
        "umbrales_por_modelo": {k: m["threshold"] for k, m in models.items()},
        "ninguna_metrica_de_prueba_utilizada": True,
        "pesos_clase_train": {"No": best["class_weights"][0], "Yes": best["class_weights"][1]}}
    write_json(ctx["output"]/"decision_congelada_entrenamiento.json", frozen)
    ctx["frozen_hash"] = sha256(ctx["output"]/"decision_congelada_entrenamiento.json")
    ctx["checks"]["Newton_conciliado_con_GLM_statsmodels"] = True
    print("Modelo elegido exclusivamente en entrenamiento:", best["name"], best["features"])
    print("Umbral F1 OOF:", best["threshold"])
    return summary


def evaluar_modelos(ctx):
    rows, preds = [], pd.DataFrame({"indice_original": ctx["test"].index,
        "y_real": ctx["test"].y.to_numpy()}).set_index("indice_original")
    for name, model in ctx["models"].items():
        for label, frame in (("train", ctx["train"]), ("test", ctx["test"])):
            X = model["prep"].transform(frame)
            pp = expit(_design(X, model["features"]) @ np.asarray(model["fit"].params))
            y = frame.loc[X.index, "y"]
            model["p_"+label] = pd.Series(pp, index=X.index)
            for rule, threshold in (("F1_OOF", model["threshold"]), ("referencia_0.5", .5)):
                rows.append({"modelo": name, "conjunto": label, "regla_umbral": rule,
                             **metrics(y, pp, threshold)})
            if label == "test":
                preds["score_"+name] = model["p_test"]
                preds["pred_"+name] = (model["p_test"] >= model["threshold"]).astype(int)
    result = table(ctx, "metricas_tres_modelos", rows)
    table(ctx, "predicciones_prueba_tres_modelos", preds.reset_index())
    ctx["metrics"] = result
    assert sha256(ctx["output"]/"decision_congelada_entrenamiento.json") == ctx["frozen_hash"]
    ctx["checks"]["seleccion_y_umbrales_congelados_antes_de_prueba"] = True
    return result


def comparar_imputacion(ctx):
    best, rows, coefs, distributions, models = ctx["best"], [], [], [], {}
    refmean, refscale = best["mean"], best["scale"]
    features = best["features"]
    required = raw_dependencies(features)
    common = ctx["test"].dropna(subset=required).index
    correlation_rows = []
    for strategy in ("eliminacion", "mediana", "regresion"):
        prep = Prepared(ctx["train"], ctx["numeric"], ctx["prior"], ctx["cfg"], strategy,
                        features, bank=ctx["bank"] if strategy != "eliminacion" else None)
        model = _fit_full(ctx, prep, features, best["name"], best["threshold"])
        models[strategy] = model
        coefs.append(_coef_table(model, refmean, refscale))
        Xte = prep.transform(ctx["test"])
        pp = pd.Series(expit(_design(Xte, features) @ np.asarray(model["fit"].params)), index=Xte.index)
        model["p_test"] = pp
        for population, index in (("disponible_por_estrategia", Xte.index), ("casos_comunes", common)):
            m = metrics(ctx["test"].loc[index, "y"], pp.loc[index], best["threshold"])
            rows.append({"estrategia": strategy, "poblacion_prueba": population,
                "n_train": model["n_train"], "localidades_train": ctx["train"].loc[model["X"].index].Location.nunique(),
                "localidades_test": ctx["test"].loc[index].Location.nunique(),
                "cobertura_test": len(index)/len(ctx["test"]), **m})
        if strategy == "eliminacion":
            completed = ctx["train"].dropna(subset=required)[ctx["numeric"]]
        else:
            completed = ctx["bank"].transform(ctx["train"], strategy)
        for col in required:
            obs = ctx["train"][col].dropna()
            z = completed[col].dropna()
            distributions.append({"estrategia": strategy, "variable": col, "n": len(z),
                "media": z.mean(), "DE": z.std(), "mediana": z.median(),
                "q25": z.quantile(.25), "q75": z.quantile(.75),
                "DE_observada_train": obs.std(), "razon_DE_vs_observada": z.std()/obs.std()})
        for x, y in itertools.combinations(required, 2):
            prior_known = x in ctx["prior"].index and y in ctx["prior"].columns
            correlation_rows.append({"estrategia": strategy, "variable_x": x, "variable_y": y,
                "rho_despues": completed[[x, y]].corr(method="spearman").iloc[0, 1],
                "rho_S1": ctx["prior"].loc[x, y] if prior_known else np.nan,
                "rho_observada_train": ctx["train"][[x, y]].corr(method="spearman").iloc[0, 1]})
    ctx["imputation_models"] = models
    ctx["imputation_comparison"] = table(ctx, "impacto_imputacion_metricas", rows)
    ctx["imputation_coefs"] = table(ctx, "impacto_imputacion_coeficientes_escala_comun", pd.concat(coefs, ignore_index=True))
    table(ctx, "impacto_imputacion_distribuciones", distributions)
    table(ctx, "impacto_imputacion_correlaciones", correlation_rows)
    ctx["checks"]["impacto_tres_estrategias_mismos_predictores_y_casos_comunes"] = len(models) == 3
    return ctx["imputation_comparison"]


def _bootstrap_fit(ctx, multipliers):
    """Reajuste del pipeline con multiplicidades de localidades, sin expandir filas."""
    model, bank, frame = ctx["best"], ctx["bank"], ctx["train"]
    features = model["features"]
    frequency = np.asarray(multipliers)[bank.codes].astype(float)
    raw = bank.transform(frame, ctx["primary"], multipliers=multipliers,
                         columns=raw_dependencies(features))
    z = engineer(raw)[features].to_numpy(float)
    mean = np.average(z, axis=0, weights=frequency)
    scale = np.sqrt(np.average((z-mean)**2, axis=0, weights=frequency))
    if (scale < 1e-10).any(): raise ValueError("Predictor constante en remuestra")
    design = np.column_stack([np.ones(len(z)), (z-mean)/scale])
    weights, _ = class_weights(frame.y, frequency)
    beta_raw = np.asarray(model["fit"].params)[1:]/model["scale"]
    intercept_raw = float(model["fit"].params.iloc[0])-np.dot(beta_raw, model["mean"])
    start = np.r_[intercept_raw+np.dot(beta_raw, mean), beta_raw*scale]
    beta, _, it = logit_fast(design, frame.y.to_numpy(), weights, start=start)
    original = beta[1:]/scale
    b0 = beta[0]-np.dot(original, mean)
    reference = np.r_[b0+np.dot(original, model["mean"]), original*model["scale"]]
    return reference, int(frequency.sum()), it


def verificar_equivalencia_bootstrap(ctx):
    """Contrasta el cálculo por pesos con una expansión real de una remuestra."""
    bank, model = ctx["bank"], ctx["best"]
    counts = np.ones(bank.L, dtype=int)
    counts[0], counts[1] = 2, 0
    fast, _, _ = _bootstrap_fit(ctx, counts)
    freq = counts[bank.codes]
    idx = np.repeat(np.arange(len(ctx["train"])), freq)
    original = bank.raw[idx].copy(); filled = original.copy()
    medians = np.nanmedian(original, axis=0)
    for col in raw_dependencies(model["features"]):
        j = bank.numeric.index(col); mask = ~np.isfinite(original[:, j])
        if not mask.any(): continue
        if ctx["primary"] == "mediana": filled[mask, j] = medians[j]; continue
        m = bank.models[col]
        donor = np.isfinite(original[:, [j]+m["positions"]]).all(axis=1)
        xp = original[donor][:, m["positions"]]
        Z = np.column_stack([np.ones(donor.sum()), (xp-m["center"])/m["scale"]])
        beta = np.linalg.lstsq(Z, original[donor, j], rcond=None)[0]
        xp = original[mask][:, m["positions"]]
        xp = np.where(np.isfinite(xp), xp, medians[m["positions"]])
        pp = beta[0]+((xp-m["center"])/m["scale"]) @ beta[1:]
        filled[mask, j] = bank._bound(col, pp)
    eng = engineer(pd.DataFrame(filled, columns=bank.numeric))[model["features"]].to_numpy()
    mean, scale = eng.mean(axis=0), eng.std(axis=0)
    D = np.column_stack([np.ones(len(eng)), (eng-mean)/scale])
    y = ctx["train"].y.to_numpy()[idx]
    weights, _ = class_weights(y)
    explicit = sm.GLM(y, D, family=sm.families.Binomial(), freq_weights=weights).fit(
        maxiter=100, tol=1e-10)
    rawbeta = np.asarray(explicit.params)[1:]/scale
    reference = np.r_[explicit.params[0]-np.dot(rawbeta, mean)+np.dot(rawbeta, model["mean"]),
                      rawbeta*model["scale"]]
    np.testing.assert_allclose(fast, reference, rtol=0, atol=2e-7)
    np.testing.assert_allclose(bank.weighted_medians(counts), medians, rtol=0, atol=1e-12)
    ctx["checks"]["bootstrap_ponderado_equivale_a_duplicar_localidades"] = True
    print("Bootstrap: equivalencia con duplicación explícita y GLM verificada.", flush=True)


def bootstrap_modelo(ctx):
    cfg, bank, model = ctx["cfg"], ctx["bank"], ctx["best"]
    verificar_equivalencia_bootstrap(ctx)
    rows, failures, attempt = [], [], 0
    names = ["const"]+model["features"]
    t0 = time.monotonic()
    while len(rows) < cfg.bootstrap_replicas:
        rng = np.random.default_rng(np.random.SeedSequence([cfg.semilla_bootstrap, attempt]))
        draws = rng.integers(0, bank.L, size=bank.L)
        multiplicity = np.bincount(draws, minlength=bank.L)
        try:
            b, n, it = _bootstrap_fit(ctx, multiplicity)
            if not np.isfinite(b).all(): raise ValueError("Coeficiente no finito")
            rows.append({"replica_valida": len(rows)+1, "intento": attempt,
                "n_filas_con_multiplicidad": n,
                "localidades_distintas": int((multiplicity > 0).sum()), "iteraciones_Newton": it,
                **dict(zip(names, b))})
        except (ValueError, RuntimeError, np.linalg.LinAlgError) as exc:
            failures.append({"intento": attempt, "error": str(exc)})
        attempt += 1
        if attempt > cfg.bootstrap_replicas*1.1+50:
            raise RuntimeError("Demasiados fallos de bootstrap; revisar el diagnóstico")
        if len(rows) and len(rows) % 100 == 0:
            table(ctx, "bootstrap_coeficientes_replicas", rows)
            print(f"Bootstrap: {len(rows)}/{cfg.bootstrap_replicas} válidas; "
                  f"{len(failures)} fallos; {time.monotonic()-t0:.1f} s", flush=True)
    boot = table(ctx, "bootstrap_coeficientes_replicas", rows)
    table(ctx, "bootstrap_ajustes_fallidos", pd.DataFrame(failures, columns=["intento", "error"]))
    print("Calculando jackknife de 49 localidades para influencia y aceleración BCa...", flush=True)
    jack, influence = [], []
    original = np.asarray(model["fit"].params)
    for loc in range(bank.L):
        counts = np.ones(bank.L, dtype=int); counts[loc] = 0
        b, n, it = _bootstrap_fit(ctx, counts)
        jack.append(b)
        influence.append({"localidad_omitida": bank.locations[loc], "n_train": n,
            "max_cambio_absoluto_beta_referencia": np.max(np.abs(b[1:]-original[1:])),
            **{"cambio_"+name: delta for name, delta in zip(names, b-original)}})
    jack = np.array(jack)
    table(ctx, "jackknife_localidades_influencia", pd.DataFrame(influence).sort_values(
        "max_cambio_absoluto_beta_referencia", ascending=False))
    summary, conv = [], []
    wald = _coef_table(model).set_index("termino")
    for j, name in enumerate(names):
        draws = boot[name].to_numpy(); hat = original[j]
        lo, hi = np.quantile(draws, [.025, .975])
        delta = jack[:, j].mean()-jack[:, j]
        acceleration = np.sum(delta**3)/(6*np.sum(delta**2)**1.5) if np.sum(delta**2) > 0 else 0
        bias_fraction = (np.sum(draws < hat)+.5*np.sum(draws == hat))/len(draws)
        z0 = st.norm.ppf(np.clip(bias_fraction, .5/len(draws), 1-.5/len(draws)))
        za = st.norm.ppf([.025, .975])
        aa = st.norm.cdf(z0+(z0+za)/(1-acceleration*(z0+za)))
        bca_lo, bca_hi = np.quantile(draws, np.clip(aa, 0, 1))
        sign = np.mean(draws > 0) if hat >= 0 else np.mean(draws < 0)
        summary.append({"termino": name, "beta_referencia": hat,
            "ic_Wald_beta_inf": wald.loc[name, "ic_wald_beta_inf"],
            "ic_Wald_beta_sup": wald.loc[name, "ic_wald_beta_sup"],
            "ic_percentil_beta_inf": lo, "ic_percentil_beta_sup": hi,
            "ic_BCa_beta_inf": bca_lo, "ic_BCa_beta_sup": bca_hi,
            "OR": np.exp(hat), "ic_percentil_OR_inf": np.exp(lo),
            "ic_percentil_OR_sup": np.exp(hi), "ic_BCa_OR_inf": np.exp(bca_lo),
            "ic_BCa_OR_sup": np.exp(bca_hi), "frecuencia_signo_conservado": sign,
            "ic_percentil_incluye_cero": lo <= 0 <= hi,
            "ic_BCa_incluye_cero": bca_lo <= 0 <= bca_hi,
            "DE_bootstrap": np.std(draws, ddof=1), "aceleracion_BCa": acceleration,
            "z0_BCa": z0, "clasificacion": "Signo estable, condicional al modelo" if lo*hi > 0
                else "Signo inestable: intervalo incluye cero"})
        for prefix in sorted({min(k, len(draws)) for k in (200, 500, 1000, cfg.bootstrap_replicas)}):
            a, b = np.quantile(draws[:prefix], [.025, .975])
            conv.append({"termino": name, "replicas": prefix, "inferior": a, "superior": b,
                "cambio_max_vs_final": max(abs(a-lo), abs(b-hi))})
    ctx.update({"bootstrap": table(ctx, "bootstrap_intervalos_coeficientes_OR", summary),
                "bootstrap_draws": boot, "jackknife": pd.DataFrame(influence),
                "bootstrap_failures": failures, "bootstrap_attempts": attempt,
                "bootstrap_seconds": time.monotonic()-t0})
    table(ctx, "bootstrap_convergencia_intervalos", conv)
    ctx["checks"]["bootstrap_replicas_validas_y_localidades"] = len(boot) == cfg.bootstrap_replicas and len(jack) == 49
    ctx["checks"]["bootstrap_escala_comun_coeficientes_y_OR"] = True
    return ctx["bootstrap"]


def diagnosticar(ctx):
    m = ctx["best"]; X = m["design"].to_numpy(); y = m["y"].to_numpy()
    vif = pd.DataFrame([{"predictor": p, "VIF": variance_inflation_factor(X, j)}
        for j, p in enumerate(["const"]+m["features"]) if j])
    ctx["vif"] = table(ctx, "diagnostico_VIF", vif)
    # Box-Tidwell con desplazamiento positivo; lectura exploratoria bajo ajuste ponderado.
    nonlinearity = []
    weights, _ = class_weights(y)
    for j, p in enumerate(m["features"], 1):
        if p.startswith("Cloud"): continue  # Nubosidad ordinal, interpretación por octas/código.
        rawx = X[:, j]*m["scale"][j-1]+m["mean"][j-1]
        shift = max(0, 1-float(rawx.min()))
        positive = rawx+shift
        q = positive*np.log(positive)
        q = (q-q.mean())/q.std()
        augmented = np.column_stack([X, q])
        _, ll, _ = logit_fast(augmented, y, weights)
        lr = max(0, 2*(ll-float(m["fit"].llf)))
        nonlinearity.append({"predictor": p, "desplazamiento_train": shift,
            "LR_componente_no_lineal": lr, "p_exploratorio_iid": st.chi2.sf(lr, 1),
            "reduccion_deviance_relativa": lr/float(m["fit"].deviance)})
    dnl = pd.DataFrame(nonlinearity)
    dnl["p_Bonferroni"] = np.minimum(1, dnl.p_exploratorio_iid*len(dnl))
    ctx["nonlinearity"] = table(ctx, "diagnostico_linealidad_logit", dnl)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        influence = m["fit"].get_influence(observed=False)
    cooks, leverage = influence.cooks_distance[0], influence.hat_matrix_diag
    df = pd.DataFrame({"indice_original": m["X"].index,
        "localidad": ctx["train"].loc[m["X"].index, "Location"].to_numpy(),
        "fecha": ctx["train"].loc[m["X"].index, "Date"].dt.strftime("%Y-%m-%d").to_numpy(),
        "y": y, "score": m["fit"].fittedvalues,
        "Cook_D": cooks, "leverage": leverage,
        "residuo_deviance": m["fit"].resid_deviance,
        "residuo_Pearson": m["fit"].resid_pearson})
    table(ctx, "diagnostico_observaciones_influyentes_top20", df.nlargest(20, "Cook_D"))
    ctx["residuals"] = df
    ctx["influence_summary"] = {"n_Cook_mayor_4_sobre_n": int((cooks > 4/len(y)).sum()),
        "umbral_descriptivo": 4/len(y), "max_Cook_D": float(cooks.max()),
        "max_leverage": float(leverage.max()),
        "observaciones_eliminadas_por_este_diagnostico": 0,
        "normalidad_residuos_logisticos_requerida": False}
    p = m["oof"]
    cal = pd.DataFrame({"score": p, "y": ctx["train"].y})
    cal["grupo"] = pd.qcut(cal.score, 10, duplicates="drop")
    cal = cal.groupby("grupo", observed=True).agg(score=("score", "mean"),
        frecuencia_lluvia=("y", "mean"), n=("y", "size")).reset_index(drop=True)
    ctx["calibration"] = table(ctx, "diagnostico_calibracion_OOF", cal)
    return vif


def simulacion_decision(ctx):
    """Ampliación S3: capacidad para días de lluvia en un escenario de 30 días.

    Frecuencias empíricas de entrenamiento, separadas por Humidity3pm>=70.
    Escenario condicional iid y parámetros fijos, no pronóstico de fechas reales.
    """
    cfg = ctx["cfg"]
    train = ctx["train"].dropna(subset=["Humidity3pm"])
    rows, draws_rows, convergence = [], [], []
    for i, (name, mask) in enumerate([
        ("Humedad >=70%", train.Humidity3pm >= 70),
        ("Humedad <70%", train.Humidity3pm < 70)]):
        subset = train.loc[mask]; probability = subset.y.mean()
        rng = np.random.default_rng(np.random.SeedSequence([cfg.semilla_mc, i]))
        draws = rng.binomial(30, probability, cfg.montecarlo_iteraciones)
        # Cuantil discreto superior: capacidad que cubre al menos el 95% de escenarios.
        capacity = int(np.quantile(draws, .95, method="higher"))
        extremes = int((draws > 15).sum())
        upper_mc = st.beta.ppf(.95, extremes+1, len(draws)-extremes) if extremes < len(draws) else 1.
        rows.append({"escenario": name, "n_calibracion_train": len(subset),
            "probabilidad_empirica_train": probability, "dias_escenario": 30,
            "iteraciones": len(draws), "media_dias_lluvia": draws.mean(),
            "media_teorica": 30*probability, "DE_dias_lluvia": draws.std(ddof=1),
            "MCSE_media": draws.std(ddof=1)/np.sqrt(len(draws)),
            "capacidad_dias_riesgo_5pct": capacity,
            "probabilidad_exceder_15_dias": float(np.mean(draws > 15)),
            "excedencias_15_observadas": extremes,
            "probabilidad_exacta_iid_exceder_15": st.binom.sf(15, 30, probability),
            "cota_superior_MC_95_evento_exceder_15": upper_mc,
            "riesgo_operativo_supuesto": .05})
        for n in (100, 500, 1000, 5000, cfg.montecarlo_iteraciones):
            z = draws[:n]
            convergence.append({"escenario": name, "iteraciones": len(z),
                "media_dias_lluvia": z.mean(), "media_teorica": 30*probability,
                "MCSE_media": z.std(ddof=1)/np.sqrt(len(z)),
                "capacidad_95": np.quantile(z, .95, method="higher")})
        draws_rows.extend({"escenario": name, "replica": j+1, "dias_lluvia": int(v)}
                           for j, v in enumerate(draws))
    ctx["mc"] = table(ctx, "montecarlo_decision_resumen", rows)
    ctx["mc_draws"] = table(ctx, "montecarlo_decision_distribuciones", draws_rows)
    table(ctx, "montecarlo_decision_convergencia", convergence)
    ctx["checks"]["simulacion_decision_calibrada_solo_train"] = True
    return ctx["mc"]


def graficar(ctx):
    """Figuras estadísticas con datos de la ejecución actual."""
    bank, best = ctx["bank"], ctx["best"]
    sd = bank.sunshine_diagnostic
    fig, ax = plt.subplots(1, 2, figsize=(10, 3.7), constrained_layout=True)
    ax[0].hexbin(sd["actual"], sd["prediction"], gridsize=35, mincnt=1, cmap="Blues")
    ax[0].plot([0, 15], [0, 15], ls="--", color=RED)
    ax[0].set(xlabel="Sunshine observado (horas)", ylabel="Reconstrucción por regresión (horas)",
              title="Validación interna de donantes")
    st.probplot(sd["residual"], plot=ax[1])
    ax[1].set(title="QQ de residuos de reconstrucción", xlabel="Cuantiles normales", ylabel="Residuo (horas)")
    _savefig(ctx, "01_imputacion_regresion", fig)

    tr = ctx["train"]
    fig, ax = plt.subplots(1, 2, figsize=(10, 3.8), constrained_layout=True)
    miss = tr[ctx["numeric"]].isna().mean().sort_values(ascending=False).head(8)*100
    ax[0].barh(miss.index[::-1], miss.to_numpy()[::-1], color=BLUE)
    ax[0].set(xlabel="Faltantes de entrenamiento (%)", title="Patrón documentado en S1")
    for label, z, color in [
        ("Observado", tr.Sunshine.dropna(), BLUE),
        ("Mediana", bank.transform(tr, "mediana").Sunshine, ORANGE),
        ("Regresión", bank.transform(tr, "regresion").Sunshine, TEAL)]:
        ax[1].hist(z, bins=np.arange(0, 15.6, .5), histtype="step", density=True,
                   label=label, color=color, linewidth=1.5)
    ax[1].set(xlabel="Horas de sol", ylabel="Densidad", title="Imputación de Sunshine en train")
    ax[1].legend(fontsize=8)
    _savefig(ctx, "02_faltantes_distribuciones", fig)

    fig, ax = plt.subplots(1, 2, figsize=(10, 4), constrained_layout=True)
    for (name, model), color in zip(ctx["models"].items(), (BLUE, TEAL, ORANGE)):
        p = model["p_test"]; fpr, tpr, _ = roc_curve(ctx["test"].y, p)
        auc = roc_auc_score(ctx["test"].y, p)
        ax[0].plot(fpr, tpr, color=color, label=f'{name[:2]} AUC={auc:.3f}')
    ax[0].plot([0, 1], [0, 1], ls="--", color="gray", lw=.8)
    ax[0].set(xlabel="Tasa de falsos positivos", ylabel="Recall", title="ROC en prueba")
    ax[0].legend(loc="lower right", fontsize=9)
    rows = ctx["metrics"].query("conjunto == 'test' and regla_umbral == 'F1_OOF'").set_index("modelo")
    x = np.arange(3)
    for j, metric in enumerate(("precision", "recall", "f1")):
        ax[1].bar(x+(j-1)*.24, rows.loc[MODEL_NAMES, metric], width=.23,
                   label=metric, color=(BLUE, TEAL, ORANGE)[j])
    ax[1].set(xticks=x, xticklabels=["M1", "M2", "M3"], ylim=(0, 1),
              title="Métricas con umbrales F1 OOF", ylabel="Valor")
    ax[1].legend(fontsize=9)
    _savefig(ctx, "03_modelos_roc_metricas", fig)

    fig, ax = plt.subplots(2, 3, figsize=(10, 5.6), constrained_layout=True)
    for j, name in enumerate(MODEL_NAMES):
        for i, label in enumerate(("train", "test")):
            row = ctx["metrics"].query("modelo == @name and conjunto == @label and regla_umbral == 'F1_OOF'").iloc[0]
            arr = np.array([[row.tn, row.fp], [row.fn, row.tp]], float)
            normalized = arr/arr.sum(axis=1, keepdims=True)
            a = ax[i, j]; a.imshow(normalized, vmin=0, vmax=1, cmap="Blues")
            for (r, c), value in np.ndenumerate(arr):
                a.text(c, r, f"{int(value):,}\n{normalized[r,c]:.1%}", ha="center", va="center",
                       color="white" if normalized[r,c] > .55 else BLUE, fontsize=9)
            a.set(xticks=[0, 1], yticks=[0, 1], xticklabels=["No", "Yes"], yticklabels=["No", "Yes"],
                  xlabel="Predicción", ylabel="Real", title=f"{name[:2]} · {label}")
    _savefig(ctx, "04_matrices_confusion", fig)

    b = ctx["bootstrap"].query("termino != 'const'").copy()
    fig, ax = plt.subplots(figsize=(8, max(3.4, .42*len(b)+.8)), constrained_layout=True)
    for j, row in enumerate(b.itertuples()):
        color = TEAL if not row.ic_percentil_incluye_cero else ORANGE
        ax.plot([np.exp(row.ic_Wald_beta_inf), np.exp(row.ic_Wald_beta_sup)], [j+.08, j+.08],
                color="gray", lw=1.3)
        ax.plot([row.ic_percentil_OR_inf, row.ic_percentil_OR_sup], [j-.04, j-.04], color=color, lw=2.5)
        ax.scatter(row.OR, j-.04, color=color, s=28, zorder=4)
    ax.axvline(1, ls="--", color=RED, lw=1)
    ax.set(yticks=np.arange(len(b)), yticklabels=b.termino, xscale="log",
           xlabel="OR por una DE de referencia (escala logarítmica)",
           title="IC 95%: Wald (gris) y bootstrap percentil (color)")
    ax.invert_yaxis(); ax.grid(axis="x", alpha=.2)
    _savefig(ctx, "05_bootstrap_OR", fig)

    features = best["features"][:3]
    if len(best["features"]) > 3: features += [best["features"][-1]]
    fig, axes = plt.subplots(2, 2, figsize=(9, 5.3), constrained_layout=True)
    for ax, col in zip(axes.flat, features):
        values = ctx["bootstrap_draws"][col]
        ax.hist(values, bins=35, color=TEAL, alpha=.8)
        lo, hi = np.quantile(values, [.025, .975])
        ax.axvline(lo, color=ORANGE, ls="--"); ax.axvline(hi, color=ORANGE, ls="--")
        ax.axvline(0, color=RED, lw=.8)
        ax.set(title=col, xlabel="Coeficiente en escala de referencia", ylabel="Remuestras")
    for ax in list(axes.flat)[len(features):]: ax.set_visible(False)
    _savefig(ctx, "06_bootstrap_distribuciones", fig)

    fig, ax = plt.subplots(1, 2, figsize=(10, 3.8), constrained_layout=True)
    rr = ctx["residuals"].iloc[::max(1, len(ctx["residuals"])//6000)]
    ax[0].scatter(rr.score, rr.residuo_deviance, alpha=.12, s=3, color=BLUE)
    ax[0].axhline(0, color="gray", lw=.8)
    ax[0].set(xlabel="Score ponderado", ylabel="Residuo de deviance",
              title="Residuos en entrenamiento")
    cal = ctx["calibration"]
    ax[1].plot(cal.score, cal.frecuencia_lluvia, "o-", color=TEAL)
    ax[1].plot([0, 1], [0, 1], ls="--", color="gray")
    ax[1].set(xlabel="Score medio fuera de pliegue", ylabel="Frecuencia observada de lluvia",
              title="Calibración OOF de entrenamiento", xlim=(0, 1), ylim=(0, 1))
    _savefig(ctx, "07_diagnostico", fig)

    imp = ctx["imputation_comparison"]
    common = imp.query("poblacion_prueba == 'casos_comunes'")
    available = imp.query("poblacion_prueba == 'disponible_por_estrategia'")
    fig, ax = plt.subplots(1, 2, figsize=(10, 3.7), constrained_layout=True)
    labels = ["Eliminación", "Mediana", "Regresión"]
    ax[0].bar(labels, available.cobertura_test*100, color=[ORANGE, BLUE, TEAL])
    ax[0].set(ylabel="Cobertura de prueba (%)", ylim=(0, 110), title="Misma especificación logística")
    ax[1].bar(labels, common.auc, color=[ORANGE, BLUE, TEAL])
    ax[1].set(ylabel="ROC-AUC", ylim=(.5, 1), title=f"Casos comunes de prueba (n={int(common.iloc[0]['n']):,})")
    _savefig(ctx, "08_impacto_imputacion", fig)

    fig, ax = plt.subplots(1, 2, figsize=(10, 3.7), constrained_layout=True)
    for a, row in zip(ax, ctx["mc"].itertuples()):
        values = ctx["mc_draws"].loc[ctx["mc_draws"].escenario.eq(row.escenario), "dias_lluvia"]
        hist = np.bincount(values, minlength=31)/len(values)
        a.bar(np.arange(31), hist, color=TEAL if ">=" in row.escenario else BLUE)
        a.axvline(row.capacidad_dias_riesgo_5pct, color=ORANGE, ls="--",
                  label=f"Capacidad 95%: {row.capacidad_dias_riesgo_5pct} días")
        a.set(title=f"{row.escenario} · p={row.probabilidad_empirica_train:.3f}",
              xlabel="Días de lluvia en escenario de 30 días", ylabel="Frecuencia simulada")
        a.legend(fontsize=8)
    _savefig(ctx, "09_montecarlo_decision", fig)
    print("Nueve figuras estadísticas exportadas.")


def exportar(ctx):
    model = ctx["best"]
    raw = ctx["raw"]
    sources = {"S1": "134859256a519e0ffde2827319d73a603598e0ea",
               "S2": "e802fc457e97a9b42d28b45f9f11a61df865b446", "base": BASE_COMMIT}
    out = {
        "evaluacion": "Sumativa 3, Fase 4", "grupo": 7,
        "integrantes": ["Benjamín Araya", "Alan Cañete", "Patricio Cortez", "Jorge Guaico"],
        "rubrica_maximo": 108, "puntajes_criterios": [21, 30, 30, 9, 9, 9],
        "fuentes_proyecto": sources, "semillas_y_replicas": vars(ctx["cfg"]),
        "dataset": {"sha256": DATA_SHA256, "filas_originales": len(raw),
            "columnas": raw.shape[1], "respuestas_conocidas": len(ctx["df"]),
            "respuestas_ausentes_excluidas": int(raw.RainTomorrow.isna().sum()),
            "localidades": raw.Location.nunique(), "n_train": len(ctx["train"]), "n_test": len(ctx["test"]),
            "porcentaje_lluvia": 100*ctx["df"].y.mean(),
            "Sunshine_faltantes_todos_pct": 100*raw.Sunshine.isna().mean(),
            "Sunshine_faltantes_respuesta_conocida_pct": 100*ctx["df"].Sunshine.isna().mean(),
            "localidades_sin_Sunshine": raw.groupby("Location").Sunshine.count().eq(0).sum()},
        "referencia_F2_reproducida": ctx["f2"],
        "imputacion": {"estrategia_principal": ctx["primary"],
            "regla": "Reducción RMSE Sunshine >=5% en validación interna de donantes; si no, mediana",
            "reduccion_RMSE_Sunshine": ctx["imputer_rmse_improvement"],
            "diagnosticos_16_regresiones": ctx["imputer_diagnostics"].to_dict("records"),
            "modelos": {k: {a: v for a, v in m.items() if a in ("predictors", "center", "scale", "beta", "donors")}
                        for k, m in ctx["bank"].models.items()}},
        "seleccion_entrenamiento": ctx["cv_summary"].to_dict("records"),
        "modelo_final": {"nombre": model["name"], "predictores": model["features"],
            "estrategia": ctx["primary"], "umbral": model["threshold"],
            "parametros_estandarizados": dict(zip(["const"]+model["features"], model["fit"].params)),
            "medias_referencia": dict(zip(model["features"], model["mean"])),
            "DE_referencia": dict(zip(model["features"], model["scale"])),
            "pesos_clase": {"No": model["class_weights"][0], "Yes": model["class_weights"][1]},
            "criterio": "AUC OOF máxima, con margen 0.002 de parsimonia; umbral F1 OOF",
            "score": "Logit ponderado por clase; no calibrado como probabilidad operacional"},
        "coeficientes_modelo_final": _coef_table(model).to_dict("records"),
        "metricas_tres_modelos": ctx["metrics"].to_dict("records"),
        "bootstrap": {"validas": len(ctx["bootstrap_draws"]), "intentos": ctx["bootstrap_attempts"],
            "fallos": ctx["bootstrap_failures"], "unidad": "Localidad: 49 conglomerados de entrenamiento",
            "condicional_a": "Especificación logística y predictores de imputación seleccionados; no repite stepwise",
            "reajusta": "Regresiones de imputación, medianas auxiliares, escala y pesos de clase",
            "intervalos": ctx["bootstrap"].to_dict("records"),
            "jackknife_top3": ctx["jackknife"].nlargest(3, "max_cambio_absoluto_beta_referencia").to_dict("records")},
        "diagnosticos": {"VIF": ctx["vif"].to_dict("records"),
            "linealidad_logit": ctx["nonlinearity"].to_dict("records"),
            "influencia": ctx["influence_summary"]},
        "impacto_imputacion": ctx["imputation_comparison"].to_dict("records"),
        "coeficientes_impacto_escala_comun": ctx["imputation_coefs"].to_dict("records"),
        "montecarlo_decision_ampliacion_S3": ctx["mc"].to_dict("records"),
        "limites": [
            "Partición aleatoria estratificada exigida: no prueba pronóstico futuro ni localidades nuevas.",
            "El conjunto completo se exploró en S1/S2 y la prueba fue observada en F2; evaluación comparativa del proyecto.",
            "Independencia entre localidades y muestreo nacional representativo no demostrados.",
            "Faltantes por estación: MAR condicionado a covariables es un supuesto; MNAR no descartado.",
            "Regresión determinista: varianza y correlaciones pueden alterarse; remuestreo no resuelve MNAR.",
            "Intervalos bootstrap condicionados a especificaciones; excluyen incertidumbre de selección de variables.",
            "Scores ponderados no calibrados; coeficientes asociativos, sin interpretación causal.",
            "Monte Carlo: escenario iid con frecuencias fijas de entrenamiento, no pronóstico de 30 fechas reales."]}
    path = ctx["output"]/"resultados_validados_s3.json"
    write_json(path, out); ctx["results"] = _clean(out)
    print("Resultados y decisiones exportados a", path.relative_to(ROOT) if path.is_relative_to(ROOT) else path.name)
    return ctx["results"]


def validar(ctx):
    checks = ctx["checks"].copy()
    checks["dataset_original_sin_modificaciones"] = sha256(ctx["data_path"]) == DATA_SHA256
    checks["fuentes_analiticas_previas_sin_modificar"] = all(
        sha256(ROOT/p) == h for p, h in ctx["source_hashes"].items())
    checks["tres_modelos_requeridos"] = set(ctx["models"]) == set(MODEL_NAMES)
    checks["M3_reducido_propio_subconjunto_dominio"] = set(ctx["models"][MODEL_NAMES[2]]["features"]) < set(DOMAIN)
    checks["coeficientes_intervalos_finitos_y_ordenados"] = all(
        np.isfinite(ctx["bootstrap"][["ic_percentil_beta_inf", "ic_percentil_beta_sup", "OR"]]).all().all()
        and (ctx["bootstrap"].ic_percentil_beta_inf < ctx["bootstrap"].ic_percentil_beta_sup).all()
        for _ in [0])
    predictions = pd.read_csv(ctx["tables"]/"predicciones_prueba_tres_modelos.csv")
    ok = True
    for name, model in ctx["models"].items():
        recalculated = metrics(predictions.y_real, predictions["score_"+name], model["threshold"])
        stored = ctx["metrics"].query("modelo == @name and conjunto == 'test' and regla_umbral == 'F1_OOF'").iloc[0]
        for metric in ("accuracy", "precision", "recall", "f1", "auc", "tn", "fp", "fn", "tp"):
            ok &= bool(np.isclose(recalculated[metric], stored[metric], rtol=0, atol=1e-10))
    checks["metricas_recalculadas_desde_predicciones_exportadas"] = ok
    for row in ctx["bootstrap"].itertuples():
        low, high = np.quantile(ctx["bootstrap_draws"][row.termino], [.025, .975])
        np.testing.assert_allclose([low, high], [row.ic_percentil_beta_inf, row.ic_percentil_beta_sup], atol=1e-12)
        np.testing.assert_allclose(np.exp([low, high]), [row.ic_percentil_OR_inf, row.ic_percentil_OR_sup], atol=1e-12)
    checks["cuantiles_bootstrap_y_transformacion_OR_conciliados"] = True
    checks["nueve_figuras_exportadas"] = len(list(ctx["figures"].glob("*.png"))) == 9
    checks["modelo_umbrales_imputacion_no_cambiaron_tras_prueba"] = sha256(
        ctx["output"]/"decision_congelada_entrenamiento.json") == ctx["frozen_hash"]
    if not all(checks.values()): raise AssertionError({k: v for k, v in checks.items() if not v})
    env = "windows" if platform.system() == "Windows" else "work"
    files = sorted(p for p in ctx["output"].rglob("*") if p.is_file()) + [Path(__file__)]
    full = ctx["cfg"].bootstrap_replicas >= 2000 and ctx["cfg"].folds == 5
    evidence = {"fecha_utc": datetime.now(timezone.utc).isoformat(), "entorno": env,
        "perfil_plan_aprobado_completo": full,
        "sistema": platform.system(), "python": platform.python_version(),
        "versiones": {p: version(p) for p in ("numpy", "pandas", "scipy", "statsmodels", "scikit-learn", "matplotlib", "ipykernel", "nbformat")},
        "base_commit": BASE_COMMIT, "dataset_sha256": DATA_SHA256,
        "configuracion": vars(ctx["cfg"]), "controles": checks,
        "tiempo_total_segundos": time.monotonic()-ctx["start"],
        "bootstrap_segundos": ctx["bootstrap_seconds"],
        "ejecucion_windows_acreditada_por_este_registro": env == "windows",
        "archivos_sha256": {str(p.relative_to(ROOT)).replace(os.sep, "/") if p.is_relative_to(ROOT) else p.name: sha256(p) for p in files}}
    if ctx["output"] == ROOT/"results/05_sumativa3":
        destination = ROOT/f"evidence/05_sumativa3/ejecucion_sumativa3_{env}.json"
    else: destination = ctx["output"]/f"ejecucion_piloto_{env}.json"
    write_json(destination, evidence)
    print("SUMATIVA 3 - EJECUCIÓN COMPLETA: CORRECTA" if full else "PILOTO S3 - EJECUCIÓN COMPLETA: CORRECTA")
    print("Controles numéricos y trazabilidad: correctos")
    print("CSV original sin modificaciones:", checks["dataset_original_sin_modificaciones"])
    print("Entorno ejecutado:", env)
    print("Evidencia:", destination.name)
    print("Video grupal y entrega Canvas: requieren evidencia del grupo.")
    return evidence


def interpretar(ctx, section):
    """Texto del notebook construido con los resultados actuales, sin cifras pegadas."""
    if section == "imputacion":
        row = ctx["imputer_diagnostics"].set_index("variable").loc["Sunshine"]
        return (f"**Reconstrucción de Sunshine:** RMSE de {row.rmse_mediana:.3f} horas con mediana y "
            f"{row.rmse_regresion:.3f} con regresión, una reducción de {ctx['imputer_rmse_improvement']:.1%}. "
            f"La regla de entrenamiento seleccionó **{ctx['primary']}**. Los donantes completos no representan "
            "las 19 localidades sin Sunshine. Los rechazos de normalidad y homocedasticidad se conservan "
            "como limitaciones; la regresión predice un valor condicional, no reconstruye la variabilidad desconocida.")
    if section == "modelos":
        return (f"La selección OOF eligió **{ctx['best']['name']}** con {len(ctx['best']['features'])} predictores. "
            f"Su umbral {ctx['best']['threshold']:.4f} maximiza F1 OOF. La selección AIC/BIC es no ponderada y "
            "usa las mismas filas; los modelos predictivos se reajustan con pesos balanceados. "
            "M3 minimiza BIC entre subconjuntos de uno a tres predictores de dominio, no entre todos los modelos posibles.")
    if section == "rendimiento":
        name = ctx["best"]["name"]
        row = ctx["metrics"].query("modelo == @name and conjunto == 'test' and regla_umbral == 'F1_OOF'").iloc[0]
        return (f"En esta prueba, AUC={row.auc:.4f}, recall={row.recall:.2%}, precision={row.precision:.2%} "
            f"y accuracy={row.accuracy:.2%}. Quedan {int(row.fn):,} días de lluvia sin detectar. "
            f"F2 tenía recall={ctx['f2']['recall']:.2%} y accuracy={ctx['f2']['accuracy']:.2%}. "
            "La comparación cambia variables, imputación, pesos y umbral: no atribuye la mejora a una sola causa. "
            "El score ponderado necesita calibración antes de interpretarse como probabilidad operacional.")
    if section == "bootstrap":
        b = ctx["bootstrap"].query("termino != 'const'")
        unstable = b.loc[b.ic_percentil_incluye_cero, "termino"].tolist()
        return (f"Se obtuvieron **{len(ctx['bootstrap_draws']):,} réplicas válidas** y "
            f"{len(ctx['bootstrap_failures'])} fallos. Los intervalos percentil incluyen cero para: "
            f"{', '.join(unstable) if unstable else 'ningún predictor'}. "
            "Las DE y medianas se reajustan en cada remuestra. Las betas se expresan en una escala de referencia común. "
            "La frecuencia de signo es descriptiva, no una probabilidad posterior. La inferencia queda condicionada "
            "a los predictores seleccionados y a localidades aproximadamente independientes.")
    if section == "impacto":
        rows = ctx["imputation_comparison"]
        deletion = rows.query("estrategia == 'eliminacion' and poblacion_prueba == 'disponible_por_estrategia'").iloc[0]
        return (f"La eliminación cubre {deletion.cobertura_test:.2%} de prueba y {int(deletion.localidades_test)} "
            "localidades. Su AUC disponible no es directamente comparable con el de métodos que conservan toda "
            "la muestra. La tabla de casos comunes controla el conjunto evaluado. Los coeficientes se comparan "
            "por la misma DE de referencia, evitando confundir cambios de escala con cambios de efecto.")
    if section == "decision":
        a, b = list(ctx["mc"].itertuples())
        return (f"Para el escenario hipotético de 30 días con humedad >=70%, la capacidad al 95% es "
            f"{a.capacidad_dias_riesgo_5pct} días de lluvia; para humedad menor es {b.capacidad_dias_riesgo_5pct}. "
            "El riesgo de excedencia del 5% es un supuesto de planificación. Se usan frecuencias empíricas de "
            "entrenamiento y días iid. No representa un pronóstico de fechas futuras ni incorpora toda la "
            "incertidumbre climática o de estimación.")
    return ""


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bootstrap", type=int, default=2000)
    parser.add_argument("--folds", type=int, default=5)
    parser.add_argument("--salida", type=Path)
    args = parser.parse_args()
    ctx = iniciar(Config(bootstrap_replicas=args.bootstrap, folds=args.folds), args.salida)
    for fun in (reproducir_f2, estudiar_imputacion, ajustar_modelos, evaluar_modelos,
                comparar_imputacion, bootstrap_modelo, diagnosticar, simulacion_decision,
                graficar, exportar, validar):
        print("ETAPA:", fun.__name__, flush=True); fun(ctx)


if __name__ == "__main__": main()
