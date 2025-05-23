<template>
  <q-page class="bg-grey side-padding">
    <div class="row q-col-gutter-lg">
      <!-- Left Column: Profile Info and Banner -->
      <div class="col-12 col-md-7">
        <div class="br-16">
          <!-- Top section with banner and overlapping avatar -->
          <div class="relative-position">
            <!-- Banner -->
            <div class="bg-primary" style="height: 200px; border-radius: 16px 16px 0 0"></div>

            <!-- Avatar (overlapping banner and card) -->
            <q-avatar class="profile-avatar shadow-2">
              <template v-if="mainProfile.photo">
                <img
                  :src="mainProfile.photo"
                  alt="Profile Photo"
                  style="object-fit: cover; object-position: center"
                />
              </template>
              <template v-else>
                <q-icon name="person" size="60px" color="grey-5" />
              </template>
            </q-avatar>

            <!-- Card with Profile Info -->
            <q-card class="q-px-lg q-py-md" style="padding-top: 60px; border-radius: 0 0 16px 16px">
              <q-card-section>
                <div class="text-h6">{{ mainProfile.name }}</div>
                <div class="text-subtitle2 text-grey-7">{{ mainProfile.university }}</div>
                <div class="text-subtitle2 text-grey-7">{{ mainProfile.department }}</div>
              </q-card-section>
            </q-card>
          </div>
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
                :name="profile.name"
                :photo="profile.photo"
                :university="profile.university"
                :department="profile.department"
                class="q-my-sm br-16"
            /></router-link>
            <q-separator v-if="i < similarProfiles.length - 1" />
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
import { ref } from 'vue';
import ProfileCard from 'components/ProfileCard.vue';

const mainProfile = ref({
  name: 'Lauriane Bret',
  photo: 'https://www.kuleuven.be/wieiswie/en/person/00147234/photo',
  university: 'University of Lyon',
  department: 'Graphic Design',
});

const similarProfiles = ref([
  {
    id: 1,
    name: 'Marie-Rose Perret',
    photo: '',
    university: 'Design Institute Paris',
    department: 'Visual Communication',
  },
  {
    id: 2,
    name: 'Coline Wiedmann',
    photo: '',
    university: 'Marseille Art School',
    department: 'Brand Design',
  },
  {
    id: 3,
    name: 'Sophia Estevao',
    photo: '',
    university: 'Université de Nice',
    department: 'UX Research',
  },
  {
    id: 4,
    name: 'Marie-Rose Perret',
    photo: '',
    university: 'Design Institute Paris',
    department: 'Visual Communication',
  },
  {
    id: 5,
    name: 'Coline Wiedmann',
    photo: '',
    university: 'Marseille Art School',
    department: 'Brand Design',
  },
  {
    id: 6,
    name: 'Sophia Estevao',
    photo: '',
    university: 'Université de Nice',
    department: 'UX Research',
  },
  {
    id: 7,
    name: 'Marie-Rose Perret',
    photo: '',
    university: 'Design Institute Paris',
    department: 'Visual Communication',
  },
  {
    id: 8,
    name: 'Coline Wiedmann',
    photo: '',
    university: 'Marseille Art School',
    department: 'Brand Design',
  },
  {
    id: 9,
    name: 'Sophia Estevao',
    photo: '',
    university: 'Université de Nice',
    department: 'UX Research',
  },
  {
    id: 10,
    name: 'Marie-Rose Perret',
    photo: '',
    university: 'Design Institute Paris',
    department: 'Visual Communication',
  },
  {
    id: 11,
    name: 'Coline Wiedmann',
    photo: '',
    university: 'Marseille Art School',
    department: 'Brand Design',
  },
  {
    id: 12,
    name: 'Sophia Estevao',
    photo: '',
    university: 'Université de Nice',
    department: 'UX Research',
  },
]);
</script>
