<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import Swal from 'sweetalert2'
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
    Swal.fire({
      icon: 'warning',
      title: 'Belum Ada Gejala Dipilih',
      text: 'Mohon pilih minimal satu gejala fisik terlebih dahulu.',
      confirmButtonText: 'Mengerti',
      confirmButtonColor: '#065f46',
      background: '#fff',
      customClass: { popup: 'swal-rounded' }
    })
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
    Swal.fire({
      icon: 'error',
      title: 'Koneksi Gagal',
      text: 'Terjadi gangguan pada server backend. Pastikan uvicorn sudah berjalan.',
      confirmButtonText: 'Tutup',
      confirmButtonColor: '#065f46',
      background: '#fff',
      customClass: { popup: 'swal-rounded' }
    })
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="flex flex-col lg:flex-row h-screen bg-white font-sans antialiased text-slate-900 overflow-hidden">

    <!-- ═══════════════════ SIDEBAR KIRI ═══════════════════ -->
    <aside class="w-full lg:w-[28%] xl:w-[26%] bg-[#0a2a1f] flex flex-col px-8 py-9 text-white flex-shrink-0 border-r border-emerald-900/40">

      <!-- Logo -->
      <button @click="reset" class="flex items-center gap-3 mb-2 group w-fit">
        <!-- Cow + Star icon -->
        <div class="w-10 h-10 bg-emerald-500 rounded-xl flex items-center justify-center shadow-lg group-hover:scale-105 transition-transform duration-300">
          <svg class="w-6 h-6 text-white" viewBox="0 0 24 24" fill="currentColor">
            <path d="M19 3c-.55 0-1.08.1-1.58.27L15.5 2l-1.5 1.5L15 4.7A5.97 5.97 0 0 0 13 9v1H5a3 3 0 0 0-3 3v2a3 3 0 0 0 3 3h1v2a1 1 0 0 0 2 0v-2h8v2a1 1 0 0 0 2 0v-2h1a3 3 0 0 0 3-3v-2c0-.9-.4-1.71-1-2.27V9a5.97 5.97 0 0 0-2-4.3L17 3.5 15.5 2l1.92 1.27A5.96 5.96 0 0 0 19 3zM8 13a1 1 0 1 1 0 2 1 1 0 0 1 0-2zm8 0a1 1 0 1 1 0 2 1 1 0 0 1 0-2z"/>
          </svg>
        </div>
        <h1 class="text-[22px] font-black tracking-tighter">PRIME<span class="text-emerald-400">COW</span></h1>
      </button>
      <p class="text-emerald-500/60 text-[10px] font-bold tracking-[0.2em] mb-10">EXPERT DIAGNOSTIC PLATFORM</p>

      <!-- Divider -->
      <div class="h-px bg-emerald-900/50 mb-8 -mx-2"></div>

      <!-- ProgressBar stepper (only during steps 1-4) -->
      <ProgressBar v-if="currentStep > 0 && currentStep <= 4" :currentStep="currentStep" :steps="steps" />

      <!-- Idle state (Home / Result) -->
      <div v-else class="flex-1 flex flex-col items-center justify-center text-center py-8">
        <!-- Shield icon -->
        <div class="w-20 h-20 rounded-2xl bg-emerald-900/60 border border-emerald-700/40 flex items-center justify-center mb-5 shadow-inner">
          <svg class="w-10 h-10 text-emerald-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 2L3 7v5c0 5.25 3.75 10.15 9 11.25C17.25 22.15 21 17.25 21 12V7L12 2z"/>
            <path d="M9 12l2 2 4-4"/>
          </svg>
        </div>
        <p class="font-bold text-emerald-100 text-sm tracking-wide">Kurban Aman & Sehat</p>
        <p class="text-emerald-500/70 text-[11px] mt-2.5 max-w-[190px] leading-relaxed">
          Memastikan setiap hewan kurban memenuhi standar syariat dan medis.
        </p>

        <!-- Stats row -->
        <div class="mt-8 grid grid-cols-2 gap-3 w-full max-w-[200px]">
          <div class="bg-emerald-900/50 border border-emerald-800/50 rounded-xl p-3 text-center">
            <div class="text-emerald-400 font-black text-lg leading-none">34</div>
            <div class="text-emerald-600 text-[9px] font-bold uppercase tracking-wide mt-1">Gejala</div>
          </div>
          <div class="bg-emerald-900/50 border border-emerald-800/50 rounded-xl p-3 text-center">
            <div class="text-emerald-400 font-black text-lg leading-none">11</div>
            <div class="text-emerald-600 text-[9px] font-bold uppercase tracking-wide mt-1">Penyakit</div>
          </div>
        </div>
      </div>

      <!-- Footer watermark -->
      <div class="opacity-10 pointer-events-none select-none mt-auto pt-6">
        <div class="h-px bg-white/20 mb-4"></div>
        <div class="text-2xl font-black italic tracking-tighter">KELOMPOK 8</div>
        <div class="text-xs font-light tracking-widest mt-0.5">INFORMATIKA UNSOED</div>
      </div>
    </aside>

    <!-- ═══════════════════ MAIN CONTENT ═══════════════════ -->
    <main class="flex-1 flex flex-col bg-slate-50 overflow-hidden min-h-0">

      <!-- Header -->
      <header class="flex-shrink-0 h-[72px] px-10 flex items-center justify-between bg-white border-b border-slate-100 shadow-sm">
        <div>
          <p class="text-[10px] font-black uppercase tracking-[0.2em] text-emerald-600">
            {{ currentStep === 0 ? 'Beranda' : currentStep <= 4 ? 'Fase Observasi' : 'Laporan Akhir' }}
          </p>
          <h2 class="text-[17px] font-bold text-slate-800 leading-tight">
            {{ currentStep === 0 ? 'Platform Diagnostik' : currentStep <= 4 ? steps[currentStep - 1]?.title : 'Hasil Diagnosis Klinis' }}
          </h2>
        </div>
        <span class="text-[11px] text-slate-400 font-medium">Kelompok 8 &mdash; Informatika UNSOED</span>
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
        class="flex-shrink-0 absolute bottom-0 right-0 left-0 lg:left-[28%] xl:left-[26%] h-[80px] bg-white/95 backdrop-blur-md border-t border-slate-100 shadow-[0_-4px_24px_rgba(0,0,0,0.06)] px-10 flex items-center justify-between z-20"
      >
        <button
          @click="prevStep"
          :class="currentStep === 1 ? 'opacity-0 pointer-events-none' : 'opacity-100'"
          class="flex items-center gap-2 text-sm font-bold text-slate-400 hover:text-slate-900 active:scale-95 transition-all duration-200"
        >
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
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
          class="group px-7 py-2.5 bg-emerald-700 hover:bg-emerald-800 text-white font-bold rounded-xl text-sm shadow-lg shadow-emerald-700/25 hover:shadow-xl active:scale-95 transition-all duration-300 flex items-center gap-2"
        >
          Lanjut Pemeriksaan
          <svg class="w-4 h-4 group-hover:translate-x-0.5 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/>
          </svg>
        </button>
        <button
          v-else
          @click="analisis"
          :disabled="isLoading"
          class="px-7 py-2.5 bg-slate-900 hover:bg-slate-800 disabled:opacity-50 text-white font-bold rounded-xl text-sm shadow-lg active:scale-95 transition-all duration-300 flex items-center gap-2.5"
        >
          <span v-if="isLoading" class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
          <svg v-else class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"/>
          </svg>
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