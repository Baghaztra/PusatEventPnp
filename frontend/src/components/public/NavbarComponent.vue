<template>
  <div>
    <header class="header-area header-sticky">
      <div class="container">
        <div class="row">
          <div class="col-12">
            <nav class="main-nav d-flex row">
              <div class="col">
                <div class="d-flex justify-content-center mt-2 align-items-center">
                    <div>
                      <div class="profile-container me-2">
                        <img
                          v-if="isLoggedIn" 
                          :src="profilePicture || 'https://i.pinimg.com/736x/cb/45/72/cb4572f19ab7505d552206ed5dfb3739.jpg'"
                          alt="Profile Picture"
                          class="profile-image" />
                        <img v-else src="@/assets/logo.png" alt="logo" class="profile-image" />
                      </div>
                    </div>
                    <span v-if="isLoggedIn">{{ userName }}</span>
                </div>
              </div>
              <ul class="nav col">
                <li>
                  <router-link to="/home" exact-active-class="active" exact>Home</router-link>
                </li>
                <li>
                  <router-link to="/about" exact-active-class="active" exact>About</router-link>
                </li>
                <li v-if="!isLoggedIn">
                  <router-link to="/login" class="btn btn-light text-cyan">Login</router-link>
                </li>
                <li v-else>
                  <router-link to="#" @click.prevent="logout">Log out</router-link>
                </li>
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
      userName: "", // Nama pengguna
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
        const response = await fetch("http://127.0.0.1:5000/profile", {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (response.ok) {
          const data = await response.json();
          this.profilePicture = data.profile_picture; // Ambil URL gambar profil
          this.userName = data.username; // Ambil nama pengguna
        } else {
          console.error(response,"Gagal mengambil data profil pengguna");
        }
      } catch (error) {
        console.error("Error:", error);
      }
    },
    logout() {
      localStorage.removeItem("token");
      this.isLoggedIn = false;
      this.profilePicture = ""; 
      this.userName = ""; // Reset nama pengguna saat logout
      this.$router.push('/login');
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
.text-cyan {
  color: #22b3c1 !important;
}
</style>
