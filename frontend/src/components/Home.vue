<script setup>
defineEmits(['start'])
</script>

<template>
  <div class="flex flex-col items-center justify-center min-h-[78vh] max-w-4xl mx-auto text-center px-4 animate-fadein">


    <!-- Hero Icon -->
    <div class="relative mb-8">
      <div class="w-28 h-28 bg-gradient-to-br from-emerald-600 to-emerald-950 rounded-3xl flex items-center justify-center shadow-2xl shadow-emerald-900/25 border border-emerald-500/20 hover:scale-105 transition-transform duration-500">
        <!-- Cow SVG icon -->
        <svg class="w-14 h-14 text-white" viewBox="0 0 64 64" fill="currentColor">
          <path d="M50 12c-1.5 0-2.9.3-4.2.7L43 10l-4 4 2.5 2.5A16 16 0 0 0 36 24H14a8 8 0 0 0-8 8v6a8 8 0 0 0 8 8h2v5a3 3 0 0 0 6 0v-5h20v5a3 3 0 0 0 6 0v-5h2a8 8 0 0 0 8-8v-6c0-2.4-1.1-4.6-2.7-6.1V24a16 16 0 0 0-5.3-11.5L52 10l-4-4-1.8 2.7C45.5 12.3 47.7 12 50 12zM22 33a3 3 0 1 1 0 6 3 3 0 0 1 0-6zm20 0a3 3 0 1 1 0 6 3 3 0 0 1 0-6z"/>
        </svg>
      </div>
      <!-- Checkmark badge -->
      <div class="absolute -bottom-2 -right-2 w-9 h-9 bg-emerald-500 rounded-xl flex items-center justify-center shadow-lg shadow-emerald-500/40">
        <svg class="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3">
          <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/>
        </svg>
      </div>
    </div>

    <!-- Headline -->
    <h1 class="text-5xl md:text-6xl font-black tracking-tight text-slate-800 leading-tight mb-5">
      Selamat Datang di
      <span class="bg-gradient-to-r from-emerald-600 to-emerald-900 bg-clip-text text-transparent"> PrimeCow</span>
    </h1>
    <p class="text-slate-500 text-lg max-w-2xl leading-relaxed mb-10">
      Platform diagnostik berbasis Sistem Pakar untuk mengevaluasi kesehatan fisik sapi dan memvalidasi kelayakan syariat hewan kurban secara instan dan terstruktur.
    </p>

    <!-- CTA Button -->
    <button
      @click="$emit('start')"
      class="group inline-flex items-center gap-3 px-9 py-4 bg-emerald-800 hover:bg-emerald-900 text-white font-bold rounded-2xl shadow-xl shadow-emerald-900/25 hover:shadow-2xl hover:shadow-emerald-900/35 active:scale-95 transition-all duration-300 text-base"
    >
      Mulai Pemeriksaan Sekarang
      <svg class="w-5 h-5 group-hover:translate-x-1.5 transition-transform duration-300" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
        <path stroke-linecap="round" stroke-linejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6" />
      </svg>
    </button>

    <!-- Feature Cards -->
    <div class="mt-16 grid grid-cols-1 sm:grid-cols-3 gap-5 text-left w-full">

      <!-- Card 1: Cepat & Presisi -->
      <div class="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm hover:border-emerald-200 hover:shadow-md transition-all duration-300 group">
        <div class="w-11 h-11 bg-emerald-50 border border-emerald-100 rounded-xl flex items-center justify-center mb-4 group-hover:scale-110 group-hover:bg-emerald-100 transition-all duration-300">
          <!-- Lightning bolt / Zap icon -->
          <svg class="w-5 h-5 text-emerald-600" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>
          </svg>
        </div>
        <h3 class="font-bold text-slate-800 mb-1.5">Cepat & Presisi</h3>
        <p class="text-xs text-slate-500 leading-relaxed">Diagnosis instan via Forward Chaining eksak, diperkuat Scoring Engine untuk deteksi penyakit parsial.</p>
      </div>

      <!-- Card 2: Sesuai Syariat -->
      <div class="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm hover:border-emerald-200 hover:shadow-md transition-all duration-300 group">
        <div class="w-11 h-11 bg-emerald-50 border border-emerald-100 rounded-xl flex items-center justify-center mb-4 group-hover:scale-110 group-hover:bg-emerald-100 transition-all duration-300">
          <!-- Scale / Balance icon -->
          <svg class="w-5 h-5 text-emerald-600" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="12" y1="3" x2="12" y2="21"/><line x1="3" y1="6" x2="21" y2="6"/>
            <path d="M3 6l4.5 9a4.5 4.5 0 0 0 9 0L21 6"/>
          </svg>
        </div>
        <h3 class="font-bold text-slate-800 mb-1.5">Sesuai Syariat</h3>
        <p class="text-xs text-slate-500 leading-relaxed">Memvalidasi kelayakan fiqih syariat kurban secara otomatis berdasarkan aturan basis pengetahuan pakar.</p>
      </div>

      <!-- Card 3: Laporan Klinis -->
      <div class="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm hover:border-emerald-200 hover:shadow-md transition-all duration-300 group">
        <div class="w-11 h-11 bg-emerald-50 border border-emerald-100 rounded-xl flex items-center justify-center mb-4 group-hover:scale-110 group-hover:bg-emerald-100 transition-all duration-300">
          <!-- Clipboard / Report icon -->
          <svg class="w-5 h-5 text-emerald-600" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2"/>
            <rect x="9" y="3" width="6" height="4" rx="2"/>
            <line x1="9" y1="12" x2="15" y2="12"/><line x1="9" y1="16" x2="13" y2="16"/>
          </svg>
        </div>
        <h3 class="font-bold text-slate-800 mb-1.5">Laporan Klinis</h3>
        <p class="text-xs text-slate-500 leading-relaxed">Hasil dikelompokkan menjadi Status Syariat dan Temuan Klinis dengan tingkat kecocokan gejala.</p>
      </div>

    </div>
  </div>
</template>

<style scoped>
.animate-fadein {
  animation: fadeInUp 0.65s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(18px); }
  to   { opacity: 1; transform: translateY(0); }
}
</style>
