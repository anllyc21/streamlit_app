#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 20 19:09:58 2025

@author: anllycorrea
"""

import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de la página
st.set_page_config(page_title="Dashboard de Centros de Vacunación", layout="wide")

# Estilos
st.markdown("""
    <style>
    .main {background-color: #f5f7fa;}
    h1 {color: #2c3e50; font-family: 'Arial', sans-serif; text-align: center;}
    h3 {color: #2c3e50; font-family: 'Arial', sans-serif;}
    .stButton>button {
        background-color: #3498db; 
        color: white; 
        border-radius: 5px; 
        border: none; 
        padding: 8px 16px;
    }
    .stButton>button:hover {background-color: #2980b9;}
    </style>
    """, unsafe_allow_html=True)

# Título y descripción principal
st.title("📍 Dashboard de Centros de Vacunación")
st.markdown("Explora la distribución y ubicación de los centros de vacunación por entidad administrativa (DIRESA/MINSA).")

# Datos de los centros de vacunación
data = {
    "nombre": [
        "I.E. Las Mercedes", "Case Municipalidad De Huamanga", "Ex I.E. Guaman Poma De Ayala", "MICRO RED LOS LICENCIADOS",
        "Institucion Educativa Abraham Valdelomar", "Terminal Terrestre Los Libertadores De America", "I.E. Señor De Los Milagros",
        "I.E. Jose Abelardo Quiñones", "I.E. 'Nuestra Señora De Fatima'", "Eesp. Jose Salvador Cavero Ovalle",
        "I.E. Señor De Los Milagros", "I.E.P. Santa Rosa De Lima", "I.E.S. Nuestra Señora Del Perpetuo Socorro",
        "Instituto Superior Pedagogico De Puquio", "I.E Felipe Guaman Poma De Ayala", "I.E 'Martires De La Educacion'",
        "I.E.P 'Micaela Bastidas'", "I.E. 36005 Ascencion", "I.E. Secundaria Rosa De America", "C.S. Santa Ana",
        "Confavicor (Puyhuam Grande - San Cristobal)", "I.E. 37001 PEPIN"
    ],
    "latitud": [
        -13.162139, -13.149851, -13.1537746, -13.1432027, -13.180507, -13.1344276, -13.15675, -13.19191967,
        -13.923375464, -12.933687, -13.01310667, -14.668641667, -14.668641667, -14.66786996, -14.00814,
        -13.74943557, -13.65732406, -12.782758, -12.780081, -12.787558, -12.7800755, -12.7871436
    ],
    "longitud": [
        -74.210698, -74.227728, -74.223992, -74.2311973, -74.220856, -74.23036, -74.221641, -74.2248157,
        -74.33578849, -74.244139, -73.97698, -74.119545333, -74.119545333, -74.1128138, -73.84390667,
        -74.06702115, -73.95321237, -74.981384, -74.990037, -74.9690272, -74.9667152, -74.9727804
    ],
    "entidad_admin": [
        "DIRESA", "DIRESA", "DIRESA", "DIRESA", "DIRESA", "DIRESA", "DIRESA", "DIRESA", "DIRESA", "DIRESA",
        "DIRESA", "MINSA", "MINSA", "MINSA", "DIRESA", "DIRESA", "DIRESA", "DIRESA", "DIRESA", "MINSA", "DIRESA", "MINSA"
    ]
}

# Convertir a DataFrame
df = pd.DataFrame(data)

# Sección 1: Gráfico de barras
st.header("📊 Cantidad de Centros por Entidad Administrativa")
st.markdown("Visualiza la cantidad de centros de vacunación según su entidad administrativa.")

# Contar centros por entidad administrativa
counts = df["entidad_admin"].value_counts().reset_index()
counts.columns = ["entidad_admin", "cantidad"]

# Crear el gráfico de barras
fig_bar = px.bar(
    counts,
    x="entidad_admin",
    y="cantidad",
    color="entidad_admin",
    color_discrete_map={"DIRESA": "#3498db", "MINSA": "#2ecc71"},
    labels={"entidad_admin": "Entidad Administrativa", "cantidad": "Cantidad de Centros"},
    title="Distribución de Centros de Vacunación"
)

# Configurar el estilo del gráfico de barras
fig_bar.update_layout(
    plot_bgcolor="#f5f7fa",
    paper_bgcolor="#f5f7fa",
    title_font=dict(size=18, color="#2c3e50", family="Arial"),
    xaxis_title="Entidad Administrativa",
    yaxis_title="Cantidad de Centros",
    showlegend=False,
    margin=dict(l=50, r=50, t=80, b=50),
    font=dict(color="#2c3e50")
)

# Mostrar el gráfico de barras
st.plotly_chart(fig_bar, use_container_width=True)

# Separador
st.markdown("---")

# Sección 2: Mapa de dispersión
st.header("🗺️ Ubicación de Centros de Vacunación")
st.markdown("Explora las ubicaciones de los centros de vacunación. Filtra por entidad administrativa para más detalle.")

# Filtro interactivo para la entidad administrativa
entidad = st.selectbox("Selecciona la entidad administrativa:", ["Todas", "DIRESA", "MINSA"])

# Filtrar datos según la selección
df_filtered = df if entidad == "Todas" else df[df["entidad_admin"] == entidad]

# Crear el gráfico de dispersión en un mapa
fig_map = px.scatter_mapbox(
    df_filtered,
    lat="latitud",
    lon="longitud",
    hover_name="nombre",
    hover_data={"entidad_admin": True},
    color="entidad_admin",
    color_discrete_map={"DIRESA": "#3498db", "MINSA": "#2ecc71"},
    zoom=8,
    height=600,
    title="Ubicación de Centros de Vacunación"
)

# Configurar el estilo del mapa
fig_map.update_layout(
    mapbox_style="carto-positron",
    margin={"r": 0, "t": 50, "l": 0, "b": 0},
    title_font=dict(size=18, color="#2c3e50", family="Arial"),
    legend_title_text="Entidad Administrativa",
    legend=dict(font=dict(size=12, color="#2c3e50"))
)

# Mostrar el mapa
st.plotly_chart(fig_map, use_container_width=True)

# Nota al pie
st.markdown("**Nota:** Usa el filtro para explorar los centros por entidad administrativa. El gráfico de barras muestra la distribución total.")