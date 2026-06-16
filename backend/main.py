import json
# pyrefly: ignore [missing-import]
from fastapi import FastAPI
# pyrefly: ignore [missing-import]
from fastapi.middleware.cors import CORSMiddleware
# pyrefly: ignore [missing-import]
from pydantic import BaseModel
from typing import List

# Inisialisasi Aplikasi FastAPI
app = FastAPI(title="API Sistem Pakar Sapi Kurban - PrimeCow v2")

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

penyakit_db       = kb["penyakit"]
status_kurban_db  = kb["status_kurban"]
rules_diagnosis   = kb["rules_diagnosis"]
rules_kelayakan   = kb["rules_kelayakan"]

# Skema Data Input dari Frontend
class GejalaInput(BaseModel):
    gejala: List[str]


# ===========================================================================
# MESIN INFERENSI UTAMA - DUAL ENGINE
# Engine 1: Forward Chaining Eksak (issubset) — Prioritas Pertama
# Engine 2: Scoring System Parsial (>60%)    — Prioritas Kedua (fallback)
# ===========================================================================
def jalankan_diagnosa(input_gejala: set):
    penyakit_klinis_ids = set(penyakit_db.keys())  # P01 - P11

    # ------------------------------------------------------------------
    # FASE 1 — Evaluasi Status Kelayakan Kurban (K01 / K02) secara Eksak
    # Kelayakan selalu dievaluasi dengan pencocokan eksak, tidak pakai scoring
    # ------------------------------------------------------------------
    kelayakan_terdeteksi = set()
    for rule in rules_kelayakan:
        kesimpulan = rule["kesimpulan"]
        if set(rule["premis"]).issubset(input_gejala):
            kelayakan_terdeteksi.add(kesimpulan)

    # ------------------------------------------------------------------
    # FASE 2A — Pencocokan Eksak Penyakit Klinis (Prioritas Pertama)
    # ------------------------------------------------------------------
    penyakit_eksak = set()
    for rule in rules_diagnosis:
        kesimpulan = rule["kesimpulan"]
        if kesimpulan in penyakit_klinis_ids:
            if set(rule["premis"]).issubset(input_gejala):
                penyakit_eksak.add(kesimpulan)

    penyakit_terdeteksi = []

    if penyakit_eksak:
        # Ada pencocokan eksak — gunakan hasilnya
        for kode in penyakit_eksak:
            penyakit_terdeteksi.append({
                "kode": kode,
                "nama": penyakit_db.get(kode, "Tidak Diketahui"),
                "is_indikasi": False,
                "persentase": 100.0
            })
    else:
        # ------------------------------------------------------------------
        # FASE 2B — Scoring Parsial (Prioritas Kedua / Fallback)
        # Hitung % kecocokan gejala input vs premis setiap aturan klinis
        # Hanya ambil hasil dengan skor tertinggi yang melebihi threshold 60%
        # ------------------------------------------------------------------
        semua_skor = []
        for rule in rules_diagnosis:
            kesimpulan = rule["kesimpulan"]
            if kesimpulan in penyakit_klinis_ids:
                premis_set = set(rule["premis"])
                if len(premis_set) > 0:
                    cocok = len(premis_set.intersection(input_gejala))
                    skor = (cocok / len(premis_set)) * 100
                    if skor > 60.0:
                        semua_skor.append((kesimpulan, skor))

        if semua_skor:
            skor_tertinggi = max(item[1] for item in semua_skor)
            hasil_terbaik = [item for item in semua_skor if item[1] == skor_tertinggi]

            for kode, skor in hasil_terbaik:
                nama_asli = penyakit_db.get(kode, "Tidak Diketahui")
                penyakit_terdeteksi.append({
                    "kode": kode,
                    "nama": f"{nama_asli} (Indikasi: {skor:.0f}%)",
                    "is_indikasi": True,
                    "persentase": round(skor, 1)
                })

    # ------------------------------------------------------------------
    # FASE 3 — Logika Eksklusi Kelayakan
    # K01 (Layak) WAJIB dibatalkan jika:
    #   - K02 (Tidak Layak) terdeteksi secara eksak, ATAU
    #   - Penyakit berat (P01, P05, P08, P11) terdeteksi (eksak atau indikasi)
    # ------------------------------------------------------------------
    penyakit_berat = {"P01", "P05", "P08", "P11"}
    ada_penyakit_berat = any(p["kode"] in penyakit_berat for p in penyakit_terdeteksi)

    if "K02" in kelayakan_terdeteksi or ada_penyakit_berat:
        kelayakan_terdeteksi.discard("K01")
        kelayakan_terdeteksi.add("K02")

    # ------------------------------------------------------------------
    # FASE 4 — Susun Output Terstruktur
    # ------------------------------------------------------------------
    status_kelayakan = [
        {"kode": k, "nama": status_kurban_db.get(k, "Tidak Diketahui")}
        for k in kelayakan_terdeteksi
    ]

    if "K02" in kelayakan_terdeteksi:
        pesan = "Sapi dinyatakan TIDAK LAYAK KURBAN karena memenuhi kriteria cacat fisik atau terindikasi penyakit akut."
    elif "K01" in kelayakan_terdeteksi:
        pesan = "Sapi dinyatakan LAYAK KURBAN dan memenuhi syariat ketentuan hewan kurban."
    elif penyakit_terdeteksi:
        pesan = "Sapi terindikasi memiliki gejala klinis ringan. Disarankan konsultasi dengan mantri/dokter hewan sebelum mengambil keputusan."
    else:
        pesan = "Gejala tidak mengarah ke indikasi penyakit spesifik. Silakan periksa kembali kondisi fisik sapi."

    return penyakit_terdeteksi, status_kelayakan, pesan


# ===========================================================================
# ENDPOINT API
# ===========================================================================

@app.get("/")
def beranda():
    return {"pesan": "Selamat datang di API Sistem Pakar Sapi Kurban - PrimeCow v2!"}


@app.get("/api/gejala")
def get_daftar_gejala():
    daftar_gejala = [{"kode": k, "nama": v} for k, v in kb["gejala"].items()]
    return {"status": "success", "data": daftar_gejala}


@app.get("/api/status-kurban")
def get_status_kurban():
    data = [{"kode": k, "nama": v} for k, v in status_kurban_db.items()]
    return {"status": "success", "data": data}


@app.post("/api/diagnosa")
def diagnosa_sapi(data: GejalaInput):
    gejala_set = set(data.gejala)
    penyakit_terdeteksi, status_kelayakan, pesan = jalankan_diagnosa(gejala_set)

    return {
        "status": "success",
        "pesan": pesan,
        "hasil_diagnosa": {
            "penyakit": penyakit_terdeteksi,
            "status_kelayakan": status_kelayakan
        }
    }