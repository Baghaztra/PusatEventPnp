<template>
  <LpLayout>
    <div class="d-flex flex-column align-items-center main-box py-3 px-5">
      <router-link to="/" class="position-absolute top-0 end-0 text-secondary mr-2 mt-1">
        <i class="fas fa-caret-left"></i>
      </router-link>

      <div class="flex-column formulir">
        <h5 class="card-title">Create your EO Account</h5>
        <form @submit.prevent="register">
          <div class="row">
            <div class="col-md-6">
              <div class="mb-3">
                <label class="form-label" for="name">Name</label>
                <input
                  type="text"
                  class="form-control"
                  id="name"
                  v-model="name"
                  placeholder="Organization name"
                  required />
              </div>
              <div class="mb-3">
                <label class="form-label" for="email">Email address</label>
                <input
                  type="email"
                  class="form-control"
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
                    id="password"
                    v-model="password"
                    placeholder="Password"
                    required />
                  <div class="input-group-append">
                    <span class="input-group-text" @click="togglePassword">
                      <i :class="passwordVisible ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
                    </span>
                  </div>
                </div>
              </div>
              <div class="mb-3">
                <label class="form-label" for="passwordConfirm">Confirm Password</label>
                <div class="input-group">
                  <input
                    :type="confirmPasswordVisible ? 'text' : 'password'"
                    class="form-control"
                    id="passwordConfirm"
                    v-model="passwordConfirm"
                    placeholder="Confirm Password"
                    required />
                  <div class="input-group-append">
                    <span class="input-group-text" @click="toggleConfirmPassword">
                      <i :class="confirmPasswordVisible ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
                    </span>
                  </div>
                </div>
              </div>
            </div>
            <div class="col-md-6">
              <div class="mb-3">
                <label class="form-label" for="pfp">Profile picture</label>
                <input class="form-control" type="file" id="pfp" @change="onFileSelected">
              </div>
              <div class="mb-3">
                <label class="form-label" for="bio">Bio</label>
                <textarea class="form-control" id="bio" rows="8" v-model="bio" placeholder="Tell everything about your organization/community"></textarea>
              </div>
            </div>
          </div>
          <button
            type="submit"
            class="btn mb-3"
            style="background-color: #22b3c1; color: aliceblue; width: 100%">
            Request
          </button>
        </form>
        <router-link class="text-button" to="/eo-login">already have an account?</router-link>
      </div>
    </div>
  </LpLayout>
</template>

<script>
import LpLayout from "@/views/LpLayout.vue";
import axios from "axios";
import Swal from "sweetalert2";

export default {
  name: "EoRegisterPage",
  components: {
    LpLayout,
  },
  data() {
    return {
      name: "",
      email: "",
      password: "",
      passwordConfirm: "",
      passwordVisible: false,
      confirmPasswordVisible: false,
      bio: "",
      pfp: null,
    };
  },
  methods: {
    onFileSelected(event){
      this.pfp = event.target.files[0];
    },
    async register() {
      if (this.password === this.passwordConfirm) {
        const formData = new FormData();
        formData.append("name", this.name);
        formData.append("email", this.email);
        formData.append("password", this.password);
        formData.append("bio", this.bio);
        formData.append("pfp", this.pfp, this.pfp.name);

        try {
          const response = await axios.post(`${process.env.VUE_APP_BACKEND}/eo-register`, formData, {
            headers: { "Content-Type": "multipart/form-data" },
          });
          // const token = response.data.token;
          console.log("Registrasi berhasil:", response);

          this.$router.push("/waiting");
        } catch (error) {
          if (error.response) {
            // alert(error.response.data.message);
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
    togglePassword() {
      this.passwordVisible = !this.passwordVisible;
    },
    toggleConfirmPassword() {
      this.confirmPasswordVisible = !this.confirmPasswordVisible;
    },
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
