import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium

df_a = pd.read_csv('Kiihtyvyys.csv')
df_m = pd.read_csv('GPSData.csv')

st.title('Pikku happihyppely')

#Keskinopeus ja kuljettu matka
st.write("Keskinopeus on :", df_m['Speed (m/s)'].mean(),'m/s' )
st.write("Kokonaismatka on :", df_m['Distance (km)'].max(),'km' )

#Piirretään kuvaaja, kuljettu matka ja aika
st.line_chart(df_m, x = 'Time (s)', y = 'Distance (km)', y_label = 'Distance',x_label = 'Time')

#Luodaan kartta
start_lat = df_m['Latitude (°)'].mean()
start_long = df_m['Longitude (°)'].mean()
map = folium.Map(location = [start_lat,start_long], zoom_start = 14)

folium.PolyLine(df_m[['Latitude (°)','Longitude (°)']], color = 'blue', weight = 3.5, opacity = 1).add_to(map)

st_map = st_folium(map, width=900, height=650)