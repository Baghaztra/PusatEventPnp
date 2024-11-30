<template>
    <HomeLayout>
      <div class="container my-3">
        <h2 class="text-primary">Upcomming Events</h2>
        <div class="btn-group mb-3">
          <button type="button" class="btn btn-primary dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false">
            {{ filter }}
          </button>
          <ul class="dropdown-menu">
            <li><a class="dropdown-item" v-on:click="setFilter('All')">All</a></li>
            <li><a class="dropdown-item" v-on:click="setFilter('Comming soon')">Comming soon</a></li>
          </ul>
        </div>
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
      filter: 'All',
      loading: false,
    };
  },
  methods: {
    async fetchEvents() {
      this.loading = true;
      
      try {
        const response = await axios.get(
          `${process.env.VUE_APP_BACKEND}/event-latest?filter=${this.filter}`
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
    setFilter(filter){
      this.filter = filter;
      this.fetchEvents();
    }
  },
  created() {
    this.fetchEvents();
  },
};
</script>
