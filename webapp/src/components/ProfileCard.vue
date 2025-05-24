<!-- src/components/ProfileCard.vue -->
<template>
  <q-item tag="div" clickable class="q-py-sm">
    <!-- avatar -->
    <q-item-section avatar>
      <q-avatar size="56px">
        <template v-if="props.photo_url">
          <img
            :src="props.photo_url"
            alt="profile photo"
            style="object-fit: cover; object-position: center; width: 100%; height: 100%"
          />
        </template>
        <template v-else>
          <q-icon name="person" size="32px" color="grey-5" />
        </template>
      </q-avatar>
    </q-item-section>

    <!-- main content -->
    <q-item-section>
      <!-- name -->
      <div class="text-subtitle1 text-weight-bold text-black">
        {{ props.name }}
      </div>

      <!-- university -->
      <div class="text-caption text-grey-6">{{ props.university }}</div>
      <!-- department list -->
      <ul class="q-mt-xs q-mb-none" style="padding-left: 1em;">
        <li v-for="(dept, idx) in props.unit" :key="idx" class="text-caption text-grey-7">
          {{ dept }}
        </li>
      </ul>
    </q-item-section>
  </q-item>
</template>

<script setup lang="ts">
import { defineProps } from 'vue';

const props = defineProps<{
  name: string
  photo_url: string | null
  university: string
  unit: string[]
}>()
</script>