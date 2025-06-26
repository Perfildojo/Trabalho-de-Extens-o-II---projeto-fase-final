import pytest
from bot.database import salvar_ocorrencia, obter_ocorrencias_por_bairro
from pathlib import Path

@pytest.fixture
def clean_db(tmp_path):
    db_path = tmp_path / "test.db"
    return db_path

def test_ocorrencia_valida(clean_db):
    # Teste de inserção válida
    id_registro = salvar_ocorrencia("Vergel do Lago", "Roubo", "Rua Teste")
    assert id_registro is not None
    registros = obter_ocorrencias_por_bairro("Vergel do Lago")
    assert len(registros) > 0