<script setup>
defineProps({
  currentStep: { type: Number, required: true },
  steps: { type: Array, required: true }
})
</script>

<template>
  <nav class="flex-1 py-6">
    <div class="relative space-y-7">
      <!-- Connector Line -->
      <div class="absolute left-[19px] top-3 bottom-3 w-px bg-slate-700/50"></div>

      <div
        v-for="step in steps"
        :key="step.id"
        class="relative z-10 flex items-start gap-4 transition-all duration-500"
        :class="[
          currentStep === step.id ? 'opacity-100' : '',
          currentStep > step.id  ? 'opacity-80' : '',
          currentStep < step.id  ? 'opacity-30' : ''
        ]"
      >
        <!-- Step Circle -->
        <div
          class="flex-shrink-0 w-10 h-10 rounded-xl flex items-center justify-center font-bold text-sm transition-all duration-400 border"
          :class="[
            currentStep > step.id
              ? 'bg-emerald-500 border-emerald-500 text-white shadow-md shadow-emerald-500/25'
              : currentStep === step.id
                ? 'bg-gradient-to-br from-emerald-500 to-emerald-700 border-emerald-400 text-white shadow-lg shadow-emerald-600/30'
                : 'bg-slate-900 border-slate-700 text-slate-500'
          ]"
        >
          <svg v-if="currentStep > step.id" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3">
            <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
          </svg>
          <span v-else>{{ step.id }}</span>
        </div>

        <!-- Label -->
        <div class="pt-1">
          <p class="font-bold text-sm leading-tight" :class="currentStep === step.id ? 'text-white' : 'text-slate-300'">
            {{ step.title }}
          </p>
          <p class="text-[11px] mt-0.5" :class="currentStep === step.id ? 'text-emerald-400' : 'text-slate-500'">
            {{ step.desc }}
          </p>
        </div>
      </div>
    </div>
  </nav>
</template>
