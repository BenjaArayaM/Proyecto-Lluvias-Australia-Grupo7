"""Genera tablas y macros LaTeX desde resultados actuales; compilación opcional.

Desde la raíz: python src/generar_informe_sumativa3.py --compilar
Sin --compilar no exige instalar LaTeX. El texto del informe permanece editable.
"""
from pathlib import Path
import argparse
import json
import subprocess
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reports/05_sumativa3"


def esc(text):
    text=str(text)
    for a,b in (("\\",r"\textbackslash{}"),("_",r"\_"),("%",r"\%"),
                ("&",r"\&"),("#",r"\#")):
        text=text.replace(a,b)
    return text


def fmt(x, digits=3):
    if x is None or not np.isfinite(float(x)):return "---"
    return f"{float(x):,.{digits}f}".replace(",", "TEMP").replace(".", ",").replace("TEMP", r"\,")


def ci(a,b,digits=3):return "["+fmt(a,digits)+"; "+fmt(b,digits)+"]"


def tabular(headers, rows, layout=None, size=r"\small"):
    layout=layout or ("l"+"r"*(len(headers)-1))
    return (size+r"\begin{tabularx}{\linewidth}{@{}"+layout+r"@{}}\toprule"+"\n"+
        " & ".join(headers)+r"\\\midrule"+"\n"+
        "\n".join(" & ".join(map(str,row))+r"\\" for row in rows)+
        "\n"+r"\bottomrule\end{tabularx}")


