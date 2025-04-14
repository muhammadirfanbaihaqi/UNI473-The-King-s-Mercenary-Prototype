import streamlit as st

# Ganti dengan IP ESP32-CAM kamu
ESP32_STREAM_URL = "http://192.168.43.172:81/stream"

# Judul Aplikasi
st.set_page_config(page_title="ESP32-CAM Viewer", layout="centered")
st.markdown(
    """
    <style>
        .main {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }
        img {
            border-radius: 12px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("📷 Live Stream dari ESP32-CAM")
st.markdown("Berikut ini adalah tampilan kamera secara langsung dari ESP32-CAM:")

# Tampilkan Stream dengan Tag HTML
st.markdown(
    f"""
    <div style="text-align: center;">
        <img src="{ESP32_STREAM_URL}" width="640" height="480" />
    </div>
    """,
    unsafe_allow_html=True
)