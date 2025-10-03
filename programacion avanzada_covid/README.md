# 🚀 Pipeline COVID-19 Argentina con Papermill

**Pipeline automatizado que cumple con los requisitos de la tarea:**
- ✅ Descarga datos públicos de COVID-19 de Argentina
- ✅ Aplica transformaciones básicas
- ✅ Ejecuta runs parametrizados con Papermill
- ✅ Genera reporte final con los resultados

## 📋 Requisitos

- Python 3.7+
- Dependencias: `pip install -r requirements.txt`

## 🚀 Uso Rápido

```bash
# Opción 1: Ejecutar todo automáticamente
python test_pipeline.py

# Opción 2: Ejecutar paso a paso
python scripts/download_and_prep.py
python run_papermill_pipeline.py
```

## 📁 Estructura del Proyecto

```
├── notebooks/
│   └── template_notebook.ipynb    # Notebook parametrizado para Papermill
├── scripts/
│   ├── download_and_prep.py       # Descarga datos de Johns Hopkins
│   └── clean_artifacts.py         # Limpieza de archivos generados
├── templates/
│   └── report_template.html       # Template del reporte final
├── data/                          # Datos descargados (CSV de Argentina)
├── output/                        # Resultados: imágenes y JSON
├── executed/                      # Notebooks ejecutados por Papermill
├── run_papermill_pipeline.py      # Pipeline principal con Papermill
├── test_pipeline.py              # Script de pruebas
└── report.html                   # Reporte final generado
```

## 🔧 Archivos Clave

- **`run_papermill_pipeline.py`**: Pipeline principal que usa Papermill para ejecutar notebooks parametrizados
- **`notebooks/template_notebook.ipynb`**: Notebook template con parámetros para Argentina
- **`templates/report_template.html`**: Template HTML profesional para el reporte final
- **`scripts/download_and_prep.py`**: Descarga y prepara datos de Argentina de Johns Hopkins CSSE

## 📊 Características del Pipeline

### 1. **Descarga Automática de Datos**
- Descarga datos de COVID-19 desde Johns Hopkins CSSE
- Procesa datos de Argentina
- Genera archivos CSV específicos

### 2. **Procesamiento Parametrizado con Papermill**
- Ejecuta notebook template para Argentina
- Parámetros: nombre del país
- Manejo de errores robusto

### 3. **Transformaciones de Datos**
- Cálculo de nuevos casos diarios
- Media móvil de 7 días
- Estadísticas descriptivas

### 4. **Visualizaciones Automáticas**
- Gráficos de casos acumulados
- Gráficos de nuevos casos diarios con media móvil
- Imágenes de alta calidad (300 DPI)

### 5. **Reporte Final Profesional**
- Dashboard HTML responsivo
- Estadísticas resumidas
- Visualizaciones integradas
- Manejo de errores en el reporte

## 🧪 Pruebas

```bash
# Ejecutar pruebas completas
python test_pipeline.py

# Verificar dependencias
pip install -r requirements.txt

# Limpiar archivos generados
python scripts/clean_artifacts.py
```

## 📈 Resultados

El pipeline genera:
- **`report.html`**: Reporte final con todas las provincias
- **`output/`**: Imágenes PNG y archivos JSON por provincia
- **`executed/`**: Notebooks ejecutados por Papermill
- **Consola**: Log detallado del procesamiento

## 🔍 Monitoreo

El pipeline muestra progreso en tiempo real:
- ✅ Provincias procesadas exitosamente
- ❌ Provincias con errores
- 📊 Estadísticas resumidas
- 📁 Archivos generados

INTRODUCCIÓN

Tu equipo necesita un flujo reproducible que genere indicadores diarios de un dataset. Deciden usar notebooks automatizados con Papermill para facilitar la ejecución con distintos parámetros. Tu misión es construir un pipeline que ejecute notebooks parametrizados para distintas provincias argentinas y compile un reporte final.

OBJETIVO

Automatizar con Papermill la ejecución de un pipeline de notebooks que:

- Descargue datos públicos
- Aplique transformaciones básicas
- Ejecute múltiples runs parametrizados
- Genere un reporte final con los resultados

Limpieza de artefactos:
- Los resultados generados (imágenes, JSON y notebooks ejecutados) se guardan en `output/` y `executed/`. Para limpiarlos puede usar `scripts/clean_artifacts.py`.

Notas:
- Si borras los datos en `data/`, puedes regenerarlos con `python scripts/download_and_prep.py`.

```shell
# Ejemplo rápido:
python scripts/download_and_prep.py
python run_pipeline.py
```