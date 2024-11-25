<template>
  <LpLayout>
    <div class="d-flex flex-column align-items-center main-box py-3 px-5">
      <router-link to="/" class="position-absolute top-0 end-0 text-secondary mr-2 mt-1">
        <i class="fas fa-caret-left"></i>
      </router-link>

      <div class="flex-column formulir">
        <h5 class="card-title">Register</h5>
        <form @submit.prevent="register">
          <div class="mb-3">
            <label class="form-label" for="email">Name</label>
            <input
              type="text"
              class="form-control"
              style="display: block"
              id="name"
              v-model="name"
              placeholder="Your name"
              required />
          </div>
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
                class="form-control d-block"
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
          <div class="mb-3">
            <label class="form-label" for="passwordConfirm">Confirm Password</label>
            <div class="input-group">
              <input
                :type="confirmPasswordVisible ? 'text' : 'password'"
                class="form-control d-block"
                id="passwordConfirm"
                v-model="passwordConfirm"
                placeholder="Confirm Password"
                required />
              <div class="input-group-append">
                <span class="input-group-text" @click="toggleConfirmPassword">
                  <i
                    :class="confirmPasswordVisible ? 'fas fa-eye-slash' : 'fas fa-eye'"
                    id="iconShowPass"></i>
                </span>
              </div>
            </div>
          </div>
          <button
            type="submit"
            class="btn mb-3"
            style="background-color: #22b3c1; color: aliceblue; width: 100%">
            Register
          </button>
        </form>
        <router-link class="text-button" to="/login">already have an account?</router-link>
      </div>
    </div>
  </LpLayout>
</template>

<script>
import LpLayout from "@/views/LpLayout.vue";
import axios from "axios";
import Swal from "sweetalert2";

export default {
  name: "RegisterPage",
  components: {
    LpLayout
  },
  data() {
    return {
      email: "",
      password: "",
      passwordVisible: false,
      confirmPasswordVisible: false,
    };
  },
  methods: {
    async register() {
      if (this.password == this.passwordConfirm) {
        try {
          const response = await axios.post("http://localhost:5000/register", {
            name: this.name,
            email: this.email,
            password: this.password,
          });
          // const token = response.data.token;
          // localStorage.setItem("token", token);

          // Pindah ke halaman /home
          console.log(response.data.message);
          if (response.status === 201) {
            const { user_id, role } = response.data;
            this.$router.push({
              path: "/waiting",
              query: {
                user_id: user_id,
                role: role,
              },
            });
          }
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
      } else {
        alert("Password tidak cocok");
      }
    },
    loginWithGoogle() {
      window.location.href = "http://127.0.0.1:5000/google-login";
    },
    togglePassword() {
      this.passwordVisible = !this.passwordVisible;
    },
    toggleConfirmPassword() {
      this.confirmPasswordVisible = !this.confirmPasswordVisible;
    },
  },
  created() {
    const urlParams = new URLSearchParams(window.location.search);
    const token = urlParams.get("token");

    if (token) {
      localStorage.setItem("token", token);

      // this.$router.replace({ path: "/home" });
      this.$router.push("/waiting");
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
.formulir {
  width: 100%;
}

@media (max-width: 768px) {
  .formulir {
    width: 100%; 
  }
}

</style>
