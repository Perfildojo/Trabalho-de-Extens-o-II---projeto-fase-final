import pandas as pd
import sqlite3

# Carregar o CSV
df = pd.read_csv("Dados Benedito Bentes PAF - Worksheet.csv")

# Ajustar colunas
df.columns = [col.strip().upper().replace(" ", "_").replace("/", "_") for col in df.columns]
df["DATA_DO_FATO"] = pd.to_datetime(df["DATA_DO_FATO"], errors="coerce", dayfirst=True)
df["IDADE_DA_VITIMA"] = df["IDADE_DA_VITIMA"].fillna(0).astype(int)

# Criar banco
conn = sqlite3.connect("ocorrencias_benedito_bentes.db")
df.to_sql("ocorrencias_benedito_bentes", conn, if_exists="replace", index=False)
conn.close()

print("Banco criado com sucesso!")
