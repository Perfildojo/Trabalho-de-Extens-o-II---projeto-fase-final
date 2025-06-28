import pandas as pd
from pathlib import Path
import logging
from typing import Optional
import json

BASE_DIR = Path(__file__).parent.parent
CSV_PATH = BASE_DIR / "data" / "processed" / "dados_processados.csv"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def calcular_coordenadas(df, geojson_path):
    try:
        with open(geojson_path, "r") as f:
            bairros_geojson = json.load(f)

        df['lat'] = None
        df['lon'] = None

        for feature in bairros_geojson['features']:
            bairro = feature['properties']['nome']
            coords = feature['geometry']['coordinates'][0]
            lats = [p[1] for p in coords]
            lons = [p[0] for p in coords]
            lat = sum(lats) / len(lats)
            lon = sum(lons) / len(lons)
            df.loc[df['BAIRRO DO FATO'] == bairro, 'lat'] = lat
            df.loc[df['BAIRRO DO FATO'] == bairro, 'lon'] = lon

        return df
    except Exception as e:
        logger.error(f"Erro ao calcular coordenadas: {e}")
        return df

def carregar_dados() -> Optional[pd.DataFrame]:
    try:
        logger.info(f"Carregando dados de: {CSV_PATH}")

        df = pd.read_csv(
            CSV_PATH,
            delimiter=',',
            encoding='utf-8',
            parse_dates=['DATA DO FATO'],
            dayfirst=True,
            dtype={
                'BAIRRO DO FATO': 'str',
                'SUBJETIVIDADE COMPLEMENTAR': 'str',
                'CIDADE DO FATO': 'str',
                'SEXO DA VITIMA': 'str',
                'COR/RACA DA VITIMA': 'str',
                'LOCAL DO FATO': 'str'
            }
        )

        df = calcular_coordenadas(df, "bairros.geojson")
        df = df[df['CIDADE DO FATO'].str.strip().str.lower() == 'maceió']
        df = df.dropna(subset=['BAIRRO DO FATO', 'SUBJETIVIDADE COMPLEMENTAR'])

        df['BAIRRO DO FATO'] = df['BAIRRO DO FATO'].str.strip().str.title()
        df['SUBJETIVIDADE COMPLEMENTAR'] = df['SUBJETIVIDADE COMPLEMENTAR'].str.strip().str.title()
        df['SEXO DA VITIMA'] = df['SEXO DA VITIMA'].str.strip().str.title()

        logger.info(f"Dados carregados com sucesso. Total de registros: {len(df)}")
        return df

    except FileNotFoundError:
        logger.error(f"Arquivo não encontrado: {CSV_PATH}")
        return None
    except Exception as e:
        logger.error(f"Erro ao carregar dados: {e}", exc_info=True)
        return None

if __name__ == "__main__":
    df = carregar_dados()
    if df is not None:
        print(df.head())
