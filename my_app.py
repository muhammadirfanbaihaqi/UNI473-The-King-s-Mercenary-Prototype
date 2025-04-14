import sys
import types
import requests
from chatbot_page import chatAI


# Hindari streamlit mencoba "watch" torch.classes
sys.modules['torch.classes'] = types.ModuleType('torch.classes')
sys.modules['torch.classes'].__path__ = []

import streamlit as st
from monitoring_page import Monitoring_page
from chatbot_page import chatbot_page  # Import halaman chatbot

# ✅ PANGGIL set_page_config PALING ATAS SEKALI
st.set_page_config(page_title="Smart Fish Dashboard", layout="centered")

# =================== CUSTOM CSS STYLING ===================
st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            background-color: #2c3e50;
            color: white;
            padding: 2rem 1rem;
        }
        .sidebar .sidebar-content, .css-1v3fvcr {
            color: white !important;
            font-size: 22px;
            font-weight: 700;
        }
        .stRadio > div {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        label[data-baseweb="radio"] {
            background-color: #34495e;
            padding: 10px;
            border-radius: 8px;
            color: white;
            font-size: 18px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        label[data-baseweb="radio"]:hover {
            background-color: #1abc9c;
        }
        input[type="radio"] {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)
# ==========================================================

# Sidebar Navigasi
st.sidebar.title("🐟 Smart Fish Dashboard")
menu = st.sidebar.radio("📂 Pilih Halaman:", [
    "Pemantauan Suhu & Aerator",
    "Pemberi Pakan Otomatis",
    "Monitoring Kamera & YOLO",
    "Chatbot"
])

# Konten Halaman
if menu == "Pemantauan Suhu & Aerator":
    st.title("🌡️ Pemantauan Suhu Air & Kontrol Aerator")
    st.write("📊 Halaman ini akan menampilkan grafik suhu air dan status aerator.")

    flask_url = "http://192.168.42.33:5000/data"  # Ganti dengan URL Flask API kamu

    try:
        response = requests.get(flask_url)
        if response.status_code == 200:
            data = response.json()
            st.success("✅ Data berhasil diambil dari server!")

            suhu = data.get("suhu", "N/A")
            pakan = data.get("pakan", "N/A")
            pompa = data.get("pompa", False)
            timestamp = data.get("timestamp", "N/A")

            st.metric("🌡️ Suhu Air (°C)", suhu)
            st.metric("🍽️ Pakan (%)", pakan)
            st.metric("💨 Status Pompa", "Aktif" if pompa else "Mati")
            st.caption(f"⏱️ Terakhir diperbarui: {timestamp}")

            # Tombol Epik: minta saran dari AI
            if st.button("✨ Dapatkan Saran dari AI"):
                with st.spinner("Sedang memproses saran dari AI..."):
                    # Format prompt/chat history
                    history = [
                        {"role": "system", "content": "Kamu adalah asisten pintar untuk peternakan ikan."},
                        {"role": "user", "content": f"Suhu air saat ini adalah {suhu}°C, dan status aerator backup adalah {'aktif' if pompa else 'mati'}. Berikan saran agar ikan koi dapat sehat berdasarkan data tersebut."}
                    ]
                    saran = chatAI(history)
                    st.success("🤖 Saran dari AI:")
                    st.markdown(f"> {saran}")

        else:
            st.error("❌ Gagal mengambil data dari server Flask.")
    except Exception as e:
        st.error(f"⚠️ Error saat koneksi ke server: {e}")


elif menu == "Pemberi Pakan Otomatis":
    st.subheader("🕒 Atur Jadwal Pemberian Pakan (Format: Jam dan Menit)")

    with st.form("jadwal_form"):
        col1, col2, col3 = st.columns(3)

        with col1:
            jam1 = st.number_input("Jam #1", min_value=0, max_value=23, step=1, key="jam1")
            menit1 = st.number_input("Menit #1", min_value=0, max_value=59, step=1, key="menit1")
        with col2:
            jam2 = st.number_input("Jam #2", min_value=0, max_value=23, step=1, key="jam2")
            menit2 = st.number_input("Menit #2", min_value=0, max_value=59, step=1, key="menit2")
        with col3:
            jam3 = st.number_input("Jam #3", min_value=0, max_value=23, step=1, key="jam3")
            menit3 = st.number_input("Menit #3", min_value=0, max_value=59, step=1, key="menit3")

        submitted = st.form_submit_button("🚀 Kirim Jadwal ke Alat")

    if submitted:
        jadwal = []
        if jam1 != 0 or menit1 != 0:
            jadwal.append([int(jam1), int(menit1)])
        if jam2 != 0 or menit2 != 0:
            jadwal.append([int(jam2), int(menit2)])
        if jam3 != 0 or menit3 != 0:
            jadwal.append([int(jam3), int(menit3)])

        try:
            flask_url = "http://192.168.42.33:5000/jadwal_pakan"
            res = requests.post(flask_url, json={"jadwal": jadwal})
            if res.status_code == 200:
                st.success("✅ Jadwal berhasil dikirim ke alat!")
            else:
                st.error("❌ Gagal mengirim jadwal ke alat.")
        except Exception as e:
            st.error(f"⚠️ Gagal koneksi ke Flask: {e}")


elif menu == "Monitoring Kamera & YOLO":
    Monitoring_page()

elif menu == "Chatbot":
    chatbot_page()
