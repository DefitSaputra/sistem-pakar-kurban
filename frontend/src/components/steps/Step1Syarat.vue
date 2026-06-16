<script setup>
import { computed } from 'vue'

const props = defineProps({
  daftarGejala: { type: Array, required: true },
  modelValue:   { type: Array, required: true }
})
const emit = defineEmits(['update:modelValue'])

const CODES = ['G27', 'G29', 'G30', 'G31', 'G32']

const gejalaStep = computed(() => props.daftarGejala.filter(g => CODES.includes(g.kode)))

const toggle = (kode) => {
  let sel = [...props.modelValue]
  if (sel.includes(kode)) {
    sel = sel.filter(k => k !== kode)
  } else {
    // G29 ↔ G30 saling eksklusif (belum poel vs sudah poel)
    if (kode === 'G29') sel = sel.filter(k => k !== 'G30')
    if (kode === 'G30') sel = sel.filter(k => k !== 'G29')
    sel.push(kode)
  }
  emit('update:modelValue', sel)
}
</script>

<template>
  <div class="animate-step">
    <div class="mb-9">
      <span class="text-[10px] font-black uppercase tracking-widest text-emerald-600">Langkah 1 dari 4</span>
      <h2 class="text-3xl font-black text-slate-800 tracking-tight mt-1 mb-2">Syarat Mutlak Syariat</h2>
      <p class="text-slate-500 text-sm max-w-xl leading-relaxed">Verifikasi kondisi dasar syariat kurban — usia poel, cacat penglihatan, dan cacat fisik permanen.</p>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <label
        v-for="g in gejalaStep" :key="g.kode"
        class="group flex items-start gap-4 p-5 bg-white border-2 rounded-2xl cursor-pointer transition-all duration-300 hover:shadow-md"
        :class="modelValue.includes(g.kode) ? 'border-emerald-600 ring-4 ring-emerald-500/8 shadow-md' : 'border-slate-100 hover:border-emerald-200'"
      >
        <input type="checkbox" class="sr-only" :checked="modelValue.includes(g.kode)" @change="toggle(g.kode)">
        <div class="flex-shrink-0 mt-0.5 w-11 h-11 rounded-xl border flex items-center justify-center transition-all duration-300"
          :class="modelValue.includes(g.kode) ? 'bg-emerald-600 border-emerald-600 text-white' : 'bg-slate-50 border-slate-200 text-slate-400 group-hover:border-emerald-300'">
          <svg v-if="modelValue.includes(g.kode)" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/></svg>
          <span v-else class="text-[10px] font-bold">{{ g.kode }}</span>
        </div>
        <div>
          <p class="font-bold text-slate-800 text-sm leading-snug">{{ g.nama }}</p>
          <span class="text-[9px] uppercase font-bold tracking-widest text-slate-400 mt-1.5 block">Kriteria Syariat</span>
        </div>
      </label>
    </div>
  </div>
</template>

<style scoped>
.animate-step { animation: stepIn 0.45s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
@keyframes stepIn { from { opacity:0; transform:translateY(16px); } to { opacity:1; transform:translateY(0); } }
</style>
