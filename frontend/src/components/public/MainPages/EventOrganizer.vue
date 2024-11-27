<template>
  <HomeLayout>
    <div class="container">
      <div class="position-absolute top-0 start-0 mt-5 ms-5">
        <button @click="this.$router.go(-1)" class="btn btn-outline-danger">
          <i class="fas fa-arrow-left me-2"></i> Back
        </button>
      </div>
      <div class="container my-3 mt-5">
        <div class="card p-3">
          <div class="d-flex">
            <div class="image">
              <img :src="eodata.profile_picture" class="rounded" width="155" />
            </div>

            <div class="ml-3 w-100">
              <div class="d-flex align-items-center">
                <h4 class="mb-0 mt-0 d-inline me-3">{{ eodata.username }}</h4>
                <button v-if="!isOwner" class="btn btn-sm btn-primary d-inline" v-on:click="toggleFollow">Follow</button>
                <button v-else-if="isFollowing" class="btn btn-sm btn-outline-primary d-inline" v-on:click="toggleFollow">Unfollow</button>
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
              <div class=" mt-2 row">
                <p>
                  {{ eodata.bio }}
                </p>
              </div>
            </div>
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
import CardComponent from "./CardComponent.vue";
import axios from "axios";
import Swal from "sweetalert2";

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
      isOwner: false
    };
  },
  watch: {
    id: "fetchEoData",
  },
  methods: {
    async fetchEoData() {
      this.loading = true;
      try {
        const response = await axios.get(`${process.env.VUE_APP_BACKEND}/event_organizers?id=${this.id}`);
        this.eodata = response.data;
        
        this.isFollowing = this.eodata.subs.includes(this.userId); 
      } catch (error) {
        console.error("Error fetching event-organizer details:", error);
      } finally {
        this.loading = false;
        if(this.role == 'event organizer' && this.userId == this.eodata.id){
          this.isOwner = true;
        }
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
