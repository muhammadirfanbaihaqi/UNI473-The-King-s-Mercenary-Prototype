# import streamlit as st
# import cv2
# import requests
# import numpy as np
# from yolov8_utils import detect_koi
# from image_buffer import update_and_check_frozen
# from PIL import Image
# import threading
# import time

# ESP32_STREAM_URL = "http://192.168.0.105/capture"  # Ganti jika perlu

# st.set_page_config(page_title="Livestream & Deteksi Ikan Mati", layout="centered")

# st.title("🎥 Livestream & Deteksi Ikan Mati dengan YOLOv8")

# frame_placeholder = st.empty()
# status_placeholder = st.empty()

# st.markdown("""
# <style>
#     .dead-warning {
#         background-color: #e74c3c;
#         color: white;
#         padding: 1rem;
#         font-size: 20px;
#         text-align: center;
#         border-radius: 12px;
#         font-weight: bold;
#     }
# </style>
# """, unsafe_allow_html=True)

# dead_fish_detected = st.empty()

# # ============== Streaming Logic ==============
# def capture_and_detect():
#     while True:
#         try:
#             # Ambil gambar dari ESP32-CAM
#             resp = requests.get(ESP32_STREAM_URL, timeout=3)
#             img_array = np.asarray(bytearray(resp.content), dtype=np.uint8)
#             frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

#             # Deteksi koi dengan YOLOv8
#             boxes = detect_koi(frame)

#             # Gambar bounding box
#             for (x1, y1, x2, y2) in boxes:
#                 cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

#             # Konversi ke format untuk Streamlit
#             frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             pil_img = Image.fromarray(frame_rgb)

#             # Tampilkan frame
#             frame_placeholder.image(pil_img, channels="RGB")

#             # Periksa apakah ada ikan yang tidak bergerak
#             if update_and_check_frozen(boxes):
#                 dead_fish_detected.markdown("<div class='dead-warning'>⚠️ TERDETEKSI IKAN MATI! ⚠️</div>", unsafe_allow_html=True)
#             else:
#                 dead_fish_detected.empty()

#         except Exception as e:
#             status_placeholder.error(f"Terjadi kesalahan: {e}")

#         time.sleep(3)

# # ========== Penjadwalan Auto 2 Jam =============
# def run_every_2_hours():
#     while True:
#         st.session_state["auto_mode"] = True
#         capture_and_detect()  # Deteksi selama 10 menit
#         time.sleep(60 * 10)   # Tunda 10 menit kamera aktif
#         st.session_state["auto_mode"] = False
#         time.sleep(60 * 110)  # Sisa dari 2 jam (120 - 10)

# # Jalankan thread
# if "thread_started" not in st.session_state:
#     thread = threading.Thread(target=capture_and_detect)
#     thread.start()
#     st.session_state.thread_started = True
