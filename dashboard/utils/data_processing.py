import pandas as pd
import json
from typing import Dict, List, Optional

def load_data(filepath: str) -> pd.DataFrame:
    """
    Carrega dados de um arquivo CSV, JSON ou Excel.
    
    Args:
        filepath (str): Caminho do arquivo de dados
    
    Returns:
        pd.DataFrame: DataFrame com os dados carregados
    """
    if filepath.endswith('.csv'):
        return pd.read_csv(filepath)
    elif filepath.endswith('.json'):
        return pd.read_json(filepath)
    elif filepath.endswith(('.xls', '.xlsx')):
        return pd.read_excel(filepath)
    else:
        raise ValueError("Formato de arquivo não suportado")

def filter_data(df: pd.DataFrame, filters: Dict) -> pd.DataFrame:
    """
    Filtra os dados com base em critérios especificados.
    
    Args:
        df (pd.DataFrame): DataFrame com os dados
        filters (Dict): Dicionário com os filtros (ex: {"bairro": "Centro"})
    
    Returns:
        pd.DataFrame: DataFrame filtrado
    """
    for column, value in filters.items():
        df = df[df[column] == value]
    return df

def aggregate_data(df: pd.DataFrame, group_by: List[str], metrics: List[str]) -> pd.DataFrame:
    """
    Agrega dados por determinadas colunas.
    
    Args:
        df (pd.DataFrame): DataFrame com os dados
        group_by (List[str]): Lista de colunas para agrupar
        metrics (List[str]): Lista de métricas para calcular
    
    Returns:
        pd.DataFrame: DataFrame agregado
    """
    return df.groupby(group_by)[metrics].agg(['sum', 'count', 'mean']).reset_index()

def save_processed_data(df: pd.DataFrame, output_path: str) -> None:
    """
    Salva os dados processados em um arquivo.
    
    Args:
        df (pd.DataFrame): DataFrame com os dados processados
        output_path (str): Caminho para salvar o arquivo
    """
    if output_path.endswith('.csv'):
        df.to_csv(output_path, index=False)
    elif output_path.endswith('.json'):
        df.to_json(output_path, orient='records')
    else:
        raise ValueError("Formato de saída não suportado")

# Função específica para o projeto Mapa do Medo
def process_fear_map_data(raw_data: pd.DataFrame) -> pd.DataFrame:
    """
    Processa dados específicos para o Mapa do Medo.
    
    Args:
        raw_data (pd.DataFrame): Dados brutos de incidentes/ocorrências
    
    Returns:
        pd.DataFrame: Dados processados para visualização
    """
    processed = raw_data.copy()
    
    # Exemplo de processamento:
    if 'data_ocorrencia' in processed.columns:
        processed['data_ocorrencia'] = pd.to_datetime(processed['data_ocorrencia'])
        processed['hora_ocorrencia'] = processed['data_ocorrencia'].dt.time
        processed['dia_semana'] = processed['data_ocorrencia'].dt.day_name()
    
    return processed