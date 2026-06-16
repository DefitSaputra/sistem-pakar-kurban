<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import Home       from './components/Home.vue'
import ProgressBar from './components/ProgressBar.vue'
import Step1Syarat from './components/steps/Step1Syarat.vue'
import Step2Umum   from './components/steps/Step2Umum.vue'
import Step3Kepala from './components/steps/Step3Kepala.vue'
import Step4Badan  from './components/steps/Step4Badan.vue'
import Result      from './components/Result.vue'

// ─── State ──────────────────────────────────────────────────────────────────
const daftarGejala   = ref([])
const gejalaTerpilih = ref([])
const hasilDiagnosa  = ref(null)
const pesanSistem    = ref('')
const currentStep    = ref(0)   // 0=Home | 1-4=Steps | 5=Result
const isLoading      = ref(false)

// ─── Step Config ─────────────────────────────────────────────────────────────
const steps = [
  { id: 1, title: 'Syarat Syariat', desc: 'Validasi usia & fisik dasar'   },
  { id: 2, title: 'Kondisi Umum',   desc: 'Postur & perilaku sapi'        },
  { id: 3, title: 'Area Kepala',    desc: 'Mata, hidung & mulut'          },
  { id: 4, title: 'Badan & Kaki',   desc: 'Kulit, bulu & kuku'           },
]

// ─── Data Fetching ───────────────────────────────────────────────────────────
onMounted(async () => {
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/gejala')
    daftarGejala.value = res.data.data
  } catch (e) {
    console.error('Gagal mengambil data gejala:', e)
  }
})

// ─── Navigation ──────────────────────────────────────────────────────────────
const mulai    = () => { currentStep.value = 1 }
const nextStep = () => { if (currentStep.value < 4) currentStep.value++ }
const prevStep = () => { if (currentStep.value > 1) currentStep.value-- }

const reset = () => {
  gejalaTerpilih.value = []
  hasilDiagnosa.value  = null
  pesanSistem.value    = ''
  currentStep.value    = 0
}

