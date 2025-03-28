import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from PIL import Image
import os

# =====================
# Carregamento e tratamento dos dados
# =====================

# Lê o arquivo CSV com os dados do Pipefy
df = pd.read_csv("C:/Users/SKYLINE KALEB/OneDrive/Documentos/pipefy-telas/Integração Pipefy Telas e Salas -Integração.csv")

# Normaliza os nomes das colunas (removendo espaços e colocando em maiúsculo)
df.columns = df.columns.str.strip().str.upper()

# Define colunas com texto e colunas com datas
tempo_cols = ['LOCAL', 'EMPRESA', 'EMPREENDIMENTO', 'PROJETO', 'RESPONS. CLIENTE', 'TELEFONE', 'COMERCIAL', 'RESP. DESIGN', 'RESP. PROGRAMAÇÃO', 'MATERIAL', 'STATUS', 'FASE']
data_cols = ['KICKOFF', 'PRIMEIRAS TELAS', 'DESIGN FINAL', 'PROGRAMAÇÃO FINAL', 'DATA DE ENTREGA']

# Preenche colunas de texto com "Não informado"
for col in tempo_cols:
    if col in df.columns:
        df[col] = df[col].fillna('Não informado')

# Preenche colunas de datas com "-"
for col in data_cols:
    if col in df.columns:
        df[col] = df[col].fillna('-')

# Preenche valores nulos da coluna NPS com -1
if 'NPS' in df.columns:
    df['NPS'] = df['NPS'].fillna(-1)

# Preenche MÊS e ANO com "Não informado"
for col in ['MÊS', 'ANO']:
    if col in df.columns:
        df[col] = df[col].fillna('Não informado')

# Cria coluna PERÍODO combinando MÊS e ANO
df['PERÍODO'] = df['MÊS'] + ' - ' + df['ANO']

# =====================
# Configuração da página Streamlit
# =====================

# Define layout e título da página
st.set_page_config(layout="wide", page_title="Painel Pipefy", page_icon="📊")

# Caminho da imagem do logo
img_dir = "C:/Users/SKYLINE KALEB/OneDrive/Documentos/pipefy-telas/img"
logo_path = os.path.join(img_dir, "logo.png")

