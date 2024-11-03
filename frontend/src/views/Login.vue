<template>
  <div class="home" style="height: 100vh">
    <PublicStyle />
    <!-- ***** Main Banner Area Start ***** -->
    <section id="section-1">
      <div class="content-slider">
        <input type="radio" id="banner1" class="sec-1-input" name="banner" checked />
        <div class="slider">
          <div id="top-banner-1" class="banner">
            <div class="row d-flex justify-content-center align-items-center h-100">
              <div class="col-md-6">
                <div class="card">
                  <router-link
                    to="/"
                    class="position-absolute top-0 end-0 text-secondary mr-2 mt-1">
                    <i class="fas fa-caret-left"></i>
                  </router-link>

                  <div
                    class="card-body mx-3"
                    style="display: flex; flex-direction: column; text-align: left">
                    <h5 class="card-title">Login</h5>
                    <form @submit.prevent="login">
                      <div class="mb-3">
                        <label class="form-label" for="email">Email address</label>
                        <input
                          type="email"
                          class="form-control"
                          style="display: block"
                          id="email"
                          v-model="email"
                          placeholder="name@example.com"
                          required />
                      </div>
                      <div class="mb-3">
                        <label class="form-label" for="password">Password</label>
                        <input
                          type="password"
                          class="form-control"
                          style="display: block"
                          id="password"
                          v-model="password"
                          placeholder="Password"
                          required />
                      </div>
                      <button
                        type="submit"
                        class="btn mb-3"
                        style="background-color: #22b3c1; color: aliceblue; width: 100%">
                        Login
                      </button>
                    </form>
                    <span class="text-center mb-2">Or</span>
                    <button
                      @click="loginWithGoogle"
                      class="btn mb-3 btn-primary"
                      style="width: 100%">
                      Login with Google
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
    <!-- ***** Main Banner Area End ***** -->
    <PublicScripts />
  </div>
</template>

<script>
import PublicScripts from "@/components/public/PublicScripts.vue";
import PublicStyle from "@/components/public/PublicStyle.vue";
import axios from "axios";

export default {
  name: "LoginPage",
  components: {
    PublicScripts,
    PublicStyle,
  },
  data() {
    return {
      email: "",
      password: "",
    };
  },
  methods: {
    async login() {
      try {
        const response = await axios.post("http://localhost:5000/login", {
          email: this.email,
          password: this.password,
        });
        const token = response.data.token;
        localStorage.setItem("token", token);

        // Pindah ke halaman /home
        this.$router.push("/home");

        console.log("Login berhasil, token disimpan:", token);
      } catch (error) {
        if (error.response) {
          alert(error.response.data.message); // Tampilkan pesan error
        } else {
          console.error(error);
        }
      }
    },
    loginWithGoogle() {
      window.location.href = "http://127.0.0.1:5000/google-login";
    },
  },
  created() {
    const urlParams = new URLSearchParams(window.location.search);
    const token = urlParams.get("token");

    if (token) {
      localStorage.setItem("token", token);

      this.$router.replace({ path: "/home" });

      console.log("Login dengan Google berhasil, token disimpan:", token);
    }
  },

  mounted() {
    document.title = "Pusat Event Politeknik";
  },
};
</script>

<style></style>
