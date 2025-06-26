import pandas as pd

def criar_features(dados):
    """Cria novas features para o modelo."""
    
    dados["nova_feature"] = dados["coluna1"] * dados["coluna2"]

    return dados