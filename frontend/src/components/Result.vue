<script setup>
import { computed } from 'vue'

const props = defineProps({
  hasilDiagnosa: { type: Object, required: true },
  pesanSistem:   { type: String, required: true }
})
defineEmits(['reset'])

// Fix: K01 = Layak Kurban (bukan P13)
const isLayak = computed(() =>
  props.hasilDiagnosa?.status_kelayakan?.some(k => k.kode === 'K01')
)

const statusLabel = computed(() => {
  if (!props.hasilDiagnosa?.status_kelayakan?.length) return 'Status Tidak Terdefinisi'
  return props.hasilDiagnosa.status_kelayakan[0].nama
})
</script>

<template>
  <div class="max-w-5xl mx-auto animate-fadein">
    <!-- Split-screen Card -->
    <div class="rounded-3xl overflow-hidden border border-slate-100 shadow-2xl shadow-slate-200/60 flex flex-col lg:flex-row min-h-[560px]">

      <!-- ===== LEFT PANEL: STATUS SYARIAT ===== -->
      <div
        class="w-full lg:w-[44%] p-10 lg:p-12 flex flex-col justify-between relative overflow-hidden text-white transition-colors duration-500"
        :class="isLayak
          ? 'bg-gradient-to-br from-emerald-700 via-emerald-900 to-[#0a2a1f]'
          : 'bg-gradient-to-br from-rose-700 via-rose-900 to-[#2a0a0a]'"
      >
        <!-- Decorative background pattern -->
        <div class="absolute inset-0 opacity-[0.04] pointer-events-none select-none overflow-hidden">
          <svg class="absolute -right-8 -bottom-8 w-64 h-64" viewBox="0 0 100 100" fill="currentColor">
            <circle cx="50" cy="50" r="45"/>
            <path v-if="isLayak" fill="none" stroke="white" stroke-width="6" d="M25 52l16 16L75 32"/>
            <path v-else fill="none" stroke="white" stroke-width="6" d="M30 30l40 40M70 30L30 70"/>
          </svg>
        </div>

        <div>
          <!-- Status badge -->
          <div class="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-white/10 border border-white/15 text-[10px] font-black uppercase tracking-widest mb-10">
            <!-- Scale icon -->
            <svg class="w-3 h-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="12" y1="3" x2="12" y2="21"/>
              <path d="M3 6l4.5 9a4.5 4.5 0 0 0 9 0L21 6"/>
              <line x1="3" y1="6" x2="21" y2="6"/>
            </svg>
            Status Hukum Syariat
          </div>

          <!-- Status icon -->
          <div class="w-16 h-16 rounded-2xl bg-white/10 border border-white/20 flex items-center justify-center mb-5 shadow-inner">
            <!-- Layak: cow icon -->
            <svg v-if="isLayak" class="w-8 h-8" viewBox="0 0 64 64" fill="currentColor">
              <path d="M50 12c-1.5 0-2.9.3-4.2.7L43 10l-4 4 2.5 2.5A16 16 0 0 0 36 24H14a8 8 0 0 0-8 8v6a8 8 0 0 0 8 8h2v5a3 3 0 0 0 6 0v-5h20v5a3 3 0 0 0 6 0v-5h2a8 8 0 0 0 8-8v-6c0-2.4-1.1-4.6-2.7-6.1V24a16 16 0 0 0-5.3-11.5L52 10l-4-4-1.8 2.7C45.5 12.3 47.7 12 50 12zM22 33a3 3 0 1 1 0 6 3 3 0 0 1 0-6zm20 0a3 3 0 1 1 0 6 3 3 0 0 1 0-6z"/>
            </svg>
            <!-- Tidak layak: warning triangle icon -->
            <svg v-else class="w-8 h-8" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/>
              <line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>
            </svg>
          </div>

          <h2 class="text-4xl lg:text-5xl font-black tracking-tight leading-tight mb-4">
            {{ statusLabel }}
          </h2>

          <p class="text-white/75 text-sm leading-relaxed border-t border-white/15 pt-4 mt-2">
            {{ pesanSistem }}
          </p>
        </div>

        <div class="mt-8 pt-6 border-t border-white/10">
          <button
            @click="$emit('reset')"
            class="w-full py-3.5 px-6 rounded-2xl bg-white text-slate-900 font-bold text-sm hover:bg-slate-50 active:scale-97 transition-all duration-300 shadow-lg shadow-black/15 flex items-center justify-center gap-2"
          >
            <!-- Refresh icon -->
            <svg class="w-4 h-4 text-emerald-700" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="1 4 1 10 7 10"/>
              <path d="M3.51 15a9 9 0 1 0 .49-4.65"/>
            </svg>
            Periksa Sapi Baru
          </button>
        </div>
      </div>

      <!-- ===== RIGHT PANEL: TEMUAN KLINIS ===== -->
      <div class="flex-1 bg-slate-50 p-10 lg:p-12 flex flex-col">
        <div class="flex items-center justify-between pb-5 border-b border-slate-200/70 mb-7">
          <div class="flex items-center gap-2 text-[10px] font-black uppercase tracking-widest text-slate-400">
            <!-- Clipboard icon -->
            <svg class="w-3.5 h-3.5 text-slate-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2"/>
              <rect x="9" y="3" width="6" height="4" rx="2"/>
            </svg>
            Temuan & Catatan Klinis
          </div>
          <span class="text-[10px] font-bold bg-slate-200/70 text-slate-500 px-2.5 py-1 rounded-full">
            {{ hasilDiagnosa.penyakit.length }} Temuan
          </span>
        </div>

        <!-- Disease cards -->
        <div v-if="hasilDiagnosa.penyakit.length > 0" class="space-y-4 flex-1">
          <div
            v-for="p in hasilDiagnosa.penyakit" :key="p.kode"
            class="bg-white rounded-2xl border border-slate-100 p-5 shadow-sm hover:-translate-y-0.5 transition-transform duration-300"
          >
            <div class="flex items-start justify-between gap-3 mb-3">
              <div class="flex items-center gap-3">
                <div
                  class="w-9 h-9 rounded-xl flex items-center justify-center flex-shrink-0"
                  :class="p.is_indikasi ? 'bg-amber-50 text-amber-500 border border-amber-200' : 'bg-rose-50 text-rose-500 border border-rose-200'"
                >
                  <!-- Indikasi: activity/pulse icon -->
                  <svg v-if="p.is_indikasi" class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>
                  </svg>
                  <!-- Pasti: x-circle / stop icon -->
                  <svg v-else class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="12" cy="12" r="10"/>
                    <line x1="4.93" y1="4.93" x2="19.07" y2="19.07"/>
                  </svg>
                </div>
                <div>
                  <p class="font-bold text-slate-800 text-sm leading-snug">
                    {{ p.is_indikasi ? p.nama.split(' (Indikasi')[0] : p.nama }}
                  </p>
                  <p class="text-[9px] font-bold uppercase tracking-widest text-slate-400 mt-0.5">Kode: {{ p.kode }}</p>
                </div>
              </div>
              <span
                class="flex-shrink-0 text-[9px] font-black px-2.5 py-1 rounded-lg uppercase tracking-wide"
                :class="p.is_indikasi ? 'bg-amber-100/70 text-amber-700' : 'bg-rose-100/70 text-rose-700'"
              >
                {{ p.is_indikasi ? 'Indikasi' : 'Pasti' }}
              </span>
            </div>

            <!-- Progress bar for partial matches -->
            <div v-if="p.is_indikasi" class="pt-3 border-t border-slate-50">
              <div class="flex justify-between text-[10px] font-bold text-slate-400 mb-1.5">
                <span>Kecocokan Gejala</span>
                <span class="text-amber-600">{{ p.persentase }}%</span>
              </div>
              <div class="w-full bg-slate-100 rounded-full h-1.5 overflow-hidden">
                <div
                  class="bg-gradient-to-r from-amber-400 to-amber-500 h-full rounded-full transition-all duration-1000"
                  :style="{ width: `${p.persentase}%` }"
                ></div>
              </div>
            </div>
          </div>
        </div>

        <!-- Empty state -->
        <div v-else class="flex-1 flex flex-col items-center justify-center text-center py-10">
          <div class="w-16 h-16 rounded-full bg-emerald-50 border border-emerald-100 flex items-center justify-center mb-4">
            <!-- Sparkle / star icon -->
            <svg class="w-7 h-7 text-emerald-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
            </svg>
          </div>
          <p class="font-bold text-slate-700 mb-1">Tidak Ada Temuan Klinis</p>
          <p class="text-xs text-slate-400 max-w-xs leading-relaxed">Tidak ditemukan indikasi penyakit menular, penyakit kronis, maupun gejala cacat fisik yang signifikan.</p>
        </div>

        <!-- Disclaimer -->
        <div class="mt-6 pt-5 border-t border-slate-200/70 flex items-start gap-2.5 text-[10px] text-slate-400 leading-relaxed">
          <!-- Info icon -->
          <svg class="w-3.5 h-3.5 flex-shrink-0 mt-0.5 text-slate-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"/>
            <line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>
          </svg>
          <p>Hasil ini dihasilkan secara komputasi oleh Sistem Pakar Forward Chaining + Scoring Engine. Konsultasikan dengan dokter/mantri hewan berlisensi untuk keputusan medis final.</p>
        </div>
      </div>

    </div>
  </div>
</template>

<style scoped>
.animate-fadein { animation: fadeIn 0.65s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
@keyframes fadeIn { from { opacity:0; transform:scale(0.975) translateY(12px); } to { opacity:1; transform:scale(1) translateY(0); } }
</style>
