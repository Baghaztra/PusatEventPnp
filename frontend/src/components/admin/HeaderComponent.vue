<template>
  <header class="navbar navbar-dark sticky-top bg-primary flex-md-nowrap p-0 shadow">
    <button
      class="navbar-toggler d-md-none collapsed"
      type="button"
      data-bs-toggle="collapse"
      data-bs-target="#sidebarMenu"
      aria-controls="sidebarMenu"
      aria-expanded="false"
      aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <router-link class="navbar-brand fs-3 col-md-3 col-lg-2 me-0 px-3 fs-6" to="/home">
      Pusat Event Politeknik
    </router-link>
    <div class="navbar-nav">
      <div class="nav-item text-nowrap">
        <button class="nav-link px-3" v-on:click="logout">Sign out</button>
      </div>
    </div>
  </header>
</template>

<script>
export default {
  methods: {
    logout() {
      localStorage.removeItem("token");
      this.$router.push("/login");
    },
  }
}
</script>