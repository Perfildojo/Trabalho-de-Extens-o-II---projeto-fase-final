import streamlit as st
import pandas as pd
import plotly.express as px
from data_loader import carregar_dados
from visualizations import criar_mapa, criar_grafico_barras
from datetime import datetime, timedelta

# Configuração da página
st.set_page_config(
    page_title="Mapa do Medo - Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Carregamento de dados com cache
@st.cache_data(ttl=300)  # Atualiza a cada 5 minutos
def load_data():
    return carregar_dados()

df = load_data()

# Sidebar com filtros
with st.sidebar:
    st.title("Filtros")
    
    # Filtro temporal
    date_range = st.date_input(
        "Período",
        value=[datetime.now() - timedelta(days=30), datetime.now()],
        max_value=datetime.now()
    )
    
    # Filtros dinâmicos
    bairros = st.multiselect(
        "Bairros",
        options=df['bairro'].unique(),
        default=df['bairro'].unique()[:2]
    )
    
    ocorrencias = st.multiselect(
        "Tipos de Ocorrência",
        options=df['ocorrencia'].unique(),
        default=df['ocorrencia'].unique()[:3]
    )

# Aplicar filtros
if len(date_range) == 2:
    mask = (df['data_registro'] >= pd.to_datetime(date_range[0])) & \
           (df['data_registro'] <= pd.to_datetime(date_range[1]))
    df = df[mask]

if bairros:
    df = df[df['bairro'].isin(bairros)]
if ocorrencias:
    df = df[df['ocorrencia'].isin(ocorrencias)]

# Visualizações
st.title("Dashboard Mapa do Medo - Dados em Tempo Real")

# Métricas
col1, col2, col3 = st.columns(3)
col1.metric("Total Ocorrências", len(df))
col2.metric("Bairros Únicos", df['bairro'].nunique())
col3.metric("Última Atualização", df['data_registro'].max().strftime('%d/%m/%Y %H:%M'))

# Abas
tab1, tab2, tab3 = st.tabs(["Mapa", "Análise Temporal", "Comparativo"])

with tab1:
    st.plotly_chart(criar_mapa(df), use_container_width=True)

with tab2:
    fig_temp = px.line(
        df.resample('D', on='data_registro').size(),
        title="Ocorrências ao Longo do Tempo"
    )
    st.plotly_chart(fig_temp, use_container_width=True)

with tab3:
    st.plotly_chart(criar_grafico_barras(df), use_container_width=True)