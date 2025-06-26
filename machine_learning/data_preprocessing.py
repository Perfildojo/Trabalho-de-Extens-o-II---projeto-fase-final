import pandas as pd
import numpy as np
from pathlib import Path
import logging

# Configuração
BASE_DIR = Path(__file__).parent.parent
RAW_DATA_PATH = BASE_DIR / "data" / "raw" / "ocorrencias_brutas.csv"
PROCESSED_PATH = BASE_DIR / "data" / "processed" / "ocorrencias_processadas.csv"

def processar_dados():
    """Processa dados brutos para análise"""
    try:
        # Carrega dados brutos
        df = pd.read_csv(
            RAW_DATA_PATH,
            parse_dates=['data_ocorrencia'],
            encoding='latin1',
            delimiter=';'
        )
        
        # Limpeza básica
        df = (df
            .dropna(subset=['bairro', 'tipo_ocorrencia'])
            .assign(
                bairro=lambda x: x['bairro'].str.title().str.strip(),
                tipo_ocorrencia=lambda x: x['tipo_ocorrencia'].str.capitalize(),
                hora=lambda x: pd.to_datetime(x['hora_ocorrencia'], format='%H:%M').dt.time
            )
        )
        
        # Salva dados processados
        PROCESSED_PATH.parent.mkdir(exist_ok=True)
        df.to_csv(PROCESSED_PATH, index=False)
        logging.info(f"Dados processados salvos em {PROCESSED_PATH}")
        return df
    
    except Exception as e:
        logging.error(f"Erro ao processar dados: {e}")
        raise