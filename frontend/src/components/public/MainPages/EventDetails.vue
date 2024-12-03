<template>
  <HomeLayout>
    <div class="container">
      <!-- Hero -->
      <div class="bg-image bg-pkm">
        <div class="mask rounded p-5">
          <div class="position-absolute top-0 start-0 mt-5 ms-5">
            <button @click="this.$router.go(-1)" class="btn btn-outline-danger">
              <i class="fas fa-arrow-left me-2"></i> Back
            </button>
            <button
              v-if="userRole == 'event organizer' && userId == event.eo_id"
              class="btn btn-outline-warning"
              v-on:click="updatePoster(event.id)">
              <i class="fas fa-pen-to-square"></i> Change poster
            </button>
          </div>
          <div class="d-flex justify-content-center align-items-center h-100">
            <div class="text-white text-center">
              <h1 class="mb-3">
                {{ event.title }}
                <button
                  v-if="userRole == 'event organizer' && userId == event.eo_id"
                  class="btn btn-sm btn-outline-warning"
                  v-on:click="updateEvent(event.id, 'title')">
                  <i class="fas fa-pen-to-square"></i>
                </button>
              </h1>
              <h4 class="mb-3">
                {{ formatDate(event.event_date) }}
                <button
                  v-if="userRole == 'event organizer' && userId == event.eo_id"
                  class="btn btn-sm btn-outline-warning"
                  v-on:click="updateEvent(event.id, 'start_date')">
                  <i class="fas fa-pen-to-square"></i>
                </button>
              </h4>
              <a
                v-if="event.registration_url && event.registration_url == 'closed'"
                class="btn btn-primary btn-lg disabled">
                Registration Closed
              </a>
              <a
                v-else-if="event.registration_url"
                class="btn btn-outline-primary btn-lg"
                :href="event.registration_url"
                target="_blank">
                Register
              </a>
              <a
                v-if="userRole == 'event organizer' && userId == event.eo_id"
                class="btn btn-outline-warning btn-lg"
                v-on:click="updateEvent(event.id, 'registration_url')">
                <i class="fas fa-pen-to-square"></i>
              </a>
              <a
                v-if="userRole == 'event organizer' && userId == event.eo_id && event.registration_url != 'closed'"
                class="btn btn-outline-danger btn-lg"
                v-on:click="closeReg(event.id)">
                <i class="fas fa-ban"></i>
              </a>
            </div>
          </div>
        </div>
      </div>
      <!-- Hero -->
      <div class="container my-3">
        <div class="row">
          <div class="col-md-8">
            <router-link
              v-if="userRole == 'event organizer' && userId == event.eo_id"
              class="btn btn-sm btn-outline-warning"
              :to="'/edit-event/'+event.id">
              <i class="fas fa-pen-to-square"></i> Edit description
            </router-link>
            <div v-else>
              <router-link :to="'/organizer/' + event.eo_id" class="text-primary">
                {{ event.eo }}
              </router-link>
              presents:
            </div>
            <h3 class="text-primary">{{ event.title }}</h3>
            <div v-html="event.description"></div>
          </div>
          <div class="col-md-4">
            <img src="" alt="" />
          </div>
        </div>
      </div>

      <!-- Gallery -->
      <button
        v-if="userRole == 'event organizer' && userId == event.eo_id"
        class="btn btn-sm btn-warning"
        v-on:click="uploadImage(event.id)">
        <i class="fas fa-add"></i> Add new image
      </button>
      <h3 v-if="event.images && event.images.length > 0">Gallery</h3>
      <div class="row">
        <div class="col">
          <div class="d-flex overflow-auto">
            <div
              v-for="(image, index) in event.images"
              :key="index"
              class="p-2"
              style="flex: 0 0 auto">
              <div class="div position-relative">
                <button
                  v-if="userRole == 'event organizer' && userId == event.eo_id"
                  class="btn btn-sm btn-danger position-absolute top-0 end-0"
                  v-on:click="deleteImage(image.id)">
                  <i class="fas fa-trash"></i>
                </button>
                <img :src="image.path" alt="gambar" class="img-fluid rounded galery_image" />
              </div>
            </div>
          </div>
        </div>
      </div>
      <!-- Gallery -->

      <!-- Forum -->
      <h3 class="mt-3">Forum</h3>
      <!-- Comentar -->
      <section>
        <div class="container mb-5 text-body">
          <div class="row d-flex justify-content-center">
            <div class="col-md-11">
              <!-- Add new -->
              <div class="d-flex flex-start mb-4" v-if="userRole != 'event organizer'">
                <div class="pt-4">
                  <img
                    v-if="profilePicture"
                    class="rounded-circle shadow-1-strong me-3"
                    :src="profilePicture"
                    alt="avatar"
                    width="45"
                    height="45" />
                  <img
                    v-else
                    src="https://i.pinimg.com/736x/cb/45/72/cb4572f19ab7505d552206ed5dfb3739.jpg"
                    class="rounded-circle shadow-1-strong me-3"
                    alt="avatar"
                    width="45"
                    height="45" />
                </div>
                <div class="card w-100">
                  <div class="card-body p-3">
                    <div class="form-floating">
                      <textarea
                        class="form-control"
                        placeholder="Leave a comment here"
                        id="new_comment"
                        v-model="comment"
                        @input="adjustHeight($event)"
                        rows="1"
                        style="overflow: hidden; resize: none"></textarea>
                      <label for="new_comment">Say something about this?</label>
                    </div>
                    <div class="position-absolute bottom-0 end-0">
                      <button class="btn btn-sm btn-primary end-0" v-on:click="sendComment">
                        <i class="fa fa-circle-arrow-right"></i>
                      </button>
                    </div>
                    <div class="d-none text-danger" id="validation">
                      <small>Can't send empty comment</small>
                    </div>
                  </div>
                </div>
              </div>
              <!-- Add new -->

              <!-- Another comment -->
              <div v-if="event.comments && event.comments.length == 0">
                <h6 class="text-secondary">No one comment yet..</h6>
              </div>
              <div
                class="d-flex flex-start mb-4"
                v-else
                v-for="comment in event.comments"
                :key="comment">
                <div class="pt-4">
                  <img
                    v-if="comment.pfp"
                    class="rounded-circle shadow-1-strong me-3"
                    :src="comment.pfp"
                    alt="avatar"
                    width="45"
                    height="45" />
                  <img
                    v-else
                    src="https://i.pinimg.com/736x/cb/45/72/cb4572f19ab7505d552206ed5dfb3739.jpg"
                    class="rounded-circle shadow-1-strong me-3"
                    alt="avatar"
                    width="45"
                    height="45" />
                </div>
                <div class="card w-100">
                  <div class="card-body p-4">
                    <button
                      class="btn btn-outline-danger btn-sm me-1 mt-1 position-absolute top-0 end-0"
                      v-if="userRole && userRole != 'event organizer' && userId != comment.user_id"
                      v-on:click="report(comment.user_id)">
                      <i class="fas fa-flag"></i>
                    </button>
                    <h5>{{ comment.username }}</h5>
                    <p class="small text-secondary">{{ comment.created_at }}</p>
                    <p>
                      {{ comment.text }}
                    </p>
                  </div>
                  <div
                    v-if="comment.user_id == userId"
                    class="position-absolute bottom-0 end-0 me-3 mb-3">
                    <a v-on:click="deleteComment(comment.id)" class="text-danger"
                      ><small>Delete</small></a
                    >
                  </div>
                </div>
              </div>
              <!-- Another comment -->
            </div>
          </div>
        </div>
      </section>
      <!-- Forum -->
    </div>
  </HomeLayout>
