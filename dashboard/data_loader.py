import sqlite3
import pandas as pd
from pathlib import Path
import logging

# Configuração
BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR.parent / "data" / "relatos.db"
logging.basicConfig(level=logging.INFO)

def carregar_dados():
    """Carrega dados do banco SQLite com tratamento robusto"""
    try:
        conn = sqlite3.connect(DB_PATH)
        
        # Verifica se a tabela existe
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='relatos'")
        if not cursor.fetchone():
            logging.warning("Tabela 'relatos' não encontrada")
            return pd.DataFrame()
        
        # Carrega os dados
        query = """
        SELECT 
            bairro, 
            ocorrencia, 
            rua, 
            datetime(data_registro) as data_registro,
            latitude,
            longitude,
            fonte
        FROM relatos
        """
        df = pd.read_sql(query, conn)
        
        # Conversão de tipos
        if not df.empty:
            df['data_registro'] = pd.to_datetime(df['data_registro'])
            df['bairro'] = df['bairro'].astype('category')
            df['ocorrencia'] = df['ocorrencia'].astype('category')
        
        return df

    except Exception as e:
        logging.error(f"Erro ao carregar dados: {e}")
        return pd.DataFrame()
    finally:
        if 'conn' in locals():
            conn.close()