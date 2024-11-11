<template>
  <LpLayout>
    <div class="d-flex flex-column align-items-center main-box">
      <router-link to="/" class="position-absolute top-0 end-0 text-secondary mr-2 mt-1">
        <i class="fas fa-caret-left"></i>
      </router-link>

      <div class="card-body mx-3" style="display: flex; align-items: center; flex-direction: column;">
        <h5 class="card-title text-center m-3">Waiting for approval</h5>
        <div class="spinner-border text-warning m-3" style="height: 5rem; width: 5rem;" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <div class="m-3" style="display: flex; align-items: center; flex-direction: column;">
          <router-link class="text-button" to="/">back</router-link>
          <!-- <router-link class="text-button" to="/">contact admin</router-link> -->
        </div>
      </div>
    </div>
  </LpLayout>
</template>

<script>
import LpLayout from "@/views/LpLayout.vue";

export default {
  name: "WaitingPage",
  components: {
    LpLayout,
  },
  data() {
    return {
    };
  },
  methods: {

  },
};
</script>

<style scoped>
.main-box {
  max-height: 100%;
}
</style>

<style scoped>
.main-box {
  max-height: 100%;
  background-color: rgba(255, 255, 255, 0.75);
  backdrop-filter: blur(5px);
  border-radius: 10px;
}
</style>
