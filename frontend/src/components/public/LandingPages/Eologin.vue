<template>
    <LpLayout>
      <div class="d-flex flex-column align-items-center main-box">
        <router-link to="/" class="position-absolute top-0 end-0 text-secondary mr-2 mt-1">
          <i class="fas fa-caret-left"></i>
        </router-link>
  
        <div class="card-body mx-3" style="display: flex; flex-direction: column; text-align: left">
          <h5 class="card-title">Login as Event Organizer</h5>
          <form @submit.prevent="login">
            <div class="mb-3">
              <label class="form-label" for="email">Email address</label>
              <input
                type="email"
                class="form-control"
                style="display: block"
                id="email"
                v-model="email"
                placeholder="organization-official@example.com"
                required />
            </div>
            <div class="mb-3">
              <label class="form-label" for="password">Password</label>
              <div class="input-group">
                <input
                  :type="passwordVisible ? 'text' : 'password'"
                  class="form-control"
                  style="display: block"
                  id="password"
                  v-model="password"
                  placeholder="Password"
                  required />
                <div class="input-group-append">
                  <span class="input-group-text" @click="togglePassword">
                    <i
                      :class="passwordVisible ? 'fas fa-eye-slash' : 'fas fa-eye'"
                      id="iconShowPass"></i>
                  </span>
                </div>
              </div>
            </div>
  
            <button
              type="submit"
              class="btn mb-3"
              style="background-color: #22b3c1; color: aliceblue; width: 100%">
              Login
            </button>
          </form>
          <router-link class="text-button" to="/eo-register">Create new eo account</router-link>
        </div>
      </div>
    </LpLayout>
  </template>
  
  <script>
  import LpLayout from "@/views/LpLayout.vue";
  import axios from "axios";
  
  export default {
    name: "EoLoginPage",
    components: {
      LpLayout,
    },
    data() {
      return {
        email: "",
        password: "",
        passwordVisible: false,
      };
    },
    methods: {
      async login() {
        try {
          const response = await axios.post("http://localhost:5000/login-eo", {
            email: this.email,
            password: this.password,
          });
          const token = response.data.token;
          if (token) {
            localStorage.setItem("token", token);
            this.$router.push("/home");
            console.log("Login berhasil, token disimpan:", token);
          } else {
            console.error("Token tidak ditemukan di respons backend.");
          }

        } catch (error) {
          if (error.response) {
            console.error("Error dari server:", error.response);
            alert(error.response.data.message || "Login gagal");
          } else {
            console.error("Kesalahan jaringan atau lainnya:", error);
          }
        }
      },
      togglePassword() {
        this.passwordVisible = !this.passwordVisible;
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
  