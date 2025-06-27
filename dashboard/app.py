import streamlit as st
import pandas as pd
import plotly.express as px
from dashboard.database import carregar_dados
from dashboard.visualizations import criar_mapa, criar_grafico_barras
from datetime import datetime, timedelta
from pathlib import Path

st.set_page_config(
    page_title="Mapa do Medo - Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data(ttl=300)
def load_data(source="db"):
    """Carrega dados do banco ou do CSV processado"""
    if source == "csv":
        path_csv = Path(__file__).parent.parent / "data" / "processed" / "ocorrencias_processadas.csv"
        try:
            df = pd.read_csv(path_csv, parse_dates=['data_ocorrencia'])
            df = df.rename(columns={
                'data_ocorrencia': 'data_registro',
                'tipo_ocorrencia': 'ocorrencia'
            })
            df['bairro'] = df['bairro'].astype('category')
            df['ocorrencia'] = df['ocorrencia'].astype('category')
            return df
        except Exception as e:
            st.error(f"Erro ao carregar CSV: {e}")
            return pd.DataFrame()
    else:
        return carregar_dados()

# Sidebar
with st.sidebar:
    st.title("Filtros")

    # Escolher a fonte de dados
    fonte = st.radio("Fonte de Dados:", ["Banco de Dados", "Arquivo CSV Processado"])
    fonte_escolhida = "csv" if fonte == "Arquivo CSV Processado" else "db"

    # Intervalo de datas
    date_range = st.date_input(
        "Período",
        value=[datetime.now() - timedelta(days=30), datetime.now()],
        max_value=datetime.now()
    )

# Carregamento dos dados
df = load_data(fonte_escolhida)

# Filtros dinâmicos (após carregar)
if not df.empty:
    with st.sidebar:
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
    from dashboard.visualizations import criar_mapa, criar_grafico_barras

    st.title("Dashboard Mapa do Medo - Dados em Tempo Real")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Ocorrências", len(df))
    col2.metric("Bairros Únicos", df['bairro'].nunique())
    if not df['data_registro'].isnull().all():
        col3.metric("Última Atualização", df['data_registro'].max().strftime('%d/%m/%Y %H:%M'))

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
else:
    st.warning("Nenhum dado encontrado com os filtros ou na fonte selecionada.")

def main():
    """Função chamada pelo run_dashboard.py"""
    pass  # O código já roda no escopo principal