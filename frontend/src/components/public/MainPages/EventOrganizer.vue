<template>
  <HomeLayout>
    <div class="container">
      <div class="position-absolute top-0 start-0 mt-5 ms-5">
        <button @click="this.$router.go(-1)" class="btn btn-outline-danger">
          <i class="fas fa-arrow-left me-2"></i> Back
        </button>
      </div>
      <div class="container my-3">
        <div class="row">
          <div class="col-md-8">
            <h3 class="text-primary">{{ eodata.username }}</h3>
            <p>{{ eodata.bio }}</p>
          </div>
          <div class="col-md-4">
            <img src="" alt="" />
          </div>
        </div>
      </div>

      <!-- Gallery -->
      <h3>Events</h3>
      <div class="row">
        <CardComponent
          v-for="(event, index) in eodata.events"
          :key="index"
          :data="event"
          class="col-md-4 mb-3"
          @refresh-events="fetchEvents" />
      </div>

      <!-- Gallery -->
    </div>
  </HomeLayout>
</template>

<script>
import HomeLayout from "@/views/HomeLayout.vue";
import axios from "axios";
import CardComponent from "./CardComponent.vue";

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
      comment: "",
      profilePicture: "",
      userName: "",
      userId: "",
    };
  },
  watch: {
    id: "fetchEoData",
  },
  methods: {
    async fetchEoData() {
      this.loading = true;
      try {
        const response = await axios.get(`http://127.0.0.1:5000/event_organizers?id=${this.id}`);
        this.eodata = response.data;
      } catch (error) {
        console.error("Error fetching event-organizer details:", error);
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
  },
  mounted() {
    this.fetchEoData();

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
