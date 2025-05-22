<!-- src/components/ProfileCard.vue -->
<template>
    <q-item clickable class="q-py-sm">
        <!-- avatar -->
        <q-item-section avatar top>
            <q-avatar size="56px">
                <template v-if="photo">
                    <img :src="photo" alt="profile photo"
                        style="object-fit: cover; object-position: center; width: 100%; height: 100%;" />
                </template>
                <template v-else>
                    <q-icon name="person" size="32px" color="grey-5" />
                </template>
            </q-avatar>
        </q-item-section>

        <!-- main content -->
        <q-item-section>
            <!-- name -->
            <div class="text-subtitle1 text-weight-bold">
                {{ name }}
            </div>

            <!-- university • department -->
            <div class="text-caption text-grey-6">
                {{ university }} • {{ department }}
            </div>
        </q-item-section>
    </q-item>
</template>

<script setup lang="ts">
import { defineProps } from 'vue'

const { name, photo, university, department } = defineProps({
    name: {
        type: String,
        required: true
    },
    photo: {
        type: String,
        required: true
    },
    university: {
        type: String,
        required: true
    },
    department: {
        type: String,
        required: true
    }
})
</script>

<style scoped>
/* adjust spacing if needed */
.q-item {
    border-bottom: 1px solid var(--q-color-grey-3);
}
</style>
