# Preparación local del entorno — 2026-10-10

Fuente de evidencia: comandos ejecutados por Benjamín en su computador y salidas compartidas en la conversación. La asistencia no ejecutó estos comandos en el computador del estudiante.

| Comprobación | Evidencia observada |
|---|---|
| Git | `git version 2.55.0.windows.5` |
| Clonación | Mensaje de clonación y aviso de repositorio vacío. |
| Estado antes de crear el entorno | `On branch main`, `No commits yet`, `nothing to commit`. |
| Remoto origin | URL de Proyecto-Lluvias-Australia-Grupo7, tanto para fetch como para push. |
| Python disponible | `Python 3.12.0` |
| Python de .venv | `.venv/Scripts/python.exe --version` devolvió `Python 3.12.0`. |
| Activación | El indicador mostró `(.venv)`. |
| Intérprete activo | La salida de `sys.executable` terminó en `Proyecto-Lluvias-Australia-Grupo7\.venv\Scripts\python.exe`. |
| Copia de la base | `ls -a` mostró `.gitignore`, `README.md`, `requirements.txt` y los directorios de trabajo previstos en la raíz. |
| Exclusiones | `git check-ignore -v` confirmó `.venv/`, `data/raw/` y `.env`, vinculándolos a las reglas de `.gitignore`. |
| pip | Actualización completada a `26.2.1`. |
| Instalación | Instalación de las dependencias de `requirements.txt` completada según la salida compartida. |
| Consistencia de dependencias | `python -m pip check` devolvió `No broken requirements found.` |
| Importaciones | Importaciones de NumPy, pandas, SciPy, statsmodels, scikit-learn, Matplotlib, seaborn, JupyterLab, ipykernel y nbconvert completadas sin errores. |
| Versiones exactas | `python -m pip freeze --all` generó `requirements-lock-windows.txt`; el estudiante compartió la lista de versiones. |
| Registro del kernel | `ipykernel install` informó que se instaló `grupo7_mcdi501` en el directorio de kernels del usuario. |
| Configuración del kernel | La lectura de `kernel.json` confirmó el intérprete de `.venv`, `ipykernel_launcher` y el nombre visible `Python (Grupo 7 - MCDI501)`. |
| Evidencia estructurada | El código compartido generó `evidence/01_formativa1/entorno.json` y mostró su contenido. |

## Versiones principales observadas

| Paquete | Versión |
|---|---|
| numpy | 2.5.3 |
| pandas | 3.0.6 |
| scipy | 1.18.1 |
| statsmodels | 0.15.0 |
| scikit-learn | 1.9.1 |
| matplotlib | 3.11.2 |
| seaborn | 0.13.2 |
| jupyterlab | 4.6.4 |
| ipykernel | 7.4.0 |
| nbconvert | 7.17.1 |

El archivo `requirements-lock-windows.txt` conserva además las dependencias transitivas y pip. Es un registro del entorno Windows observado; la compatibilidad de versiones debe revisarse al reproducirlo en otro sistema operativo.

## Registro del entorno

- Fecha registrada en UTC: `2026-10-10T15:57:07.308999+00:00`.
- Python: `3.12.0`.
- Plataforma informada: `Windows-10-10.0.19045-SP0`.
- Kernel: `grupo7_mcdi501`.
- Nombre visible: `Python (Grupo 7 - MCDI501)`.
- SHA-256 observado de `requirements-lock-windows.txt`: `b28ffcedf8a084bbd2d9dff03e9ba1bfece206f6c9e78d87f10a1b5edcd2955d`.

La huella identifica los bytes del archivo local al generar el registro; debe recalcularse si cambia ese archivo. La ruta completa del intérprete y los argumentos del kernel están en `entorno.json`, generado por el estudiante.

## Comprobaciones pendientes

- Revisar la lista completa de archivos antes del primer commit.
- Confirmar la copia local del CSV y su huella antes del análisis.
- Abrir JupyterLab y comprobar el arranque del kernel del proyecto.
- Ejecutar y validar el notebook de la Formativa 1.

La instalación, la consistencia de dependencias, las importaciones y la configuración del kernel quedaron comprobadas mediante las salidas compartidas. Estas evidencias corresponden a preparación técnica; todavía no acreditan resultados estadísticos de la Formativa 1.
