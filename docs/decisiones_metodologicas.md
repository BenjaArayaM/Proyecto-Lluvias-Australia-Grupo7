# Registro de decisiones — MCDI501 — Grupo 7

Cada nueva decisión debe identificar fecha, fundamento, fuente, consecuencias y evidencia. Este registro distingue la preparación técnica de las decisiones estadísticas.

| ID | Fecha | Decisión | Fundamento y evidencia | Estado |
|---|---|---|---|---|
| D001 | 2026-10-10 | Utilizar el repositorio existente Proyecto-Lluvias-Australia-Grupo7. | URL proporcionada por el estudiante; clonación y `origin` verificados mediante sus salidas. | Confirmado |
| D002 | 2026-10-10 | Ubicar el proyecto en el Escritorio del estudiante. | Ruta real consultada mediante Windows; acceso comprobado con `pwd`. | Confirmado |
| D003 | 2026-10-10 | Preparar una estructura común para las cinco evaluaciones. | Propuesta aprobada; `ls -a` confirmó los directorios y archivos de la raíz. | Copia de la base observada; revisión de la lista completa de archivos pendiente |
| D004 | 2026-10-10 | Usar un entorno virtual `.venv` con Python 3.12.0. | Creación, activación, instalación de dependencias, `pip check`, importaciones y configuración del kernel comprobadas mediante salidas compartidas. | Preparación comprobada; arranque de Jupyter y ejecución del notebook pendientes |
| D005 | 2026-10-10 | Desarrollar únicamente la Formativa 1 en esta etapa. | Evaluación seleccionada por el estudiante; plan aprobado. | Activo |
| D006 | 2026-10-10 | Conservar el dataset original sin modificaciones y excluirlo de Git. | `git check-ignore -v` confirmó las reglas para `data/raw/`, `.venv/` y `.env`. | Exclusiones comprobadas; copia local del CSV pendiente |
| D007 | 2026-10-10 | Conservar un registro de las versiones instaladas y de la configuración local. | `pip freeze --all` generó `requirements-lock-windows.txt`; `evidence/01_formativa1/entorno.json` registra su SHA-256 y el kernel. | Generación confirmada mediante la salida del estudiante; revisión previa al commit pendiente |

## Decisiones estadísticas pendientes

- Delimitar el alcance poblacional y las preguntas de análisis.
- Seleccionar parámetros e intervalos de confianza para la Formativa 1.
- Elegir y justificar al menos una prueba de hipótesis después de revisar supuestos, dependencia temporal y diferencias entre localidades.
- Definir, en la fase pertinente, el instante de predicción y el esquema de validación que evite fuga de información.

La aprobación del plan no implica que estos procedimientos ya se hayan seleccionado, ejecutado o validado.
