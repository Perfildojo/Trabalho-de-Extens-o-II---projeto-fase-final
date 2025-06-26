import sqlite3
import os
from pathlib import Path

# Configuração de caminhos
BASE_DIR = Path(__file__).parent.parent
DB_PATH = BASE_DIR / "data" / "bot" / "relatos.db"
IMAGE_DIR = BASE_DIR / "data" / "bot" / "images"

def inicializar_banco():
    """Cria a estrutura do banco de dados e diretórios necessários"""
    try:
        # Cria diretórios se não existirem
        IMAGE_DIR.mkdir(parents=True, exist_ok=True)
        
        # Conecta ao banco (cria automaticamente se não existir)
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Cria tabela com schema atualizado
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
        
        # Cria índice para consultas por bairro
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_bairro ON relatos (bairro)
        """)
        
        conn.commit()
        print(f"Banco inicializado com sucesso em: {DB_PATH}")
        
    except Exception as e:
        print(f"Erro ao inicializar banco: {e}")
        raise
    finally:
        if conn:
            conn.close()

def salvar_ocorrencia(bairro: str, ocorrencia: str, rua: str = None, 
                     imagem: str = None, latitude: float = None, 
                     longitude: float = None):
    """Salva uma nova ocorrência com tratamento robusto"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO relatos 
            (bairro, ocorrencia, rua, imagem, latitude, longitude)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            bairro.strip().title(),  # Padroniza formato do bairro
            ocorrencia.strip(),
            rua.strip() if rua else None,
            imagem,
            latitude,
            longitude
        ))
        
        conn.commit()
        print("Ocorrência registrada com sucesso!")
        
        # Retorna o ID do registro inserido
        return cursor.lastrowid
        
    except sqlite3.Error as e:
        print(f"Erro ao salvar ocorrência: {e}")
        raise
    finally:
        if conn:
            conn.close()

def obter_ocorrencias_por_bairro(bairro: str, limite: int = 100):
    """Consulta ocorrências por bairro"""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row  # Para retornar dicionários
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM relatos 
            WHERE bairro = ? 
            ORDER BY data_registro DESC 
            LIMIT ?
        """, (bairro.strip().title(), limite))
        
        return [dict(row) for row in cursor.fetchall()]
        
    except sqlite3.Error as e:
        print(f"Erro na consulta: {e}")
        return []
    finally:
        if conn:
            conn.close()