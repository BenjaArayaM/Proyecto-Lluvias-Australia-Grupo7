from pathlib import Path
import time
import warnings

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats


# ============================================================
# CONFIGURACIÓN
# ============================================================

SEED = 20261018
B_PERMUTACIONES = 10_000
B_BOOTSTRAP = 10_000
ALPHA = 0.05

RUTA_DATOS = Path("data/raw/weatherAUS.csv")
RUTA_RESULTADOS = Path("results/03_sumativa2")
RUTA_TABLAS = RUTA_RESULTADOS / "tables"
RUTA_FIGURAS = RUTA_RESULTADOS / "figures"

for carpeta in (RUTA_TABLAS, RUTA_FIGURAS):
    carpeta.mkdir(parents=True, exist_ok=True)

rng = np.random.default_rng(SEED)


# ============================================================
# CARGA Y VALIDACIÓN DE DATOS
# ============================================================

if not RUTA_DATOS.exists():
    raise FileNotFoundError(
        f"No se encontró {RUTA_DATOS}. "
        "Ejecuta el script desde la raíz del repositorio."
    )

df = pd.read_csv(RUTA_DATOS, low_memory=False)

columnas_requeridas = {
    "Location",
    "RainTomorrow",
    "Humidity3pm",
    "MaxTemp",
    "Temp3pm",
    "Sunshine",
    "Rainfall",
}

faltantes = columnas_requeridas - set(df.columns)
if faltantes:
    raise ValueError(f"Faltan columnas requeridas: {sorted(faltantes)}")

df["RainTomorrow"] = df["RainTomorrow"].astype("string").str.strip()

print("=" * 70)
print("SUMATIVA 2: VALIDACIÓN POR PERMUTACIÓN Y ESTABILIDAD")
print("=" * 70)
print(f"Filas cargadas: {len(df):,}")
print(f"Localidades identificadas: {df['Location'].nunique()}")
print(f"Semilla aleatoria: {SEED}")
print(f"Permutaciones: {B_PERMUTACIONES:,}")
print(f"Réplicas bootstrap por correlación: {B_BOOTSTRAP:,}")


# ============================================================
# PUNTO 2. PRUEBA DE HIPÓTESIS MEDIANTE PERMUTACIÓN
#
# Variable: Humidity3pm
# Grupos: RainTomorrow = Yes / No
# Unidad de análisis: localidad
#
# Para cada localidad:
# D_i = media(Humidity3pm | RainTomorrow=Yes)
#       - media(Humidity3pm | RainTomorrow=No)
#
# H0: media de las diferencias = 0
# H1: media de las diferencias != 0
# ============================================================

print("\n" + "=" * 70)
print("PUNTO 2: PRUEBA DE HIPÓTESIS POR PERMUTACIÓN")
print("=" * 70)

datos_test = df.loc[
    df["RainTomorrow"].isin(["Yes", "No"]),
    ["Location", "RainTomorrow", "Humidity3pm"],
].copy()

datos_test["Humidity3pm"] = pd.to_numeric(
    datos_test["Humidity3pm"], errors="coerce"
)
datos_test = datos_test.dropna(
    subset=["Location", "RainTomorrow", "Humidity3pm"]
)

medias = (
    datos_test
    .groupby(["Location", "RainTomorrow"])["Humidity3pm"]
    .mean()
    .unstack()
)

# Conservar solo localidades que tengan observaciones de ambos grupos.
medias = medias.dropna(subset=["Yes", "No"])

diferencias = medias["Yes"] - medias["No"]
diferencias = diferencias.astype(float)

if len(diferencias) < 2:
    raise ValueError(
        "No hay suficientes localidades con datos de ambos grupos."
    )

n_localidades = len(diferencias)
diferencias_array = diferencias.to_numpy()

# Estadístico observado: diferencia media entre localidades.
estadistico_observado = float(np.mean(diferencias_array))

# Prueba paramétrica de referencia: t de una muestra sobre D_i.
resultado_t = stats.ttest_1samp(diferencias_array, popmean=0.0)
p_parametrico = float(resultado_t.pvalue)
t_observado = float(resultado_t.statistic)
gl = n_localidades - 1

# Intervalo de confianza paramétrico del 95 % para la media de D_i.
error_estandar = stats.sem(diferencias_array)
t_critico = stats.t.ppf(1 - ALPHA / 2, df=gl)

ic_t_inferior = estadistico_observado - t_critico * error_estandar
ic_t_superior = estadistico_observado + t_critico * error_estandar

