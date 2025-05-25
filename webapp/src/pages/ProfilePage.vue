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
                style="object-fit: cover; object-position: center; width: 100%; height: 100%"
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
            <!-- Absolute‐positioned logo in top right -->
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
                :src="`/university-logos/${mainProfile.university.replace(/\s+/g, '-').toLowerCase()}.png`"
                alt="University Logo"
                style="height: 100%; width: auto; object-fit: contain; display: block"
              />
            </div>

            <q-card-section>
              <div class="row items-start">
                <!-- Name and university text only; logo is absolute -->
                <div>
                  <div class="text-h6">{{ mainProfile.name }}</div>
                  <div v-if="mainProfile.university" class="text-subtitle2 text-grey-7">
                    {{ mainProfile.university }}
                  </div>
                </div>
              </div>

              <ul class="q-ma-none q-mt-md" style="padding-left: 1em">
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

              <div v-if="mainProfile.profile_url" class="q-mt-sm">
                <q-icon name="account_circle" size="xs" class="q-mr-xs" />
                <a :href="mainProfile.profile_url" target="_blank">{{ mainProfile.profile_url }}</a>
              </div>

              <div v-if="mainProfile.orcid_link" class="q-mt-sm">
                <q-icon name="account_circle" size="xs" class="q-mr-xs" />
                <a :href="mainProfile.orcid_link" target="_blank">{{ mainProfile.orcid_link }}</a>
              </div>

              <!-- Separator before Bio -->
              <q-separator v-if="mainProfile.bio?.length" class="q-my-md" />

              <!-- Bio Section: now an array of paragraphs -->
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
  profile_url?: string;
  bio?: string[]; // ← now an array of paragraphs
}

const route = useRoute();

const mainProfile = ref<Profile>({
  id: 0,
  name: '',
  university: '',
  photo_url: null,
  unit: [],
  bio: [], // default empty array
});

const similarProfiles = ref<Profile[]>([]);

async function loadProfile() {
  // 1) Read numeric ID from URL
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
    };
    similarProfiles.value = [];
    return;
  }

  // 2) Fetch full list of professors
  const response = await fetch('/professors.json');
  const data: Profile[] = await response.json();

  // 3) Find and set mainProfile
  const profile = data.find((p) => p.id === id);
  if (profile) {
    mainProfile.value = {
      ...profile,
      photo_url: profile.photo_url ?? null,
      orcid_link: profile.orcid_link ?? null,
      bio: profile.bio ?? [],
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
    };
  }

  // 4) Compute similarProfiles (unchanged)
  if (profile) {
    const baseName = profile.name.toLowerCase().trim();
    const baseUnits = profile.unit.map((u) => u.toLowerCase());

    const scoredProfiles = data
      .filter((p) => p.id !== profile.id)
      .map((p) => {
        const otherUnits = p.unit.map((u) => u.toLowerCase());
        const sharedUnits = otherUnits.filter((u) => baseUnits.includes(u));
        const sharedUnitCount = sharedUnits.length;

        const baseNameWords = baseName.split(/\s+/);
        const otherName = p.name.toLowerCase().trim();
        const otherNameWords = otherName.split(/\s+/);
        const sharedNameWords = baseNameWords.filter((w) => otherNameWords.includes(w));
        const nameScore = sharedNameWords.length > 0 ? sharedNameWords.length : 0;

        // Adjust weights as desired:
        const score = sharedUnitCount * 2 + nameScore * 1;
        return { profile: p, score };
      })
      .filter((item) => item.score > 0)
      .sort((a, b) => b.score - a.score)
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
