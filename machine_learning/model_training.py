import pandas as pd
from sklearn.model_selection import train_test_split
from .data_preprocessing import preprocessar_dados
from .feature_engineering import criar_features
from .random_forest_model import treinar_random_forest, salvar_modelo

def treinar_modelo():
    """Função principal para treinar o modelo."""
    
    dados = pd.read_csv("dados_ocorrencias.csv")  

    dados = preprocessar_dados(dados)

    dados = criar_features(dados)

    X = dados.drop("target", axis=1)  
    y = dados["target"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    modelo = treinar_random_forest(X_train, y_train)

    salvar_modelo(modelo, "modelo_random_forest.pkl")

    print("Modelo treinado e salvo com sucesso!")