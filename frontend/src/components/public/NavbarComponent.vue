<template>
  <div>
    <header class="header-area header-sticky">
      <div class="container">
        <div class="row">
          <div class="col-12">
            <nav class="main-nav d-flex">
              <a href="">
                <img src="@/assets/logo.png" alt="" style="height: 4rem; width: auto" />
              </a>
              <ul class="nav">
                <li>
                  <router-link to="/home" exact-active-class="active" exact>Home</router-link>
                </li>
                <li>
                  <router-link to="/about" exact-active-class="active" exact>About</router-link>
                </li>
                <template v-if="!isLoggedIn">
                  <router-link to="/login" class="btn btn-primary">Login</router-link>
                </template>
                <template v-else>
                  <div class="d-flex align-items-center">
                    <img
                      :src="profilePicture || 'https://i.pinimg.com/736x/cb/45/72/cb4572f19ab7505d552206ed5dfb3739.jpg'"
                      alt="Profile Picture"
                      class="rounded-circle me-2 profile-image" />
                    <span>Nama User</span>
                    <a class="dropdown-item" href="#" @click.prevent="logout">Sign out</a>
                  </div>
                </template>
              </ul>
              <a class="menu-trigger">
                <span>Menu</span>
              </a>
            </nav>
          </div>
        </div>
      </div>
    </header>
  </div>
</template>

<script>
export default {
  name: "NavbarComponent",
  data() {
    return {
      isLoggedIn: false, // Status login pengguna
      profilePicture: "", // URL gambar profil pengguna
    };
  },
  mounted() {
    // Cek status login berdasarkan keberadaan token
    const token = localStorage.getItem("token");
    this.isLoggedIn = !!token; // Jika token ada, set isLoggedIn ke true

    if (this.isLoggedIn) {
      // Panggil fungsi untuk mengambil data profil
      this.fetchUserProfile(token);
    }
  },

  methods: {
    async fetchUserProfile(token) {
      try {
        const response = await fetch("/profile", {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (response.ok) {
          const data = await response.json();
          this.profilePicture = data.profile_picture;
        } else {
          console.error("Gagal mengambil data profil pengguna");
        }
      } catch (error) {
        console.error("Error:", error);
      }
    },
    logout() {
      localStorage.removeItem("token");
      this.isLoggedIn = false;
      this.profilePicture = ""; 
      this.$router.push('/login');
    },
  },
};
</script>

<style>
.profile-image {
  width: 3rem; /* Atur ukuran sesuai keinginan */
  height: 3rem;
  object-fit: contain; /* Sesuaikan tinggi gambar dengan container */
}
</style>
