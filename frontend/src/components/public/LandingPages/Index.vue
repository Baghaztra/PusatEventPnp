<template>
  <LpLayout>
    <div class="d-flex flex-column align-items-center main-box text-center">
      <h5 class="text-light">Explore any up comming event in State Polytechnic of Padang</h5>
      <h1 class="text-light title">Pusat Event Politeknik</h1>
      <router-link class="btn btn-primary btn-lg m-3" to="/login">Login</router-link>
      <router-link class="text-button" to="/register">dont have any account yet</router-link>
      <router-link class="text-button" to="/home">enter without login</router-link>
      <router-link class="text-button" to="/eo-login">event organizer</router-link>
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
  /* background-color: rgba(255, 255, 255, 0.75); */
  border-radius: 10px;
}
.title {
  font-size: 4rem;
  font-weight: bold;
}
</style>
