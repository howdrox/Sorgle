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
              <ul v-if="mainProfile.unit.length" class="q-ma-none q-mt-md" style="padding-left: 0">
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
import Fuse from 'fuse.js';
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

// --- 1) Update Profile interface so optional fields explicitly include `undefined` ---
interface Profile {
  id: number;
  name: string;
  university: string;
  photo_url: string | null;
  orcid_link: string | null;
  email: string | undefined;
  phone: string[] | undefined;
  unit: string[];
  functions: string[] | undefined;
  profile_url: string | undefined;
  bio: string[] | undefined;
  title: string | undefined;
}

const route = useRoute();

// --- 2) Initialize `mainProfile` with every field explicitly present (no omitted keys) ---
const mainProfile = ref<Profile>({
  id: 0,
  name: '',
  university: '',
  photo_url: null,
  orcid_link: null,
  email: undefined,
  phone: undefined,
  unit: [],
  functions: undefined,
  profile_url: undefined,
  bio: undefined,
  title: undefined,
});

const similarProfiles = ref<Profile[]>([]);

// We will keep the full list of all profiles here, and a single Fuse index
let allProfiles: Profile[] = [];
let fuse: Fuse<Profile> | null = null;

async function loadAllProfiles() {
  const response = await fetch('/professors.json');
  const data: Profile[] = await response.json();

  // Normalize any missing fields so they match our interface exactly
  allProfiles = data.map((p) => ({
    id: p.id,
    name: p.name,
    university: p.university,
    photo_url: p.photo_url ?? null,
    orcid_link: p.orcid_link === 'None' ? null : (p.orcid_link ?? null),
    email: p.email ?? undefined,
    phone: p.phone ?? undefined,
    unit: p.unit ?? [],
    functions: p.functions ?? undefined,
    profile_url: p.profile_url ?? undefined,
    bio: p.bio ?? undefined,
    title: p.title ?? undefined,
  }));

  // Build Fuse over name, university, and unit fields
  fuse = new Fuse(allProfiles, {
    keys: [
      { name: 'name', weight: 0.8 },
      { name: 'university', weight: 0.19 },
      { name: 'unit', weight: 0.01 },
    ],
    threshold: 0.4,
    distance: 100,
    ignoreLocation: true,
  });
}

async function loadProfile() {
  const id = Number(route.params.id);
  if (isNaN(id)) {
    // Invalid ID: reset mainProfile and clear similarProfiles
    mainProfile.value = {
      id: 0,
      name: '',
      university: '',
      photo_url: null,
      orcid_link: null,
      email: undefined,
      phone: undefined,
      unit: [],
      functions: undefined,
      profile_url: undefined,
      bio: undefined,
      title: undefined,
    };
    similarProfiles.value = [];
    return;
  }

  // 1) Ensure we have allProfiles + fuse built
  if (!allProfiles.length || !fuse) {
    await loadAllProfiles();
  }

  // 2) Find and set mainProfile
  const found = allProfiles.find((p) => p.id === id);
  if (found) {
    mainProfile.value = { ...found };
  } else {
    // No profile with that ID → reset and bail
    mainProfile.value = {
      id: 0,
      name: '',
      university: '',
      photo_url: null,
      orcid_link: null,
      email: undefined,
      phone: undefined,
      unit: [],
      functions: undefined,
      profile_url: undefined,
      bio: undefined,
      title: undefined,
    };
    similarProfiles.value = [];
    return;
  }

  // 3) Build a single “combined” search string from name, university, and units
  const combinedQuery = [
    mainProfile.value.name,
    mainProfile.value.university,
    ...(mainProfile.value.unit || []),
  ]
    .filter((s) => Boolean(s))
    .join(' ');

  // 4) Run Fuse search and filter out the main profile itself
  const results = fuse!.search(combinedQuery, { limit: 10 });
  similarProfiles.value = results
    .map((res) => res.item)
    .filter((p) => p.id !== mainProfile.value.id)
    .slice(0, 10);
}

onMounted(() => {
  void loadProfile();
});

watch(
  () => route.params.id,
  () => {
    void loadProfile();
  },
);
</script>
