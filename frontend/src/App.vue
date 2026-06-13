<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'

// State Management
const daftarGejala = ref([])
const gejalaTerpilih = ref([])
const hasilDiagnosa = ref(null)
const pesanSistem = ref('')
const currentStep = ref(1)
const isLoading = ref(false)

// Konfigurasi Navigasi Stepper Vertikal
const steps = [
  { id: 1, title: 'Syarat Syariat', icon: '⚖️', desc: 'Validasi usia & fisik dasar' },
  { id: 2, title: 'Kondisi Umum', icon: '🐂', desc: 'Postur & perilaku sapi' },
  { id: 3, title: 'Area Kepala', icon: '👁️', desc: 'Mata, hidung & mulut' },
  { id: 4, title: 'Badan & Kaki', icon: '🦶', desc: 'Kulit, bulu & kuku' }
]

const stepKategori = {
  1: { gejala: ['G27', 'G29', 'G30', 'G31', 'G32'] },
  2: { gejala: ['G01', 'G02', 'G03', 'G18', 'G19', 'G20', 'G24', 'G28'] },
  3: { gejala: ['G04', 'G05', 'G06', 'G07', 'G08', 'G15', 'G21', 'G22', 'G23'] },
  4: { gejala: ['G09', 'G10', 'G11', 'G12', 'G13', 'G14', 'G16', 'G17', 'G25', 'G26', 'G33', 'G34'] }
}

const ambilGejala = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/api/gejala')
    daftarGejala.value = response.data.data
  } catch (error) {
    console.error("Gagal mengambil data gejala:", error)
  }
}

const gejalaSaatIni = computed(() => {
  if (daftarGejala.value.length === 0 || currentStep.value > 4) return []
  const filterKode = stepKategori[currentStep.value].gejala
  return daftarGejala.value.filter(g => filterKode.includes(g.kode))
})

const nextStep = () => { if (currentStep.value < 4) currentStep.value++ }
const prevStep = () => { if (currentStep.value > 1) currentStep.value-- }
const resetForm = () => {
  gejalaTerpilih.value = []
  hasilDiagnosa.value = null
  pesanSistem.value = ''
  currentStep.value = 1
}

const analisisKondisi = async () => {
  if (gejalaTerpilih.value.length === 0) {
    alert("Mohon pilih minimal satu gejala fisik terlebih dahulu.")
    return
  }
  isLoading.value = true
  try {
    const response = await axios.post('http://127.0.0.1:8000/api/diagnosa', {
      gejala: gejalaTerpilih.value
    })
    hasilDiagnosa.value = response.data.hasil_diagnosa
    pesanSistem.value = response.data.pesan
    currentStep.value = 5
  } catch (error) {
    alert("Terjadi gangguan pada server backend.")
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  ambilGejala()
})
</script>

