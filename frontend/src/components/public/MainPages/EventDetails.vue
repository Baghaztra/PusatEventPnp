<template>
  <HomeLayout>
    <div class="container">
      <!-- Hero -->
      <div
        class="bg-image"
        style="
          background-image: url('https://mdbcdn.b-cdn.net/img/new/slides/041.webp');
          background-repeat: no-repeat;
          background-position: center;
          background-size: cover;
          height: 100vh;
          display: flex;
          align-items: center;
          justify-content: center;
        ">
        <div class="mask rounded p-5" style="background-color: rgba(0, 0, 0, 0.6)">
          <div class="position-absolute top-0 start-0 mt-5 ms-5">
            <button @click="this.$router.go(-1)" class="btn btn-outline-danger">
              <i class="fas fa-arrow-left me-2"></i> Back
            </button>
          </div>
          <div class="d-flex justify-content-center align-items-center h-100">
            <div class="text-white text-center">
              <h1 class="mb-3">{{ event.title }}</h1>
              <h4 class="mb-3">{{ formatDate(event.event_date) }}</h4>
              <a class="btn btn-outline-primary btn-lg" href="">Register!</a>
            </div>
          </div>
        </div>
      </div>
      <!-- Hero -->
      <div class="container my-3">
        <div class="row">
          <div class="col-md-8">
            <h3 class="text-primary">{{ event.title }}</h3>
            <p>{{ event.description }}</p>
          </div>
          <div class="col-md-4">
            <img src="" alt="" />
          </div>
        </div>
      </div>

      <!-- Gallery -->
      <h3>Gallery</h3>
      <div class="row">
        <div class="col">
          <div class="d-flex overflow-auto">
            <div
              v-for="(image, index) in event.images"
              :key="index"
              class="p-2 image-container"
              style="flex: 0 0 auto">
              <img :src="image" alt="gambar" class="img-fluid rounded" />
            </div>
          </div>
        </div>
      </div>

      <!-- Gallery -->

      <!-- Forum -->
      <h3>Forum <i class="fa fa-thumbs-up"></i></h3>
      <!-- Comentar -->
      <section>
        <div class="container mb-5 text-body">
          <div class="row d-flex justify-content-center">
            <div class="col-md-11">
              <!-- Add new -->
              <div class="d-flex flex-start mb-4">
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
              <div class="d-flex flex-start mb-4" v-for="comment in event.comments" :key="comment">
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
    };
  },
  watch: {
    id: "fetchEventDetails",
  },
  methods: {
    async fetchEventDetails() {
      this.loading = true;
      try {
        const response = await axios.get(`http://127.0.0.1:5000/event/${this.id}`);
        this.event = response.data;
      } catch (error) {
        console.error("Error fetching event details:", error);
      } finally {
        this.loading = false;
      }
    },

    async fetchUserProfile() {
      try {
        const response = await axios.get("http://127.0.0.1:5000/profile", {
          headers: {
            Authorization: `Bearer ${this.token}`,
          },
        });

        const data = response.data;
        this.profilePicture = data.profile_picture;
        this.userName = data.username;
        this.userId = data.user_id;
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

          const response = await axios.post("http://127.0.0.1:5000/comment", payload, {
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
          confirmButton: "btn btn-sm btn-danger me-3",
          cancelButton: "btn btn-sm btn-secondary ms-3",
        },
        buttonsStyling: false,
      });
      if (result.isConfirmed) {
        try {
          const response = await axios.delete("http://127.0.0.1:5000/comment", {
            data: { comment_id: id },
          });
          console.log(response.data);
          this.fetchEventDetails();
          Swal.fire({
            title: "Comment deleted!",
            text: "The comment has been successfully deleted.",
            icon: "success",
            customClass: {
              popup: "card",
              title: "h4",
              content: "small",
              confirmButton: "btn btn-sm btn-success",
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
                confirmButton: "btn btn-sm btn-success",
              },
              buttonsStyling: false,
            });
          } else {
            console.error(error);
          }
        }
      }
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
.link-muted {
  color: #aaa;
}
.link-muted:hover {
  color: #1266f1;
}
.image-container {
  height: 400px;
  width: auto;
}
</style>
