<template>
  <LpLayout>
    <div class="d-flex flex-column align-items-center main-box p-3">
      <router-link to="/" class="position-absolute top-0 end-0 text-secondary me-2 mt-1">
        <i class="fas fa-caret-left"></i>
      </router-link>

      <div class="card-body mx-3" style="display: flex; flex-direction: column; text-align: left">
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
            <div class="input-group">
              <input
                :type="passwordVisible ? 'text' : 'password'"
                class="form-control"
                style="display: block"
                id="password"
                v-model="password"
                placeholder="Password"
                required />
                <span class="input-group-text" @click="togglePassword">
                  <i
                    :class="passwordVisible ? 'fas fa-eye-slash' : 'fas fa-eye'"
                    id="iconShowPass"></i>
                </span>
            </div>
          </div>

          <button
            type="submit"
            class="btn btn-primary mb-3"
            style="width: 100%">
            Login
          </button>
        </form>
        <button @click="loginWithGoogle" class="btn mb-3 btn-info" style="width: 100%">
          Login with Google
        </button>
        <router-link class="text-button" to="/register">dont have any account?</router-link>
      </div>
    </div>
  </LpLayout>
</template>

<script>
import LpLayout from "@/views/LpLayout.vue";
import axios from "axios";
import Swal from "sweetalert2";

export default {
  name: "LoginPage",
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
        const response = await axios.post(`${process.env.VUE_APP_BACKEND}/login`, {
          email: this.email,
          password: this.password,
        });
        const token = response.data.token;
        localStorage.setItem("token", token);
        console.log(response.data);

        if (response.data.role == "admin") {
          this.$router.push("/admin");
        } else {
          this.$router.push("/home");
        }

        console.log("Login berhasil, token disimpan:", token);
      } catch (error) {
        if (error.response) {
          Swal.fire({
            title: "Something went wrong",
            text: error.response.data.message,
            icon: "error",
          });
        } else {
          console.error(error);
        }
      }
    },
    loginWithGoogle() {
      window.location.href = `${process.env.VUE_APP_BACKEND}/google-login`;
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
  background-color: rgba(255, 255, 255, 0.75);
  backdrop-filter: blur(5px);
  border-radius: 10px;
}
</style>
