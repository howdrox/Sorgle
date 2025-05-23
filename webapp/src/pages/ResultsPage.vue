<template>
  <q-page padding class="bg-grey side-padding">
    <div v-if="loading" class="text-center">Loading...</div>
    <div v-else-if="errorMsg" class="text-negative">{{ errorMsg }}</div>
    <div v-else>
      <div class="q-mb-sm">
        <div class="text-subtitle2 text-grey-7">Showing {{ filteredProfiles.length }} profiles</div>
      </div>

      <q-card flat bordered class="q-px-sm br-16 shadow-1">
        <div v-for="(profile, i) in filteredProfiles" :key="profile.id">
          <router-link
            :to="{ name: 'profile', params: { id: profile.id } }"
            style="text-decoration: none"
          >
            <ProfileCard
              :name="profile.name"
              :photo_url="profile.photo_url || ''"
              :university="profile.university"
              :unit="profile.unit"
              class="q-my-sm br-16"
            />
          </router-link>
          <q-separator v-if="i < filteredProfiles.length - 1" />
        </div>

        <div v-if="filteredProfiles.length === 0" class="text-center text-grey-6 q-pa-md">
          No results for "{{ query }}".
        </div>
      </q-card>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue';
import { useRoute } from 'vue-router';
import ProfileCard from 'components/ProfileCard.vue';

interface Professor {
  id: number;
  first_name?: string;
  last_name?: string;
  name: string;
  university: string;
  phone?: string[];
  unit: string[];
  functions?: string[];
  title?: string;
  url?: string;
  orcid_link?: string | null;
  photo_url?: string | null;
}

const route = useRoute();
const allProfs = ref<Professor[]>([]);
const loading = ref(false);
const errorMsg = ref<string | null>(null);

const query = ref<string>(route.query.q ? String(route.query.q) : '');

watch(
  () => route.query.q,
  (newQ) => {
    query.value = newQ ? String(newQ) : '';
  },
);

onMounted(async () => {
  loading.value = true;
  try {
    const response = await fetch('/professors.json');
    if (!response.ok) {
      throw new Error(`Network error: ${response.status}`);
    }
    const data = (await response.json()) as Professor[];
    allProfs.value = data.map((p) => ({
      ...p,
      photo_url: p.photo_url ?? null,
      orcid_link: p.orcid_link ?? null,
    }));
  } catch (err: unknown) {
    if (err instanceof Error) {
      errorMsg.value = err.message;
    } else {
      errorMsg.value = 'An unknown error occurred';
    }
  } finally {
    loading.value = false;
  }
});

const filteredProfiles = computed(() => {
  const q = query.value.trim().toLowerCase();
  if (!q) return allProfs.value.slice(0, 200);

  return allProfs.value.filter((p) => p.name.toLowerCase().includes(q)).slice(0, 200);
});
</script>
