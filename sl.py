import streamlit as st
import requests
import time

API_URL = "http://192.168.0.104:5000/data"  # Sesuaikan dengan IP Flask kamu

st.set_page_config(page_title="Monitoring Ikan", layout="centered")

st.title("🐟 Monitoring Kolam Ikan Otomatis")

placeholder = st.empty()

while True:
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            data = response.json()
            with placeholder.container():
                st.metric("🌡️ Suhu", f"{data['suhu']} °C")
                st.metric("🍽️ Pakan Tersisa", f"{data['pakan']} %")
                st.metric("💧 Status Pompa", "HIDUP" if data['pompa'] else "MATI")
                st.caption(f"⏰ Terakhir diperbarui: {data['timestamp']}")
        else:
            st.error("Gagal mengambil data dari server")
    except Exception as e:
        st.error(f"Error: {e}")

    time.sleep(5)  # refresh setiap 5 detik
