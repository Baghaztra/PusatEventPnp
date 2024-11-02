<template>
  <div>
    <header class="header-area header-sticky">
      <div class="container">
        <div class="row">
          <div class="col-12">
            <nav class="main-nav d-flex">
              <!-- ***** Logo Start ***** -->
              <a href="">
                <img src="@/assets/logo.png" alt="" style="height: 4rem; width: auto;"/>
              </a>
              <!-- ***** Logo End ***** -->
              <!-- ***** Menu Start ***** -->
              <ul class="nav">
                <li><router-link to="/home" exact-active-class="active" exact>Home</router-link></li>
                <li><router-link to="/about" exact-active-class="active" exact>About</router-link></li>
                <li><router-link to="/other" exact-active-class="active" exact>Apa kek</router-link></li>
                <template v-if="!isLoggedIn">
                  <router-link to="/login" class="btn btn-primary">Login</router-link>
                </template>
                <template v-else>
                  <router-link to="/profile" class="btn btn-secondary">
                    <img :src="profilePicture" alt="Profile" class="profile-image">
                  </router-link>
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
      isLoggedIn: false,      // Status login pengguna
      profilePicture: "",     // URL gambar profil pengguna
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
        const response = await fetch('/profile', {
          method: 'GET',
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (response.ok) {
          const data = await response.json();
          this.profilePicture = data.profile_picture;
        } else {
          console.error('Gagal mengambil data profil pengguna');
        }
      } catch (error) {
        console.error('Error:', error);
      }
    },
  },
};
</script>

<style>
.profile-image {
  border-radius: 50%;      /* Membuat gambar bulat */
  width: 1rem;             /* Atur ukuran sesuai keinginan */
  height: 1rem;
  object-fit: contain;     /* Sesuaikan tinggi gambar dengan container */
}
</style>
