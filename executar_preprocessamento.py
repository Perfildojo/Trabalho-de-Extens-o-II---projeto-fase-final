from dashboard.data_preprocessing import processar_dados

if __name__ == "__main__":
    df = processar_dados()
    print(f"{len(df)} registros processados com sucesso.")
