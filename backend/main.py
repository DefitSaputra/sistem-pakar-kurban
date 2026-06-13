import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

# Inisialisasi Aplikasi FastAPI
app = FastAPI(title="API Sistem Pakar Sapi Kurban")

# Konfigurasi CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load data JSON (Knowledge Base)
with open("knowledge_base.json", "r") as file:
    kb = json.load(file)

penyakit_db = kb["penyakit"]
rules_db = kb["rules"]

# Skema Data Input dari Frontend
class GejalaInput(BaseModel):
    gejala: List[str]

# Algoritma Forward Chaining (Tetap Utuh Sesuai Source Code Asli Anda)
def jalankan_forward_chaining(input_gejala: set):
    hasil_penyakit = []
    
    # Looping mengecek setiap rule
    for rule in rules_db:
        # Jika premis rule adalah himpunan bagian (subset) dari input gejala
        if set(rule["premis"]).issubset(input_gejala):
            kode_penyakit = rule["kesimpulan"]
            
            # Tambahkan ke hasil jika belum ada
            hasil = {
                "kode": kode_penyakit,
                "nama": penyakit_db.get(kode_penyakit, "Tidak Diketahui")
            }
            if hasil not in hasil_penyakit:
                hasil_penyakit.append(hasil)
                
    return hasil_penyakit

# --- ENDPOINT ---

# 1. Endpoint Beranda (Mencegah 404 Not Found)
@app.get("/")
def beranda():
    return {"pesan": "Selamat datang di API Sistem Pakar Sapi Kurban Kelompok 8!"}

# 2. Endpoint untuk mengambil daftar gejala (Untuk dirender di Frontend)
@app.get("/api/gejala")
def get_daftar_gejala():
    daftar_gejala = [{"kode": k, "nama": v} for k, v in kb["gejala"].items()]
    return {
        "status": "success",
        "data": daftar_gejala
    }

# --- ENDPOINT UTAMA (DISESUAIKAN AGAR TERSTRUKTUR & VALID) ---

# 3. Endpoint API Diagnosa
@app.post("/api/diagnosa")
def diagnosa_sapi(data: GejalaInput):
    # Ubah list input menjadi set agar mudah dicocokkan dengan operasi himpunan
    gejala_set = set(data.gejala)
    
    # Jalankan mesin inferensi forward chaining dasar
    hasil_raw = jalankan_forward_chaining(gejala_set)
    
    # Ekstrak semua kode kesimpulan yang berhasil dikumpulkan oleh mesin
    kode_kesimpulan = {h["kode"] for h in hasil_raw}
    
    # [LOGIKA EKSKLUSI KHUSUS - FILTER NOT & KONFLIK KELAYAKAN]
    # Jika terdeteksi penyakit berat (P01, P05, P08, P11) ATAU status Tidak Layak (P12),
    # maka status Layak Kurban (P13) otomatis dibatalkan/dihapus agar tidak kontradiktif.
    penyakit_berat = {"P01", "P05", "P08", "P11"}
    if "P12" in kode_kesimpulan or (kode_kesimpulan & penyakit_berat):
        if "P13" in kode_kesimpulan:
            kode_kesimpulan.remove("P13")
            
    # Pemisahan hasil akhir menjadi dua kategori terstruktur
    penyakit_terdeteksi = []
    status_kelayakan = []
    
    for kode in kode_kesimpulan:
        nama_kondisi = penyakit_db.get(kode, "Tidak Diketahui")
        obj_hasil = {"kode": kode, "nama": nama_kondisi}
        
        if kode in ["P12", "P13"]:
            status_kelayakan.append(obj_hasil)
        else:
            penyakit_terdeteksi.append(obj_hasil)
            
    # Penentuan teks pesan kesimpulan yang akurat dan tidak bertubrukan
    if "P12" in kode_kesimpulan:
        pesan = "Sapi dinyatakan TIDAK LAYAK KURBAN karena memenuhi kriteria cacat fisik atau terindikasi penyakit akut."
    elif "P13" in kode_kesimpulan:
        pesan = "Sapi dinyatakan LAYAK KURBAN dan memenuhi syariat ketentuan hewan kurban."
    elif penyakit_terdeteksi:
        pesan = "Sapi terindikasi memiliki gejala klinis ringan. Disarankan konsultasi dengan mantri/dokter hewan sebelum mengambil keputusan."
    else:
        pesan = "Gejala tidak mengarah ke indikasi penyakit spesifik. Silakan periksa kembali kondisi fisik sapi."
        
    return {
        "status": "success",
        "pesan": pesan,
        "hasil_diagnosa": {
            "penyakit": penyakit_terdeteksi,
            "status_kelayakan": status_kelayakan
        }
    }