<template>
  <div>
    <div class="card p-2">
      <button
        class="btn btn-danger me-1 mt-1 position-absolute top-0 end-0"
        v-if="userRole == 'event organizer' && userId == data.eo_id"
        v-on:click="deleteEvent">
        <i class="fas fa-trash-can"></i>
      </button>
      <button
        class="btn btn-outline-danger btn-sm me-1 mt-1 position-absolute top-0 end-0"
        v-else-if="userRole && userRole != 'event organizer'"
        v-on:click="report(data.id)">
        <i class="fas fa-flag"></i>
      </button>
      <img
        :src="data.poster"
        alt="Event Image"
        class="rounded"
        style="width: 100%; aspect-ratio: 3 / 4" />
      <div class="col-body d-flex flex-column">
        <h5 class="text-primary" style="font-weight: bold">{{ data.title }}</h5>
        <span class="text-secondary">
          By <router-link :to="`/organizer/${data.eo_id}`">{{ data.eo }}</router-link>
        </span>
        <span class="text-primary">{{ formatDate(data.event_date) }}</span>
        <div class="mb-1">
          <a
            v-if="data.registration_url && data.registration_url == 'closed'"
            class="btn btn-primary me-1 disabled"
            disabled>
            Registration Closed
          </a>
          <a
            class="btn btn-primary me-1"
            v-else-if="data.registration_url"
            :href="data.registration_url"
            target="_blank"
            >Register</a
          >
          <button
            class="btn btn-warning me-1"
            v-else-if="userRole == 'event organizer' && userId == data.eo_id"
            v-on:click="linkPendaftaran(data.id)">
            Add a registration
          </button>
          <router-link class="btn btn-primary me-1" :to="`/event/${data.id}`">More</router-link>
          <button class="btn" :class="{ 'text-primary': isLiked }" @click="toggleLike">
            <span class="me-1">{{ data.likes?.length ?? 0 }}</span>
            <i :class="isLiked ? 'fas fa-thumbs-up' : 'far fa-thumbs-up'"></i>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Swal from "sweetalert2";

export default {
  name: "CardComponent",
  props: {
    data: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      isLiked: false,
      userId: null,
      userRole: null,
    };
  },
  methods: {
    async deleteEvent() {
      try {
        const result = await Swal.fire({
          title: "Are you sure?",
          text: "This post will gone forever",
          icon: "warning",
          showCancelButton: true,
          confirmButtonText: "Yes, Delete it",
          cancelButtonText: "Cancel",
          customClass: {
            confirmButton: "btn btn-danger me-3",
            cancelButton: "btn btn-success ms-3",
          },
          buttonsStyling: false,
        });
        if (result.isConfirmed) {
          const response = await axios.delete(
            `${process.env.VUE_APP_BACKEND}/delete/event?id=${this.data.id}`,
            {
              headers: {
                Authorization: `Bearer ${localStorage.getItem("token")}`,
              },
            }
          );
          console.log(response);
          if (response.status == 200) {
            Swal.fire({
              title: "Deleted",
              text: response.data.message,
              icon: "success",
            });
            this.$emit("refresh-events");
          } else {
            Swal.fire({
              title: "Failed",
              text: response.data.message,
              icon: "error",
            });
          }
        }
      } catch (error) {
        console.log("error", error);

        Swal.fire({
          title: "Error!",
          text: error,
          icon: "error",
          customClass: {
            popup: "alert alert-danger",
            title: "h4",
            content: "small",
            confirmButton: "btn btn-sm btn-success",
          },
          buttonsStyling: false,
        });
      }
    },
    async toggleLike() {
      if (this.userRole && this.userRole == "event organizer") {
        Swal.fire({
          title: "Sorry :(",
          icon: "warning",
          text: "Event organizer cannot give a like or comment",
          // icon: "error",
        });
      } else {
        try {
          // const response = await axios.post(
          await axios.post(
            `${process.env.VUE_APP_BACKEND}/like/${this.data.id}`,
            {}, // Body kosong
            {
              headers: {
                Authorization: `Bearer ${localStorage.getItem("token")}`,
              },
            }
          );
          // console.log(response.data.msg);
          this.isLiked = !this.isLiked;
          // console.log(this.isLiked);
          this.$emit("refresh-events");
          // this.isLiked = response.data.liked;
        } catch (error) {
          console.error("Error saat mengirim permintaan like:", error);
          Swal.fire({
            title: "Login",
            text: "Login to interact with this event",
            // icon: "error",
            showCancelButton: false,
            confirmButtonText: "Login",
          }).then((result) => {
            if (result.isConfirmed) {
              window.location.href = "/login";
            }
          });
        }
      }
    },
    formatDate(dateString) {
      if (!dateString) return "Tanggal tidak tersedia"; // Validasi
      const options = { weekday: "long", day: "2-digit", month: "long", year: "numeric" };
      try {
        return new Intl.DateTimeFormat("id-ID", options).format(new Date(dateString));
      } catch {
        return "Format tanggal tidak valid";
      }
    },
    truncateText(text, maxLength) {
      if (text.length > maxLength) {
        return text.slice(0, maxLength) + "...";
      }
      return text;
    },
    async linkPendaftaran(event_id) {
      Swal.fire({
        title: "Paste your registration form here",
        input: "text",
        inputPlaceholder: "https://forms.gle/XXXXX",
        inputAttributes: {
          autocapitalize: "off",
          class: "form-control",
        },
        showCancelButton: true,
        confirmButtonText: '<i class="fas fa-save"></i> Save',
        cancelButtonText: '<i class="fas fa-cancel"></i> Cancel',
        footer:
          '<a id="open-google-forms" class="text-primary" href="https://forms.google.com" target="_blank"><i class="fas fa-external-link-alt"></i> Create Google Form</a>',
        customClass: {
          title: "fs-5 text-primary",
          confirmButton: "btn btn-primary",
          cancelButton: "btn btn-secondary",
        },
        showLoaderOnConfirm: true,
        preConfirm: async (link) => {
          if (!link) {
            Swal.showValidationMessage("Url can't be empty");
            return;
          }

          try {
            const token = localStorage.getItem("token");
            const response = await axios.patch(
              `${process.env.VUE_APP_BACKEND}/update/event`,
              {
                id: event_id,
                key: "registration_url",
                value: link,
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
          this.$emit("refresh-events");
        }
      });
    },
    async report(event_id) {
      Swal.fire({
        title: `Report event "${this.data.title}"`,
        input: "text",
        icon: "warning",
        inputPlaceholder: "Tell us what's wrong with this content",
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
                id: event_id,
                type: "event",
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
  async created() {
    try {
      const token = localStorage.getItem("token");
      if (!token) {
        console.error("Token tidak ditemukan. User belum login.");
        return;
      }

      const response = await axios.get(`${process.env.VUE_APP_BACKEND}/profile`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      this.userId = response.data.user_id;
      this.userRole = response.data.role;

      this.isLiked = this.data.likes.includes(this.userId);
    } catch (error) {
      console.error("Error saat mendapatkan profil:", error.message);
    }
  },
  mounted() {
    this.isLiked = !!this.data.isLiked;
  },
};
</script>

<style></style>
