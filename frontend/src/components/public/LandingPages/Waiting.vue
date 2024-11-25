<template>
  <LpLayout>
    <div class="d-flex flex-column align-items-center main-box">
      <router-link to="/" class="position-absolute top-0 end-0 text-secondary mr-2 mt-1">
        <i class="fas fa-caret-left"></i>
      </router-link>

      <div class="card-body mx-3" style="display: flex; align-items: center; flex-direction: column;">
        <h5 class="card-title text-center m-3">Waiting for approval</h5>
        <div class="spinner-border text-warning m-3" style="height: 5rem; width: 5rem;" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <h6 class="card-title text-center mt-3">Check on your email</h6>
        <a class="text-primary" v-on:click="resend">resend confirmation email</a>
        <div class="m-3" style="display: flex; align-items: center; flex-direction: column;">
          <router-link class="text-button" to="/">ok</router-link>
          <!-- <router-link class="text-button" to="/">contact admin</router-link> -->
        </div>
      </div>
    </div>
  </LpLayout>
</template>

<script>
import LpLayout from "@/views/LpLayout.vue";
import axios from "axios";
import Swal from "sweetalert2";

export default {
  name: "WaitingPage",
  components: {
    LpLayout,
  },
  data() {
    return {
    };
  },
  methods: {
    async resend(){
      const result = await Swal.fire({
        title: "Resend confirmation email",
        icon: "info",
        showCancelButton: true,
        confirmButtonText: "Yes",
        cancelButtonText: "Cancel",
        customClass: {
          popup: "card",
          title: "h5",
          confirmButton: "btn btn-sm btn-danger me-3",
          cancelButton: "btn btn-sm btn-secondary ms-3",
        },
        buttonsStyling: false,
      });
      if (result.isConfirmed) {
        try {
          const response = await axios.post("http://127.0.0.1:5000/resend", {
            id: this.$route.query.user_id,
            role: this.$route.query.role,
          });
          console.log(response.data);
          Swal.fire({
            title: "Success",
            text: response.data.message,
            icon: "success",
            customClass: {
              popup: "card",
              title: "h4",
              content: "small",
              confirmButton: "btn btn-sm btn-success",
            },
            buttonsStyling: false,
          }).then(() => {
            // Navigasi ke "/"
            this.$router.push("/");
          });

        } catch (error) {
          if (error.response) {
            Swal.fire({
              title: "Error!",
              text: error.response.data.message,
              icon: "error",
              customClass: {
                popup: "alert alert-danger",
                title: "h4",
                content: "small",
                confirmButton: "btn btn-sm btn-success",
              },
              buttonsStyling: false,
            });
          } else {
            console.error(error);
          }
        }
      }
    }
  },
  mounted() {
    const userId = this.$route.query.user_id;
    const role = this.$route.query.role;
    console.log("User ID:", userId);
    console.log("Role:", role);
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
