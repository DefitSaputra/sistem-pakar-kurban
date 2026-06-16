<script setup>
import { computed } from 'vue'

const props = defineProps({
  hasilDiagnosa: { type: Object, required: true },
  pesanSistem:   { type: String, required: true }
})
defineEmits(['reset'])

const isLayak = computed(() =>
  props.hasilDiagnosa?.status_kelayakan?.some(k => k.kode === 'P13')
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
          ? 'bg-gradient-to-br from-emerald-800 via-emerald-900 to-emerald-950'
          : 'bg-gradient-to-br from-rose-800 via-rose-900 to-rose-950'"
      >
        <!-- Decorative bg letter -->
        <div class="absolute right-0 bottom-0 text-[200px] font-black leading-none select-none pointer-events-none opacity-[0.04] translate-x-8 translate-y-8">
          {{ isLayak ? '✓' : '✗' }}
        </div>

        <div>
          <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/10 border border-white/10 text-[10px] font-black uppercase tracking-widest mb-10">
            ⚖️ Status Hukum Syariat
          </div>

          <div class="w-16 h-16 rounded-2xl bg-white/10 border border-white/15 flex items-center justify-center text-4xl mb-5">
            {{ isLayak ? '🐂' : '⚠️' }}
          </div>

          <h2 class="text-4xl lg:text-5xl font-black tracking-tight leading-tight mb-4">
            {{ statusLabel }}
          </h2>

          <p class="text-white/75 text-sm leading-relaxed border-t border-white/10 pt-4 mt-2">
            {{ pesanSistem }}
          </p>
        </div>

        <div class="mt-8 pt-6 border-t border-white/10">
          <button
            @click="$emit('reset')"
            class="w-full py-3.5 px-6 rounded-2xl bg-white text-slate-900 font-bold text-sm hover:bg-slate-50 active:scale-97 transition-all duration-300 shadow-lg shadow-black/15 flex items-center justify-center gap-2"
          >
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 1121.21 7.89M9 11l3-3 3 3m-3-3v12"/>
            </svg>
            Periksa Sapi Baru
          </button>
        </div>
      </div>

      <!-- ===== RIGHT PANEL: TEMUAN KLINIS ===== -->
      <div class="flex-1 bg-slate-50 p-10 lg:p-12 flex flex-col">
        <div class="flex items-center justify-between pb-5 border-b border-slate-200/70 mb-7">
          <h3 class="text-[10px] font-black uppercase tracking-widest text-slate-400">📋 Temuan & Catatan Klinis</h3>
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
                  class="w-9 h-9 rounded-xl flex items-center justify-center text-base flex-shrink-0"
                  :class="p.is_indikasi ? 'bg-amber-50 text-amber-600' : 'bg-rose-50 text-rose-600'"
                >
                  {{ p.is_indikasi ? '⚡' : '🛑' }}
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
                :class="p.is_indikasi ? 'bg-amber-100/70 text-amber-800' : 'bg-rose-100/70 text-rose-800'"
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
          <div class="w-16 h-16 rounded-full bg-emerald-50 flex items-center justify-center text-3xl mb-4">✨</div>
          <p class="font-bold text-slate-700 mb-1">Tidak Ada Temuan Klinis</p>
          <p class="text-xs text-slate-400 max-w-xs leading-relaxed">Tidak ditemukan indikasi penyakit menular, penyakit kronis, maupun gejala cacat fisik yang signifikan.</p>
        </div>

        <!-- Disclaimer -->
        <div class="mt-6 pt-5 border-t border-slate-200/70 flex items-start gap-2 text-[10px] text-slate-400 leading-relaxed">
          <span class="flex-shrink-0">ℹ️</span>
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
