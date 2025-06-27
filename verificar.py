import pandas as pd
df = pd.read_csv('data/processed/ocorrencias_processadas.csv')
print("Colunas presentes:", df.columns.tolist())
print("\nPrimeiras linhas:")
print(df.head())