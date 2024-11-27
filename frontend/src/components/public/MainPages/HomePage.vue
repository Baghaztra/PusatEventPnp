<template>
    <HomeLayout>
      <div class="container my-3">
        <h2 class="text-primary">Upcomming Events</h2>
        <div class="row">
          <CardComponent 
            v-for="(event, index) in events" 
            :key="index" 
            :data="event"
            class="col-md-4 mb-3" 
            @refresh-events="fetchEvents"
          />
        </div>
      </div>
    </HomeLayout>
</template>

<script>
import HomeLayout from "@/views/HomeLayout.vue";
import CardComponent from "./CardComponent.vue";
import axios from "axios";

export default {
  name: "HomeView",
  components: {
    HomeLayout,
    CardComponent
  },
  data() {
    return {
      events: [],
      loading: false,
    };
  },
  methods: {
    async fetchEvents() {
      this.loading = true;
      console.log("isi env",process.env.VUE_APP_BACKEND);
      
      try {
        const response = await axios.get(
          `${process.env.VUE_APP_BACKEND}/event-latest`
        );
        this.events = response.data;
      } catch (error) {
        console.error(error);
      } finally {
        this.loading = false;
      }
    },
    checkToken() {
      const urlParams = new URLSearchParams(window.location.search);
      const token = urlParams.get("token");
      if (token) {
        localStorage.setItem("token", token);
        this.$router.push("/home");
      } else {
        window.location.reload();
      }
    },
  },
  created() {
    this.fetchEvents();
  },
};
</script>
