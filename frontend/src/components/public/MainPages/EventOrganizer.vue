<template>
  <HomeLayout>
    <div class="container" style="min-height: 75vh">
      <div class="position-absolute top-0 start-0 mt-5 ms-5">
        <button @click="this.$router.go(-1)" class="btn btn-outline-danger">
          <i class="fas fa-arrow-left me-2"></i> Back
        </button>
      </div>
      <div class="container my-3 mt-5">
        <div class="card p-3">
          <button
            class="btn btn-outline-danger btn-sm me-1 mt-1 position-absolute top-0 end-0"
            v-if="role && role != 'event organizer'"
            v-on:click="report(eodata.id)">
            <i class="fas fa-flag"></i>
          </button>
          <div class="d-flex">
            <div class="image position-relative">
              <img 
                :src="eodata.profile_picture" 
                class="rounded" 
                width="155" 
                @click="handleImageClick"
                :class="{ 'cursor-pointer': role == 'event organizer' && userId == eodata.id }"
                alt="Profile Picture"
              />
              <input 
                v-if="role == 'event organizer' && userId == eodata.id" 
                type="file" 
                class="position-absolute top-0 start-0 w-100 h-100 opacity-0 cursor-pointer" 
                @change="updateProfilePicture"
                accept="image/*"
              />
              <div v-if="role == 'event organizer' && userId == eodata.id" 
                  class="position-absolute top-50 start-50 translate-middle text-secondary file-icon">
                <i class="fas fa-pen-to-square"></i>
              </div>
            </div>


            <div class="ml-3 ms-3 w-100">
              <div class="d-flex align-items-center">
                <h4 class="mb-0 mt-0 d-inline me-3">{{ eodata.username }}</h4>
                <a
                  v-if="role == 'event organizer' && userId == eodata.id"
                  class="btn btn-outline-warning btn-sm"
                  v-on:click="updateProfile(eodata.id, 'username', eodata.username)">
                  <i class="fas fa-pen-to-square"></i>
                </a>
                <button
                  v-if="this.role != 'event organizer' && !isFollowing"
                  class="btn btn-sm btn-primary d-inline"
                  v-on:click="toggleFollow">
                  Follow
                </button>
                <button
                  v-else-if="this.role != 'event organizer' && isFollowing"
                  class="btn btn-sm btn-outline-primary d-inline"
                  v-on:click="toggleFollow">
                  Unfollow
                </button>
              </div>
              <div class="d-flex rounded stats">
                <div class="d-inline pe-2">
                  <span class="small text-secondary mx-1">Events</span>
                  <span class="small text-secondary mx-1">{{ eodata.events?.length ?? 0 }}</span>
                </div>
                <div class="d-inline pe-2">
                  <span class="small text-secondary mx-1">Followers</span>
                  <span class="small text-secondary mx-1">{{ eodata.subs?.length ?? 0 }}</span>
                </div>
              </div>
              <div class="mt-2 row">
                <p>
                  {{ eodata.bio }}
                  <a
                    v-if="role == 'event organizer' && userId == eodata.id"
                    class="btn btn-outline-warning btn-sm"
                    v-on:click="updateProfile(eodata.id, 'bio', eodata.bio )">
                    <i class="fas fa-pen-to-square"></i>
                  </a>
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Events -->
      <h3>Events</h3>
      <div v-if="eodata.events && eodata.events.length == 0">
        <h6 class="text-secondary">No event published yet..</h6>
      </div>
      <div v-else class="row">
        <CardComponent
          v-for="(event, index) in eodata.events"
          :key="index"
          :data="event"
          class="col-md-4 mb-3"
          @refresh-events="fetchEoData" />
      </div>
      <!-- Events -->
    </div>
  </HomeLayout>
</template>

<script>
import HomeLayout from "@/views/HomeLayout.vue";
import CardComponent from "./CardComponent.vue";
import axios from "axios";
import Swal from "sweetalert2";
import router from "@/router";

