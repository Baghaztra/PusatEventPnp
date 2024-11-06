<template>
  <div class="home">
    <PublicStyle />
    <NavbarComponent />
    <!-- ***** Main Banner Area Start ***** -->
    <div class="visit-country bg-white text-dark">
      <div class="container">
        <div class="row">
          <div class="col-lg-5">
            <div class="section-heading">
              <h2>Upcomming Events</h2>
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
                      <div class="col-lg-6 col-sm-5">
                        <div v-if="event.images && event.images.length > 0" class="image-container">
                          <img :src="event.images[0]" class="image-cover" alt="Event Image" />
                        </div>
                      </div>
                      <div class="col-lg-6 col-sm-7">
                        <div class="right-content">
                          <h4>{{ event.title }}</h4>
                          <span>{{ event.event_date }}</span>
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

                        <div class="position-absolute bottom-0 end-0">
                          <div class="main-button">
                            <a href="about.html">Explore More</a>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <!-- Page number -->
                <div class="col-lg-12">
                  <ul class="page-numbers">
                    <li>
                      <a @click="goToPage(currentPage - 1)" :disabled="currentPage === 1"
                        ><i class="fa fa-arrow-left"></i
                      ></a>
                    </li>
                    <li>
                      <span>Page {{ currentPage }} of {{ pages }}</span> pages
                    </li>
                    <li>
                      <a @click="goToPage(currentPage + 1)" :disabled="currentPage === pages"
                        ><i class="fa fa-arrow-right"></i
                      ></a>
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
    <PublicScripts />
  </div>
</template>

<script>
import FooterComponent from "@/components/public/FooterComponent.vue";
import NavbarComponent from "@/components/public/NavbarComponent.vue";
import PublicScripts from "@/components/public/PublicScripts.vue";
import PublicStyle from "@/components/public/PublicStyle.vue";
import axios from "axios";

export default {
  name: "HomeView",
  components: {
    NavbarComponent,
    FooterComponent,
    PublicStyle,
    PublicScripts,
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
  watch: {
    $route: "checkToken",
  },
  mounted() {
    document.title = "Pusat Event Politeknik";
    const urlParams = new URLSearchParams(window.location.search);
    const token = urlParams.get("token");
    if (token) {
      localStorage.setItem("token", token);
      this.$router.push("/home");
    }
  },
};
</script>

<style scoped>
.image-container {
  height: 15rem;
  width: 100%;
  overflow: hidden;
}
.image-cover {
  height: 100%;
  width: 100%;
  object-fit: cover;
}
</style>