// ─── Diagnosis ────────────────────────────────────────────────────────────────
const analisis = async () => {
  if (!gejalaTerpilih.value.length) {
    alert('Mohon pilih minimal satu gejala fisik terlebih dahulu.')
    return
  }
  isLoading.value = true
  try {
    const res = await axios.post('http://127.0.0.1:8000/api/diagnosa', {
      gejala: gejalaTerpilih.value
    })
    hasilDiagnosa.value = res.data.hasil_diagnosa
    pesanSistem.value   = res.data.pesan
    currentStep.value   = 5
  } catch {
    alert('Terjadi gangguan pada server backend. Pastikan uvicorn sudah berjalan.')
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="flex flex-col lg:flex-row h-screen bg-white font-sans antialiased text-slate-900 overflow-hidden">

    <!-- ═══════════════════ SIDEBAR KIRI ═══════════════════ -->
    <aside class="w-full lg:w-[28%] xl:w-[26%] bg-emerald-950 flex flex-col px-10 py-10 text-white flex-shrink-0">
      <!-- Logo -->
      <button @click="reset" class="flex items-center gap-3 mb-2 group w-fit">
        <div class="w-10 h-10 bg-emerald-500 rounded-xl flex items-center justify-center text-xl shadow-lg group-hover:scale-105 transition-transform">🏆</div>
        <h1 class="text-[22px] font-black tracking-tighter">PRIME<span class="text-emerald-400">COW</span></h1>
      </button>
      <p class="text-emerald-400/50 text-[10px] font-bold tracking-[0.2em] mb-10">EXPERT DIAGNOSTIC PLATFORM</p>

      <!-- ProgressBar stepper (only during steps 1-4) -->
      <ProgressBar v-if="currentStep > 0 && currentStep <= 4" :currentStep="currentStep" :steps="steps" />

      <!-- Idle state (Home / Result) -->
      <div v-else class="flex-1 flex flex-col items-center justify-center text-center opacity-60 py-8">
        <span class="text-5xl mb-3">🛡️</span>
        <p class="font-bold text-emerald-100 text-sm">Kurban Aman & Sehat</p>
        <p class="text-emerald-400/70 text-[11px] mt-2 max-w-[190px] leading-relaxed">
          Memastikan setiap hewan kurban memenuhi standar syariat dan medis.
        </p>
      </div>

      <!-- Footer watermark -->
      <div class="opacity-10 pointer-events-none select-none mt-auto">
        <div class="text-3xl font-black italic tracking-tighter">KELOMPOK 8</div>
        <div class="text-sm font-light tracking-widest mt-0.5">INFORMATIKA UNSOED</div>
      </div>
    </aside>

    <!-- ═══════════════════ MAIN CONTENT ═══════════════════ -->
    <main class="flex-1 flex flex-col bg-slate-50 overflow-hidden min-h-0">

      <!-- Header -->
      <header class="flex-shrink-0 h-[76px] px-10 flex items-center justify-between bg-white border-b border-slate-200/60">
        <div>
          <p class="text-[10px] font-black uppercase tracking-[0.2em] text-emerald-600">
            {{ currentStep === 0 ? 'Beranda' : currentStep <= 4 ? 'Fase Observasi' : 'Laporan Akhir' }}
          </p>
          <h2 class="text-[17px] font-bold text-slate-800 leading-tight">
            {{ currentStep === 0 ? 'Platform Diagnostik' : currentStep <= 4 ? steps[currentStep - 1]?.title : 'Hasil Diagnosis Klinis' }}
          </h2>
        </div>
        <div class="flex items-center gap-3 text-[11px] text-slate-400 font-medium">
          <span>Kelompok 8</span>
          <span class="w-1 h-1 bg-slate-300 rounded-full"></span>
          <span>v2.0</span>
        </div>
      </header>

      <!-- Scrollable viewport -->
      <div class="flex-1 overflow-y-auto px-8 lg:px-12 py-10 pb-32 min-h-0 scrollbar-hide">
        <Home          v-if="currentStep === 0"                       @start="mulai" />
        <Step1Syarat   v-else-if="currentStep === 1" :daftarGejala="daftarGejala" v-model="gejalaTerpilih" />
        <Step2Umum     v-else-if="currentStep === 2" :daftarGejala="daftarGejala" v-model="gejalaTerpilih" />
        <Step3Kepala   v-else-if="currentStep === 3" :daftarGejala="daftarGejala" v-model="gejalaTerpilih" />
        <Step4Badan    v-else-if="currentStep === 4" :daftarGejala="daftarGejala" v-model="gejalaTerpilih" />
        <Result        v-else-if="currentStep === 5 && hasilDiagnosa"
                       :hasilDiagnosa="hasilDiagnosa" :pesanSistem="pesanSistem"
                       @reset="reset" />
      </div>

      <!-- Navigation Footer (Steps 1-4 only) -->
      <footer
        v-if="currentStep > 0 && currentStep <= 4"
        class="flex-shrink-0 absolute bottom-0 right-0 left-0 lg:left-[28%] xl:left-[26%] h-[84px] bg-white/90 backdrop-blur-md border-t border-slate-200/60 px-10 flex items-center justify-between z-20"
      >
        <button
          @click="prevStep"
          :class="currentStep === 1 ? 'opacity-0 pointer-events-none' : 'opacity-100'"
          class="flex items-center gap-2 text-sm font-bold text-slate-400 hover:text-slate-900 active:scale-95 transition-all duration-200"
        >
          <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/>
          </svg>
          Kembali
        </button>

        <!-- Step pills indicator -->
        <div class="flex items-center gap-1.5">
          <div v-for="s in steps" :key="s.id"
            class="h-1.5 rounded-full transition-all duration-300"
            :class="s.id === currentStep ? 'w-6 bg-emerald-600' : s.id < currentStep ? 'w-3 bg-emerald-400' : 'w-3 bg-slate-200'"
          ></div>
        </div>

        <button
          v-if="currentStep < 4"
          @click="nextStep"
          class="px-8 py-3 bg-emerald-700 hover:bg-emerald-800 text-white font-bold rounded-xl text-sm shadow-lg shadow-emerald-700/20 hover:shadow-xl active:scale-95 transition-all duration-300"
        >
          Lanjut Pemeriksaan
        </button>
        <button
          v-else
          @click="analisis"
          :disabled="isLoading"
          class="px-8 py-3 bg-slate-900 hover:bg-slate-800 disabled:opacity-50 text-white font-bold rounded-xl text-sm shadow-lg active:scale-95 transition-all duration-300 flex items-center gap-2.5"
        >
          <span v-if="isLoading" class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
          Finalisasi Diagnosa
        </button>
      </footer>

    </main>
  </div>
</template>

<style>
.scrollbar-hide::-webkit-scrollbar { display: none; }
.scrollbar-hide { -ms-overflow-style: none; scrollbar-width: none; }
</style>