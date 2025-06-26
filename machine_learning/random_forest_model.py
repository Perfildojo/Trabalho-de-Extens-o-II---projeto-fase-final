from sklearn.ensemble import RandomForestClassifier
import joblib

def treinar_random_forest(X_train, y_train):
    """Treina um modelo Random Forest."""
    modelo = RandomForestClassifier(n_estimators=100, random_state=42)
    modelo.fit(X_train, y_train)
    return modelo

def salvar_modelo(modelo, caminho):
    """Salva o modelo treinado em um arquivo."""
    joblib.dump(modelo, caminho)