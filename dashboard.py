import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
data = pd.read_csv('data.csv')

# Filter data berdasarkan jam
jam_mulai = st.sidebar.slider('Jam Mulai', 0, 23, 0)
jam_selesai = st.sidebar.slider('Jam Selesai', 0, 23, 23)

# Filter data berdasarkan jam
filtered_data = data[(data['hour'] >= jam_mulai) & (data['hour'] <= jam_selesai)]

# Tambahkan kolom 'Kategori Jam'
filtered_data['Kategori Jam'] = pd.cut(filtered_data['hour'], bins=[0, 6, 12, 18, 24], labels=['Dini Hari', 'Pagi', 'Siang', 'Malam'])

# Sidebar untuk pilihan grafik
selected_chart = st.sidebar.selectbox('Pilih Grafik', ['Scatter Plot PM2.5 vs WSPM', 'Line Plot PM10 Berdasarkan Kategori Jam', 'Grafik Rata-rata PM2.5 dan PM10', 'Distribusi Nilai PM2.5 dan PM10'])
st.set_option('deprecation.showPyplotGlobalUse', False)
# Judul Dashboard
st.title('Dashboard Kualitas Udara')

# Visualisasi data
if selected_chart == 'Scatter Plot PM2.5 vs WSPM':
    st.subheader('Scatter Plot PM2.5 vs WSPM')
    fig, ax = plt.subplots()
    sns.scatterplot(x='WSPM', y='PM2.5', data=filtered_data, ax=ax)
    st.pyplot(fig)

elif selected_chart == 'Line Plot PM10 Berdasarkan Kategori Jam':
    st.subheader('Line Plot PM10 Berdasarkan Kategori Jam')
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(x='hour', y='PM10', data=filtered_data, hue='Kategori Jam', ci=None)
    ax.set_xticks(range(24))
    ax.set_xlabel('Jam')
    ax.set_ylabel('PM10')
    st.pyplot(fig)

elif selected_chart == 'Grafik Rata-rata PM2.5 dan PM10':
    st.subheader('Grafik Rata-rata PM2.5 dan PM10')
    average_pm25_pm10 = data.groupby('year')[['PM2.5', 'PM10']].mean()
    plt.figure(figsize=(12, 6))
    plt.plot(average_pm25_pm10.index, average_pm25_pm10['PM2.5'], marker='o', color='skyblue', label='PM2.5')
    plt.plot(average_pm25_pm10.index, average_pm25_pm10['PM10'], marker='o', color='orange', label='PM10')
    plt.title('Rata-rata PM2.5 dan PM10 per Tahun')
    plt.xlabel('Tahun')
    plt.ylabel('Rata-rata PM')
    plt.legend()
    st.pyplot()

elif selected_chart == 'Distribusi Nilai PM2.5 dan PM10':
    st.subheader('Distribusi Nilai PM2.5 dan PM10')
    plt.figure(figsize=(12, 6))
    sns.histplot(data=filtered_data, x='PM2.5', kde=True, label='PM2.5', color='blue')
    sns.histplot(data=filtered_data, x='PM10', kde=True, label='PM10', color='orange')
    plt.title('Distribusi Nilai PM2.5 dan PM10')
    plt.xlabel('Konsentrasi')
    plt.ylabel('Frekuensi')
    plt.legend()
    st.pyplot()

# Tampilkan data
st.subheader('Data Hasil Describe')
st.dataframe(data.describe())

# Footer
st.text('Dikembangkan oleh Hikmat Hidayat')

