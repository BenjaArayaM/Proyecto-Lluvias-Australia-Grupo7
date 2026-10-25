"""Revisa la evidencia de S3 sin modificar archivos ni volver a entrenar.

Uso desde la raíz: python src/verificar_entrega_sumativa3.py
La evidencia debe corresponder al sistema actual; un registro Work no acredita Windows.
"""
import hashlib
import json
import platform
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
EXPECTED='573fd715cd69fcacc4df32024d823b450ae3edaae7e8ff2eeb623adbed424014'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    env='windows' if platform.system()=='Windows' else 'work'
    source=ROOT/f'evidence/05_sumativa3/ejecucion_sumativa3_{env}.json'
    if not source.is_file():
        raise FileNotFoundError(f'Falta {source.name}. Ejecuta el notebook completo en este sistema.')
    e=json.loads(source.read_text(encoding='utf-8-sig'))
    n=json.loads((ROOT/'notebooks/05_sumativa3_modelamiento_integrado.ipynb').read_text(encoding='utf-8-sig'))
    code=[c for c in n['cells'] if c['cell_type']=='code']
    errors=[o for c in code for o in c.get('outputs',[]) if o['output_type']=='error']
    altered=[p for p,h in e['archivos_sha256'].items()
             if not (ROOT/p).is_file() or digest(ROOT/p)!=h]
    checks={
        'Evidencia del sistema actual':e['entorno']==env and e['sistema']==platform.system(),
        '16 celdas ejecutadas en orden':[c.get('execution_count') for c in code]==list(range(1,17)),
        'Cuaderno sin errores':not errors,
        '22 controles correctos':len(e['controles'])==22 and all(v is True for v in e['controles'].values()),
        'Perfil completo aprobado':e['perfil_plan_aprobado_completo'] is True,
        'CSV original intacto':digest(ROOT/'data/raw/weatherAUS.csv')==e['dataset_sha256']==EXPECTED,
        'Resultados y módulo coinciden con evidencia':not altered,
    }
    print('Fecha UTC de ejecución:',e['fecha_utc'])
    print('Python:',e['python'],'| Sistema:',e['sistema'])
    for name,value in checks.items():print(f'{name}: {value}')
    if altered:print('Archivos diferentes o ausentes:',altered)
    if errors:print('Errores guardados:',[(x['ename'],x['evalue']) for x in errors])
    if not all(checks.values()):raise AssertionError('Existen verificaciones pendientes; comparte la salida.')
    print(f'VERIFICACIÓN {env.upper()} S3: CORRECTA')
    print('PDF, presentación, participación y Canvas requieren su revisión específica.')


if __name__=='__main__':main()
