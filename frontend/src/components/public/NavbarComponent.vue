<template>
  <div>
    <header class="header-area header-sticky">
      <div class="container">
        <div class="row">
          <div class="col-12">
            <nav class="main-nav d-flex">
              <!-- ***** Logo Start ***** -->
              <a href="">
                <img src="@/assets/logo.png" alt="" style="height: 4rem; width: auto" />
              </a>
              <!-- ***** Logo End ***** -->
              <!-- ***** Menu Start ***** -->
              <ul class="nav align-item-left">
                <li>
                  <router-link to="/home" exact-active-class="active" exact>Home</router-link>
                </li>
                <li>
                  <router-link to="/about" exact-active-class="active" exact>About</router-link>
                </li>
                <li>
                  <router-link to="/other" exact-active-class="active" exact>Apa kek</router-link>
                </li>
                <template v-if="!isLoggedIn">
                  <router-link to="/login" class="btn btn-primary">Login</router-link>
                </template>
                <template v-else>
                  <div class="dropdown">
                    <a class="btn btn-secondary dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                      <img
                        :src="profilePicture || 'https://github.com/mdo.png'"
                        alt=""
                        style="width: 32px !important; height: 32px !important;"
                        class="rounded-circle me-2" />
                      Dropdown link
                    </a>

                    <ul class="dropdown-menu">
                      <li><a class="dropdown-item" href="#" @click.prevent="logout">Sign out</a></li>
                    </ul>
                  </div>
                </template>
              </ul>
              <a class="menu-trigger">
                <span>Menu</span>
              </a>
              <!-- ***** Menu End ***** -->
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
      // Hapus token dari localStorage
      localStorage.removeItem("token");
      // Set isLoggedIn ke false
      this.isLoggedIn = false;
      this.profilePicture = ""; // Kosongkan gambar profil
      // Alihkan pengguna ke halaman login
      this.$router.push('/login');
    },
  },
};
</script>

<style>
.profile-image {
  border-radius: 50%; /* Membuat gambar bulat */
  width: 1rem; /* Atur ukuran sesuai keinginan */
  height: 1rem;
  object-fit: contain; /* Sesuaikan tinggi gambar dengan container */
}
</style>