<template>
  <div class="flex h-screen bg-white font-sans antialiased text-slate-900 overflow-hidden">
    
    <aside class="w-[30%] bg-emerald-950 flex flex-col p-12 text-white relative">
      <div class="mb-16">
        <div class="flex items-center gap-3 mb-2">
          <div class="w-10 h-10 bg-emerald-500 rounded-xl flex items-center justify-center text-2xl shadow-sm">🏆</div>
          <h1 class="text-2xl font-black tracking-tighter">PRIME<span class="text-emerald-400">COW</span></h1>
        </div>
        <p class="text-emerald-400/60 text-[11px] font-bold tracking-[0.15em]">EXPERT DIAGNOSTIC PLATFORM</p>
      </div>

      <nav class="flex-1">
        <div class="space-y-10 relative">
          <div class="absolute left-5 top-2 bottom-2 w-0.5 bg-emerald-800/50"></div>
          
          <div v-for="step in steps" :key="step.id" 
               class="relative z-10 flex items-start gap-6 transition-all duration-500"
               :class="currentStep === step.id ? 'opacity-100' : 'opacity-40'">
            
            <div class="w-10 h-10 rounded-xl flex items-center justify-center font-bold text-sm transition-all"
                 :class="currentStep >= step.id ? 'bg-emerald-500 text-white shadow-lg shadow-emerald-500/20' : 'bg-emerald-900 text-emerald-100'">
              {{ step.id }}
            </div>
            
            <div>
              <h3 class="font-bold text-lg leading-tight">{{ step.title }}</h3>
              <p class="text-emerald-400/80 text-xs mt-1">{{ step.desc }}</p>
            </div>
          </div>
        </div>
      </nav>

      <div class="mt-auto opacity-[0.15] pointer-events-none -ml-4">
        <div class="text-6xl font-black italic tracking-tighter leading-none">KELOMPOK 8</div>
        <div class="text-2xl font-light tracking-widest mt-2">INFORMATIKA UNSOED</div>
      </div>
    </aside>

    <main class="flex-1 flex flex-col bg-slate-50 relative overflow-hidden">
      
      <header class="h-24 px-12 flex items-center justify-between bg-white border-b border-slate-100">
        <div v-if="currentStep <= 4">
          <span class="text-[10px] font-black uppercase tracking-[0.2em] text-emerald-600">Fase Observasi</span>
          <h2 class="text-xl font-bold text-slate-800">{{ steps[currentStep-1]?.title }}</h2>
        </div>
        <div v-else>
          <span class="text-[10px] font-black uppercase tracking-[0.2em] text-emerald-600">Laporan Akhir</span>
          <h2 class="text-xl font-bold text-slate-800">Hasil Diagnosis Klinis</h2>
        </div>
        <div class="flex items-center gap-4 text-slate-400 text-xs font-medium">
          <span>Kelompok 8</span>
          <div class="w-1 h-1 bg-slate-300 rounded-full"></div>
          <span>V.2.0</span>
        </div>
      </header>

      <div class="flex-1 overflow-y-auto p-12 pb-32">
        
        <div v-if="currentStep <= 4" class="max-w-4xl animate-in slide-in-from-bottom-4 duration-700">
          <div class="mb-12">
            <h3 class="text-3xl font-black text-slate-800 tracking-tight mb-3">
              Identifikasi {{ steps[currentStep-1]?.title }}
            </h3>
            <p class="text-slate-500 max-w-xl leading-relaxed">
              Silakan amati kondisi sapi dengan teliti. Pilih opsi di bawah ini yang sesuai dengan temuan fisik di lapangan.
            </p>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <label v-for="gejala in gejalaSaatIni" :key="gejala.kode" 
                   class="group relative flex items-center p-6 bg-white border-2 rounded-2xl cursor-pointer transition-all duration-300"
                   :class="gejalaTerpilih.includes(gejala.kode) ? 'border-emerald-500 shadow-xl shadow-emerald-500/5 ring-4 ring-emerald-500/5' : 'border-white hover:border-emerald-200 shadow-sm'">
              
              <input type="checkbox" :value="gejala.kode" v-model="gejalaTerpilih" class="sr-only">
              
              <div class="w-12 h-12 rounded-xl border flex items-center justify-center transition-all"
                   :class="gejalaTerpilih.includes(gejala.kode) ? 'bg-emerald-500 border-emerald-500 text-white' : 'bg-slate-50 border-slate-100 text-slate-300 group-hover:border-emerald-200'">
                <span v-if="!gejalaTerpilih.includes(gejala.kode)" class="text-[10px] font-bold">{{ gejala.kode }}</span>
                <svg v-else class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                </svg>
              </div>

              <div class="ml-5">
                <p class="text-sm font-bold text-slate-700 leading-tight">{{ gejala.nama }}</p>
                <span class="text-[10px] uppercase font-bold tracking-widest text-slate-400 mt-1 block">Data Klinis</span>
              </div>
            </label>
          </div>
        </div>

        <div v-if="currentStep === 5 && hasilDiagnosa" class="max-w-5xl animate-in fade-in duration-1000">
          <div class="flex flex-col md:flex-row gap-8">
            <div class="flex-1 space-y-8">
              <div class="bg-white p-10 rounded-[2.5rem] shadow-sm border border-slate-100">
                <div class="w-14 h-14 rounded-2xl bg-emerald-50 text-emerald-600 flex items-center justify-center text-3xl mb-6">📝</div>
                <h3 class="text-3xl font-black text-slate-800 tracking-tighter mb-4">Kesimpulan Pemeriksaan</h3>
                <p class="text-slate-600 leading-relaxed text-lg">{{ pesanSistem }}</p>
                <button @click="resetForm" class="mt-10 px-8 py-4 bg-slate-900 text-white rounded-2xl font-bold hover:bg-slate-800 transition shadow-lg shadow-slate-200">
                  Periksa Sapi Baru
                </button>
              </div>
            </div>

            <div class="w-full md:w-[400px] space-y-6">
              <div class="p-8 rounded-[2rem]" 
                   :class="hasilDiagnosa.status_kelayakan.some(k => k.kode === 'P13') ? 'bg-emerald-600 text-white shadow-xl shadow-emerald-200' : 'bg-red-600 text-white shadow-xl shadow-red-200'">
                <h4 class="text-[10px] font-black uppercase tracking-[0.2em] opacity-60 mb-6">Status Hukum Syariat</h4>
                <div v-if="hasilDiagnosa.status_kelayakan.length > 0">
                  <div v-for="status in hasilDiagnosa.status_kelayakan" :key="status.kode" class="text-2xl font-black">
                    {{ status.nama }}
                  </div>
                </div>
                <div v-else class="font-bold italic">Status Tidak Terdefinisi</div>
              </div>

              <div class="bg-white p-8 rounded-[2rem] border border-slate-100 shadow-sm">
                <h4 class="text-[10px] font-black uppercase tracking-[0.2em] text-slate-400 mb-6">Temuan Klinis</h4>
                <div v-if="hasilDiagnosa.penyakit.length > 0" class="space-y-4">
                  <div v-for="p in hasilDiagnosa.penyakit" :key="p.kode" class="flex items-center gap-4 p-4 bg-slate-50 rounded-2xl border border-slate-100">
                    <span class="text-xl">⚠️</span>
                    <span class="font-bold text-sm text-slate-700">{{ p.nama }}</span>
                  </div>
                </div>
                <div v-else class="text-slate-400 italic text-sm text-center py-6">
                  Tidak ditemukan indikasi penyakit menular/berat.
                </div>
              </div>
            </div>
          </div>
        </div>

      </div>

      <footer v-if="currentStep <= 4" class="absolute bottom-0 left-0 right-0 h-24 bg-white/80 backdrop-blur-md border-t border-slate-100 px-12 flex items-center justify-between">
        <button @click="prevStep" :class="currentStep === 1 ? 'opacity-0 pointer-events-none' : 'opacity-100'"
                class="flex items-center gap-2 font-bold text-slate-400 hover:text-slate-900 transition">
          <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" /></svg>
          Kembali
        </button>

        <div class="flex items-center gap-3">
          <button v-if="currentStep < 4" @click="nextStep"
                  class="bg-emerald-600 hover:bg-emerald-700 text-white px-10 py-4 rounded-2xl font-bold shadow-lg shadow-emerald-200 transition-all active:scale-95">
            Lanjut Pemeriksaan
          </button>
          <button v-else @click="analisisKondisi" :disabled="isLoading"
                  class="bg-slate-900 hover:bg-slate-800 text-white px-10 py-4 rounded-2xl font-bold shadow-lg shadow-slate-300 transition-all active:scale-95 flex items-center gap-3">
            <span v-if="isLoading" class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
            Finalisasi Diagnosa
          </button>
        </div>
      </footer>

    </main>
  </div>
</template>

<style>
/* Smooth Viewport Animations */
@keyframes slideUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.animate-in {
  animation: slideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

/* Hide Scrollbar but keep functionality */
.overflow-y-auto::-webkit-scrollbar {
  display: none;
}
.overflow-y-auto {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>