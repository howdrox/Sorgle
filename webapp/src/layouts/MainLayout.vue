<template>
  <q-layout view="hHh lpR fFf">
    <q-header elevated>
      <q-toolbar class="bg-white justify-center">
        <!-- Logo -->
        <q-btn flat to="/" class="">
          <q-img src="/sorgle_full.png" alt="Sorgle Logo" style="width: 100px" />
        </q-btn>

        <!-- Search bar -->
        <q-input
          v-model="query"
          placeholder="Search..."
          dense
          rounded
          outlined
          autofocus
          @keyup.enter="onSearch"
          style="width: 100%; max-width: 400px"
        >
          <template v-slot:prepend>
            <q-icon name="search" color="secondary" />
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
import { ref } from 'vue';
import { onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import { useRoute } from 'vue-router';

const query = ref('');
const router = useRouter();

const route = useRoute();

onMounted(() => {
  query.value = route.query.q ? String(route.query.q) : '';
});

// Keep query in sync if route changes
watch(
  () => route.query.q,
  (newQ) => {
    query.value = newQ ? String(newQ) : '';
  },
);

async function onSearch() {
  if (!query.value) {
    return;
  }
  await router.push(`/results?q=${encodeURIComponent(query.value)}`);
}
</script>
