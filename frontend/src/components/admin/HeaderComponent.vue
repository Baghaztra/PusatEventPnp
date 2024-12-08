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
import Swal from 'sweetalert2';

export default {
  methods: {
    logout() {
      Swal.fire({
        title: "Are you sure?",
        text: "You will be logged out.",
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: '<i class="fas fa-check"></i> Yes, logout',
        cancelButtonText: '<i class="fas fa-times"></i> Cancel',
        customClass: {
          content: "fs-6 text-secondary",  
          confirmButton: "btn btn-primary mx-3", 
          cancelButton: "btn btn-secondary mx-3"
        },
        buttonsStyling: false,
      }).then((result) => {
        if (result.isConfirmed) {
          localStorage.removeItem("token");
          this.$router.push("/login");
          Swal.fire({
            title: "Logged out!",
            text: "You have been logged out successfully.",
            icon: "success",
            confirmButtonText: "OK",
            customClass: {
              confirmButton: "btn btn-success",
            },
            buttonsStyling: false,
          });
        }
      });
    }
  }
}
</script>