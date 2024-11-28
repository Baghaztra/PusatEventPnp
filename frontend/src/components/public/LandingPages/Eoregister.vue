<template>
  <LpLayout>
    <div class="d-flex flex-column align-items-center main-box py-3 px-5">
      <router-link to="/" class="position-absolute top-0 end-0 text-secondary me-2 mt-1">
        <i class="fas fa-caret-left"></i>
      </router-link>

      <div class="flex-column formulir">
        <h5 class="card-title">Create your EO Account</h5>
        <!-- <form @submit.prevent="register"> -->
          <div class="row">
            <div :class=" page1? 'd-block' : 'd-none'" >
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
                    <span class="input-group-text" @click="togglePassword">
                      <i :class="passwordVisible ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
                    </span>
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
                    <span class="input-group-text" @click="toggleConfirmPassword">
                      <i :class="confirmPasswordVisible ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
                    </span>
                </div>
              </div>
              <button class="btn btn-primary mb-3 w-100" @click="togglePage">Next <i class="fas fa-arrow-right"></i></button>
            </div>
            <div :class=" page1? 'd-none' : 'd-block'">
              <div class="mb-3">
                <label class="form-label" for="pfp">Profile picture</label>
                <input class="form-control" type="file" id="pfp" @change="onFileSelected">
              </div>
              <div class="mb-3">
                <label class="form-label" for="bio">Bio</label>
                <textarea class="form-control" id="bio" rows="8" v-model="bio" placeholder="Tell everything about your organization/community"></textarea>
              </div>
              <div class="d-flex justify-content-between mb-3">
                <button class="btn btn-secondary col-5" @click="togglePage"><i class="fas fa-arrow-left"></i> Previous</button>
                <button
                  type="submit"
                  class="btn btn-primary col-5"
                  v-on:click="register"
                >
                  Request
                </button>
              </div>
            </div>
          </div>
        <!-- </form> -->
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
      page1: true,
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

          const { user_id, role } = response.data;
            this.$router.push({
              path: "/waiting",
              query: {
                user_id: user_id,
                role: role,
              },
            });
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
    togglePage() {
      this.page1 = !this.page1;
    },
    togglePassword() {
      this.passwordVisible = !this.passwordVisible;
    },
    toggleConfirmPassword() {
      this.confirmPasswordVisible = !this.confirmPasswordVisible;
    },
  },
  mounted() {
    this.page1 = true;
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
