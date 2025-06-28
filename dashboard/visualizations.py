import plotly.express as px
import pandas as pd

def criar_mapa(df):
    """Cria um mapa scatter plot com os dados de ocorrências"""
    if df is None or df.empty:
        return px.scatter_mapbox(title="Sem dados disponíveis para exibir no mapa")
    
    try:
        # Verifica se temos colunas necessárias
        if not all(col in df.columns for col in ['latitude', 'longitude']):
            # Se não tiver coordenadas, agrupa por bairro (exemplo)
            if 'bairro' in df.columns:
                df_agg = df['bairro'].value_counts().reset_index()
                df_agg.columns = ['bairro', 'contagem']
                # Aqui você precisaria de um dicionário de coordenadas por bairro
                # bairro_coords = {...}  # Mapeamento de bairro para lat/long
                # df_agg['latitude'] = df_agg['bairro'].map(lambda x: bairro_coords.get(x, (0,0))[0])
                # df_agg['longitude'] = df_agg['bairro'].map(lambda x: bairro_coords.get(x, (0,0))[1])
                # Por enquanto, vamos retornar um mapa vazio
                return px.scatter_mapbox(title="Coordenadas não disponíveis - Adicione um mapeamento de bairros")
            else:
                return px.scatter_mapbox(title="Dados insuficientes para criar o mapa")
        
        # Cria o mapa com os dados disponíveis
        fig = px.scatter_mapbox(
            df,
            lat="latitude",
            lon="longitude",
            color="ocorrencia",
            hover_name="bairro",
            hover_data=["rua", "data_registro"],
            zoom=12,
            height=600,
            title="Ocorrências por Localização"
        )
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
        return fig
    except Exception as e:
        print(f"Erro ao criar mapa: {str(e)}")
        return px.scatter_mapbox(title="Erro ao gerar o mapa")

def criar_grafico_barras(df):
    """Cria um gráfico de barras comparativo"""
    if df is None or df.empty:
        return px.bar(title="Sem dados disponíveis para exibir")
    
    try:
        # Agrupa por tipo de ocorrência e bairro
        df_agg = df.groupby(['ocorrencia', 'bairro']).size().reset_index(name='contagem')
        
        fig = px.bar(
            df_agg,
            x='ocorrencia',
            y='contagem',
            color='bairro',
            barmode='group',
            title="Comparativo de Ocorrências por Bairro",
            labels={'contagem': 'Número de Ocorrências', 'ocorrencia': 'Tipo de Ocorrência'}
        )
        return fig
    except Exception as e:
        print(f"Erro ao criar gráfico de barras: {str(e)}")
        return px.bar(title="Erro ao gerar gráfico")