<!-- ESTADO_S3_WINDOWS -->
> **Estado S3 actualizado al 25 de octubre de 2026:** reproducción Windows
> verificada: 16 celdas en orden, ningún error y 22 controles correctos.
> Los resultados cotejados coinciden con Work dentro de tolerancia 1e-7.
> Benjamín confirmó que PDF y PowerPoint abren en su computador.
> Evidencias: `evidence/05_sumativa3/validacion_windows.json` y
> `evidence/05_sumativa3/validacion_windows.md`.
> Permanecen pendientes revisión académica grupal, ensayo/grabación,
> revisión para commit, publicación y entrega en Canvas.
>
> Los registros originales de Work y las menciones de pendientes en los
> materiales preparados entonces se conservan como antecedentes históricos.
> Esta actualización acredita reproducción y apertura; no acredita por sí
> sola revisión visual exhaustiva, participación grupal ni entrega.
<!-- FIN_ESTADO_S3_WINDOWS -->

# Reproducción y edición — Sumativa 3 — Grupo 7

## Incorporar la carpeta al proyecto

El ZIP es una **actualización sobre el proyecto existente**, con rutas relativas desde su raíz. No es un repositorio nuevo ni incluye `.git`. Se preparó contra `main` en el commit `28e3a8a0805e11fd1b93beb273db7ca4060aa557`, que ya contiene S1, S2 y F2. No debe extraerse en una rama antigua sin esos antecedentes.

1. Descargar el ZIP y mantenerlo sin extraer en el repositorio.
2. Compartir `git status` del proyecto con la asistencia. Después se verificarán cambios locales, referencias y base remota antes de indicar la creación de la nueva rama. El nombre sugerido es `sumativa3-benjamin`; no se afirma que exista.
3. El estudiante ejecutará cada comando Git Bash por separado y compartirá su salida. No hay operaciones Git automáticas en este paquete.
4. Con la rama nueva y la base verificadas, extraer el contenido en `C:\Users\benja\OneDrive\Escritorio\Proyecto-Lluvias-Australia-Grupo7`, combinando carpetas. Deben quedar `src/sumativa3.py` y `notebooks/05_sumativa3_modelamiento_integrado.ipynb` directamente en las carpetas existentes, sin una raíz duplicada.
5. Revisar la lista de cambios antes de cualquier commit. La actualización modifica README y continuidad general, y añade exclusivamente productos S3. No reemplaza los análisis anteriores.

## Requisitos del entorno

Se utiliza Python 3.12, el entorno `.venv` del proyecto y el kernel `grupo7_mcdi501`. Se conserva el lock Windows histórico; no se reemplaza por versiones de Work. Las dependencias directas se declaran en `requirements-sumativa3.txt`. La instalación y `pip check` se comprobarán en el computador del estudiante antes de ejecutar el cuaderno. Si falta un paquete, se diagnostica el error antes de continuar.

El CSV debe estar en `data/raw/weatherAUS.csv`: 14.094.055 bytes, 145.460 × 23 y SHA-256 `573fd715cd69fcacc4df32024d823b450ae3edaae7e8ff2eeb623adbed424014`. El archivo se obtiene legítimamente de la fuente; no se distribuye en este ZIP. El módulo detiene la ejecución ante una identidad diferente.

Los archivos analíticos de S1, S2 y F2 identificados en `evidence/05_sumativa3/fuentes_base.json` deben existir. No se requiere repetir esas evaluaciones: S3 reproduce las métricas de F2 y concilia las fuentes previas directamente.

## Ejecución del notebook

Estas instrucciones son una referencia de reproducción; en la sesión se avanzará una verificación por vez.

**Directorio:** raíz de `Proyecto-Lluvias-Australia-Grupo7`.

**Objetivo:** ejecutar las 16 celdas desde un kernel nuevo y guardar las salidas.

Con entorno y kernel verificados, el comando Git Bash que ejecutará el estudiante es:

```bash
./.venv/Scripts/python.exe -m nbconvert --to notebook --execute --inplace --ExecutePreprocessor.kernel_name=grupo7_mcdi501 --ExecutePreprocessor.timeout=3600 notebooks/05_sumativa3_modelamiento_integrado.ipynb
```