# =====================
# Estilos personalizados (CSS)
# =====================
st.markdown("""
    <style>
    html, body, .main {
        background-color: #080830 !important;
        color: white !important;
    }
    .stApp {
        background-color: transparent;
    }
    .stDataFrame thead tr th {
        background-color: #251fce !important;
        color: white !important;
        font-size: 16px !important;
    }
    .stDataFrame tbody tr td {
        color: white !important;
        font-size: 15px !important;
    }
    .metric-container {
        margin: 16px;
        background-color: #0f0f3d;
        padding: 15px;
        border-radius: 50px;
        box-shadow: 0 0 8px rgba(0, 0, 0, 0.3);
        text-align: center;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .metric-container:hover {
        transform: scale(1.03);
        box-shadow: 0 0 12px rgba(156, 252, 249, 0.6);
    }
    .metric-container h3 {
        font-size: 72px;
        color: #9CFCF9;
        margin: 25px;
    }
    .metric-container p {
        font-size: 48px;
        color: #FFFFFF;
        margin: 25px 0 0;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# =====================
# Exibe o logotipo
# =====================
if os.path.exists(logo_path):
    st.image(logo_path, width=450)

# =====================
# Título do dashboard
# =====================
st.markdown("""<h1 style='color: white; text-align:center; font-size: 64px'>PAINEL EXPERIÊNCIAS INTERATIVAS - TELAS E SALAS</h1>""", unsafe_allow_html=True)

# =====================
# Filtro de período selecionado
# =====================
periodos = sorted(df['PERÍODO'].unique())
periodo_selecionado = st.selectbox("Selecionar Período", periodos)
df_filtrado = df[df['PERÍODO'] == periodo_selecionado]

# =====================
# Bloco: Visão Geral do Status
# =====================
with st.container():
    st.markdown("""<h2 style='color:white; text-align:center; font-size: 48px;'>📊 Visão Geral do Status</h2>""", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([2, 1, 1])

    # Gráfico gauge para "Em Andamento"
    em_andamento = df_filtrado.shape[0]
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=em_andamento,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Em Andamento", 'font': {'size': 45, 'color': "white"}},
        gauge={
            'axis': {'range': [0, 100], 'tickcolor': "white"},
            'bar': {'color': "#020133"},
            'bgcolor': "white",
            'steps': [
                {'range': [0, 33], 'color': '#9CFCF9'},
                {'range': [33, 66], 'color': '#60bfff'},
                {'range': [66, 100], 'color': '#0f3bff'}
            ]
        },
        number={'font': {'color': '#FFFFFF', 'size': 100}}
    ))
    fig.update_layout(paper_bgcolor="#080830", height=300, margin=dict(t=10, b=10, l=10, r=10))
    col1.plotly_chart(fig, use_container_width=True)

    # Blocos com métricas de Salas e Telas
    with col2:
        st.markdown(f"""
            <div class='metric-container'>
                <h3>{df_filtrado['EMPREENDIMENTO'].nunique()}</h3>
                <p>Salas</p>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <div class='metric-container'>
                <h3>{df_filtrado['PROJETO'].nunique()}</h3>
                <p>Telas</p>
            </div>
        """, unsafe_allow_html=True)

# =====================
# Bloco: Progresso das Etapas
# =====================
with st.container():
    st.markdown("""<h2 style='color:white; text-align:center; font-size: 48px;'>⚙️ Progresso das Etapas</h2>""", unsafe_allow_html=True)
    col4, col5, col6 = st.columns(3)
    col7, col8, col9 = st.columns(3)

    # Cada coluna mostra uma métrica com contador
    with col4:
        st.markdown(f"""
            <div class='metric-container'>
                <h3>{(df_filtrado['MATERIAL'] == 'Não informado').sum()}</h3>
                <p>Aguardando Materiais</p>
            </div>
        """, unsafe_allow_html=True)
    with col5:
        st.markdown(f"""
            <div class='metric-container'>
                <h3>{(df_filtrado['DESIGN FINAL'] != '-').sum()}</h3>
                <p>Design Final</p>
            </div>
        """, unsafe_allow_html=True)
    with col6:
        st.markdown(f"""
            <div class='metric-container'>
                <h3>{(df_filtrado['FASE'].str.lower().str.contains("design")).sum()}</h3>
                <p>Ajustes Design</p>
            </div>
        """, unsafe_allow_html=True)

    with col7:
        st.markdown(f"""
            <div class='metric-container'>
                <h3>{(df_filtrado['PRIMEIRAS TELAS'] != '-').sum()}</h3>
                <p>Primeiras Telas</p>
            </div>
        """, unsafe_allow_html=True)
    with col8:
        st.markdown(f"""
            <div class='metric-container'>
                <h3>{(df_filtrado['PROGRAMAÇÃO FINAL'] != '-').sum()}</h3>
                <p>Programação Final</p>
            </div>
        """, unsafe_allow_html=True)
    with col9:
        st.markdown(f"""
            <div class='metric-container'>
                <h3>{(df_filtrado['FASE'].str.lower().str.contains("programa")).sum()}</h3>
                <p>Ajustes Programação</p>
            </div>
        """, unsafe_allow_html=True)

# =====================
# Bloco: Entregas
# =====================
with st.container():
    st.markdown("""<h2 style='color:white;text-align:center; font-size: 48px;'>🚎 Entregas</h2>""", unsafe_allow_html=True)
    entregues = (df_filtrado['FASE'].str.lower() == 'entregue').sum()
    col10, col11 = st.columns(2)
    with col10:
        st.markdown(f"""
            <div class='metric-container'>
                <h3>{entregues}</h3>
                <p>Entregues</p>
            </div>
        """, unsafe_allow_html=True)
    with col11:
        st.markdown(f"""
            <div class='metric-container'>
                <h3>{df_filtrado.shape[0] - entregues}</h3>
                <p>Em Espera</p>
            </div>
        """, unsafe_allow_html=True)

# =====================
# Bloco: Tabela com detalhamento
# =====================
st.markdown("""<h2 style='color:white; text-align:center; font-size: 48px;'>📋 Detalhamento das Entradas</h2>""", unsafe_allow_html=True)
st.dataframe(df_filtrado.reset_index(drop=True), use_container_width=True)