export default {
  name: "EventDetails",
  components: {
    HomeLayout,
    CardComponent,
  },
  props: {
    id: String,
  },
  data() {
    return {
      token: "",
      eodata: {},
      loading: false,
      isLoggedIn: false,
      isFollowing: false,
      comment: "",
      profilePicture: "",
      userName: "",
      userId: "",
      role: "",
      isOwner: false,
    };
  },
  watch: {
    id: "fetchEoData",
  },
  methods: {
    async fetchEoData() {
      this.loading = true;
      try {
        const response = await axios.get(
          `${process.env.VUE_APP_BACKEND}/event_organizers?id=${this.id}`
        );
        this.eodata = response.data;
        if (!this.eodata || this.eodata.status != "Active") {
          router.push("/404_");
        }

        this.isFollowing = this.eodata.subs.includes(this.userId);
      } catch (error) {
        console.error("Error fetching event-organizer details:", error);
      } finally {
        this.loading = false;
      }
      if (this.role == "event organizer" && this.userId == this.eodata.id) {
        this.isOwner = true;
      }
    },

    async fetchUserProfile() {
      try {
        const response = await axios.get(`${process.env.VUE_APP_BACKEND}/profile`, {
          headers: {
            Authorization: `Bearer ${this.token}`,
          },
        });

        const data = response.data;
        this.profilePicture = data.profile_picture;
        this.userName = data.username;
        this.userId = data.user_id;
        this.role = data.role;
      } catch (error) {
        if (error.response) {
          console.error("Gagal mengambil data profil pengguna:", error.response);
        } else {
          console.error("Error:", error.message);
        }
      }
    },

    async toggleFollow() {
      try {
        // const response = await axios.post(
        await axios.post(
          `${process.env.VUE_APP_BACKEND}/subscribe/${this.eodata.id}`,
          {}, // Body kosong
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("token")}`,
            },
          }
        );
        // console.log(response.data.message);
        this.isFollowing = !this.isFollowing;
        // console.log("following: ", this.isFollowing);
        this.fetchEoData();
        // this.isFollowing = response.data.liked;
      } catch (error) {
        console.error("Error saat mengirim permintaan like:", error);
        Swal.fire({
          title: "Login",
          text: "Anda harus login untuk berinteraksi",
          // icon: "error",
          showCancelButton: false,
          confirmButtonText: "Login",
        }).then((result) => {
          if (result.isConfirmed) {
            window.location.href = "/login";
          }
        });
      }
    },

    async report(user_id) {
      Swal.fire({
        title: `Report this EO?`,
        input: "text",
        icon: "warning",
        inputPlaceholder: "Tell us what's wrong with this EO",
        inputAttributes: {
          autocapitalize: "off",
          class: "form-control",
        },
        showCancelButton: true,
        confirmButtonText: '<i class="fas fa-flag"></i> Report',
        cancelButtonText: '<i class="fas fa-cancel"></i> Cancel',
        customClass: {
          title: "fs-5 text-primary",
          confirmButton: "btn btn-danger",
          cancelButton: "btn btn-secondary",
        },
        showLoaderOnConfirm: true,
        preConfirm: async (message) => {
          if (!message) {
            Swal.showValidationMessage("Message can't be empty");
            return;
          }

          try {
            const token = localStorage.getItem("token");
            const response = await axios.post(
              `${process.env.VUE_APP_BACKEND}/report`,
              {
                id: user_id,
                type: "eo",
                message: message,
              },
              {
                headers: {
                  Authorization: `Bearer ${token}`,
                  "Content-Type": "application/json",
                },
              }
            );

            if (response.status !== 200) {
              Swal.showValidationMessage(`${response.data.message || "Error"}`);
            }
            return response.data;
          } catch (error) {
            Swal.showValidationMessage(
              `Request failed: ${error.response?.data?.message || error.message}`
            );
          }
        },
        allowOutsideClick: () => !Swal.isLoading(),
      }).then((result) => {
        if (result.isConfirmed) {
          Swal.fire({
            title: "Success!",
            text: `${result.value.message}`,
            icon: "success",
          });
          this.$emit("refresh-events");
        }
      });
    },

    async updateProfile(id, key, _default) {
      Swal.fire({
        title: `Update ${key}`,
        input: key === "bio" ? "textarea" : "text",
        inputAttributes: {
          autocapitalize: "off",
          class: "form-control",
        },
        inputValue: _default,
        showCancelButton: true,
        confirmButtonText: '<i class="fas fa-save"></i> Save',
        cancelButtonText: '<i class="fas fa-cancel"></i> Cancel',
        customClass: {
          title: "fs-5 text-primary",
          confirmButton: "btn btn-primary",
          cancelButton: "btn btn-secondary",
        },
        showLoaderOnConfirm: true,
        preConfirm: async (value) => {
          if (!value) {
            Swal.showValidationMessage("Value can't be empty");
            return;
          }

          try {
            const token = localStorage.getItem("token");
            const response = await axios.patch(
              `${process.env.VUE_APP_BACKEND}/update/profile`,
              {
                id: id,
                key: key,
                value: value,
              },
              {
                headers: {
                  Authorization: `Bearer ${token}`,
                  "Content-Type": "application/json",
                },
              }
            );

            if (response.status !== 200) {
              Swal.showValidationMessage(`Gagal menyimpan: ${response.data.message || "Error"}`);
            }
            return response.data;
          } catch (error) {
            Swal.showValidationMessage(
              `Request failed: ${error.response?.data?.message || error.message}`
            );
          }
        },
        allowOutsideClick: () => !Swal.isLoading(),
      }).then((result) => {
        if (result.isConfirmed) {
          Swal.fire({
            title: "Success!",
            text: `${result.value.message}`,
            icon: "success",
          });
          this.fetchEoData();
        }
      });
    },

    handleImageClick() {
      if (this.role === 'event organizer' && this.userId === this.eodata.id) {
        this.$refs.fileInput.click();
      }
    },
    async updateProfilePicture(event) {
      const file = event.target.files[0];
      if (!file) return;

      const formData = new FormData();
      formData.append("profile_picture", file);

      try {
        const response = await axios.patch(
          `${process.env.VUE_APP_BACKEND}/file/update-profile-picture`,
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data", // Wajib untuk mengunggah file
              Authorization: `Bearer ${localStorage.getItem("token")}`, // Menambahkan token JWT untuk otentikasi
            },
          }
        );
        console.log(response.data.message);
        this.fetchEoData();
        Swal.fire({
          title: "Success!",
          text: "Profile picture updated successfully.",
          icon: "success",
          confirmButtonText: "OK",
        });
      } catch (error) {
        Swal.fire({
          title: "Error",
          text: error.response?.data?.message || "Failed to update profile picture.",
          icon: "error",
          confirmButtonText: "OK",
        });
      }
    },
  },
  mounted() {
    this.token = localStorage.getItem("token");
    if (this.token != "") {
      this.isLoggedIn = true;
      this.fetchUserProfile();
    }
    this.fetchEoData();
  },
};
</script>
