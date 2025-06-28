import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from data_loader import carregar_dados
import folium
from streamlit_folium import folium_static
from folium.plugins import HeatMap
import json

# Configuração da página
st.set_page_config(
    page_title="Mapa do Medo - Maceió",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data(ttl=3600)
def load_data():
    df = carregar_dados()
    if df is not None:
        df['data'] = pd.to_datetime(df['DATA DO FATO'], dayfirst=True)
        df['bairro'] = df['BAIRRO DO FATO'].astype('category')
        df['ocorrencia'] = df['SUBJETIVIDADE COMPLEMENTAR'].astype('category')
        df['hora'] = df['HORA DO FATO']
    return df

df = load_data()

if df is None or df.empty:
    st.error("Falha ao carregar dados ou nenhum dado encontrado.")
    st.stop()

# Sidebar - Filtros
with st.sidebar:
    st.title("Filtros")
    min_date = df['data'].min().date()
    max_date = df['data'].max().date()
    date_range = st.date_input("Período", [max_date - timedelta(days=30), max_date], min_value=min_date, max_value=max_date)

    bairros = st.multiselect("Bairros", options=sorted(df['bairro'].unique()), default=sorted(df['bairro'].unique()))
    ocorrencias = st.multiselect("Tipos de Ocorrência", options=sorted(df['ocorrencia'].unique()), default=sorted(df['ocorrencia'].unique()))
    sexos = st.multiselect("Sexo da Vítima", options=sorted(df['SEXO DA VITIMA'].dropna().unique()), default=sorted(df['SEXO DA VITIMA'].dropna().unique()))

# Aplicação dos filtros
df_filtrado = df.copy()
if len(date_range) == 2:
    df_filtrado = df_filtrado[(df_filtrado['data'].dt.date >= date_range[0]) & (df_filtrado['data'].dt.date <= date_range[1])]
if bairros:
    df_filtrado = df_filtrado[df_filtrado['bairro'].isin(bairros)]
if ocorrencias:
    df_filtrado = df_filtrado[df_filtrado['ocorrencia'].isin(ocorrencias)]
if sexos:
    df_filtrado = df_filtrado[df_filtrado['SEXO DA VITIMA'].isin(sexos)]

# Visualização
st.title("Mapa do Medo - Maceió")

col1, col2, col3 = st.columns(3)
col1.metric("Total Ocorrências", len(df_filtrado))
col2.metric("Bairros Distintos", df_filtrado['bairro'].nunique())
col3.metric("Período", f"{df_filtrado['data'].min().date()} a {df_filtrado['data'].max().date()}")

# Abas
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Distribuição Temporal", "Tipos de Ocorrência", "Vítimas", "Mapa", "Ocorrências por Horário", "Ranking de Bairros"])

with tab1:
    st.subheader("Ocorrências ao Longo do Tempo")
    df_temporal = df_filtrado.resample('M', on='data').size().reset_index(name='count')
    fig = px.line(df_temporal, x='data', y='count', labels={'data': 'Data', 'count': 'Ocorrências'})
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Distribuição por Tipo de Ocorrência")
    df_tipos = df_filtrado.groupby('ocorrencia').size().reset_index(name='count')
    fig = px.pie(df_tipos, values='count', names='ocorrencia')
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("Perfil das Vítimas")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Distribuição por Sexo**")
        df_sexo = df_filtrado['SEXO DA VITIMA'].value_counts().reset_index()
        df_sexo.columns = ['Sexo', 'Quantidade']
        fig = px.bar(df_sexo, x='Sexo', y='Quantidade', labels={'Sexo': 'Sexo', 'Quantidade': 'Quantidade'})
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.markdown("**Distribuição por Idade**")
        fig = px.histogram(df_filtrado, x='IDADE DA VITIMA', nbins=20)
        st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.subheader("Mapa de Ocorrências por Bairro")
    try:
        with open("bairros.geojson", "r") as f:
            bairros_geojson = json.load(f)

        mapa = folium.Map(location=[-9.59, -35.73], zoom_start=13, tiles='cartodbpositron')

        cores_ocorrencias = {
            "Roubo": "red",
            "Homicídio": "black",
            "Assalto": "orange",
            "Feminicídio": "purple"
        }

        for _, row in df_filtrado.iterrows():
            if 'lat' in row and 'lon' in row and pd.notnull(row['lat']) and pd.notnull(row['lon']):
                tipo = row['ocorrencia']
                cor = cores_ocorrencias.get(tipo, "blue")

                popup_text = f"""
                    <b>Bairro:</b> {row['bairro']}<br>
                    <b>Tipo:</b> {tipo}<br>
                    <b>Data:</b> {row['DATA DO FATO']}<br>
                    <b>Hora:</b> {row['HORA DO FATO']}<br>
                    <b>Local:</b> {row['LOCAL DO FATO']}
                """

                folium.CircleMarker(
                    location=[row['lat'], row['lon']],
                    radius=5,
                    popup=popup_text,
                    color=cor,
                    fill=True,
                    fill_color=cor,
                    fill_opacity=0.7
                ).add_to(mapa)

        if 'lat' in df_filtrado.columns and 'lon' in df_filtrado.columns:
            HeatMap(df_filtrado[['lat', 'lon']].dropna().values.tolist(), radius=25).add_to(mapa)

        folium.LayerControl().add_to(mapa)
        folium_static(mapa, width=1000, height=600)

    except Exception as e:
        st.error(f"Erro ao carregar o mapa: {str(e)}")
        st.warning("Mostrando mapa simplificado como fallback")
        if 'lat' in df_filtrado.columns and 'lon' in df_filtrado.columns:
            st.map(df_filtrado[['lat', 'lon']].dropna(), zoom=12)
        else:
            st.info("Colunas de latitude/longitude ausentes.")

with tab5:
    st.subheader("Ocorrências por Horário")
    if 'hora' in df_filtrado.columns:
        df_filtrado['hora_num'] = pd.to_datetime(df_filtrado['hora'], format='%H:%M', errors='coerce').dt.hour
        df_hora = df_filtrado['hora_num'].value_counts().sort_index().reset_index()
        df_hora.columns = ['Hora do Dia', 'Quantidade']
        fig = px.bar(df_hora, x='Hora do Dia', y='Quantidade', labels={'Hora do Dia': 'Hora do Dia', 'Quantidade': 'Ocorrências'})
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Coluna de hora não disponível.")

with tab6:
    st.subheader("Ranking de Bairros com Mais Ocorrências")
    df_bairros = df_filtrado['bairro'].value_counts().reset_index()
    df_bairros.columns = ['Bairro', 'Quantidade']
    fig = px.bar(df_bairros, x='Bairro', y='Quantidade', labels={'Bairro': 'Bairro', 'Quantidade': 'Ocorrências'})
    st.plotly_chart(fig, use_container_width=True)

if st.button("Atualizar Dados"):
    st.cache_data.clear()
    st.experimental_rerun()
