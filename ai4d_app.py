import streamlit as st
import pandas as pd
import math
import random
import datetime
import itertools
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from collections import Counter

st.set_page_config(page_title="Prediksi Angka 4D AI", layout="centered")
st.title("🔢 Prediksi Angka 4D AI Lengkap")
st.caption("Logika Logaritma + Kombinasi + Shio + ML + 2D/3D/4D + Analisa Frekuensi")

# === Fungsi Bantu ===

def hitung_shio(tahun):
    daftar_shio = ['Tikus', 'Kerbau', 'Macan', 'Kelinci', 'Naga', 'Ular',
                   'Kuda', 'Kambing', 'Monyet', 'Ayam', 'Anjing', 'Babi']
    return daftar_shio[(tahun - 4) % 12]

def prediksi_logika(angka):
    try:
        n = int(angka)
        log_value = math.log(n + random.uniform(0.1, 0.9))
        log_str = str(log_value).replace('.', '')[-6:]
        return {
            '2D': log_str[-2:],
            '3D': log_str[-3:],
            '4D': log_str[-4:]
        }
    except:
        return {'2D': '00', '3D': '000', '4D': '0000'}

def train_ml_model(data):
    clean_data = [x.strip() for x in data.split(',') if len(x.strip()) == 4 and x.strip().isdigit()]
    if len(clean_data) < 5:
        return None
    X = [[int(ch) for ch in num] for num in clean_data]
    y = [1 if int(num[-1]) % 2 == 0 else 0 for num in clean_data]  # Dummy label: genap = 1, ganjil = 0
    model = LogisticRegression()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    model.fit(X_train, y_train)
    return model

def analisa_digit_semua(prediksi_df):
    semua_digit = ''.join(prediksi_df['2D'].tolist() + prediksi_df['3D'].tolist() + prediksi_df['4D'].tolist())
    hitung = Counter(semua_digit)
    semua = set('0123456789')
    sering = sorted(hitung.items(), key=lambda x: -x[1])[:3]
    jarang = sorted(hitung.items(), key=lambda x: x[1])[:3]
    belum_muncul = list(semua - set(hitung.keys()))
    return [d[0] for d in sering], [d[0] for d in jarang], belum_muncul

def kombinasi_dari_digit(digits1, digits2, digits3):
    hasil = set()
    for a in digits1:
        for b in digits2:
            for c in digits3:
                hasil.add(a + b + c + random.choice(digits1))
                hasil.add(a + random.choice(digits2) + c + random.choice(digits3))
    return list(hasil)

# === Input User ===

input_angka_terakhir = st.text_input("Masukkan 3 angka 4D terakhir (pisahkan koma)", "8865,7065,1775")
angka_real = st.text_area("Masukkan angka real untuk model ML (pisahkan koma)", "2438,9258,4500")
jumlah_prediksi = st.slider("Jumlah prediksi acak awal", 1, 10, 5)

tanggal = datetime.date.today()
shio = hitung_shio(tanggal.year)
st.text(f"Tanggal: {tanggal} | Shio Hari Ini: {shio}")

if st.button("🔮 Prediksi Sekarang"):
    try:
        angka_list = [x.strip() for x in input_angka_terakhir.split(',') if len(x.strip()) == 4]
        if len(angka_list) < 3:
            st.error("Masukkan minimal 3 angka 4D valid.")
        else:
            df_prediksi = pd.DataFrame(columns=['Asal', '2D', '3D', '4D', 'Sumber'])

            # === Prediksi awal (logika log) ===
            for angka in angka_list:
                hasil = prediksi_logika(angka)
                df_prediksi.loc[len(df_prediksi)] = [angka, hasil['2D'], hasil['3D'], hasil['4D'], 'Logika']

            # === Kombinasi 2 angka ===
            kombinasi = list(itertools.combinations(angka_list, 2))
            for a1, a2 in kombinasi:
                gabungan = a1[:2] + a2[-2:]
                hasil = prediksi_logika(gabungan)
                df_prediksi.loc[len(df_prediksi)] = [f"{a1}+{a2}", hasil['2D'], hasil['3D'], hasil['4D'], 'Kombinasi']

            # === Prediksi acak ===
            for _ in range(jumlah_prediksi):
                acak = ''.join(random.choices('0123456789', k=4))
                hasil = prediksi_logika(acak)
                df_prediksi.loc[len(df_prediksi)] = [f"Acak:{acak}", hasil['2D'], hasil['3D'], hasil['4D'], 'Acak']

            # === Prediksi Ulang (rekursif)
            for _, row in df_prediksi.iterrows():
                ulang = row['4D']
                hasil = prediksi_logika(ulang)
                df_prediksi.loc[len(df_prediksi)] = [f"Ulang:{ulang}", hasil['2D'], hasil['3D'], hasil['4D'], 'Rekursif']

            # === Analisis Frekuensi
            st.subheader("📊 Analisis Digit")
            digit_sering, digit_jarang, digit_belum = analisa_digit_semua(df_prediksi)
            st.write(f"Digit Paling Sering: {digit_sering}")
            st.write(f"Digit Jarang Muncul: {digit_jarang}")
            st.write(f"Digit Belum Muncul: {digit_belum or ['-']}")

            # === Kombinasi dari analisis digit
            hasil_kombinasi = kombinasi_dari_digit(digit_sering, digit_jarang, digit_belum or digit_jarang)
            st.subheader("🔁 Kombinasi Hasil Prediksi")
            for i, angka in enumerate(hasil_kombinasi[:10]):
                st.write(f"{i+1}. {angka}")

            # === Machine Learning
            model = train_ml_model(angka_real)
            if model:
                st.success("Model ML berhasil dilatih.")
                fitur = [int(d) for d in angka_list[-1]]
                hasil_ml = model.predict([fitur])[0]
                st.write(f"📈 ML Prediksi Genap=1 / Ganjil=0: **{hasil_ml}**")
            else:
                st.warning("Model ML butuh minimal 5 data angka 4D untuk dilatih.")

            # === Tampilkan tabel hasil
            st.subheader("📋 Tabel Hasil Prediksi")
            st.dataframe(df_prediksi)

            # === Unduh CSV
            nama_file = f"hasil_prediksi_{tanggal}.csv"
            st.download_button("📥 Unduh Hasil ke CSV", df_prediksi.to_csv(index=False), file_name=nama_file)

    except Exception as e:
        st.error(f"Terjadi kesalahan saat prediksi: {e}")
