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
st.sidebar.title("🐟 Smart Fish Dashboard The King's Mercenary")
menu = st.sidebar.radio("📂 Pilih Halaman:", [
    "Pemantauan Suhu, Pakan & Aerator",
    "Pemberi Pakan Otomatis",
    "Monitoring Kamera & YOLO",
    "Chatbot"
])

# Konten Halaman
if menu == "Pemantauan Suhu, Pakan & Aerator":
    st.title("🌡️ Pemantauan Suhu Air, Pakan & Kontrol Aerator")
    st.write("📊 Halaman ini akan menampilkan grafik suhu air dan status aerator.")

    flask_url = "http://192.168.42.33:5000/sensor"  # Ganti dengan URL Flask API kamu

    try:
        response = requests.get(flask_url)
        if response.status_code == 200:
            data = response.json()
            print(data)
            st.success("✅ Data berhasil diambil dari server!")

            suhu = data.get("suhu", "N/A")
            pakan = data.get("pakan(%)", "N/A")
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
    st.title("📅 Atur Jadwal Pakan Ikan Hias")

    API_URL = "http://192.168.42.33:5000/jadwal_pakan"  # Ganti sesuai IP Flask kamu

    # Input jam & menit
    jam = st.number_input("Jam", min_value=0, max_value=23, step=1)
    menit = st.number_input("Menit", min_value=0, max_value=59, step=1)

    # Tombol untuk menambahkan jadwal
    if st.button("➕ Tambah ke Jadwal"):
        try:
            response = requests.get(API_URL)
            if response.status_code == 200:
                data = response.json()
                jadwal = data.get("jadwal", [])

                if [jam, menit] not in jadwal:
                    jadwal.append([jam, menit])
                    res = requests.post(API_URL, json={"jadwal": jadwal})
                    if res.status_code == 200:
                        st.success("✅ Jadwal berhasil diperbarui!")
                    else:
                        st.error("❌ Gagal memperbarui jadwal.")
                else:
                    st.info("ℹ️ Jadwal ini sudah ada.")
            else:
                st.error(f"{response.status_code}")
        except Exception as e:
            st.error(f"⚠️ Gagal terhubung ke server: {e}")

    # Menampilkan jadwal terkini dengan opsi hapus
    st.markdown("---")
    st.subheader("🕒 Jadwal Saat Ini")

    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            data = response.json()
            jadwal = data.get("jadwal", [])
            if jadwal:
                for idx, (j, m) in enumerate(sorted(jadwal)):
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.write(f"- {j:02d}:{m:02d}")
                    with col2:
                        if st.button("❌ Hapus", key=f"hapus_{idx}"):
                            jadwal.remove([j, m])
                            res = requests.post(API_URL, json={"jadwal": jadwal})
                            if res.status_code == 200:
                                st.success(f"✅ Jadwal {j:02d}:{m:02d} berhasil dihapus!")
                                st.rerun()
                            else:
                                st.error("❌ Gagal menghapus jadwal.")
            else:
                st.write("Belum ada jadwal.")
        else:
            st.warning(f"⚠️ Gagal mengambil jadwal: {response.status_code}")
    except Exception as e:
        st.warning(f"⚠️ Gagal mengambil jadwal: {e}")




elif menu == "Monitoring Kamera & YOLO":
    Monitoring_page()

elif menu == "Chatbot":
    chatbot_page()
