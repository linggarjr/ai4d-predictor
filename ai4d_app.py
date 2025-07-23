import random
import json
import os

# =============================
# === Penyimpanan Internal ===
# =============================

data_latih = []     # Angka yang ditandai BENAR
angka_buruk = []    # Angka yang ditandai SALAH

# =================================
# === Fungsi RNG Otomatis (4D) ===
# =================================

def rng_murni(jumlah=10):
    """Menghasilkan angka 4 digit secara acak."""
    hasil = []
    for _ in range(jumlah):
        angka = ''.join(random.choices('0123456789', k=4))
        hasil.append(angka)
    return hasil

# ========================================
# === Fungsi Pembelajaran Manual User ===
# ========================================

def tandai_benar(angka):
    """Menandai angka sebagai BENAR dan simpan ke data latih."""
    if angka not in data_latih:
        data_latih.append(angka)
        print(f"[✓] Angka {angka} ditandai sebagai BENAR.")

def tandai_salah(angka):
    """Menandai angka sebagai SALAH dan simpan ke angka buruk."""
    if angka not in angka_buruk:
        angka_buruk.append(angka)
        print(f"[✗] Angka {angka} ditandai sebagai SALAH.")

# ==================================
# === Fungsi Simpan & Muat File ===
# ==================================

def simpan_ke_file():
    """Simpan data_latih dan angka_buruk ke file JSON."""
    with open("pembelajaran.json", "w") as f:
        json.dump({
            "data_latih": data_latih,
            "angka_buruk": angka_buruk
        }, f, indent=4)
    print("📁 Data berhasil disimpan ke pembelajaran.json")

def muat_dari_file():
    """Muat data_latih dan angka_buruk dari file jika ada."""
    global data_latih, angka_buruk
    if os.path.exists("pembelajaran.json"):
        with open("pembelajaran.json", "r") as f:
            data = json.load(f)
            data_latih = data.get("data_latih", [])
            angka_buruk = data.get("angka_buruk", [])
        print("📁 Data pembelajaran berhasil dimuat.")
    else:
        print("⚠️ File pembelajaran.json belum ada. Mulai baru.")

# ====================
# === Contoh Pakai ===
# ====================

if __name__ == "__main__":
    muat_dari_file()

    print("\n=== Hasil RNG 4D Otomatis ===")
    hasil_rng = rng_murni(10)
    for angka in hasil_rng:
        print(angka)

    # Simulasi pembelajaran manual
    print("\n=== Pembelajaran Manual ===")
    tandai_benar(hasil_rng[0])
    tandai_salah(hasil_rng[1])

    # Simpan hasil ke file
    simpan_ke_file()

    # Tampilkan isi data latih & angka buruk
    print("\nData Latih:", data_latih)
    print("Angka Buruk:", angka_buruk)
