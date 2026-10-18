from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats


# Configuracion reproducible
SEMILLA = 20261018
B = 10_000
CONFIANZA = 0.95

RAIZ = Path(__file__).resolve().parents[1]
ARCHIVO_DATOS = RAIZ / "data" / "raw" / "weatherAUS.csv"
CARPETA_TABLAS = RAIZ / "results" / "03_sumativa2" / "tables"
CARPETA_FIGURAS = RAIZ / "results" / "03_sumativa2" / "figures"

CARPETA_TABLAS.mkdir(parents=True, exist_ok=True)
CARPETA_FIGURAS.mkdir(parents=True, exist_ok=True)

VARIABLES = {
    "Humidity3pm": {
        "nombre": "Humedad a las 3 PM",
        "unidad": "%",
    },
    "MaxTemp": {
        "nombre": "Temperatura maxima",
        "unidad": "°C",
    },
    "MinTemp": {
        "nombre": "Temperatura minima",
        "unidad": "°C",
    },
}


def main():
    if not ARCHIVO_DATOS.is_file():
        raise FileNotFoundError(
            f"No se encontro el archivo original: {ARCHIVO_DATOS}"
        )

    df = pd.read_csv(
        ARCHIVO_DATOS,
        usecols=["Location", *VARIABLES.keys()],
        low_memory=False,
    )

    # La unidad de analisis es la localidad, no el registro diario.
    medias_locales = (
        df.groupby("Location", observed=True)[list(VARIABLES)]
        .mean()
    )

    if len(medias_locales) != 49:
        raise ValueError(
            f"Se esperaban 49 localidades; se encontraron "
            f"{len(medias_locales)}."
        )

    rng = np.random.default_rng(SEMILLA)
    resultados = []
    distribuciones = []

    for numero, (variable, info) in enumerate(VARIABLES.items()):
        valores = medias_locales[variable].dropna().to_numpy(dtype=float)
        n = len(valores)

        if n != 49:
            raise ValueError(
                f"{variable}: se esperaban 49 medias locales; hay {n}."
            )

        # Estimacion original e intervalo t clasico de la Sumativa 1.
        estimacion = float(np.mean(valores))
        desviacion = float(np.std(valores, ddof=1))
        error_estandar = desviacion / np.sqrt(n)
        t_critico = stats.t.ppf(0.975, df=n - 1)

        clasico_inf = estimacion - t_critico * error_estandar
        clasico_sup = estimacion + t_critico * error_estandar

        # Bootstrap no parametrico: remuestreo de localidades con reemplazo.
        rng_local = np.random.default_rng(SEMILLA + numero)
        indices = rng_local.integers(0, n, size=(B, n))
        estadisticos = valores[indices].mean(axis=1)

        percentil_inf, percentil_sup = np.quantile(
            estadisticos, [0.025, 0.975]
        )

        # Intervalo BCa calculado con SciPy.
        resultado_bca = stats.bootstrap(
            (valores,),
            np.mean,
            vectorized=False,
            n_resamples=B,
            confidence_level=CONFIANZA,
            method="BCa",
            rng=np.random.default_rng(SEMILLA + 100 + numero),
        )

        bca_inf = float(resultado_bca.confidence_interval.low)
        bca_sup = float(resultado_bca.confidence_interval.high)

        if not np.isfinite([bca_inf, bca_sup]).all():
            raise ValueError(
                f"El intervalo BCa de {variable} no es finito. "
                "Hay que revisar los datos y el resultado."
            )

        resultados.append({
            "Variable": variable,
            "Parametro": info["nombre"],
            "Unidad": info["unidad"],
            "Localidades": n,
            "Remuestreos": B,
            "Semilla": SEMILLA,
            "Estimacion_S1": estimacion,
            "IC_clasico_inferior": clasico_inf,
            "IC_clasico_superior": clasico_sup,
            "IC_percentil_inferior": float(percentil_inf),
            "IC_percentil_superior": float(percentil_sup),
            "IC_BCa_inferior": bca_inf,
            "IC_BCa_superior": bca_sup,
            "Ancho_clasico": clasico_sup - clasico_inf,
            "Ancho_percentil": float(percentil_sup - percentil_inf),
            "Ancho_BCa": bca_sup - bca_inf,
            "Diferencia_inf_percentil_vs_clasico":
                float(percentil_inf - clasico_inf),
            "Diferencia_sup_percentil_vs_clasico":
                float(percentil_sup - clasico_sup),
            "Diferencia_inf_BCa_vs_clasico":
                bca_inf - clasico_inf,
            "Diferencia_sup_BCa_vs_clasico":
                bca_sup - clasico_sup,
        })

        for i, valor in enumerate(estadisticos):
            distribuciones.append({
                "Variable": variable,
                "Remuestreo": i + 1,
                "Media_bootstrap": float(valor),
            })

        print(f"\n{info['nombre']} ({variable})")
        print(f"  Estimacion S1: {estimacion:.6f} {info['unidad']}")
        print(
            f"  IC clasico:    [{clasico_inf:.6f}, "
            f"{clasico_sup:.6f}]"
        )
        print(
            f"  IC percentil:  [{percentil_inf:.6f}, "
            f"{percentil_sup:.6f}]"
        )
        print(f"  IC BCa:        [{bca_inf:.6f}, {bca_sup:.6f}]")

    tabla = pd.DataFrame(resultados)
    tabla.to_csv(
        CARPETA_TABLAS / "bootstrap_ic_s2_resumen.csv",
        index=False,
        encoding="utf-8-sig",
    )

    tabla_distribuciones = pd.DataFrame(distribuciones)
    tabla_distribuciones.to_csv(
        CARPETA_TABLAS / "bootstrap_ic_s2_distribuciones.csv",
        index=False,
        encoding="utf-8-sig",
    )

    # Figura comparativa de las distribuciones bootstrap.
    fig, ejes = plt.subplots(1, 3, figsize=(16, 5))

    for ax, (variable, info) in zip(ejes, VARIABLES.items()):
        valores_bootstrap = tabla_distribuciones.loc[
            tabla_distribuciones["Variable"] == variable,
            "Media_bootstrap",
        ].to_numpy()

        fila = tabla.loc[tabla["Variable"] == variable].iloc[0]

        ax.hist(
            valores_bootstrap,
            bins=40,
            density=True,
            alpha=0.75,
            edgecolor="white",
        )

        ax.axvline(
            fila["Estimacion_S1"],
            linestyle="-",
            linewidth=2,
            label="Estimacion S1",
        )
        ax.axvline(
            fila["IC_clasico_inferior"],
            linestyle=":",
            linewidth=1.5,
            label="Limites IC clasico",
        )
        ax.axvline(
            fila["IC_clasico_superior"],
            linestyle=":",
            linewidth=1.5,
        )
        ax.axvline(
            fila["IC_percentil_inferior"],
            linestyle="--",
            linewidth=1.5,
            label="Limites bootstrap percentil",
        )
        ax.axvline(
            fila["IC_percentil_superior"],
            linestyle="--",
            linewidth=1.5,
        )
        ax.axvline(
            fila["IC_BCa_inferior"],
            linestyle="-.",
            linewidth=1.5,
            label="Limites bootstrap BCa",
        )
        ax.axvline(
            fila["IC_BCa_superior"],
            linestyle="-.",
            linewidth=1.5,
        )

        ax.set_title(info["nombre"])
        ax.set_xlabel(f"Media por localidad ({info['unidad']})")
        ax.set_ylabel("Densidad")
        ax.grid(axis="y", alpha=0.2)

    handles, labels = ejes[0].get_legend_handles_labels()
    fig.legend(
        handles,
        labels,
        loc="lower center",
        ncol=3,
        bbox_to_anchor=(0.5, -0.02),
    )
    fig.suptitle(
        "Validacion de intervalos de confianza mediante bootstrap",
        fontsize=14,
    )
    fig.tight_layout(rect=[0, 0.12, 1, 0.93])

    ruta_figura = CARPETA_FIGURAS / "bootstrap_ic_s2_distribuciones.png"
    fig.savefig(ruta_figura, dpi=300, bbox_inches="tight")
    plt.close(fig)

    print("\n=== RESUMEN COMPARATIVO ===")
    columnas = [
        "Variable",
        "IC_clasico_inferior",
        "IC_clasico_superior",
        "IC_percentil_inferior",
        "IC_percentil_superior",
        "IC_BCa_inferior",
        "IC_BCa_superior",
    ]
    print(tabla[columnas].to_string(index=False))

    print("\nArchivos generados:")
    print(CARPETA_TABLAS / "bootstrap_ic_s2_resumen.csv")
    print(CARPETA_TABLAS / "bootstrap_ic_s2_distribuciones.csv")
    print(ruta_figura)
    print("\nProceso finalizado correctamente.")


if __name__ == "__main__":
    main()