No exige abrir un servidor JupyterLab. `--inplace` guarda nuevamente el notebook con las salidas actuales. El proceso realiza cinco pliegues y 2.000 remuestras; mientras no regrese el prompt puede seguir trabajando. El tiempo depende del equipo; el timeout es por celda. No se inventa un tiempo Windows a partir del tiempo Work.

Resultado esperado: escritura del notebook sin traceback y mensaje final `SUMATIVA 3 - EJECUCIÓN COMPLETA: CORRECTA`. Se genera `evidence/05_sumativa3/ejecucion_sumativa3_windows.json`. Ese registro es distinto del Work entregado.

Después de revisar esa salida, se comprobará sin reentrenar:

```bash
./.venv/Scripts/python.exe src/verificar_entrega_sumativa3.py
```

Debe mostrar 16 celdas en orden, ningún error, 22 controles correctos, perfil completo, CSV intacto y huellas de resultados/módulo coincidentes. Compararemos también las cifras principales con el informe. No se sustituye esta verificación por la mera apertura del notebook.

Semillas: partición 42; imputación 50101; CV 50102; bootstrap 50103; Monte Carlo 50104. El CSV original nunca se escribe. Los resultados se regeneran en `results/05_sumativa3/`. Los CSV usan UTF-8 con BOM para Excel.

## Informe LaTeX editable

Fuente principal: `reports/05_sumativa3/informe_sumativa3_grupo7.tex`. La portada institucional está separada en `portada_unab.tex` y conserva el logo original. Las tablas y cifras proceden de `datos_sumativa3.tex`, generado desde resultados actuales. Las figuras se leen con rutas relativas desde `results/05_sumativa3/figures/`.

Para un cambio solo de redacción, editar el `.tex` y recompilar; no es necesario repetir bootstrap. Si cambia el análisis, ejecutar primero el notebook completo y regenerar los datos LaTeX:

```bash
./.venv/Scripts/python.exe src/generar_informe_sumativa3.py
```

Ese comando no exige instalar LaTeX. Con pdfLaTeX disponible en PATH, añadir `--compilar` genera el PDF con dos pasadas. Si no está instalado, usar el ZIP LaTeX autónomo en Overleaf, documento principal `informe_sumativa3_grupo7.tex`, motor pdfLaTeX. No se instala software de edición sin verificar el entorno del estudiante.

El PDF entregado fue compilado y sus diez páginas fueron revisadas en Work. Incluye portada y referencias dentro del máximo de diez páginas. Tras cualquier cambio comprobar nuevamente la extensión, los nombres y la coincidencia de cifras. La fecha de preparación no es una fecha de entrega inventada.

## Presentación y video

`presentations/05_sumativa3/presentacion_sumativa3_grupo7.pptx` contiene 12 diapositivas editables, tablas/gráficos nativos y notas del orador. `guion_presentacion.md` propone 2:30 por integrante. `datos_presentacion.json` conserva cifras y datos de gráficos; el material se apoya en resultados completos, con redondeo de presentación. La tipografía Nimbus Sans puede sustituirse por Arial si el equipo no la tiene; comprobar ajuste y legibilidad en PowerPoint antes de grabar.

No se acredita apertura en Windows ni reproducción idéntica en todas las versiones de PowerPoint. Revisar el programa de grabación, ensayar los cuatro bloques, grabar a los cuatro integrantes y comprobar diez minutos, audio, dominio y coordinación. El PPTX/guion no equivale al video exigido.

## Antes de entregar

- Conciliar las cifras actuales del notebook, PDF y diapositivas; conservar evidencias separadas por plataforma.
- Confirmar en Canvas fecha, formato del video/presentación y enlace de entrega. El instructivo señala un intento y productos PDF + `.ipynb` + presentación + enlace GitHub.
- Revisar la auditoría de 108 puntos. No asignar puntos a participación aún no acreditada.
- Revisar archivos antes de commit; el dataset original, `.venv`, credenciales y auxiliares LaTeX deben seguir excluidos.
- El estudiante crea rama, commit y push desde Git Bash, con verificación paso a paso. La asistencia conserva acceso remoto de lectura.
