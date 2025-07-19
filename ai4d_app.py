import streamlit as st
import pandas as pd
import random
from datetime import datetime
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

st.set_page_config(page_title="Prediksi Angka 4D AI", layout="centered")

st.title("🔢 Prediksi Angka 4D AI")
st.caption("Fitur lengkap: Shio Harian, Kombinasi, 2D/3D/4D, Machine Learning")

# ==== Input ====
last3 = st.text_input("Masukkan 3 angka 4D terakhir (pisahkan koma)", "2438,9258,4500")
target = st.text_input("Target angka (opsional, ex: 1784)")
n = st.slider("Jumlah prediksi", 1, 10, 5)
tanggal_shio = st.text_input("Tanggal untuk Shio Harian (opsional)", value=str(datetime.today().date()))
angka_real = st.text_area("Masukkan angka real untuk pelatihan model ML (pisahkan koma)", "2438,9258,4500")

# ==== Fungsi Kombinasi & Prediksi ====
def generate_predictions(last3, target=None, n=5):
    freq = {}
    for num in last3:
        for d in num:
            freq[d] = freq.get(d, 0) + 1

    all_digits = set('0123456789')
    sering = {d for d, f in freq.items() if f >= 2}
    jarang = all_digits - set(freq.keys())

    preds = []
    for _ in range(n):
        if target and len(target) == 4:
            prefix = target[:2]
            combo = ''.join(random.choices(tuple(sering or all_digits), k=1) +
                            random.choices(tuple(jarang or all_digits), k=1))
            num = prefix + combo
        else:
            num = ''.join(random.choices(tuple(jarang or all_digits), k=2) +
                          random.choices(tuple(sering or all_digits), k=2))

        colored = [f"{ch}{'🔵' if ch in jarang else '🔴'}" for ch in num]
        preds.append((''.join(colored), num))

    return preds, sering, jarang

# ==== Machine Learning untuk Prediksi 4D ====
def train_ml_model(data):
    data = [x.strip() for x in data.split(',') if len(x.strip()) == 4 and x.strip().isdigit()]
    if len(data) < 5:
        return None

    # Ekstrak fitur angka sebagai digit
    X = [[int(ch) for ch in num] for num in data]
    y = [1 if int(num[-1]) % 2 == 0 else 0 for num in data]  # Label dummy: genap/ganjil

    model = LogisticRegression()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model.fit(X_train, y_train)
    return model

# ==== Proses ====
if st.button("🔮 Prediksi Sekarang"):
    parts = [s.strip() for s in last3.split(',') if len(s.strip()) == 4 and s.strip().isdigit()]
    if len(parts) != 3:
        st.error("Masukkan harus 3 angka 4D valid, contoh: 2438,9258,4500")
    else:
        st.subheader("🔢 Frekuensi Digit")
        preds, sering, jarang = generate_predictions(parts, target, n)
        st.write(f"Angka sering muncul: {', '.join(sorted(sering))}")
        st.write(f"Angka jarang muncul: {', '.join(sorted(jarang))}")

        st.subheader("📈 Prediksi Kombinasi 4D")
        for colored, raw in preds:
            st.markdown(f"- {colored} ➤ `{raw}`")

        # ==== Prediksi ML ====
        model = train_ml_model(angka_real)
        if model:
            st.subheader("🧠 Prediksi ML 2D/3D (dari angka real)")
            last_data = [int(d) for d in parts[-1]]
            pred_ml = model.predict([last_data])[0]
            st.write(f"Prediksi akhir berdasarkan model ML (Genap=1 / Ganjil=0): **{pred_ml}**")
        else:
            st.warning("Data angka real terlalu sedikit untuk pelatihan ML.")

        st.subheader("📅 Shio Harian (placeholder)")
        st.info(f"Fitur Shio berdasarkan tanggal: {tanggal_shio} — (fitur ini bisa ditambah dengan mapping shio).")
