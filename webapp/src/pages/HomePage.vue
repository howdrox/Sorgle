<template>
  <div class="q-pa-md flex flex-center column" style="min-height: 70vh">
    <img
      src="/sorgle_full.png"
      alt="Sorgle Logo"
      style="width: 600px; cursor: pointer;"
      @click="router.push('/easteregg')"
    />

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
        <q-icon
          name="search"
          color="secondary"
        />
      </template>
    </q-input>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const query = ref('');
const router = useRouter();

async function onSearch() {
  if (!query.value) {
    return;
  }
  await router.push(`/results?q=${encodeURIComponent(query.value)}`);
}
</script>