</template>

<script>
import router from "@/router";
import HomeLayout from "@/views/HomeLayout.vue";
import axios from "axios";
import Swal from "sweetalert2";

export default {
  name: "EventDetails",
  components: {
    HomeLayout,
  },
  props: {
    id: String,
  },
  data() {
    return {
      token: "",
      event: {},
      loading: false,
      isLoggedIn: false,
      comment: "",
      profilePicture: "",
      userName: "",
      userId: "",
      userRole: "",
    };
  },
  watch: {
    id: "fetchEventDetails",
  },
  methods: {
    async fetchEventDetails() {
      this.loading = true;
      try {
        const response = await axios.get(`${process.env.VUE_APP_BACKEND}/event/${this.id}`);
        this.event = response.data;
        if (this.event.eo_status != "Active") {
          router.push("/404_");
        }
      } catch (error) {
        console.error("Error fetching event details:", error);
      } finally {
        this.loading = false;
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
        this.userRole = data.role;
      } catch (error) {
        if (error.response) {
          console.error("Gagal mengambil data profil pengguna:", error.response);
        } else {
          console.error("Error:", error.message);
        }
      }
    },

    formatDate(dateString) {
      const date = new Date(Date.parse(dateString));
      if (isNaN(date)) {
        return "";
      }
      const options = { weekday: "long", day: "2-digit", month: "long", year: "numeric" };
      return new Intl.DateTimeFormat("id-ID", options).format(date);
    },

    adjustHeight(event) {
      const textarea = event.target;
      textarea.style.height = "auto"; // Reset tinggi
      textarea.style.height = textarea.scrollHeight + "px"; // Sesuaikan tinggi
    },

    async sendComment() {
      if (this.comment != "") {
        try {
          const payload = {
            message: this.comment,
            event_id: this.event.id,
          };

          // Debug: log data yang akan dikirim
          console.log("Payload yang dikirim:", payload);

          const response = await axios.post(`${process.env.VUE_APP_BACKEND}/comment`, payload, {
            headers: {
              Authorization: `Bearer ${this.token}`,
            },
          });

          console.log(response.data);

          this.fetchEventDetails();

          this.comment = "";
          document.getElementById("validation").classList.add("d-none");
          document.getElementById("validation").classList.remove("d-block");
        } catch (error) {
          if (error.response) {
            // alert(error.response.data.message);
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
          } else {
            console.error(error);
          }
        }
      } else {
        document.getElementById("validation").classList.add("d-block");
        document.getElementById("validation").classList.remove("d-none");
      }
    },

    async deleteComment(id) {
      const result = await Swal.fire({
        title: "Delete this comment?",
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Yes",
        cancelButtonText: "Cancel",
        customClass: {
          popup: "card",
          title: "h5",
          confirmButton: "btn btn-danger me-3",
          cancelButton: "btn btn-secondary ms-3",
        },
        buttonsStyling: false,
      });
      if (result.isConfirmed) {
        try {
          const response = await axios.delete(`${process.env.VUE_APP_BACKEND}/comment`, {
            data: { comment_id: id },
          });
          console.log(response.data);
          this.fetchEventDetails();
          Swal.fire({
            title: "Comment deleted!",
            text: "The comment is successfully deleted.",
            icon: "success",
            customClass: {
              popup: "card",
              title: "h4",
              content: "small",
              confirmButton: "btn btn-success",
            },
            buttonsStyling: false,
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
                confirmButton: "btn btn-success",
              },
              buttonsStyling: false,
            });
          } else {
            console.error(error);
          }
        }
      }
    },

    async deleteImage(id) {
      const result = await Swal.fire({
        title: "Delete this image?",
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Yes",
        cancelButtonText: "Cancel",
        customClass: {
          popup: "card",
          title: "h5",
          confirmButton: "btn btn-danger me-3",
          cancelButton: "btn btn-secondary ms-3",
        },
        buttonsStyling: false,
      });
      if (result.isConfirmed) {
        try {
          const response = await axios.delete(`${process.env.VUE_APP_BACKEND}/file/delete/${id}`);
          console.log(response.data);
          this.fetchEventDetails();
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
                confirmButton: "btn btn-success",
              },
              buttonsStyling: false,
            });
          } else {
            console.error(error);
          }
        }
      }
    },

    async closeReg(id) {
      const result = await Swal.fire({
        title: "Close registration?",
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: '<i class="fas fa-ban"></i> Yes',
        cancelButtonText: '<i class="fas fa-cancel"></i> Cancel',
        customClass: {
          popup: "card",
          title: "h5",
          confirmButton: "btn btn-danger me-3",
          cancelButton: "btn btn-secondary ms-3",
        },
        buttonsStyling: false,
      });
      if (result.isConfirmed) {
        try {
          const token = localStorage.getItem("token");
          const response = await axios.patch(
              `${process.env.VUE_APP_BACKEND}/update/event`,
              {
                id: id,
                key: 'registration_url',
                value: 'closed',
              },
              {
                headers: {
                  Authorization: `Bearer ${token}`,
                  "Content-Type": "application/json",
                },
              }
            );
          console.log(response.data);
          this.fetchEventDetails();
          Swal.fire({
            title: "Registration Closed",
            icon: "success",
            customClass: {
              popup: "card",
              title: "h4",
              content: "small",
              confirmButton: "btn btn-success",
            },
            buttonsStyling: false,
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
                confirmButton: "btn btn-success",
              },
              buttonsStyling: false,
            });
          } else {
            console.error(error);
          }
        }
      }
    },

    async updateEvent(id, key) {
      Swal.fire({
        title: `New ${key}`,
        input: key == "start_date" ? "date" : "text",
        inputAttributes: {
          autocapitalize: "off",
          class: "form-control",
        },
        showCancelButton: true,
        confirmButtonText: '<i class="fas fa-save"></i> Save',
        cancelButtonText: '<i class="fas fa-cancel"></i> Cancel',
        footer:
          key == "registration_url"
            ? '<a id="open-google-forms" class="text-primary" href="https://forms.google.com" target="_blank"><i class="fas fa-external-link-alt"></i> Create Google Form</a>'
            : "",
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
              `${process.env.VUE_APP_BACKEND}/update/event`,
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
          this.fetchEventDetails();
        }
      });
    },

    async updatePoster(id) {
      Swal.fire({
        title: `New Poster`,
        input: "file",
        inputAttributes: {
          autocapitalize: "off",
          accept: "image/*", // Hanya menerima file gambar
          class: "form-control",
        },
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

          const file = value;
          const formData = new FormData();
          formData.append("id", id);
          formData.append("poster", file);

          try {
            const token = localStorage.getItem("token");
            const response = await axios.patch(
              `${process.env.VUE_APP_BACKEND}/update/poster`,
              formData,
              {
                headers: {
                  Authorization: `Bearer ${token}`,
                  "Content-Type": "multipart/form-data",
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
        }
      });
    },

    async uploadImage(id) {
      Swal.fire({
        title: `New Image`,
        input: "file",
        inputAttributes: {
          autocapitalize: "off",
          accept: "image/*",
          class: "form-control",
        },
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

          const file = value;
          const formData = new FormData();
          formData.append("id", id);
          formData.append("image", file);

          try {
            const response = await axios.post(
              `${process.env.VUE_APP_BACKEND}/file/upload/${id}`,
              formData,
              {
                headers: {
                  "Content-Type": "multipart/form-data",
                },
              }
            );

            if (response.status !== 200) {
              Swal.showValidationMessage(`Gagal menyimpan: ${response.data.message || "Error"}`);
            }
            this.fetchEventDetails();
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
        }
      });
    },

    async report(user_id) {
      Swal.fire({
        title: `Report this comment?`,
        input: "text",
        icon: "warning",
        inputPlaceholder: "Tell us what's wrong with this comment",
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
                type: "user",
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
  },
  mounted() {
    this.fetchEventDetails();

    this.token = localStorage.getItem("token");
    if (this.token != "") {
      this.isLoggedIn = true;
      this.fetchUserProfile();
    }
  },
};
</script>

<style scoped>
.bg-pkm {
  background-image: url("../../../../public/assets/img/bg-pkm.jpg");
  background-color: rgba(0, 0, 0, 0.6);
  background-blend-mode: overlay;
  background-repeat: no-repeat;
  background-position: center;
  background-size: cover;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
}
.link-muted {
  color: #aaa;
}
.link-muted:hover {
  color: #1266f1;
}
.galery_image {
  height: 20rem;
  width: auto;
}
</style>
