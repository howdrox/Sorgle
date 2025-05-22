<template>
  <q-page class="bg-grey-2">
    <!-- Top section with banner and overlapping avatar -->
    <div class="relative-position q-mb-xl">
      <!-- Banner -->
      <div class="bg-primary" style="height: 200px; border-radius: 0 0 8px 8px;"></div>

      <!-- Avatar Positioned Absolutely -->
      <div class="absolute" style="top: 130px; left: 32px;">
        <q-avatar size="120px" class="shadow-2">
          <template v-if="mainProfile.photo">
            <img :src="mainProfile.photo" alt="main profile photo"
              style="object-fit: cover; object-position: center; width: 100%; height: 100%;" />
          </template>
          <template v-else>
            <q-icon name="person" size="60px" color="grey-5" />
          </template>
        </q-avatar>
      </div>
    </div>

    <!-- Content below banner -->
    <div class="row q-col-gutter-md">
      <!-- Left Column: Profile Info -->
      <div class="col-12 col-md-8">
        <q-card class="q-pt-xl q-pl-lg q-pr-lg q-pb-md">
          <q-card-section>
            <div class="text-h6 q-mb-xs">{{ mainProfile.name }}</div>
            <div class="text-subtitle2 text-grey-7">{{ mainProfile.university }}</div>
            <div class="text-subtitle2 text-grey-7">{{ mainProfile.department }}</div>
          </q-card-section>
        </q-card>
      </div>

      <!-- Right Column: Similar Profiles -->
      <div class="col-12 col-md-4">
        <q-card class="q-pa-sm">
          <div class="text-subtitle2 q-mb-sm">Similar profiles</div>
          <q-separator class="q-mb-sm" />

          <div v-for="profile in similarProfiles" :key="profile.id" class="q-mb-sm">
            <ProfileCard
              :name="profile.name"
              :photo="profile.photo"
              :university="profile.university"
              :department="profile.department"
            />
          </div>
        </q-card>
      </div>
    </div>
  </q-page>
</template>


<script setup lang="ts">
import { ref } from 'vue'
import ProfileCard from 'components/ProfileCard.vue'

const mainProfile = ref({
  name: 'Lauriane Bret',
  photo: '',
  university: 'University of Lyon',
  department: 'Graphic Design'
})

const similarProfiles = ref([
  {
    id: 1,
    name: 'Marie-Rose Perret',
    photo: '',
    university: 'Design Institute Paris',
    department: 'Visual Communication'
  },
  {
    id: 2,
    name: 'Coline Wiedmann',
    photo: '',
    university: 'Marseille Art School',
    department: 'Brand Design'
  },
  {
    id: 3,
    name: 'Sophia Estevao',
    photo: '',
    university: 'Université de Nice',
    department: 'UX Research'
  },
  {
    id: 4,
    name: 'Marie-Rose Perret',
    photo: '',
    university: 'Design Institute Paris',
    department: 'Visual Communication'
  },
  {
    id: 5,
    name: 'Coline Wiedmann',
    photo: '',
    university: 'Marseille Art School',
    department: 'Brand Design'
  },
  {
    id: 6,
    name: 'Sophia Estevao',
    photo: '',
    university: 'Université de Nice',
    department: 'UX Research'
  },
  {
    id: 7,
    name: 'Marie-Rose Perret',
    photo: '',
    university: 'Design Institute Paris',
    department: 'Visual Communication'
  },
  {
    id: 8,
    name: 'Coline Wiedmann',
    photo: '',
    university: 'Marseille Art School',
    department: 'Brand Design'
  },
  {
    id: 9,
    name: 'Sophia Estevao',
    photo: '',
    university: 'Université de Nice',
    department: 'UX Research'
  },
  {
    id: 10,
    name: 'Marie-Rose Perret',
    photo: '',
    university: 'Design Institute Paris',
    department: 'Visual Communication'
  },
  {
    id: 11,
    name: 'Coline Wiedmann',
    photo: '',
    university: 'Marseille Art School',
    department: 'Brand Design'
  },
  {
    id: 12,
    name: 'Sophia Estevao',
    photo: '',
    university: 'Université de Nice',
    department: 'UX Research'
  }
])
</script>
