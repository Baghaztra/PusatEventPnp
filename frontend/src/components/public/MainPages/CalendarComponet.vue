<template>
  <HomeLayout>
    <div class="container my-3">
      <h2 class="text-primary">Upcomming Events</h2>
      <div class="btn-group mb-3">
        <button
          type="button"
          class="btn btn-primary dropdown-toggle"
          data-bs-toggle="dropdown"
          aria-expanded="false">
          {{ filter }}
        </button>
        <ul class="dropdown-menu">
          <li><a class="dropdown-item" v-on:click="setFilter('All')">All</a></li>
          <li><a class="dropdown-item" v-on:click="setFilter('Comming soon')">Comming soon</a></li>
        </ul>
      </div>
      <div class="container col-lg-9 mt-3">
        <div class="card w-100">
          <div class="card-body p-3">
            <FullCalendar :options="calendarOptions" style="height: 100%;"/>
          </div>
        </div>
      </div>
    </div>
  </HomeLayout>
</template>

<script>
import HomeLayout from "@/views/HomeLayout.vue";
import axios from "axios";

import FullCalendar from "@fullcalendar/vue3";
import dayGridPlugin from "@fullcalendar/daygrid";
import interactionPlugin from "@fullcalendar/interaction";

export default {
  name: "HomeView",
  components: {
    HomeLayout,
    FullCalendar,
  },
  data() {
    return {
      filter: "All",
      loading: false,
      calendarOptions: {
        plugins: [dayGridPlugin, interactionPlugin],
        initialView: "dayGridMonth",
        events: [],
        height: 'auto',
        contentHeight: 'auto',
        eventContent: function(info) {
          return {
            html: `<div class="badge text-bg-primary text-wrap">${info.event.title}</div>`
          };
        },
        headerToolbar: {
          right: 'today prev,next',
          left: 'title',
        },
      }
    };
  },
  methods: {
    async fetchEvents() {
      this.loading = true;

      try {
        const response = await axios.get(
          `${process.env.VUE_APP_BACKEND}/event-latest?filter=${this.filter}`
        );
        this.calendarOptions.events = response.data.map((event) => ({
          id: event.id,
          title: event.title,
          start: new Date(new Date(event.event_date)).toISOString(),
          url: `/event/${event.id}`,
        }));

        console.log("Event:", this.calendarOptions.events);
      } catch (error) {
        console.error(error);
      } finally {
        this.loading = false;
      }
    },
    setFilter(filter) {
      this.filter = filter;
      this.fetchEvents();
    },
  },
  watch: {
    events: {
      handler() {
        this.calendarOptions.events = [...this.events];
      },
      deep: true,
    },
  },
  created() {
    this.fetchEvents();
  },
};
</script>

<style>
.fc a {
  color: inherit;
  text-decoration: none;
}

.fc-button-primary {
  background-color: #e95420 !important;
  border-color: #e95420 !important;
  color: #fff;
}

.fc-button-primary:hover {
  background-color: #d14c1b !important;
  border-color: #d14c1b !important;
}

.fc-button-primary:active {
  background-color: #b34314 !important;
  border-color: #b34314 !important;
}

.fc-button-primary:focus {
  box-shadow: 0 0 5px rgba(233, 84, 32, 0.8) !important;
}

.fc-toolbar-chunk {
  display: flex;
  justify-content: flex-end;
}
</style>
