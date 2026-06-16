<script setup>
defineEmits(['start'])
</script>

<template>
  <div class="flex flex-col items-center justify-center min-h-[78vh] max-w-4xl mx-auto text-center px-4 animate-fadein">

    <!-- Status Badge -->
    <div class="inline-flex items-center gap-2 px-4 py-1.5 bg-emerald-50 border border-emerald-100 rounded-full text-emerald-800 text-[11px] font-bold tracking-wide mb-8">
      <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse inline-block"></span>
      Sistem Pakar · Forward Chaining + Scoring Engine v2
    </div>

    <!-- Hero Icon -->
    <div class="relative mb-8">
      <div class="w-28 h-28 bg-gradient-to-br from-emerald-700 to-emerald-950 rounded-3xl flex items-center justify-center text-6xl shadow-2xl shadow-emerald-900/20 border border-emerald-600/20 hover:scale-105 transition-transform duration-500">
        🐂
      </div>
      <div class="absolute -bottom-2 -right-2 w-9 h-9 bg-emerald-500 rounded-xl flex items-center justify-center text-white text-lg font-black shadow-lg">✓</div>
    </div>

    <!-- Headline -->
    <h1 class="text-5xl md:text-6xl font-black tracking-tight text-slate-800 leading-tight mb-5">
      Selamat Datang di
      <span class="bg-gradient-to-r from-emerald-700 to-emerald-950 bg-clip-text text-transparent"> PrimeCow</span>
    </h1>
    <p class="text-slate-500 text-lg max-w-2xl leading-relaxed mb-10">
      Platform diagnostik berbasis Sistem Pakar untuk mengevaluasi kesehatan fisik sapi dan memvalidasi kelayakan syariat hewan kurban secara instan dan terstruktur.
    </p>

    <!-- CTA Button -->
    <button
      @click="$emit('start')"
      class="group inline-flex items-center gap-3 px-9 py-4 bg-emerald-800 hover:bg-emerald-900 text-white font-bold rounded-2xl shadow-xl shadow-emerald-900/20 hover:shadow-2xl hover:shadow-emerald-900/30 active:scale-95 transition-all duration-300 text-base"
    >
      Mulai Pemeriksaan Sekarang
      <svg class="w-5 h-5 group-hover:translate-x-1.5 transition-transform duration-300" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
        <path stroke-linecap="round" stroke-linejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6" />
      </svg>
    </button>

    <!-- Feature Cards -->
    <div class="mt-16 grid grid-cols-1 sm:grid-cols-3 gap-5 text-left w-full">
      <div class="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm hover:border-emerald-200 hover:shadow-md transition-all duration-300 group">
        <div class="w-11 h-11 bg-emerald-50 rounded-xl flex items-center justify-center text-2xl mb-4 group-hover:scale-110 transition-transform">⚡</div>
        <h3 class="font-bold text-slate-800 mb-1.5">Cepat & Presisi</h3>
        <p class="text-xs text-slate-500 leading-relaxed">Diagnosis instan via Forward Chaining eksak, diperkuat Scoring Engine untuk deteksi penyakit parsial.</p>
      </div>
      <div class="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm hover:border-emerald-200 hover:shadow-md transition-all duration-300 group">
        <div class="w-11 h-11 bg-emerald-50 rounded-xl flex items-center justify-center text-2xl mb-4 group-hover:scale-110 transition-transform">⚖️</div>
        <h3 class="font-bold text-slate-800 mb-1.5">Sesuai Syariat</h3>
        <p class="text-xs text-slate-500 leading-relaxed">Memvalidasi kelayakan fiqih syariat kurban secara otomatis berdasarkan aturan basis pengetahuan pakar.</p>
      </div>
      <div class="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm hover:border-emerald-200 hover:shadow-md transition-all duration-300 group">
        <div class="w-11 h-11 bg-emerald-50 rounded-xl flex items-center justify-center text-2xl mb-4 group-hover:scale-110 transition-transform">📋</div>
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
