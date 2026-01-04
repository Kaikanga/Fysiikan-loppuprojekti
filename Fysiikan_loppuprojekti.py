import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium
from scipy.signal import butter,filtfilt
import numpy as np

def butter_lowpass_filter(data, cutoff, nyq, order):
    normal_cutoff = cutoff / nyq
    # Get the filter coefficients
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = filtfilt(b, a, data)
    return y

def butter_highpass_filter(data, cutoff,  nyq, order):
    normal_cutoff = cutoff / nyq
    # Get the filter coefficients 
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    y = filtfilt(b, a, data)
    return y

url ="https://raw.githubusercontent.com/Kaikanga/Fysiikan-loppuprojekti/refs/heads/main/combined.csv"
df = pd.read_csv(url)

st.title('Pikku happihyppely pakkasessa')

#Keskinopeus ja kuljettu matka
st.write("Keskinopeus on :", df['Speed (m/s)'].mean(),'m/s' )
st.write("Kokonaismatka on :", df['Distance (km)'].max(),'km' )

data = df['Linear Acceleration y (m/s^2)']
T_tot = df['Time (s)'].max() #Koko datan pituus
n = len(df['Time (s)']) #Datapisteiden lukumäärä
fs = n/T_tot #Näytteenottotaajus
nyq = fs/2 #Nyqvistin taajuus
order = 3
cutoff = 1/0.4
data_filt = butter_lowpass_filter(data, cutoff, nyq, order)

#Lasketaan askeleet
jaksot = 0
for i in range(n-1):
    if data_filt[i]/data_filt[i+1] < 0:
        jaksot = jaksot + 1/2

st.write('Askelten määrä laskettuna suodatuksen avulla:', jaksot , 'askelta')

signal = df['Linear Acceleration y (m/s^2)']
t = df['Time (s)']
N = len(signal)
dt = np.max(t)/N

#Fourier-analyysi
fourier = np.fft.fft(signal,N) #Fourier-muunnos
psd = fourier*np.conj(fourier)/N #Tehospektri
freq = np.fft.fftfreq(N,dt) #Taajuudet
L = np.arange(1,int(N/2))

f_max = freq[L][psd[L] == np.max(psd[L])][0]
T = 1/f_max #Askeleeseen kuluva aika (jaksonaika)
steps =  f_max*np.max(t) #Askelmäärä

st.write('Askelten määrä laskettuna Fourier-analyysin avulla: ', np.round(steps), 'askelta')

distance = df['Distance (km)'].max()
askelpituus = (distance/steps)*100000

st.write('Askelpituus on ', np.round(askelpituus), 'cm')

st.title('Suodatetun kiihtyvyysdatan y-komponentin kuvaaja')

#Piirretään kuvaaja suodatetusta signaalista, josta laskettu askelmäärä
st.line_chart(data_filt, y_label = 'Suodatettu data y, m/s^2',x_label = 'Aika [a]' )

#Piirretään kuvaaja, kuljettu matka ja aika
#st.line_chart(df_m, x = 'Time (s)', y = 'Distance (km)', y_label = 'Distance',x_label = 'Time')

#Luodaan kartta
map_df = df.dropna(
    subset=["Latitude (°)", "Longitude (°)"]
)

start_lat = map_df['Latitude (°)'].mean()
start_long = map_df['Longitude (°)'].mean()
map = folium.Map(location = [start_lat,start_long], zoom_start = 14)

folium.PolyLine(map_df[['Latitude (°)','Longitude (°)']], color = 'blue', weight = 3.5, opacity = 1).add_to(map)

st.title('Karttakuva happihyppelystä')

st_map = st_folium(map, width=900, height=650)