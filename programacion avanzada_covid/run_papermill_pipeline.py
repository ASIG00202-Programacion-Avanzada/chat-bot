"""
Pipeline principal con Papermill para procesar datos de COVID-19 de Argentina.
Este script cumple con los requisitos de la tarea:
- Descarga datos públicos
- Aplica transformaciones básicas  
- Ejecuta runs parametrizados con Papermill
- Genera un reporte final con los resultados
"""
import json
import papermill as pm
from pathlib import Path
from jinja2 import Template
import traceback
import sys

# Configuración de directorios
DATA_DIR = Path('data')
OUTPUT_DIR = Path('output')
EXECUTED_DIR = Path('executed')
TEMPLATE_NB = Path('notebooks/template_notebook.ipynb')
REPORT_TEMPLATE = Path('templates/report_template.html')

def ensure_directories():
    """Crear directorios necesarios si no existen"""
    for dir_path in [OUTPUT_DIR, EXECUTED_DIR]:
        dir_path.mkdir(exist_ok=True)
        print(f"OK - Directorio {dir_path} listo")

def load_countries():
    """Cargar lista de países desde el archivo JSON"""
    countries_file = DATA_DIR / 'countries.json'
    if not countries_file.exists():
        raise FileNotFoundError(f"Archivo de países no encontrado: {countries_file}")
    
    with open(countries_file, 'r', encoding='utf-8') as f:
        countries = json.load(f)
    
    print(f"OK - Cargados {len(countries)} países: {', '.join(countries)}")
    return countries

def execute_notebook_for_country(country, template_nb, executed_dir):
    """
    Ejecutar el notebook template para un país específico usando Papermill
    
    Args:
        country: Nombre del país
        template_nb: Ruta al notebook template
        executed_dir: Directorio donde guardar notebooks ejecutados
    
    Returns:
        dict: Resultado de la ejecución con metadatos
    """
    print(f"\n[PROCESANDO] País: {country}")
    
    # Crear nombre seguro para archivos
    country_safe = country.replace('/', '_').replace(' ', '_')
    executed_nb = executed_dir / f"{country_safe}_executed.ipynb"
    
    try:
        # Ejecutar notebook con Papermill
        pm.execute_notebook(
            input_path=str(template_nb),
            output_path=str(executed_nb),
            parameters={'country': country},
            kernel_name='python3'
        )
        
        print(f"OK - Notebook ejecutado: {executed_nb}")
        
        # Cargar resultados del notebook ejecutado
        result = load_notebook_results(country, country_safe)
        result['executed_notebook'] = str(executed_nb)
        result['status'] = 'success'
        
        return result
        
    except Exception as e:
        print(f"ERROR - Error procesando {country}: {str(e)}")
        return {
            'country': country,
            'status': 'error',
            'error': str(e),
            'executed_notebook': None
        }

def load_notebook_results(country, country_safe):
    """
    Cargar resultados generados por el notebook (JSON summary e imágenes)
    
    Args:
        country: Nombre del país
        country_safe: Nombre seguro para archivos
    
    Returns:
        dict: Resultados cargados
    """
    result = {'country': country}
    
    # Cargar summary JSON
    summary_file = OUTPUT_DIR / f"{country_safe}_summary.json"
    if summary_file.exists():
        with open(summary_file, 'r', encoding='utf-8') as f:
            result['summary'] = json.load(f)
    else:
        result['summary'] = {'error': 'Summary no generado'}
    
    # Verificar imágenes generadas
    cumulative_img = OUTPUT_DIR / f"{country_safe}_cumulative.png"
    daily_img = OUTPUT_DIR / f"{country_safe}_daily_ma7.png"
    
    result['cumulative_img'] = str(cumulative_img) if cumulative_img.exists() else None
    result['daily_img'] = str(daily_img) if daily_img.exists() else None
    
    return result

def generate_final_report(results, report_template, output_file):
    """
    Generar reporte final HTML con todos los resultados
    
    Args:
        results: Lista de resultados por provincia
        report_template: Ruta al template HTML
        output_file: Archivo de salida del reporte
    """
    print(f"\n[GENERANDO] Reporte final...")
    
    # Cargar template
    with open(report_template, 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    # Renderizar con Jinja2
    template = Template(template_content)
    html_content = template.render(results=results)
    
    # Guardar reporte
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"OK - Reporte generado: {output_file}")

def print_pipeline_summary(results):
    """Imprimir resumen del pipeline ejecutado"""
    print("\n" + "="*50)
    print("RESUMEN DEL PIPELINE")
    print("="*50)
    
    successful = [r for r in results if r.get('status') == 'success']
    failed = [r for r in results if r.get('status') == 'error']
    
    print(f"OK - Análisis procesados exitosamente: {len(successful)}")
    print(f"ERROR - Análisis con errores: {len(failed)}")
    
    if successful:
        print("\nAnálisis exitosos:")
        for result in successful:
            summary = result.get('summary', {})
            total = summary.get('total_confirmed', 'N/A')
            latest = summary.get('latest_new', 'N/A')
            print(f"  - {result['country']}: {total} total, {latest} nuevos")
    
    if failed:
        print("\nAnálisis con errores:")
        for result in failed:
            print(f"  - {result['country']}: {result.get('error', 'Error desconocido')}")

def main():
    """Función principal del pipeline"""
    print("Iniciando pipeline de COVID-19 Argentina con Papermill")
    print("="*50)
    
    try:
        # 1. Preparar directorios
        ensure_directories()
        
        # 2. Cargar países (solo Argentina)
        countries = load_countries()
        
        # 3. Verificar que existe el template
        if not TEMPLATE_NB.exists():
            raise FileNotFoundError(f"Template notebook no encontrado: {TEMPLATE_NB}")
        
        # 4. Ejecutar notebook para Argentina
        results = []
        for i, country in enumerate(countries, 1):
            print(f"\n[{i}/{len(countries)}] Procesando: {country}")
            result = execute_notebook_for_country(country, TEMPLATE_NB, EXECUTED_DIR)
            results.append(result)
        
        # 5. Generar reporte final
        generate_final_report(results, REPORT_TEMPLATE, 'report.html')
        
        # 6. Mostrar resumen
        print_pipeline_summary(results)
        
        print(f"\nPipeline completado! Revisa 'report.html' para ver los resultados.")
        
    except Exception as e:
        print(f"\nERROR - Error en el pipeline: {str(e)}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
