import streamlit as st
import random
from collections import Counter

st.set_page_config(page_title="🧠 RNG 4D", layout="centered")
st.title("🎰 Sistem RNG 4D dan Manipulasi Peluang")

# Inisialisasi session state
if "angka_terakhir" not in st.session_state:
    st.session_state.angka_terakhir = ""
if "riwayat_rng" not in st.session_state:
    st.session_state.riwayat_rng = []
if "angka_bagus" not in st.session_state:
    st.session_state.angka_bagus = []
if "angka_buruk" not in st.session_state:
    st.session_state.angka_buruk = []

# Fungsi generate angka 4D
def generate_angka():
    angka = str(random.randint(0, 9999)).zfill(4)
    st.session_state.angka_terakhir = angka
    st.session_state.riwayat_rng.append(angka)

# Fungsi masukkan angka manual
def masukkan_angka_manual(angka):
    if len(angka) == 4 and angka.isdigit():
        st.session_state.angka_terakhir = angka
        st.session_state.riwayat_rng.append(angka)
    else:
        st.warning("Masukkan angka 4 digit yang valid.")

# Fungsi kombinasi acak angka bagus + buruk
def kombinasi_acak():
    if len(st.session_state.angka_bagus) > 0 and len(st.session_state.angka_buruk) > 0:
        bagus = random.choice(st.session_state.angka_bagus)
        buruk = random.choice(st.session_state.angka_buruk)

        bagus2 = bagus[-2:]
        buruk2 = buruk[:2]

        metode = random.choice(["bagus+buruk", "buruk+bagus", "acak per digit"])

        if metode == "bagus+buruk":
            kombinasi = bagus2 + buruk2
        elif metode == "buruk+bagus":
            kombinasi = buruk2 + bagus2
        else:
            digit1 = random.choice([bagus[0], buruk[0]])
            digit2 = random.choice([bagus[1], buruk[1]])
            digit3 = random.choice([bagus[2], buruk[2]])
            digit4 = random.choice([bagus[3], buruk[3]])
            kombinasi = digit1 + digit2 + digit3 + digit4

        st.session_state.angka_terakhir = kombinasi
        st.session_state.riwayat_rng.append(kombinasi)
        st.success(f"Kombinasi ({metode}): {kombinasi}")
    else:
        st.info("Tambahkan setidaknya 1 angka bagus dan 1 angka buruk untuk membuat kombinasi.")

# Tombol generate angka baru
st.button("🎲 Generate Angka 4D", on_click=generate_angka)

# Input angka manual
with st.expander("✍️ Masukkan Angka Manual (4D)"):
    angka_manual = st.text_input("Masukkan angka 4 digit:", value="")
    if st.button("🔍 Cek dan Masukkan"):
        masukkan_angka_manual(angka_manual)

# Tampilkan angka terakhir
if st.session_state.angka_terakhir:
    st.markdown("### 🎯 Angka Terakhir:")
    st.code(st.session_state.angka_terakhir)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Tandai Bagus"):
            if st.session_state.angka_terakhir not in st.session_state.angka_bagus:
                st.session_state.angka_bagus.append(st.session_state.angka_terakhir)
    with col2:
        if st.button("❌ Tandai Buruk"):
            if st.session_state.angka_terakhir not in st.session_state.angka_buruk:
                st.session_state.angka_buruk.append(st.session_state.angka_terakhir)

# Kombinasi acak dari angka bagus + buruk
st.subheader("🔀 Kombinasi Acak Angka Bagus + Buruk")
st.button("🔁 Buat Kombinasi Acak", on_click=kombinasi_acak)

# Riwayat RNG
st.subheader("📜 Riwayat Angka RNG")
st.write(", ".join(st.session_state.riwayat_rng[-20:]))

# Statistik
st.subheader("📊 Statistik Manipulasi")
st.write(f"✅ Total Angka Bagus: {len(st.session_state.angka_bagus)}")
st.write(f"❌ Total Angka Buruk: {len(st.session_state.angka_buruk)}")

angka_langka = [angka for angka, count in Counter(st.session_state.riwayat_rng).items() if count >= 3]
if angka_langka:
    st.write(f"🔥 Angka Langka (Muncul ≥3x): {angka_langka}")
else:
    st.write("🔥 Angka Langka (Muncul ≥3x): []")