# Permutación por inversión de signos a nivel de localidad.
# Esto conserva cada diferencia local y cambia aleatoriamente su signo.
# Es una prueba bilateral para la hipótesis de media nula.
estadisticos_perm = np.empty(B_PERMUTACIONES, dtype=float)

inicio = time.time()

for b in range(B_PERMUTACIONES):
    signos = rng.choice(
        np.array([-1.0, 1.0]),
        size=n_localidades,
        replace=True,
    )
    estadisticos_perm[b] = np.mean(diferencias_array * signos)

    if (b + 1) % 2000 == 0:
        print(f"Permutaciones completadas: {b + 1:,}/{B_PERMUTACIONES:,}")

# Corrección +1: evita informar p = 0 en una simulación Monte Carlo.
extremos = np.sum(
    np.abs(estadisticos_perm) >= abs(estadistico_observado)
)
p_permutacion = (extremos + 1) / (B_PERMUTACIONES + 1)

resumen_perm = pd.DataFrame([{
    "variable": "Humidity3pm",
    "grupo_yes": "RainTomorrow=Yes",
    "grupo_no": "RainTomorrow=No",
    "unidad_analisis": "Location",
    "n_localidades": n_localidades,
    "n_permutaciones": B_PERMUTACIONES,
    "media_diferencias_pp": estadistico_observado,
    "ic95_t_inferior": ic_t_inferior,
    "ic95_t_superior": ic_t_superior,
    "estadistico_t": t_observado,
    "grados_libertad": gl,
    "p_parametrico_t": p_parametrico,
    "extremos_permutacion": int(extremos),
    "p_permutacion": p_permutacion,
    "alpha": ALPHA,
    "decision_parametrica": (
        "Rechazar H0" if p_parametrico < ALPHA else "No rechazar H0"
    ),
    "decision_permutacion": (
        "Rechazar H0" if p_permutacion < ALPHA else "No rechazar H0"
    ),
    "semilla": SEED,
}])

resumen_perm.to_csv(
    RUTA_TABLAS / "prueba_permutacion_humedad.csv",
    index=False,
)

tabla_diferencias = diferencias.rename(
    "diferencia_humedad_yes_menos_no"
).reset_index()

tabla_diferencias.to_csv(
    RUTA_TABLAS / "diferencias_humedad_por_localidad.csv",
    index=False,
)

# Figura de la distribución nula por permutación.
fig, ax = plt.subplots(figsize=(10, 6))

ax.hist(
    estadisticos_perm,
    bins=50,
    density=True,
    alpha=0.75,
    edgecolor="white",
)

ax.axvline(
    estadistico_observado,
    linestyle="--",
    linewidth=2,
    label=f"Observado = {estadistico_observado:.3f}",
)

ax.axvline(
    -estadistico_observado,
    linestyle=":",
    linewidth=1.5,
    label="Valor observado simétrico",
)

ax.set_title(
    "Prueba de permutación: diferencia de humedad a las 15:00"
)
ax.set_xlabel(
    "Diferencia media de Humidity3pm (Yes − No), en puntos porcentuales"
)
ax.set_ylabel("Densidad")
ax.legend()
fig.tight_layout()

fig.savefig(
    RUTA_FIGURAS / "permutacion_humedad.png",
    dpi=180,
    bbox_inches="tight",
)
plt.close(fig)

print("\nResultados de la prueba de permutación:")
print(resumen_perm.to_string(index=False))
print(f"Tiempo punto 2: {time.time() - inicio:.1f} segundos")


# ============================================================
# PUNTO 3. ESTABILIDAD DE CORRELACIONES MEDIANTE BOOTSTRAP
#
# Correlaciones seleccionadas de la S1:
# 1. MaxTemp - Temp3pm
# 2. Humidity3pm - Sunshine
# 3. Humidity3pm - Rainfall
#
# Unidad de remuestreo: localidad completa.
# En cada réplica se vuelven a calcular los rangos de Spearman
# en la muestra remuestreada.
# ============================================================

print("\n" + "=" * 70)
print("PUNTO 3: ESTABILIDAD DE CORRELACIONES")
print("=" * 70)

pares = [
    ("MaxTemp", "Temp3pm"),
    ("Humidity3pm", "Sunshine"),
    ("Humidity3pm", "Rainfall"),
]

# Preparar los datos por par: se eliminan faltantes por pares,
# no globalmente, para conservar el tamaño muestral de cada correlación.
datos_pares = {}

