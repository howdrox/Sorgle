<template>
  <q-page class="bg-grey side-padding">
    <div class="row q-col-gutter-lg">
      <!-- Left Column: Profile Info and Banner -->
      <div class="col-12 col-md-7">
        <div class="relative-position">
          <!-- Banner -->
          <div class="bg-primary" style="height: 200px; border-radius: 16px 16px 0 0"></div>

          <!-- Avatar (overlapping banner and card) -->
          <q-avatar class="profile-avatar shadow-2">
            <template v-if="mainProfile.photo_url">
              <img
                :src="mainProfile.photo_url"
                alt="Profile Photo"
                style="
                  object-fit: cover;
                  object-position: center;
                  width: 100%;
                  height: 100%;
                  border-radius: 50%;
                "
              />
            </template>
            <template v-else>
              <q-icon name="person" size="60px" color="grey-5" />
            </template>
          </q-avatar>

          <!-- Card with Profile Info -->
          <q-card
            class="q-px-lg q-py-md relative-position"
            style="padding-top: 60px; border-radius: 0 0 16px 16px; overflow: visible"
          >
            <!-- University logo (top-right) -->
            <div
              v-if="mainProfile.university"
              style="
                position: absolute;
                top: 32px;
                right: 32px;
                height: 50px;
                width: auto;
                z-index: 1;
              "
            >
              <img
                :src="`/university-logos/${slugify(mainProfile.university)}.png`"
                alt="University Logo"
                style="height: 100%; width: auto; object-fit: contain; display: block"
              />
            </div>

            <q-card-section>
              <!-- Name -->
              <div class="text-h6">{{ mainProfile.name }}</div>

              <!-- University text (logo separate) -->
              <div v-if="mainProfile.university" class="text-subtitle2 text-grey-7">
                {{ mainProfile.university }}
              </div>

              <!-- Unit (departments) as bullet list -->
              <ul v-if="mainProfile.unit?.length" class="q-ma-none q-mt-md" style="padding-left: 0">
                <li
                  v-for="(dept, idx) in mainProfile.unit"
                  :key="idx"
                  class="text-subtitle2 text-grey-7"
                  style="display: flex; align-items: center"
                >
                  <q-icon name="badge" size="xs" class="q-mr-xs" />
                  {{ dept }}
                </li>
              </ul>

              <!-- Title / Department -->
              <div v-if="mainProfile.title" class="text-subtitle2 text-grey-7 q-mt-sm">
                <q-icon name="badge" size="xs" class="q-mr-xs" />
                {{ mainProfile.title }}
              </div>

              <!-- Email -->
              <div v-if="mainProfile.email" class="text-subtitle2 text-grey-7 q-mt-sm">
                <q-icon name="email" size="xs" class="q-mr-xs" />
                <a :href="`mailto:${mainProfile.email}`">{{ mainProfile.email }}</a>
              </div>

              <!-- Phone (string or array) -->
              <div v-if="mainProfile.phone?.length" class="text-subtitle2 text-grey-7 q-mt-sm">
                <q-icon name="phone" size="xs" class="q-mr-xs" />
                <span v-if="typeof mainProfile.phone === 'string'">
                  {{ mainProfile.phone }}
                </span>
                <span v-else>
                  {{ (mainProfile.phone as string[]).join(', ') }}
                </span>
              </div>

              <!-- Functions / roles -->
              <div v-if="mainProfile.functions?.length" class="text-subtitle2 text-grey-7 q-mt-sm">
                <q-icon name="work" size="xs" class="q-mr-xs" />
                {{ mainProfile.functions.join(', ') }}
              </div>

              <!-- Profile URL (personal page) -->
              <div v-if="mainProfile.profile_url" class="text-subtitle2 text-grey-7 q-mt-sm">
                <q-icon name="account_circle" size="xs" class="q-mr-xs" />
                <a :href="mainProfile.profile_url" target="_blank">{{ mainProfile.profile_url }}</a>
              </div>

              <!-- ORCID link -->
              <div v-if="mainProfile.orcid_link" class="text-subtitle2 text-grey-7 q-mt-sm">
                <q-icon name="account_circle" size="xs" class="q-mr-xs" />
                <a :href="mainProfile.orcid_link" target="_blank">{{ mainProfile.orcid_link }}</a>
              </div>

              <!-- Separator before Bio -->
              <q-separator v-if="mainProfile.bio?.length" class="q-my-md" />

              <!-- Bio Section: render each paragraph -->
              <div v-if="mainProfile.bio?.length">
                <div class="text-subtitle2 text-grey-7 q-mb-xs">Bio</div>
                <div
                  v-for="(paragraph, idx) in mainProfile.bio"
                  :key="idx"
                  class="text-body2 q-mb-sm"
                >
                  {{ paragraph }}
                </div>
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
  left: 32px;
  top: 140px; /* 200px banner – (120px avatar ÷ 2) = 140px */
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

