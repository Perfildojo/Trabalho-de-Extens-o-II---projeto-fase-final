import sqlite3
import pandas as pd
from pathlib import Path
import logging
from typing import Optional

# Configuração
BASE_DIR = Path(__file__).parent.parent  # Ajuste para pegar o diretório raiz
DB_PATH = BASE_DIR / "data" / "ocorrencias.db"  # Padronizando nome
IMAGE_DIR = BASE_DIR / "data" / "images"

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Adicione temporariamente no database.py
def popular_dados_teste():
    from datetime import datetime
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO relatos 
    (bairro, ocorrencia, rua, data_registro, fonte)
    VALUES (?, ?, ?, ?, ?)
    """, ('Vergel', 'Roubo', 'Rua Teste', datetime.now(), 'bot'))
    conn.commit()
    conn.close()

def inicializar_banco() -> None:
    """Inicializa o banco de dados e estrutura de diretórios"""
    try:
        # Cria diretórios necessários
        IMAGE_DIR.mkdir(parents=True, exist_ok=True)
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Verifica se a tabela já existe
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS relatos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bairro TEXT NOT NULL,
                ocorrencia TEXT NOT NULL,
                rua TEXT,
                imagem TEXT,
                latitude REAL,
                longitude REAL,
                data_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                fonte TEXT DEFAULT 'bot'
            )
        """)
        
        # Cria índices para melhor performance
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_bairro ON relatos (bairro)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_data ON relatos (data_registro)")
        
        conn.commit()
        logger.info(f"Banco inicializado em: {DB_PATH}")
        
    except Exception as e:
        logger.error(f"Falha ao inicializar banco: {e}")
        raise
    finally:
        if 'conn' in locals():
            conn.close()

def carregar_dados() -> pd.DataFrame:
    """Carrega dados do banco com tratamento robusto"""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row  # Para retornar dicionários
        
        # Verifica se a tabela existe
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='relatos'")
        if not cursor.fetchone():
            logger.warning("Tabela 'relatos' não encontrada")
            return pd.DataFrame()
        
        # Query com tratamento de datas
        query = """
        SELECT 
            id,
            bairro,
            ocorrencia,
            rua,
            imagem,
            latitude,
            longitude,
            datetime(data_registro) as data_registro,
            fonte
        FROM relatos
        ORDER BY data_registro DESC
        """
        
        df = pd.read_sql(query, conn)
        
        # Conversão de tipos
        if not df.empty:
            df['data_registro'] = pd.to_datetime(df['data_registro'])
            df['bairro'] = df['bairro'].astype('category')
            df['ocorrencia'] = df['ocorrencia'].astype('category')
            df['fonte'] = df['fonte'].astype('category')
            
        logger.info(f"Carregados {len(df)} registros")
        return df
        
    except Exception as e:
        logger.error(f"Erro ao carregar dados: {e}", exc_info=True)
        return pd.DataFrame()
    finally:
        if 'conn' in locals():
            conn.close()

def salvar_ocorrencia(
    bairro: str,
    ocorrencia: str,
    rua: Optional[str] = None,
    imagem: Optional[str] = None,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None
) -> int:
    """Salva uma nova ocorrência com validação"""
    try:
        if not bairro or not ocorrencia:
            raise ValueError("Bairro e ocorrência são obrigatórios")
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO relatos 
            (bairro, ocorrencia, rua, imagem, latitude, longitude)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            bairro.strip().title(),
            ocorrencia.strip(),
            rua.strip() if rua else None,
            imagem,
            latitude,
            longitude
        ))
        
        conn.commit()
        registro_id = cursor.lastrowid
        logger.info(f"Ocorrência {registro_id} registrada")
        return registro_id
        
    except sqlite3.Error as e:
        logger.error(f"Erro SQL ao salvar: {e}")
        raise
    except Exception as e:
        logger.error(f"Erro ao salvar ocorrência: {e}")
        raise
    finally:
        if 'conn' in locals():
            conn.close()

def testar_conexao() -> dict:
    """Testa a conexão e retorna estatísticas"""
    stats = {
        'caminho_banco': str(DB_PATH),
        'tabela_existe': False,
        'total_registros': 0,
        'ultima_ocorrencia': None
    }
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Verifica tabela
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='relatos'")
        stats['tabela_existe'] = bool(cursor.fetchone())
        
        if stats['tabela_existe']:
            # Conta registros
            cursor.execute("SELECT COUNT(*) FROM relatos")
            stats['total_registros'] = cursor.fetchone()[0]
            
            # Pega última ocorrência
            cursor.execute("SELECT MAX(data_registro) FROM relatos")
            stats['ultima_ocorrencia'] = cursor.fetchone()[0]
        
        return stats
        
    except Exception as e:
        logger.error(f"Teste de conexão falhou: {e}")
        return stats
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    # Teste do módulo
    print("\n=== Teste do Banco de Dados ===")
    inicializar_banco()
    
    stats = testar_conexao()
    print(f"\nStatus do banco:")
    print(f"- Caminho: {stats['caminho_banco']}")
    print(f"- Tabela existe: {'Sim' if stats['tabela_existe'] else 'Não'}")
    print(f"- Total registros: {stats['total_registros']}")
    print(f"- Última ocorrência: {stats['ultima_ocorrencia'] or 'N/A'}")
    
    if stats['tabela_existe'] and stats['total_registros'] == 0:
        print("\nInserindo dados de teste...")
        salvar_ocorrencia(
            bairro="Vergel do Lago",
            ocorrencia="Teste",
            rua="Rua Exemplo"
        )
        print("Dados de teste inseridos. Execute novamente para verificar.")