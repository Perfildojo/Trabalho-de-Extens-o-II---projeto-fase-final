import plotly.express as px
import pandas as pd

def criar_mapa(dados):
    """Gera mapa interativo com clusters"""
    if dados.empty or 'latitude' not in dados.columns:
        return px.scatter_mapbox(title="Sem dados geoespaciais disponíveis")
    
    fig = px.density_mapbox(
        dados,
        lat='latitude',
        lon='longitude',
        radius=10,
        zoom=12,
        hover_name='bairro',
        hover_data=['ocorrencia', 'rua', 'data_registro'],
        mapbox_style="open-street-map",
        title="Densidade de Ocorrências"
    )
    fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
    return fig

def criar_grafico_barras(dados):
    """Comparativo por bairro e tipo"""
    if dados.empty:
        return px.bar(title="Sem dados disponíveis")
    
    contagem = dados.groupby(['bairro', 'ocorrencia']).size().reset_index(name='contagem')
    fig = px.bar(
        contagem,
        x='bairro',
        y='contagem',
        color='ocorrencia',
        barmode='stack',
        title='Ocorrências por Bairro e Tipo'
    )
    return fig