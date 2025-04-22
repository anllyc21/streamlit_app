#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 22 00:24:05 2025

@author: anllycorrea
"""

import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de la página (must be the first Streamlit command)
st.set_page_config(
    page_title="🌍 Tendencias Sísmicas 1960-2023",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for updated color scheme
st.markdown("""
    <style>
    html, body, .stApp {
        background-color: #FFFFFF;
        color: #2e3c50;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #2e3c50;
    }

    .stMarkdown, .stText, .stDataFrame, .stTable {
        color: #2e3c50;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #1E1E2F;
        color: #FFFFFF;
    }

    /* Widgets */
    .stSlider > div, .stNumberInput > div {
        background-color: #2e3c50;
        border-radius: 10px;
        padding: 10px;
    }

    /* Slider thumb & track */
    .stSlider [type="range"]::-webkit-slider-thumb {
        background: #FFFFFF;
    }
    .stSlider [type="range"] {
        background: linear-gradient(to right, #00FEC6, #2A6F73);
    }

    /* Titles */
    .css-10trblm, .css-hxt7ib {
        color: #FFFFFF !important;
    }

    /* Scrollbars */
    ::-webkit-scrollbar {
        width: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #1E1E2F;
    }
    ::-webkit-scrollbar-thumb {
        background: #00FEC6;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Cargar los datos
@st.cache_data
def load_data():
    df = pd.read_excel("Catalogo1960_2023.xlsx", sheet_name="Catalogo1960_2023")
    df['FECHA'] = pd.to_datetime(df['FECHA_UTC'].astype(str), format='%Y%m%d', errors='coerce')
    df['AÑO'] = df['FECHA'].dt.year
    return df.dropna(subset=['FECHA'])

df = load_data()

# Título y descripción
st.title("🌍 Tendencias Sísmicas en el Perú (1960 - 2023)")
st.markdown("""
Explora la actividad sísmica registrada en el Perú desde 1960 hasta 2023. Visualiza tendencias de magnitud y epicentros usando filtros interactivos.
""")

# Filtros laterales
with st.sidebar:
    st.header("🎚️ Filtros Interactivos")
    years = st.slider("Selecciona el rango de años", int(df['AÑO'].min()), int(df['AÑO'].max()), (2000, 2023))
    mag_range = st.slider("Rango de magnitud", float(df['MAGNITUD'].min()), float(df['MAGNITUD'].max()), (5.0, 8.0))
    depth_range = st.slider("Rango de profundidad (km)", int(df['PROFUNDIDAD'].min()), int(df['PROFUNDIDAD'].max()), (0, 300))
    top_n = st.number_input("Mostrar top N eventos por magnitud", min_value=10, max_value=1000, value=100, step=10)

# Aplicar filtros
filtered_df = df[
    (df['AÑO'] >= years[0]) & (df['AÑO'] <= years[1]) &
    (df['MAGNITUD'] >= mag_range[0]) & (df['MAGNITUD'] <= mag_range[1]) &
    (df['PROFUNDIDAD'] >= depth_range[0]) & (df['PROFUNDIDAD'] <= depth_range[1])
]

# Filtro adicional: Top N eventos por magnitud
filtered_df = filtered_df.nlargest(top_n, 'MAGNITUD')

# Gráfico de línea: Tendencia de magnitud por año
st.subheader("📈 Tendencia de Magnitudes por Año")
tendencia = filtered_df.groupby('AÑO')['MAGNITUD'].mean().reset_index()
fig_line = px.line(
    tendencia,
    x='AÑO',
    y='MAGNITUD',
    markers=True,
    title='Magnitud Promedio por Año',
    color_discrete_sequence=['#00feca']  # Bright cyan for visibility
)
fig_line.update_layout(
    height=400,
    plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
    paper_bgcolor='rgba(0,0,0,0)',  # Transparent paper background
    font_color='#E0E0E0',  # Light text color
    xaxis_title='Año',
    yaxis_title='Magnitud Promedio',
    title_x=0.5,
    xaxis=dict(gridcolor='#444', linecolor='#444'),
    yaxis=dict(gridcolor='#444', linecolor='#444')
)
st.plotly_chart(fig_line, use_container_width=True)

# Mapa interactivo mejorado
st.subheader("🗺️ Mapa Interactivo de Epicentros")

# Normalize the size of the points
filtered_df['normalized_size'] = (filtered_df['MAGNITUD'] - filtered_df['MAGNITUD'].min()) / (filtered_df['MAGNITUD'].max() - filtered_df['MAGNITUD'].min()) * 5 + 2

fig_map = px.scatter_mapbox(
    filtered_df,
    lat="LATITUD",
    lon="LONGITUD",
    color="MAGNITUD",
    size="normalized_size",
    size_max=8,
    opacity=0.4,
    hover_name="FECHA",
    hover_data={
        "MAGNITUD": True,
        "PROFUNDIDAD": True,
        "LATITUD": False,
        "LONGITUD": False
    },
    color_continuous_scale="Viridis",  # Better contrast on dark background
    zoom=5,
    center={"lat": -9.19, "lon": -75.01},
    height=600,
)

fig_map.update_layout(
    mapbox_style="open-street-map",
    margin={"r":0, "t":0, "l":0, "b":0},
    paper_bgcolor='rgba(0,0,0,0)',  # Transparent background for map
    font_color='#E0E0E0'
)

st.plotly_chart(fig_map, use_container_width=True)

# Pie de página
st.markdown("---")
st.markdown("🛠️ Aplicación creada por Anlly usando Streamlit y Plotly. Fuente: Catálogo Sísmico 1960-2023.")