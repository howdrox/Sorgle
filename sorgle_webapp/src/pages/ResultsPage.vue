<!-- src/pages/ResultsPage.vue -->
<template>
  <q-page padding class="bg-grey-2">
    <div style="width: 70%; margin: 0 auto;">
      <div class="q-mb-lg">
        <div class="text-subtitle2 text-grey-7">
          Showing {{ profiles.length }} profiles
        </div>
      </div>

      <!-- Wrap everything in one Card -->
      <q-card flat bordered class="shadow-1">
        <div v-for="(profile, i) in profiles" :key="profile.id">
          <!-- Each card section holds one ProfileCard -->
          <q-card-section>
            <ProfileCard :name="profile.name" :photo="profile.photo" :university="profile.university"
              :department="profile.department" />
          </q-card-section>

          <!-- Separator, except after last -->
          <q-separator inset v-if="i < profiles.length - 1" />
        </div>
      </q-card>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import ProfileCard from 'components/ProfileCard.vue'

interface Profile {
  id: number
  name: string
  photo: string
  university: string
  department: string
}

const profiles = ref<Profile[]>([
  {
    id: 1,
    name: 'Alice Nguyen',
    photo: '',
    university: 'University of Lyon',
    department: 'Graphic Design'
  },
  {
    id: 2,
    name: 'Bob Dubois',
    photo: '',
    university: 'Aix-en-Provence Institute',
    department: 'UX/UI Design'
  },
  {
    id: 3,
    name: 'Claire Martin',
    photo: 'https://www.kuleuven.be/wieiswie/en/person/00147234/photo',
    university: 'St-Étienne University',
    department: 'Full-Stack Development'
  }
])
</script>
