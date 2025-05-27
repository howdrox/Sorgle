<template>
  <q-page padding class="bg-grey side-padding">
    <q-card class="q-pa-md q-mx-auto bg-white" style="max-width: 700px; border-radius: 16px;">
      <!-- Card Title -->
      <q-card-section class="section-rounded">
        <div class="text-h5">Data Overview</div>
      </q-card-section>

      <q-separator />

      <!-- Professors by University -->
      <q-card-section class="section-rounded q-mt-md">
        <div class="text-h6 q-mb-sm">Professors by University</div>
        <q-list bordered class="section-rounded">
          <q-item v-for="(count, university) in professorsByUniversity" :key="university">
            <q-item-section>
              <q-item-label><strong>{{ university }}:</strong> {{ count }}</q-item-label>
            </q-item-section>
          </q-item>
        </q-list>
      </q-card-section>

      <q-separator />

      <!-- Most Used Names -->
      <q-card-section class="section-rounded q-mt-md">
        <div class="text-h6 q-mb-sm">Most Used Names</div>
        <q-list bordered class="section-rounded">
          <q-item v-for="(count, name) in mostUsedNames" :key="name">
            <q-item-section>
              <q-item-label><strong>{{ name }}:</strong> {{ count }}</q-item-label>
            </q-item-section>
          </q-item>
        </q-list>
      </q-card-section>

      <q-separator />

      <!-- Most Used Units -->
      <q-card-section class="section-rounded q-mt-md q-mb-md">
        <div class="text-h6 q-mb-sm">Most Used Units</div>
        <q-list bordered class="section-rounded">
          <q-item v-for="(count, unit) in mostUsedUnits" :key="unit">
            <q-item-section>
              <q-item-label><strong>{{ unit }}:</strong> {{ count }}</q-item-label>
            </q-item-section>
          </q-item>
        </q-list>
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script setup lang="ts">
const professorsByUniversity = {
  'Imperial College London': 411,
  'INSA Lyon': 999,
  'KU Leuven': 1414,
  'Tsinghua University': 118,
};

const mostUsedNames = {
  Nicolas: 18,
  Paul: 16,
  Thomas: 15,
  David: 14,
  Frederic: 13,
  Eric: 12,
  Hugo: 11,
  Jan: 11,
  Christophe: 10,
  Mohamed: 10,
};

const mostUsedUnits = {
  'Foundation Course for Engineering': 160,
  'Department of Computer Science and Technology': 118,
  'Computer Science & Image Laboratory': 106,
  'Applied Mechanics & Computational Structures': 89,
  'Materials, Architecture & Soil Science': 79,
  'Mechanical Engineering': 76,
  'PhD Students (Doctoral Program)': 67,
  'Ampère Laboratory (Electrical Engineering & Power Electronics)': 65,
  'Interdisciplinary Center for Intelligent Transportation': 63,
  'Department of Surgery & Cancer - Faculty of Medicine': 61,
};
</script>

<style scoped>
.section-rounded {
  border-radius: 16px;
}
</style>
