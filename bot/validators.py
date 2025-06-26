from bot.config import BAIRROS, OCORRENCIAS

def normalizar_entrada(texto: str) -> str:
    """Normaliza o texto para comparação: remove espaços extras e padroniza capitalização"""
    return ' '.join(texto.strip().split()).title()

def validar_bairro(bairro: str) -> str:
    """Padroniza e valida o bairro com tratamento robusto"""
    try:
        # Normaliza a entrada
        bairro_normalizado = normalizar_entrada(bairro)
        
        # Extrai os nomes dos bairros válidos
        bairros_validos = [normalizar_entrada(b[0]) for b in BAIRROS]
        
        # Verifica se o bairro está na lista
        if bairro_normalizado not in bairros_validos:
            raise ValueError(
                f"Bairro inválido. Opções válidas são: {', '.join(bairros_validos)}"
            )
            
        return bairro_normalizado
        
    except Exception as e:
        raise ValueError(f"Erro ao validar bairro: {str(e)}")

def validar_ocorrencia(ocorrencia: str) -> str:
    """Padroniza e valida o tipo de ocorrência com tratamento robusto"""
    try:
        # Normaliza a entrada
        ocorrencia_normalizada = normalizar_entrada(ocorrencia)
        
        # Extrai as ocorrências válidas
        ocorrencias_validas = [normalizar_entrada(o[0]) for o in OCORRENCIAS]
        
        # Verifica se a ocorrência está na lista
        if ocorrencia_normalizada not in ocorrencias_validas:
            raise ValueError(
                f"Ocorrência inválida. Opções válidas são: {', '.join(ocorrencias_validas)}"
            )
            
        return ocorrencia_normalizada
        
    except Exception as e:
        raise ValueError(f"Erro ao validar ocorrência: {str(e)}")