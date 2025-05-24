<template>
  <q-page class="bg-grey side-padding">
    <div class="row q-col-gutter-lg">
      <!-- Left Column: Profile Info and Banner -->
      <div class="col-12 col-md-7">
        <!-- Top section with banner and overlapping avatar -->
        <div class="relative-position">
          <!-- Banner -->
          <div class="bg-primary" style="height: 200px; border-radius: 16px 16px 0 0"></div>

          <!-- Avatar (overlapping banner and card) -->
          <q-avatar class="profile-avatar shadow-2">
            <template v-if="mainProfile.photo_url">
              <img
                :src="mainProfile.photo_url"
                alt="Profile Photo"
                style="object-fit: cover; object-position: center; width: 100%; height: 100%"
              />
            </template>
            <template v-else>
              <q-icon name="person" size="60px" color="grey-5" />
            </template>
          </q-avatar>

          <!-- Card with Profile Info -->
          <q-card
            class="q-px-lg q-py-md"
            style="padding-top: 60px; border-radius: 0 0 16px 16px; overflow: visible"
          >
            <q-card-section>
              <div class="text-h6">{{ mainProfile.name }}</div>
                <div class="text-subtitle2 text-grey-7 flex items-center">
                <img
                  v-if="mainProfile.university"
                  :src="`/university-logos/${mainProfile.university.replace(/\s+/g, '-').toLowerCase()}.png`"
                  alt="University Logo"
                  style="height: 24px; width: 24px; object-fit: contain; margin-right: 8px"
                />
                {{ mainProfile.university }}
                </div>
              <ul class="q-ma-none" style="padding-left: 1em">
                <li
                  v-for="(dept, idx) in mainProfile.unit"
                  :key="idx"
                  class="text-subtitle2 text-grey-7"
                >
                  {{ dept }}
                </li>
              </ul>

              <div v-if="mainProfile.phone?.length" class="q-mt-sm">
                <q-icon name="phone" size="xs" class="q-mr-xs" />
                {{ mainProfile.phone.join(', ') }}
              </div>

              <div v-if="mainProfile.functions?.length" class="q-mt-sm">
                <q-icon name="work" size="xs" class="q-mr-xs" />
                {{ mainProfile.functions.join(', ') }}
              </div>

              <div v-if="mainProfile.url" class="q-mt-sm">
                <q-icon name="link" size="xs" class="q-mr-xs" />
                <a :href="mainProfile.url" target="_blank">{{ mainProfile.url }}</a>
              </div>

              <div v-if="mainProfile.orcid_link" class="q-mt-sm">
                <q-icon name="account_circle" size="xs" class="q-mr-xs" />
                <a :href="mainProfile.orcid_link" target="_blank">{{ mainProfile.orcid_link }}</a>
              </div>
            </q-card-section>
          </q-card>
        </div>
      </div>

      <!-- Right Column: Similar Profiles -->
      <div class="col-12 col-md-5">
        <q-card class="q-pa-md br-16 shadow-1">
          <div class="text-subtitle1 text-weight-bold">Similar profiles</div>
          <q-separator class="q-my-sm" />

          <div v-for="(profile, i) in similarProfiles" :key="profile.id">
            <router-link
              :to="{ name: 'profile', params: { id: profile.id } }"
              style="text-decoration: none"
            >
              <ProfileCard
                :id="profile.id"
                :name="profile.name"
                :photo_url="profile.photo_url"
                :university="profile.university"
                :unit="profile.unit"
                class="q-my-sm br-16"
              />
            </router-link>
            <q-separator v-if="i < similarProfiles.length - 1" />
          </div>

          <div v-if="similarProfiles.length === 0" class="text-center text-grey-6 q-pa-md">
            No similar profiles found.
          </div>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<style scoped>
.profile-avatar {
  position: absolute;
  top: 140px;
  left: 32px;
  width: 120px;
  height: 120px;
  background-color: white;
  z-index: 10;
}
</style>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import ProfileCard from 'components/ProfileCard.vue';

interface Profile {
  id: number;
  name: string;
  university: string;
  photo_url: string | null;
  orcid_link?: string | null;
  phone?: string[];
  unit: string[];
  functions?: string[];
  url?: string;
}

const route = useRoute();

const mainProfile = ref<Profile>({
  id: 0,
  name: '',
  university: '',
  photo_url: null,
  unit: [],
});

const similarProfiles = ref<Profile[]>([]);

async function loadProfile() {
  // 1) Read the numeric id from the URL. If it's not a number, bail out.
  const id = Number(route.params.id);
  if (isNaN(id)) {
    mainProfile.value = {
      id: 0,
      name: '',
      university: '',
      photo_url: null,
      orcid_link: null,
      unit: [],
    };
    similarProfiles.value = [];
    return;
  }

  // 2) Fetch the full list of professors
  const response = await fetch('/professors.json');
  const data: Profile[] = await response.json();

  // 3) Find and set the main profile
  const profile = data.find((p) => p.id === id);
  if (profile) {
    mainProfile.value = {
      ...profile,
      photo_url: profile.photo_url ?? null,
      orcid_link: profile.orcid_link ?? null,
    };
  } else {
    mainProfile.value = {
      id: 0,
      name: '',
      university: '',
      photo_url: null,
      orcid_link: null,
      unit: [],
    };
  }

  // 4) Compute “similar” profiles by:
  //    • Shared units (case‐insensitive) → higher weight
  //    • Name similarity (substring match, case‐insensitive) → lower weight
  //    • Combine into one score and pick top 5
  if (profile) {
    const baseName = profile.name.toLowerCase().trim();
    const baseUnits = profile.unit.map((u) => u.toLowerCase());

    const scoredProfiles = data
      .filter((p) => p.id !== profile.id)
      .map((p) => {
        // Shared units (case‐insensitive)
        const otherUnits = p.unit.map((u) => u.toLowerCase());
        const sharedUnits = otherUnits.filter((u) => baseUnits.includes(u));
        const sharedUnitCount = sharedUnits.length;

        // Name similarity: simple substring match
        // Split names into words for better similarity matching
        const baseNameWords = baseName.split(/\s+/);
        const otherName = p.name.toLowerCase().trim();
        const otherNameWords = otherName.split(/\s+/);

        // Name similarity: count overlapping words (case-insensitive)
        const sharedNameWords = baseNameWords.filter(word => otherNameWords.includes(word));
        const nameScore = sharedNameWords.length > 0 ? sharedNameWords.length : 0;

        // Final scoring: units carry a higher weight (e.g. weight = 5 each),
        // name similarity carries a lower weight (weight = 1).
        const score = sharedUnitCount * 2 + nameScore * 1;

        return { profile: p, score };
      })
      // Exclude anyone with zero total score (no shared unit AND no name match)
      .filter((item) => item.score > 0)
      // Sort descending by score
      .sort((a, b) => b.score - a.score)
      // Take top 5
      .slice(0, 5)
      .map((item) => item.profile);

    similarProfiles.value = scoredProfiles;
  } else {
    similarProfiles.value = [];
  }
}

onMounted(loadProfile);

watch(
  () => route.params.id,
  () => {
    void loadProfile();
  }
);
</script>