/**
 * Slugify function for university → logo filename.
 * E.g. "Tsinghua University" → "tsinghua-university"
 */
function slugify(str: string): string {
  return str
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/[^\w\s-]/g, '')
    .trim()
    .replace(/\s+/g, '-')
    .toLowerCase();
}

interface Profile {
  id: number;
  name: string;
  university: string;
  photo_url: string | null;
  orcid_link?: string | null | undefined;
  email?: string | undefined;
  phone?: string | string[] | undefined;
  unit: string[];
  functions?: string[] | undefined;
  profile_url?: string | undefined;
  bio?: string[] | undefined;
  title?: string | undefined;
}

const route = useRoute();

const mainProfile = ref<Profile>({
  id: 0,
  name: '',
  university: '',
  photo_url: null,
  orcid_link: null,
  unit: [],
  bio: [],
  phone: undefined,
  functions: [],
  profile_url: undefined,
  email: undefined,
  title: undefined,
});

const similarProfiles = ref<Profile[]>([]);

async function loadProfile() {
  const id = Number(route.params.id);
  if (isNaN(id)) {
    mainProfile.value = {
      id: 0,
      name: '',
      university: '',
      photo_url: null,
      orcid_link: null,
      unit: [],
      bio: [],
      phone: undefined,
      functions: [],
      profile_url: undefined,
      email: undefined,
      title: undefined,
    };
    similarProfiles.value = [];
    return;
  }

  const response = await fetch('/professors.json');
  const data: Profile[] = await response.json();

  // Find the main profile by ID
  const profile = data.find((p) => p.id === id);
  if (profile) {
    mainProfile.value = {
      ...profile,
      // Convert literal "None" or missing fields to null/undefined
      photo_url: profile.photo_url ?? null,
      orcid_link: profile.orcid_link === 'None' ? null : (profile.orcid_link ?? null),
      bio: profile.bio ?? [],
      phone: profile.phone ?? undefined,
      functions: profile.functions ?? [],
      profile_url: profile.profile_url ?? undefined,
      email: profile.email ?? undefined,
      title: profile.title ?? undefined,
    };
  } else {
    mainProfile.value = {
      id: 0,
      name: '',
      university: '',
      photo_url: null,
      orcid_link: null,
      unit: [],
      bio: [],
      phone: undefined,
      functions: [],
      profile_url: undefined,
      email: undefined,
      title: undefined,
    };
  }

  // Compute similar profiles (shared units & name)
  if (profile) {
    const baseName = profile.name.toLowerCase().trim();
    const baseUnits = profile.unit.map((u) => u.toLowerCase());

    const scoredArray = data
      .filter((p) => p.id !== profile.id)
      .map((p) => {
        // Shared units
        const otherUnits = p.unit.map((u) => u.toLowerCase());
        const sharedUnitCount = otherUnits.filter((u) => baseUnits.includes(u)).length;

        // Name similarity (count of shared words)
        const baseWords = baseName.split(/\s+/);
        const otherName = p.name.toLowerCase().trim();
        const otherWords = otherName.split(/\s+/);
        const sharedWordsCount = baseWords.filter((w) => otherWords.includes(w)).length;

        // Scoring: shared unit = 2 pts each, shared word = 1 pt each
        const score = sharedUnitCount * 2 + sharedWordsCount;

        return { profile: p, score };
      })
      .filter((item) => item.score > 0)
      .sort((a, b) => b.score - a.score)
      .slice(0, 5)
      .map((item) => item.profile);

    similarProfiles.value = scoredArray;
  } else {
    similarProfiles.value = [];
  }
}

onMounted(loadProfile);

watch(
  () => route.params.id,
  () => {
    void loadProfile();
  },
);
</script>
