<template>
  <q-page padding class="bg-grey side-padding">
    <div v-if="loading" class="text-center">Loading...</div>
    <div v-else-if="errorMsg" class="text-negative">{{ errorMsg }}</div>
    <div v-else>
      <div class="q-mb-sm">
        <div class="text-subtitle2 text-grey-7">
          Showing {{ filteredProfiles.length }} profiles
        </div>
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
import Fuse from 'fuse.js';
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

// The user's search query
const query = ref<string>(route.query.q ? String(route.query.q) : '');

// Our Fuse.js instance (fuse.value will be initialized once data is loaded)
const fuse = ref<Fuse<Professor> | null>(null);

// Whenever route.query.q changes, update query.value
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

    // Initialize Fuse.js now that we have allProfs
    fuse.value = new Fuse(allProfs.value, {
      keys: [
        { name: 'name', weight: 0.7 },
        { name: 'university', weight: 0.3 },
      ],
      threshold: 0.4,      // Adjust between 0.0 (exact) and 1.0 (match all)
      distance: 100,       // How far in the string to look
      ignoreLocation: true // We don't care where in the string the match was
    });
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

/**
 * filteredProfiles:
 *  - If query is empty → return first 200 from allProfs
 *  - Otherwise → run fuse.search(query), extract `item`, then take top 200
 */
const filteredProfiles = computed(() => {
  const q = query.value.trim();
  if (!q || !fuse.value) {
    // No search term yet, or fuse not initialized
    return allProfs.value.slice(0, 200);
  }

  // Use Fuse.js to get fuzzy matches on `name` + `university`
  const results = fuse.value.search(q, { limit: 50 });
  // Each result is { item: Professor; refIndex: number; score: number }
  return results.map((r) => r.item);
});
</script>
