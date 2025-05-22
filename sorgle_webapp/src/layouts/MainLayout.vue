<template>
  <q-layout view="hHh lpR fFf">
    <q-header elevated>
      <q-toolbar class="bg-white justify-center">
        <!-- Logo -->
        <q-img
          src="/sorgle_full.png"
          alt="Sorgle Logo"
          class="q-ma-sm"
          style="width: 100px;"
        />

        <!-- This expands to fill the gap automatically -->
          <q-input
            v-model="query"
            placeholder="Search..."
            dense
            rounded
            outlined
            class="search-input"
            style="max-width: 400px; width: 100%;"
            @keyup.enter="onSearch"
          >
            <template #append>
              <q-btn flat round icon="search" @click="onSearch" />
            </template>
          </q-input>
      </q-toolbar>
    </q-header>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const query = ref('')
const router = useRouter()

async function onSearch() {
  if (!query.value) return
  // navigate to results, passing q=…
  await router.push({ name: 'results', query: { q: query.value } })
}
</script>

<style scoped>
.search-input .q-field__control {
  text-align: left;
}
</style>
