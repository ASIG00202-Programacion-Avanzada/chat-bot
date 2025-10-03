"""
Script de prueba para verificar que el pipeline con Papermill funciona correctamente.
Este script ejecuta una prueba rápida con una sola provincia para validar la configuración.
"""
import subprocess
import sys
from pathlib import Path

def run_command(command, description):
    """Ejecutar un comando y mostrar el resultado"""
    print(f"\n[EJECUTANDO] {description}")
    print(f"Comando: {command}")
    print("-" * 50)
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, encoding='cp1252', errors='ignore')
        if result.returncode == 0:
            print("OK - Comando ejecutado exitosamente")
            if result.stdout:
                print("Salida:", result.stdout)
        else:
            print("ERROR - Error en el comando")
            print("Error:", result.stderr)
            return False
    except Exception as e:
        print(f"ERROR - Excepcion: {e}")
        return False
    
    return True

def main():
    """Función principal de prueba"""
    print("INICIANDO PRUEBAS DEL PIPELINE")
    print("=" * 50)
    
    # Verificar que existen los archivos necesarios
    required_files = [
        'requirements.txt',
        'scripts/download_and_prep.py',
        'notebooks/template_notebook.ipynb',
        'run_papermill_pipeline.py'
    ]
    
    print("Verificando archivos necesarios...")
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"OK - {file_path}")
        else:
            print(f"ERROR - {file_path} - FALTANTE")
            return False
    
    # Paso 1: Instalar dependencias
    if not run_command("pip install -r requirements.txt", "Instalando dependencias"):
        return False
    
    # Paso 2: Descargar y preparar datos
    if not run_command("python scripts/download_and_prep.py", "Descargando y preparando datos"):
        return False
    
    # Verificar que se generaron los datos
    data_dir = Path('data')
    if not data_dir.exists():
        print("ERROR - Directorio 'data' no se creo")
        return False
    
    csv_files = list(data_dir.glob('*.csv'))
    if not csv_files:
        print("ERROR - No se generaron archivos CSV")
        return False
    
    # Verificar que existe el archivo de países
    countries_file = data_dir / 'countries.json'
    if not countries_file.exists():
        print("ERROR - Archivo 'countries.json' no se genero")
        return False
    
    print(f"OK - Se generaron {len(csv_files)} archivos CSV")
    print(f"OK - Archivo de países: {countries_file}")
    
    # Paso 3: Ejecutar pipeline con Papermill
    if not run_command("python run_papermill_pipeline.py", "Ejecutando pipeline con Papermill"):
        return False
    
    # Verificar que se generaron los resultados
    output_dir = Path('output')
    executed_dir = Path('executed')
    
    if output_dir.exists():
        output_files = list(output_dir.glob('*'))
        print(f"OK - Se generaron {len(output_files)} archivos en 'output/'")
    else:
        print("ERROR - Directorio 'output' no se creo")
        return False
    
    if executed_dir.exists():
        executed_files = list(executed_dir.glob('*'))
        print(f"OK - Se generaron {len(executed_files)} notebooks ejecutados en 'executed/'")
    else:
        print("ERROR - Directorio 'executed' no se creo")
        return False
    
    # Verificar reporte final
    if Path('report.html').exists():
        print("OK - Reporte final 'report.html' generado")
    else:
        print("ERROR - Reporte final no se genero")
        return False
    
    print("\n¡TODAS LAS PRUEBAS PASARON EXITOSAMENTE!")
    print("=" * 50)
    print("El pipeline esta listo para usar")
    print("Revisa 'report.html' para ver los resultados")
    print("Los notebooks ejecutados estan en 'executed/'")
    print("Los archivos de salida estan en 'output/'")
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
