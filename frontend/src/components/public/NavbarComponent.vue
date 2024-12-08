<template>
  <!-- Navbar -->
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <!-- Container wrapper -->
    <div class="container">
      <!-- Navbar brand -->
      <div class="d-flex align-items-center">
        <div class="me-2">
          <img
            v-if="isLoggedIn"
            :src="
              profilePicture ||
              'https://i.pinimg.com/736x/cb/45/72/cb4572f19ab7505d552206ed5dfb3739.jpg'
            "
            alt="pfp"
            class="profile-image rounded-circle"
            style="width: 34px; height: 34px" />
          <img
            v-else
            src="../../../public/logo pnp.svg"
            alt="logo"
            class="profile-image rounded-circle"
            style="width: 34px; height: 34px" />
        </div>
        <span v-if="isLoggedIn">{{ userName }}</span>
      </div>

      <!-- Toggle button -->
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarButtonsExample"
        aria-controls="navbarButtonsExample"
        aria-expanded="false"
        aria-label="Toggle navigation">
        <i class="fas fa-bars"></i>
      </button>

      <!-- Collapsible wrapper -->
      <div class="collapse navbar-collapse" id="navbarButtonsExample">
        <div class="d-flex ms-auto align-items-center">
          <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <router-link class="nav-link" to="/home">Home</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/calendar">Calendar</router-link>
            </li>
            <li class="nav-item" v-if="role == 'event organizer'">
              <router-link class="nav-link" :to="'/organizer/'+user_id">Profile</router-link>
            </li>
            <li class="nav-item" v-if="role == 'admin'">
              <router-link class="nav-link" to="/admin">Dashboard</router-link>
            </li>
            <li class="nav-item" v-if="role == 'event organizer'">
              <router-link class="nav-link" to="/create-event">Create Event</router-link>
            </li>
            <li class="nav-item" v-if="!isLoggedIn">
              <!-- Show Login and Sign Up buttons if not logged in -->
              <router-link to="/login" class="nav-link text-primary me-2">Login</router-link>
            </li>
            <li class="nav-item" v-else>
              <!-- Show Log out button if logged in -->
              <a href="#" @click.prevent="logout" class="nav-link text-danger me-2">Log out</a>
            </li>
          </ul>
        </div>
      </div>
      <!-- Collapsible wrapper -->
    </div>
    <!-- Container wrapper -->
  </nav>
  <!-- Navbar -->
</template>

<script>
import axios from "axios";
import Swal from "sweetalert2";

export default {
  name: "NavbarComponent",
  data() {
    return {
      isLoggedIn: false,
      id: "",
      profilePicture: "",
      userName: "",
      role: "",
    };
  },
  mounted() {
    // Cek status login berdasarkan keberadaan token
    const token = localStorage.getItem("token");
    if (token != null) {
      this.isLoggedIn = true;
      this.fetchUserProfile(token);
    }
  },

  methods: {
    async fetchUserProfile(token) {
      try {
        const response = await axios.get(`${process.env.VUE_APP_BACKEND}/profile`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        // Jika respons berhasil (status 200), langsung ambil data
        const data = response.data;
        this.user_id = data.user_id; 
        this.profilePicture = data.profile_picture; 
        this.userName = data.username; 
        this.role = data.role; 

        // console.log(this.role);
        
      } catch (error) {
        // if (error.response) {
        //   console.error("Gagal mengambil data profil pengguna:", error.response);
        // } else {
        //   console.error("Error:", error.message);
        // }
      }
    },
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
          this.isLoggedIn = false;
          this.profilePicture = "";
          this.userName = "";
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
    },
  },
};
</script>

<style scoped>
.profile-container {
  width: 3rem;
  height: 3rem;
  overflow: hidden;
  border-radius: 50%;
}

.profile-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.router-link-active {
  font-weight: bold;
  color: #fff !important;
  background-color: #e95420;
  text-align: center;
  border-radius: 0.375rem
}
</style>
