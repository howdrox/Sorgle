<template>
  <div class="easter-egg-page bg-grey">
    <img src="egg.jpg" alt="Easter Egg" class="egg-image" />
  </div>
</template>

<style scoped>
.easter-egg-page {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.egg-image {
  max-width: 90vw;
  max-height: 80vh;
  border-radius: 16px;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.12);
}
</style>
