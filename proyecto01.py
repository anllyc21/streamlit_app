# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import streamlit as st
import numpy as np
import datetime 
from datetime import time
import pandas as pd

st.title('Mi nuevo proyecto de ciencia de datos')
st.write('Hola **como** estas')

st.title("Titulo")
num = st.slider("Barra de numeros", 0, 100, step=10)
st.write("El numero ingresado es {}".format(num))

appointment = st.slider(
 "Programe la asesoria:",
 value=(time(11, 30), time(12, 45)))
st.write("Esta agendado para:", appointment)

d = st.date_input(
 "Fecha de cumpleaños",
 datetime.date(2019, 7, 6))
st.write('Tu cumpleños es:', d)

n = st.slider("n", 5,100, step=1)
chart_data = pd.DataFrame(np.random.randn(n),columns=['data'])
st.line_chart(chart_data)

df = pd.DataFrame(
 np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
 columns=['lat', 'lon'])
st.map(df)
