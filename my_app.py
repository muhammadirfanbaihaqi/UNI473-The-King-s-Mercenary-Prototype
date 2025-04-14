import sys
import types

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

elif menu == "Pemberi Pakan Otomatis":
    st.title("🍽️ Pemberi Pakan Ikan Otomatis")
    st.write("🐟 Atur jadwal pemberian pakan dan lihat status ketinggian pakan.")

elif menu == "Monitoring Kamera & YOLO":
    Monitoring_page()

elif menu == "Chatbot":
    chatbot_page()
