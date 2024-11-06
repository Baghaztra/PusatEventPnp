<template>
  <LpLayout>
    <div class="d-flex flex-column align-items-center main-box p-5">
      <h5 class="text-secondary">Explore any up comming event in State Polytechnic of Padang</h5>
      <h1>Pusat Event Politeknik</h1>
      <router-link class="btn btn-primary" to="/login">Login!</router-link>
      <router-link class="text-button" to="/register">dont have any account yet</router-link>
      <router-link class="text-button" to="/home">enter without login</router-link>
      <router-link class="text-button" to="/event-organizer">event organizer</router-link>
    </div>
  </LpLayout>
</template>

<script>
import LpLayout from "@/views/LpLayout.vue";
export default {
  name: "LandingPage",
  components: {
    LpLayout,
  },
};
</script>

<style scoped>
.main-box {
  max-height: 100%;
  background-color: rgba(255, 255, 255, 0.75);
  backdrop-filter: blur(5px);
  border-radius: 10px;
}
</style>
