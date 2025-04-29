import streamlit as st
import requests


def pakan_page():
    # ================ ISI HALAMAN ================

    # Judul halaman
    st.title("📅 Atur Jadwal Pakan Ikan Hias")

    # URL API FLASK
    API_URL = "http://192.168.42.33:5000/jadwal_pakan"  # Ganti sesuai IP Flask kamu

    # Input jam dan menit untuk mengatur jadwal pakan
    jam = st.number_input("Jam", min_value=0, max_value=23, step=1)
    menit = st.number_input("Menit", min_value=0, max_value=59, step=1)

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