for x, y in pares:
    temporal = df[["Location", x, y]].copy()
    temporal[x] = pd.to_numeric(temporal[x], errors="coerce")
    temporal[y] = pd.to_numeric(temporal[y], errors="coerce")
    temporal = temporal.dropna(subset=["Location", x, y])

    # Eliminar valores infinitos, si los hubiera.
    temporal = temporal[
        np.isfinite(temporal[x]) & np.isfinite(temporal[y])
    ]

    grupos = []
    for localidad, grupo in temporal.groupby("Location", sort=True):
        xv = grupo[x].to_numpy(dtype=float)
        yv = grupo[y].to_numpy(dtype=float)

        if len(xv) >= 2:
            grupos.append((localidad, xv, yv))

    if len(grupos) < 2:
        raise ValueError(
            f"No hay suficientes localidades para {x} y {y}."
        )

    datos_pares[(x, y)] = {
        "datos": temporal,
        "grupos": grupos,
        "rho_s1": float(stats.spearmanr(
            temporal[x].to_numpy(),
            temporal[y].to_numpy(),
        ).statistic),
        "n_pares": len(temporal),
        "n_localidades": len(grupos),
    }

# Mismas localidades base por par; el bootstrap selecciona localidades
# con reemplazo y concatena todos sus registros válidos para ese par.
resultados_correlaciones = []
distribuciones_bootstrap = {}

for x, y in pares:
    info = datos_pares[(x, y)]
    grupos = info["grupos"]
    n_grupos = len(grupos)

    rho_original = info["rho_s1"]
    n_pares = info["n_pares"]

    print(
        f"\nProcesando {x} vs. {y}: "
        f"n={n_pares:,}; localidades={n_grupos}"
    )

    boot = np.empty(B_BOOTSTRAP, dtype=float)
    inicio_par = time.time()

    for b in range(B_BOOTSTRAP):
        # Remuestreo de conglomerados: se seleccionan tantas localidades
        # como había originalmente, con reemplazo.
        indices = rng.integers(0, n_grupos, size=n_grupos)

        xb = np.concatenate([grupos[i][1] for i in indices])
        yb = np.concatenate([grupos[i][2] for i in indices])

        # Se recalcula Spearman en la muestra remuestreada completa.
        # Esto vuelve a calcular los rangos en cada réplica.
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            rho_b = stats.spearmanr(xb, yb).statistic

        boot[b] = rho_b

        if (b + 1) % 1000 == 0:
            print(
                f"  {x} vs. {y}: "
                f"{b + 1:,}/{B_BOOTSTRAP:,} réplicas"
            )

    # Eliminar posibles resultados no finitos antes de calcular el IC.
    boot_validos = boot[np.isfinite(boot)]

    if len(boot_validos) < 0.95 * B_BOOTSTRAP:
        raise RuntimeError(
            f"Demasiadas réplicas no válidas para {x} vs. {y}: "
            f"{len(boot_validos)}/{B_BOOTSTRAP}"
        )

    ic_inferior, ic_superior = np.quantile(
        boot_validos, [ALPHA / 2, 1 - ALPHA / 2]
    )

    incluye_cero = bool(ic_inferior <= 0 <= ic_superior)
    amplitud_ic = float(ic_superior - ic_inferior)
    desviacion_bootstrap = float(np.std(boot_validos, ddof=1))

    if incluye_cero:
        clasificacion = "Inestable respecto al signo; IC incluye cero"
    elif amplitud_ic < 0.10:
        clasificacion = "Robusta; IC estrecho y excluye cero"
    else:
        clasificacion = "Asociación consistente; IC excluye cero"

    resultados_correlaciones.append({
        "variable_x": x,
        "variable_y": y,
        "n_pares_original": n_pares,
        "n_localidades": n_grupos,
        "rho_spearman_s1": rho_original,
        "n_bootstrap_solicitado": B_BOOTSTRAP,
        "n_bootstrap_valido": len(boot_validos),
        "ic95_inferior": float(ic_inferior),
        "ic95_superior": float(ic_superior),
        "amplitud_ic95": amplitud_ic,
        "desviacion_bootstrap": desviacion_bootstrap,
        "ic95_incluye_cero": incluye_cero,
        "clasificacion": clasificacion,
        "metodo": "Bootstrap por conglomerados de localidad; Spearman recalculado",
        "semilla": SEED,
    })

    distribuciones_bootstrap[(x, y)] = boot_validos

    print(f"  Spearman S1: {rho_original:.4f}")
    print(f"  IC bootstrap 95 %: [{ic_inferior:.4f}, {ic_superior:.4f}]")
    print(f"  IC incluye cero: {incluye_cero}")
    print(f"  Tiempo: {time.time() - inicio_par:.1f} segundos")

