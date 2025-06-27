import pandas as pd
from pathlib import Path
import logging
from typing import Optional

# Configuração
BASE_DIR = Path(__file__).parent.parent
CSV_PATH = BASE_DIR / "data" / "processed" / "ocorrencias_processadas.csv"

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def carregar_csv_processado() -> Optional[pd.DataFrame]:
    """Carrega e padroniza o CSV com suas colunas específicas"""
    if not CSV_PATH.exists():
        logger.error(f"Arquivo não encontrado: {CSV_PATH}")
        return None
        
    try:
        # Carrega mantendo todas as colunas originais
        df = pd.read_csv(
            CSV_PATH,
            delimiter=',',
            encoding='latin1',
            parse_dates=['DATA DO FATO', 'data_registro'],
            dayfirst=True  # Importante para datas no formato dd/mm/yyyy
        )
        
        # Padroniza nomes e conteúdo
        df = df.rename(columns={
            'BAIRRO DO FATO': 'bairro',
            'SUBJETIVIDADE': 'ocorrencia',
            'DATA DO FATO': 'data',
            'LOCAL DO FATO': 'rua',
            'HORA DO FATO': 'hora'
        })
        
        # Filtra apenas Maceió
        df = df[df['CIDADE DO FATO'] == 'Maceió']
        
        # Limpeza e transformações
        df = df.assign(
            bairro=df['bairro'].str.title().fillna('DESCONHECIDO'),
            ocorrencia=df['ocorrencia'].str.replace('CVLI', 'Crime Violento').str.title(),
            data=pd.to_datetime(df['data']),
            rua=df['rua'].fillna('VIA PÚBLICA').str.title(),
            cidade='Maceió',
            fonte='oficial'
        )
        
        # Seleciona e ordena colunas
        cols_principais = [
            'data', 'bairro', 'ocorrencia', 'rua', 
            'hora', 'SEXO DA VITIMA', 'IDADE DA VITIMA',
            'INSTRUMENTO UTILIZADO', 'fonte'
        ]
        
        return df[cols_principais].sort_values('data', ascending=False)
        
    except Exception as e:
        logger.error(f"Erro ao processar CSV: {e}", exc_info=True)
        return None

def gerar_csv_exemplo():
    """Gera um CSV de exemplo com sua estrutura"""
    dados = {
        'D_CONTROLE': [1, 2],
        'SUBJETIVIDADE': ['CVLI', 'Roubo'],
        'DATA DO FATO': ['29/05/2012', '30/05/2012'],
        'BAIRRO DO FATO': ['Benedito Bentes', 'Vergel'],
        'CIDADE DO FATO': ['Maceió', 'Maceió'],
        'LOCAL DO FATO': ['Rua X', 'Avenida Y']
    }
    df = pd.DataFrame(dados)
    df.to_csv(CSV_PATH, index=False, encoding='latin1')
    print(f"CSV exemplo gerado em: {CSV_PATH}")

if __name__ == "__main__":
    # Teste
    print("=== Teste de Leitura ===")
    df = carregar_csv_processado()
    
    if df is not None:
        print("\nDados carregados:")
        print(df.head())
        print(f"\nTotal de registros: {len(df)}")
        print(f"Período: {df['data'].min().date()} a {df['data'].max().date()}")
    else:
        print("\n❌ Falha ao carregar dados. Gerando exemplo...")
        gerar_csv_exemplo()