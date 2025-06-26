import joblib
import pandas as pd
from .data_preprocessing import preprocessar_dados
from .feature_engineering import criar_features

def carregar_modelo(caminho_modelo):
    """Carrega o modelo treinado."""
    return joblib.load(caminho_modelo)

def fazer_previsoes(dados, caminho_modelo):
    """Faz previsões com base nos dados fornecidos."""
    dados = preprocessar_dados(dados)
    dados = criar_features(dados)
    modelo = carregar_modelo(caminho_modelo)
    previsoes = modelo.predict(dados)
    return previsoes