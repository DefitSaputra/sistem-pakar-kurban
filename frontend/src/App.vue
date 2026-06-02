<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

// State Management
const daftarGejala = ref([])
const gejalaTerpilih = ref([])
const hasilDiagnosa = ref(null)
const pesanSistem = ref('')

// Mengambil data gejala dari FastAPI
const ambilGejala = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/api/gejala')
    daftarGejala.value = response.data.data
  } catch (error) {
    console.error("Gagal mengambil data gejala:", error)
  }
}

// Mengirim gejala yang dicentang ke FastAPI
const analisisKondisi = async () => {
  if (gejalaTerpilih.value.length === 0) {
    alert("Pilih minimal satu gejala fisik terlebih dahulu!")
    return
  }
  
  try {
    const response = await axios.post('http://127.0.0.1:8000/api/diagnosa', {
      gejala: gejalaTerpilih.value
    })
    hasilDiagnosa.value = response.data.hasil_diagnosa
    pesanSistem.value = response.data.pesan
  } catch (error) {
    console.error("Gagal menganalisis kondisi sapi:", error)
  }
}

// Dijalankan otomatis saat halaman web dimuat
onMounted(() => {
  ambilGejala()
})
</script>

<template>
  <div class="min-h-screen bg-gray-50 py-10 px-4 font-sans">
    <div class="max-w-4xl mx-auto bg-white rounded-2xl shadow-xl overflow-hidden border border-gray-100">
      
      <div class="bg-emerald-600 p-8 text-white text-center">
        <h1 class="text-3xl font-extrabold tracking-tight">Sistem Pakar Sapi Kurban</h1>
        <p class="mt-2 text-emerald-100 text-lg">Pilih gejala fisik yang terlihat pada sapi untuk mengecek kelayakannya</p>
      </div>

      <div class="p-8">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
          <label v-for="gejala in daftarGejala" :key="gejala.kode" 
                 class="flex items-center p-4 border rounded-xl cursor-pointer transition-all duration-200 hover:shadow-md"
                 :class="gejalaTerpilih.includes(gejala.kode) ? 'border-emerald-500 bg-emerald-50' : 'border-gray-200 hover:border-emerald-300'">
            
            <input type="checkbox" :value="gejala.kode" v-model="gejalaTerpilih" 
                   class="w-5 h-5 text-emerald-600 rounded border-gray-300 focus:ring-emerald-500">
            <span class="ml-4 text-gray-700 font-medium">[{{ gejala.kode }}] {{ gejala.nama }}</span>
          </label>
        </div>

        <button @click="analisisKondisi" 
                class="w-full bg-emerald-600 hover:bg-emerald-700 text-white font-bold py-4 rounded-xl transition duration-300 shadow-lg text-lg">
          Analisis Kondisi Sapi
        </button>

        <div v-if="pesanSistem" class="mt-8 p-6 rounded-xl border-2 transition-all duration-500"
             :class="hasilDiagnosa.length > 0 ? 'bg-red-50 border-red-200' : 'bg-emerald-50 border-emerald-200'">
          
          <h2 class="text-2xl font-bold mb-2" 
              :class="hasilDiagnosa.length > 0 ? 'text-red-700' : 'text-emerald-700'">
            Hasil Identifikasi:
          </h2>
          <p class="text-gray-800 text-lg mb-4 font-medium">{{ pesanSistem }}</p>
          
          <ul v-if="hasilDiagnosa.length > 0" class="space-y-2">
            <li v-for="hasil in hasilDiagnosa" :key="hasil.kode" 
                class="flex items-center text-red-700 bg-red-100 p-3 rounded-lg font-semibold">
              ⚠️ Terindikasi: {{ hasil.nama }} ({{ hasil.kode }})
            </li>
          </ul>
        </div>
        
      </div>
    </div>
  </div>
</template>