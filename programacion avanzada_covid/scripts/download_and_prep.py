"""
Descarga el CSV de Johns Hopkins y prepara archivos por provincia Argentina.
Genera:
- data/argentina_confirmed.csv  (filtrado)
- data/provinces.json            (lista de provincias encontradas)
- data/{province}.csv            (serie por provincia)
"""
import os
import json
from pathlib import Path
import requests
"""
Descarga el CSV de Johns Hopkins y prepara archivos por provincia Argentina.
Genera:
- data/argentina_confirmed.csv  (filtrado)
- data/provinces.json            (lista de provincias encontradas)
- data/{province}.csv            (serie por provincia)
"""
import os
import json
from pathlib import Path
import requests
import pandas as pd

URL = (
    "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/"
    "csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
)

OUTDIR = Path('data')
"""
Descarga el CSV de Johns Hopkins y prepara archivos para Argentina.
Genera:
- data/argentina_confirmed_timeseries.csv  (serie agregada)
- data/countries.json                       (lista con Argentina)
- data/Argentina.csv                        (serie de Argentina)
"""
import json
from pathlib import Path
import requests
import pandas as pd

URL = (
    "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/"
    "csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
)

OUTDIR = Path('data')
OUTDIR.mkdir(parents=True, exist_ok=True)


def download_csv(url: str) -> pd.DataFrame:
    """Descarga el CSV remoto y devuelve un DataFrame."""
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    from io import StringIO
    return pd.read_csv(StringIO(r.text))


def prepare_countries(df: pd.DataFrame) -> pd.DataFrame:
    """Prepara datos de Argentina para análisis."""
    # Solo Argentina para este análisis
    countries_of_interest = ['Argentina']
    
    # Filtrar solo Argentina
    df_countries = df[df['Country/Region'].isin(countries_of_interest)].copy()
    
    return df_countries


def pivot_to_timeseries(df_countries: pd.DataFrame) -> pd.DataFrame:
    """Convierte el DataFrame JHU al formato time-series por país."""
    # Las columnas de fecha empiezan en la posición 4 en el CSV original
    date_cols = df_countries.columns[4:]
    grouped = df_countries.groupby('Country/Region')[date_cols].sum()
    ts = grouped.T
    ts.index = pd.to_datetime(ts.index)
    ts.columns.name = 'Country'
    return ts


def save_per_country(ts: pd.DataFrame):
    countries = []
    for country in ts.columns:
        country_safe = country.replace('/', '_').replace(' ', '_')
        dfc = ts[[country]].reset_index()
        dfc.columns = ['date', 'confirmed']
        path = OUTDIR / f"{country_safe}.csv"
        dfc.to_csv(path, index=False)
        countries.append({'name': country, 'file': str(path)})
    
    # Guardar lista de países (solo Argentina)
    names = [c['name'] for c in countries]
    (OUTDIR / 'countries.json').write_text(json.dumps(names, ensure_ascii=False))
    
    # Guardar serie de Argentina
    ts.reset_index().to_csv(OUTDIR / 'argentina_confirmed_timeseries.csv', index=False)
    print(f"Saved {len(countries)} country files in {OUTDIR}")


if __name__ == '__main__':
    print('Descargando CSV...')
    df = download_csv(URL)
    print('Preparando datos de Argentina...')
    df_countries = prepare_countries(df)
    ts = pivot_to_timeseries(df_countries)
    save_per_country(ts)
    print('Hecho.')