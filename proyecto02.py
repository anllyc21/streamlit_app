#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 20 18:33:52 2025

@author: anllycorrea
"""

import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de la página
st.set_page_config(page_title="Mapa de Centros de Vacunación", layout="wide")

# Estilos
st.markdown("""
    <style>
    .main {background-color: #f5f7fa;}
    h1 {color: #2c3e50; font-family: 'Arial', sans-serif; text-align: center;}
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

# Título y descripción
st.title("📍 Mapa de Centros de Vacunación")
st.markdown("Explora la ubicación de los centros de vacunación por entidad administrativa (DIRESA/MINSA). Selecciona una entidad para filtrar los datos.")

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

# Filtro interactivo para la entidad administrativa
entidad = st.selectbox("Selecciona la entidad administrativa:", ["Todas", "DIRESA", "MINSA"])

# Filtrar datos según la selección
if entidad != "Todas":
    df = df[df["entidad_admin"] == entidad]

# Gráfico de dispersión en un mapa con Plotly
fig = px.scatter_mapbox(
    df,
    lat="latitud",
    lon="longitud",
    hover_name="nombre",
    hover_data={"entidad_admin": True},
    color="entidad_admin",
    color_discrete_map={"DIRESA": "#3498db", "MINSA": "#2ecc71"},  # Colores minimalistas de salud
    zoom=8,
    height=600,
    title="Ubicación de Centros de Vacunación"
)

# Configurar el estilo del mapa
fig.update_layout(
    mapbox_style="carto-positron",
    margin={"r": 0, "t": 50, "l": 0, "b": 0},
    title_font=dict(size=20, color="#2c3e50", family="Arial"),
    legend_title_text="Entidad Administrativa",
    legend=dict(font=dict(size=12, color="#2c3e50"))
)

# Mostrar el gráfico
st.plotly_chart(fig, use_container_width=True)

# Nota al pie
st.markdown("**Nota:** Los puntos en el mapa representan centros de vacunación. Usa el filtro para explorar por entidad administrativa.")