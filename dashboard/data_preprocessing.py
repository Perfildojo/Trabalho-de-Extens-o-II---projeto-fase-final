import pandas as pd
from pathlib import Path
import logging
from datetime import datetime

# Configuração de caminhos
BASE_DIR = Path(__file__).parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_PATH = PROCESSED_DIR / "ocorrencias_processadas.csv"

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(BASE_DIR / 'data_processing.log'),
        logging.StreamHandler()
    ]
)

def processar_dados():
    """
    Processa arquivos CSV de ocorrências policiais com tratamento robusto para arquivos vazios.
    """
    try:
        arquivos_csv = list(RAW_DIR.glob("*.csv"))
        if not arquivos_csv:
            logging.warning(f"Nenhum arquivo CSV encontrado em {RAW_DIR}")
            return pd.DataFrame()

        dataframes = []
        colunas_necessarias = ["DATA DO FATO", "HORA DO FATO", "BAIRRO DO FATO", "SUBJETIVIDADE COMPLEMENTAR"]
        
        for arquivo in arquivos_csv:
            try:
                # Verifica se o arquivo não está vazio
                if arquivo.stat().st_size == 0:
                    logging.warning(f"Arquivo vazio ignorado: {arquivo.name}")
                    continue
                
                # Tenta ler o CSV com múltiplos engines como fallback
                try:
                    df = pd.read_csv(arquivo, encoding='utf-8', delimiter=',', engine='python')
                except:
                    try:
                        df = pd.read_csv(arquivo, encoding='latin1', delimiter=';', engine='python')
                    except Exception as e:
                        logging.error(f"Falha ao ler {arquivo.name}: {str(e)}")
                        continue
                
                # Verifica se o DataFrame está vazio
                if df.empty:
                    logging.warning(f"Arquivo {arquivo.name} não contém dados válidos")
                    continue
                
                # Restante do processamento...
                if all(col in df.columns for col in colunas_necessarias):
                    df_processado = (
                        df.dropna(subset=colunas_necessarias)
                        .assign(
                            data_registro=lambda x: pd.to_datetime(
                                x["DATA DO FATO"] + " " + x["HORA DO FATO"], 
                                errors='coerce'
                            )
                        )
                        .dropna(subset=['data_registro'])
                    )
                    dataframes.append(df_processado)
                else:
                    logging.warning(f"Colunas ausentes em {arquivo.name}")

            except Exception as e:
                logging.error(f"Erro ao processar {arquivo.name}: {str(e)}", exc_info=True)
                continue

        if not dataframes:
            return pd.DataFrame()

        df_final = pd.concat(dataframes, ignore_index=True)
        df_final.to_csv(PROCESSED_PATH, index=False)
        return df_final

    except Exception as e:
        logging.error(f"Erro crítico: {str(e)}", exc_info=True)
        return pd.DataFrame()