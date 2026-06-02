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

# Algoritma Forward Chaining
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
    # Mengubah format dictionary JSON menjadi list of dictionaries agar mudah dilooping di React/Vue
    daftar_gejala = [{"kode": k, "nama": v} for k, v in kb["gejala"].items()]
    return {
        "status": "success",
        "data": daftar_gejala
    }

# --- ENDPOINT UTAMA ---

# 3. Endpoint API Diagnosa
@app.post("/api/diagnosa")
def diagnosa_sapi(data: GejalaInput):
    # Ubah list input menjadi set agar mudah dicocokkan dengan operasi himpunan
    gejala_set = set(data.gejala)
    
    # Jalankan mesin inferensi
    hasil = jalankan_forward_chaining(gejala_set)
    
    # Tentukan rekomendasi dasar
    if not hasil:
        pesan = "Gejala tidak mengarah ke penyakit spesifik atau Sapi Layak Kurban."
    else:
        pesan = "Sapi terindikasi memiliki penyakit / Tidak Layak Kurban."
        
    return {
        "status": "success",
        "pesan": pesan,
        "hasil_diagnosa": hasil
    }