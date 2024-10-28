<template>
  <div class="home">
    <NavbarComponent />
    <!-- ***** Main Banner Area Start ***** -->
    <div class="visit-country bg-white text-dark">
      <div class="container">
        <div class="row">
          <div class="col-lg-5">
            <div class="section-heading">
              <h2>Visit One Of Our Countries Now</h2>
              <p>
                Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
                eiusmod tempor incididunt ut labore.
              </p>
            </div>
          </div>
        </div>
        <div class="row">
          <div class="col-lg-12">
            <div class="items">
              <div v-if="loading" class="row">Loading...</div>
              <div v-else class="row">
                <!-- Content -->
                <div v-for="event in events" :key="event.id" class="col-lg-12">
                  <div class="item">
                    <div class="row">
                      <div class="col-lg-4 col-sm-5">
                        <div v-if="event.images && event.images.length > 0">
                          <img :src="event.images[0]" alt="Event Image" />
                        </div>
                      </div>
                      <div class="col-lg-8 col-sm-7">
                        <div class="right-content">
                          <h4>{{ event.title }}</h4>
                          <span>{{ event.event_date }}</span>
                          <div class="main-button">
                            <a href="about.html">Explore More</a>
                          </div>
                          <div>
                            {{ event.description }}
                          </div>
                          <!-- <ul class="info">
                            <li><i class="fa fa-user"></i> 8.66 Mil People</li>
                            <li><i class="fa fa-globe"></i> 41.290 km2</li>
                            <li><i class="fa fa-home"></i> $1.100.200</li>
                          </ul>
                          <div class="text-button">
                            <a href="about.html"
                              >Need Directions ?
                              <i class="fa fa-arrow-right"></i
                            ></a>
                          </div> -->
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <!-- Page number -->
                <div class="col-lg-12">
                  <ul class="page-numbers">
                    <li>
                      <a @click="goToPage(currentPage - 1)" :disabled="currentPage === 1"><i class="fa fa-arrow-left"></i></a>
                    </li>
                    <li><span>Page {{ currentPage }} of {{ pages }}</span> pages</li>
                    <li>
                      <a @click="goToPage(currentPage + 1)" :disabled="currentPage === pages"><i class="fa fa-arrow-right"></i></a>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <!-- ***** Main Banner Area End ***** -->
    <FooterComponent />
  </div>
</template>

<script>
import FooterComponent from "@/components/public/FooterComponent.vue";
import NavbarComponent from "@/components/public/NavbarComponent.vue";
import axios from "axios";

export default {
  name: "HomeView",
  components: {
    NavbarComponent,
    FooterComponent,
  },
  data() {
    return {
      events: [],
      total: 0,
      pages: 0,
      currentPage: 1,
      perPage: 5,
      loading: false,
    };
  },
  methods: {
    async fetchEvents(page = 1) {
      this.loading = true;
      try {
        const response = await axios.get(
          `http://127.0.0.1:5000/event-latest?page=${page}&per_page=${this.perPage}`
        );
        this.events = response.data.events;
        this.total = response.data.total;
        this.pages = response.data.pages;
        this.currentPage = response.data.current_page;
      } catch (error) {
        console.error(error);
      } finally {
        this.loading = false;
      }
    },
    goToPage(page) {
      if (page > 0 && page <= this.pages) {
        this.fetchEvents(page);
      }
    },
  },
  created() {
    this.fetchEvents();
  },
  mounted() {},
};
</script>