# Tabla de resultados.
tabla_corr = pd.DataFrame(resultados_correlaciones)
tabla_corr.to_csv(
    RUTA_TABLAS / "estabilidad_correlaciones_bootstrap.csv",
    index=False,
)

# Gráfico 1: distribuciones bootstrap.
fig, axes = plt.subplots(
    nrows=len(pares),
    ncols=1,
    figsize=(10, 13),
)

for ax, (x, y) in zip(axes, pares):
    boot = distribuciones_bootstrap[(x, y)]
    fila = tabla_corr[
        (tabla_corr["variable_x"] == x)
        & (tabla_corr["variable_y"] == y)
    ].iloc[0]

    ax.hist(
        boot,
        bins=50,
        density=True,
        alpha=0.75,
        edgecolor="white",
    )

    ax.axvline(
        fila["rho_spearman_s1"],
        linestyle="--",
        linewidth=2,
        label=f"Spearman S1 = {fila['rho_spearman_s1']:.3f}",
    )

    ax.axvline(0, linestyle=":", linewidth=1.5, label="Cero")
    ax.axvline(
        fila["ic95_inferior"],
        linestyle="-.",
        linewidth=1.3,
        label=f"IC95 % inferior = {fila['ic95_inferior']:.3f}",
    )
    ax.axvline(
        fila["ic95_superior"],
        linestyle="-.",
        linewidth=1.3,
        label=f"IC95 % superior = {fila['ic95_superior']:.3f}",
    )

    ax.set_title(f"Bootstrap por localidad: {x} vs. {y}")
    ax.set_xlabel("Coeficiente de correlación de Spearman")
    ax.set_ylabel("Densidad")
    ax.legend()

fig.tight_layout()
fig.savefig(
    RUTA_FIGURAS / "distribuciones_bootstrap_correlaciones.png",
    dpi=180,
    bbox_inches="tight",
)
plt.close(fig)

# Gráfico 2: comparación visual de coeficientes e IC del 95 %.
fig, ax = plt.subplots(figsize=(10, 6))

posiciones = np.arange(len(tabla_corr))
rho = tabla_corr["rho_spearman_s1"].to_numpy()
inferior = tabla_corr["ic95_inferior"].to_numpy()
superior = tabla_corr["ic95_superior"].to_numpy()

ax.errorbar(
    rho,
    posiciones,
    xerr=np.vstack([rho - inferior, superior - rho]),
    fmt="o",
    capsize=5,
    label="Spearman S1 e IC bootstrap 95 %",
)

ax.axvline(0, linestyle="--", linewidth=1.5, label="Cero")
ax.set_yticks(posiciones)
ax.set_yticklabels(
    tabla_corr["variable_x"] + " vs. " + tabla_corr["variable_y"]
)
ax.set_xlabel("Correlación de Spearman")
ax.set_title("Estabilidad de las correlaciones seleccionadas")
ax.legend()
fig.tight_layout()

fig.savefig(
    RUTA_FIGURAS / "intervalos_confianza_correlaciones.png",
    dpi=180,
    bbox_inches="tight",
)
plt.close(fig)

# Resumen de texto para facilitar la interpretación del equipo.
with open(
    RUTA_RESULTADOS / "resumen_validacion_s2.txt",
    "w",
    encoding="utf-8",
) as archivo:
    archivo.write("SUMATIVA 2: RESUMEN DE VALIDACIÓN\n")
    archivo.write("=" * 50 + "\n\n")

    archivo.write("PUNTO 2: PERMUTACIÓN\n")
    archivo.write(resumen_perm.to_string(index=False))
    archivo.write("\n\nPUNTO 3: ESTABILIDAD DE CORRELACIONES\n")
    archivo.write(tabla_corr.to_string(index=False))
    archivo.write("\n")

print("\n" + "=" * 70)
print("ANÁLISIS COMPLETADO")
print("=" * 70)
print("\nTabla de permutación:")
print(RUTA_TABLAS / "prueba_permutacion_humedad.csv")
print("\nTabla de correlaciones:")
print(RUTA_TABLAS / "estabilidad_correlaciones_bootstrap.csv")
print("\nFiguras generadas:")
print(RUTA_FIGURAS / "permutacion_humedad.png")
print(RUTA_FIGURAS / "distribuciones_bootstrap_correlaciones.png")
print(RUTA_FIGURAS / "intervalos_confianza_correlaciones.png")
print("\nResumen:")
print(RUTA_RESULTADOS / "resumen_validacion_s2.txt")