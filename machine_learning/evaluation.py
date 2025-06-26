from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

def avaliar_modelo(y_true, y_pred):
    """Avalia o modelo com base em métricas de desempenho."""
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)

    print(f"Acurácia: {accuracy:.2f}")
    print(f"Precisão: {precision:.2f}")
    print(f"Recall: {recall:.2f}")
    print(f"F1-Score: {f1:.2f}")