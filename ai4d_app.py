import random
import streamlit as st

st.set_page_config(page_title="🎰 RNG 4D Kombinasi", layout="wide")
st.title("🎯 Sistem RNG 4D dengan Pedoman Manipulasi")

# Angka pedoman dari user
pedoman_angka = [
    "2215", "2039", "9361", "9739", "9467", "3114", "8296", "1034", "1032", "5823",
    "3754", "6440", "5891", "7496", "5979", "6948", "7947", "0372", "1036", "1666",
    "7894", "4846", "9286", "4239", "5384", "0516", "7139", "8573", "0881", "1711",
    "8208", "8333", "2135", "1565", "3312", "6904", "4299", "0557"
]

st.header("📝 Masukkan Angka Manual")
input_manual = st.text_input("Masukkan 1–5 angka acak (pisahkan koma):", placeholder="Contoh: 2215,1032")

# Fungsi sistem RNG + kombinasi manipulasi
def rng_prediksi_berpedoman(input_list, pedoman):
    hasil = []
    for idx, angka in enumerate(input_list):
        angka = angka.zfill(4)
        seed = sum(int(d) for d in angka)
        random.seed(seed)
        prediksi = [random.choice(pedoman) for _ in range(3)]
        kombinasi = []
        for p in prediksi:
            kombinasi.append(angka[:2] + p[2:])  # gabung depan input + belakang prediksi
            kombinasi.append(p[:2] + angka[2:])  # gabung depan prediksi + belakang input
        hasil.append({
            "input": angka,
            "prediksi_rng": prediksi,
            "kombinasi": kombinasi[:3]
        })
    return hasil

# Proses input dan tampilkan hasil
if input_manual:
    cleaned = input_manual.replace(" ", "").split(",")
    valid_input = [x for x in cleaned if x.isdigit() and len(x) <= 4]
    if 1 <= len(valid_input) <= 5:
        output = rng_prediksi_berpedoman(valid_input, pedoman_angka)
        for blok in output:
            st.subheader(f"🔢 Input: {blok['input']}")
            st.write("🎲 Prediksi RNG dari Pedoman:")
            st.write(", ".join(blok["prediksi_rng"]))
            st.write("🧬 Kombinasi Manipulasi:")
            st.write(", ".join(blok["kombinasi"]))
            st.markdown("---")
    else:
        st.warning("Masukkan minimal 1 dan maksimal 5 angka (1-4 digit) dipisahkan koma.")
else:
    st.info("Masukkan angka lalu tekan enter untuk melihat prediksi.")