def build():
    r=json.loads((ROOT/"results/05_sumativa3/resultados_validados_s3.json").read_text(encoding="utf-8"))
    T=ROOT/"results/05_sumativa3/tables"
    d=[]
    def macro(name, value):d.append("\\newcommand{\\"+name+"}{"+str(value)+"}")
    best=r['modelo_final'];name=best['nombre']
    test=next(x for x in r['metricas_tres_modelos'] if x['modelo']==name and x['conjunto']=='test' and x['regla_umbral']=='F1_OOF')
    train=next(x for x in r['metricas_tres_modelos'] if x['modelo']==name and x['conjunto']=='train' and x['regla_umbral']=='F1_OOF')
    for key,val,digits in [
        ('AUCFinal',test['auc'],4),('RecallFinal',test['recall']*100,2),
        ('PrecisionFinal',test['precision']*100,2),('AccuracyFinal',test['accuracy']*100,2),
        ('FUnoFinal',test['f1'],4),('PRAUCFinal',test['pr_auc'],4),
        ('UmbralFinal',best['umbral'],4),('FalsosNegativos',test['fn'],0),
        ('FalsosPositivos',test['fp'],0),('VerdaderosPositivos',test['tp'],0),
        ('CambioRecall',100*(test['recall']-r['referencia_F2_reproducida']['recall']),2),
        ('CambioAccuracy',100*(test['accuracy']-r['referencia_F2_reproducida']['accuracy']),2),
        ('PesoYes',best['pesos_clase']['Yes'],4),('PesoNo',best['pesos_clase']['No'],4),
        ('MejoraRMSE',r['imputacion']['reduccion_RMSE_Sunshine']*100,2),
        ('BootstrapValidas',r['bootstrap']['validas'],0),
        ('FaltantesSunModelo',r['dataset']['Sunshine_faltantes_respuesta_conocida_pct'],2),
        ('MaxVIF',max(x['VIF'] for x in r['diagnosticos']['VIF']),3),
        ('CookMarcados',r['diagnosticos']['influencia']['n_Cook_mayor_4_sobre_n'],0),
    ]:macro(key,fmt(val,digits))
    macro('ModeloFinal',esc(name.replace('_',' ')))
    macro('VariablesFinales',', '.join(r'\texttt{'+esc(x)+'}' for x in best['predictores']))
    diag=r['imputacion']['diagnosticos_16_regresiones']
    sunshine=next(x for x in diag if x['variable']=='Sunshine')
    for key,val,digits in [('RMSESolReg',sunshine['rmse_regresion'],3),('RMSESolMed',sunshine['rmse_mediana'],3),('RDSol',sunshine['r2_validacion'],3)]:macro(key,fmt(val,digits))
    rows=[]
    for row in diag:
        rows.append([esc(row['variable']),esc(row['predictores']),fmt(row['n_ajuste_completos'],0),
                     fmt(row['r2_validacion'],3),fmt(row['rmse_regresion'],2),fmt(row['rmse_mediana'],2)])
    macro('TablaImputacion',tabular(['Variable','Tres predictores','Donantes',r'$R^2$ val.','RMSE reg.','RMSE med.'],
          rows,'lXrrrr',r'\fontsize{8.3}{10.2}\selectfont'))
    selection=r['seleccion_entrenamiento']
    macro('TablaSeleccion',tabular(['Modelo','p','AIC','BIC','AUC OOF','Umbral'],[
        [x['modelo'][:2],str(x['n_predictores']),fmt(x['AIC_seleccion_no_ponderado'],1),
         fmt(x['BIC_seleccion_no_ponderado'],1),fmt(x['oof_auc'],4),fmt(x['umbral_F1_OOF'],4)] for x in selection],
          'lrrrrr'))
    coefs=pd.read_csv(T/'coeficientes_tres_modelos.csv')
    terms=list(dict.fromkeys(coefs.termino))
    rows=[]
    for term in terms:
        row=[esc(term)]
        for model in ('M1_dominio','M2_stepwise_AIC','M3_reducido_BIC'):
            z=coefs.loc[coefs.modelo.eq(model)&coefs.termino.eq(term)]
            row.append('---' if z.empty else fmt(z.iloc[0].coeficiente,3)+' ('+fmt(z.iloc[0].odds_ratio,3)+')')
        rows.append(row)
    macro('TablaCoeficientesTres',tabular(['Predictor',r'M1 $\beta$ (OR)',r'M2 $\beta$ (OR)',r'M3 $\beta$ (OR)'],rows,'lrrr'))
    rows=[]
    for x in r['metricas_tres_modelos']:
        if x['regla_umbral']=='F1_OOF':
            rows.append([x['modelo'][:2],x['conjunto'],fmt(x['accuracy']*100,2),fmt(x['precision']*100,2),
                fmt(x['recall']*100,2),fmt(x['f1'],3),fmt(x['auc'],4)])
    macro('TablaMetricas',tabular(['Modelo','Muestra',r'Acc.\%',r'Prec.\%',r'Recall\%','F1','AUC'],rows,'llrrrrr'))
    rows=[]
    for x in r['bootstrap']['intervalos']:
        if x['termino']=='const':continue
        rows.append([esc(x['termino']),fmt(x['beta_referencia'],3),
            ci(x['ic_Wald_beta_inf'],x['ic_Wald_beta_sup']),
            ci(x['ic_percentil_beta_inf'],x['ic_percentil_beta_sup']),
            fmt(x['OR'],3)+' '+ci(x['ic_percentil_OR_inf'],x['ic_percentil_OR_sup']),
            fmt(x['frecuencia_signo_conservado']*100,1)])
    macro('TablaBootstrap',tabular(['Predictor',r'$\hat\beta$','IC Wald beta','IC boot beta','OR [IC boot]',r'Signo\%'],rows,'lrrrrr',r'\fontsize{8.4}{10.3}\selectfont'))
    unstable=[x['termino'] for x in r['bootstrap']['intervalos'] if x['termino']!='const' and x['ic_percentil_incluye_cero']]
    macro('PredictoresInestables',', '.join(r'\texttt{'+esc(x)+'}' for x in unstable) if unstable else 'ninguno')
    macro('NumeroFallosBootstrap',str(len(r['bootstrap']['fallos'])))
    top=r['bootstrap']['jackknife_top3']
    macro('LocalidadesInfluyentes',', '.join(esc(x['localidad_omitida']) for x in top))
    macro('TablaVIF',tabular(['Predictor','VIF'],[[esc(x['predictor']),fmt(x['VIF'],3)] for x in r['diagnosticos']['VIF']],'lr'))
    rows=[]
    for x in r['diagnosticos']['linealidad_logit']:
        pv='$<0{,}001$' if x['p_Bonferroni']<.001 else fmt(x['p_Bonferroni'],3)
        rows.append([esc(x['predictor']),pv,fmt(100*x['reduccion_deviance_relativa'],3)])
    macro('TablaLinealidad',tabular(['Predictor','p ajustado',r'$\Delta$ dev.\%'],rows,'lrr',r'\footnotesize'))
    rows=[]
    for x in r['impacto_imputacion']:
        label={'eliminacion':'Eliminación','mediana':'Mediana','regresion':'Regresión'}[x['estrategia']]
        pop='Propia' if x['poblacion_prueba']=='disponible_por_estrategia' else 'Común'
        rows.append([label,pop,fmt(x['n_train'],0),fmt(x['n'],0),str(x['localidades_test']),
            fmt(x['auc'],4),fmt(100*x['accuracy'],2),fmt(100*x['recall'],2)])
    macro('TablaImpacto',tabular(['Estrategia','Prueba',r'$n_{train}$',r'$n_{test}$','Loc.','AUC',r'Acc.\%',r'Recall\%'],rows,'llrrrrrr'))
    deletion=next(x for x in r['impacto_imputacion'] if x['estrategia']=='eliminacion' and x['poblacion_prueba']=='disponible_por_estrategia')
    macro('CoberturaEliminacion',fmt(deletion['cobertura_test']*100,2));macro('LocEliminacion',str(deletion['localidades_test']))
    rows=[]
    ico=pd.DataFrame(r['coeficientes_impacto_escala_comun'])
    for term in best['predictores']:
        row=[esc(term)]
        for strategy in ('eliminacion','mediana','regresion'):
            z=ico.loc[ico.estrategia.eq(strategy)&ico.termino.eq(term)].iloc[0]
            row.append(fmt(z.coeficiente,3)+' '+ci(z.ic_wald_beta_inf,z.ic_wald_beta_sup))
        rows.append(row)
    macro('TablaCoefImpacto',tabular(['Predictor','Eliminación','Mediana','Regresión'],rows,'lrrr',r'\footnotesize'))
    mc=r['montecarlo_decision_ampliacion_S3']
    macro('TablaMonteCarlo',tabular(['Humedad',r'$n$ train','p lluvia','Media /30',r'Capacidad 95\%','MCSE'],[
        [('Alta' if '>=' in x['escenario'] else 'Menor'),fmt(x['n_calibracion_train'],0),fmt(x['probabilidad_empirica_train'],4),
         fmt(x['media_dias_lluvia'],2),str(x['capacidad_dias_riesgo_5pct']),fmt(x['MCSE_media'],3)] for x in mc],'lrrrrr'))
    macro('CapacidadAlta',str(mc[0]['capacidad_dias_riesgo_5pct']));macro('CapacidadBaja',str(mc[1]['capacidad_dias_riesgo_5pct']))
    for j,x in enumerate(mc):
        macro('MediaMC'+('Alta' if j==0 else 'Baja'),fmt(x['media_dias_lluvia'],2))
        macro('ProbMC'+('Alta' if j==0 else 'Baja'),fmt(x['probabilidad_empirica_train']*100,2))
    row=next(x for x in r['bootstrap']['intervalos'] if x['termino']=='Humidity3pm')
    macro('ORHumedad',fmt(row['OR'],3));macro('ICHumedad',ci(row['ic_percentil_OR_inf'],row['ic_percentil_OR_sup']))
    macro('DEHumedad',fmt(best['DE_referencia']['Humidity3pm'],2))
    rawbeta=best['parametros_estandarizados'].get('log1p_Rainfall',0)/best['DE_referencia'].get('log1p_Rainfall',1)
    macro('ORDoblarRain',fmt(np.exp(rawbeta*np.log(2)),3))
    counts=pd.read_csv(T/'imputacion_conteos.csv')
    x=counts.query("estrategia == 'regresion' and conjunto == 'train' and variable == 'Sunshine'").iloc[0]
    macro('FallbackSol',fmt(x.n_fallback_auxiliar_mediana,0));macro('ImputadosSol',fmt(x.n_imputados,0))
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/'datos_sumativa3.tex').write_text('\n'.join(d)+'\n',encoding='utf-8')
    return r


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--compilar',action='store_true')
    args=parser.parse_args()
    build()
    if args.compilar:
        for _ in range(2):
            subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error',
                            'informe_sumativa3_grupo7.tex'],cwd=OUT,check=True,
                           stdout=subprocess.PIPE,stderr=subprocess.STDOUT,
                           text=True,encoding='utf-8',errors='replace')
        print('PDF compilado:',OUT/'informe_sumativa3_grupo7.pdf')
    else:print('Datos LaTeX actualizados; el cuerpo del informe conserva su edición.')


if __name__=='__main__':main()
