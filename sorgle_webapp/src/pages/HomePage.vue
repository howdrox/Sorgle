<template>
  <div class="q-pa-md flex flex-center column" style="min-height: 70vh;">
    <img src="/sorgle_full.png" alt="Sorgle Logo" class="logo-img" />
    <q-input v-model="query" placeholder="Search..." @keyup.enter="onSearch" dense rounded outlined class="search-input"
      style="max-width: 400px; width: 100%">
      <template #append>
        <q-btn flat round icon="search" @click="onSearch" />
      </template>
    </q-input>
  </div>
</template>

<style scoped>
.logo-img {
  width: 600px;
  height: auto;
}
</style>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const query  = ref('')
const router = useRouter()

async function onSearch() {
  if (!query.value) return
  // await the promise so errors bubble up
  await router.push({ name: 'results', query: { q: query.value } })
}
</script>
