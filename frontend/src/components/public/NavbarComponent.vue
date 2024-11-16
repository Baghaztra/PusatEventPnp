<template>
  <!-- Navbar -->
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <!-- Container wrapper -->
    <div class="container">
      <!-- Navbar brand -->
      <div class="d-flex align-items-center">
        <div class="me-2">
          <img v-if="isLoggedIn" :src="profilePicture ||
            'https://i.pinimg.com/736x/cb/45/72/cb4572f19ab7505d552206ed5dfb3739.jpg'
            " alt="pfp" class="profile-image rounded-circle" style="width: 34px; height: 34px" />
          <img v-else src="@/assets/logo.png" alt="logo" class="profile-image rounded-circle"
            style="width: 34px; height: 34px" />
        </div>
        <span v-if="isLoggedIn">{{ userName }}</span>
      </div>

      <!-- Toggle button -->
      <button data-mdb-collapse-init class="navbar-toggler" type="button" data-mdb-toggle="collapse"
        data-mdb-target="#navbarButtonsExample">
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
              <router-link class="nav-link" to="/">Landing page</router-link>
            </li>
            <li class="nav-item" v-if="!isLoggedIn">
              <!-- Show Login and Sign Up buttons if not logged in -->
              <router-link to="/login" class="nav-link text-primary me-2">Login</router-link>
            </li>
            <li class="nav-item" v-else>
              <!-- Show Log out button if logged in -->
              <a href="#" @click.prevent="logout" class="nav-link text-primary me-2">Log out</a>
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
import axios from 'axios';

export default {
  name: "NavbarComponent",
  data() {
    return {
      isLoggedIn: false, // Status login pengguna
      profilePicture: "", // URL gambar profil pengguna
      userName: "", // Nama pengguna
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
        const response = await axios.get("http://127.0.0.1:5000/profile", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        // Jika respons berhasil (status 200), langsung ambil data
        const data = response.data;
        this.profilePicture = data.profile_picture; // Ambil URL gambar profil
        this.userName = data.username; // Ambil nama pengguna

        console.log("Data profil pengguna:", data);
      } catch (error) {
        // Jika terjadi error, tampilkan pesan error
        if (error.response) {
          console.error("Gagal mengambil data profil pengguna:", error.response);
        } else {
          console.error("Error:", error.message);
        }
      }
    },
    logout() {
      localStorage.removeItem("token");
      this.isLoggedIn = false;
      this.profilePicture = "";
      this.userName = ""; // Reset nama pengguna saat logout
      this.$router.push("/login");
    },
  },
};
</script>

<style>
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
</style>
