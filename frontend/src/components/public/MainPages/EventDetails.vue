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
                      class="rounded-circle shadow-1-strong me-3"
                      src="https://mdbcdn.b-cdn.net/img/Photos/Avatars/img%20(32).webp"
                      alt="avatar"
                      width="45"
                      height="45" />
                </div>
                <div class="card w-100">
                  <div class="card-body p-4">
                    <div class="form-floating">
                      <textarea
                        class="form-control"
                        placeholder="Leave a comment here"
                        id="new_comment"></textarea>
                      <label for="new_comment">Say something about this?</label>
                    </div>
                  </div>
                </div>
              </div>
              <!-- Add new -->

              <!-- Another comment -->
              <div class="d-flex flex-start mb-4" v-for="_ in 10" :key="_">
                <div class="pt-4">
                    <img
                      class="rounded-circle shadow-1-strong me-3"
                      src="https://mdbcdn.b-cdn.net/img/Photos/Avatars/img%20(32).webp"
                      alt="avatar"
                      width="45"
                      height="45" />
                </div>
                <div class="card w-100">
                  <div class="card-body p-4">
                    <h5>John Doe</h5>
                    <p class="small text-secondary  ">barusan banget</p>
                    <p>
                      Lorem ipsum dolor sit amet consectetur adipisicing elit. Delectus voluptates distinctio minima officiis modi ipsum sunt facilis asperiores totam! Aspernatur magnam reprehenderit molestias est laboriosam esse atque inventore deleniti dolorem?
                    </p>
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
      event: {},
      loading: false,
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

    formatDate(dateString) {
      const date = new Date(Date.parse(dateString));
      if (isNaN(date)) {
        console.error("Invalid date", dateString);
        return "";
      }
      const options = { weekday: "long", day: "2-digit", month: "long", year: "numeric" };
      return new Intl.DateTimeFormat("id-ID", options).format(date);
    },
  },
  mounted() {
    this.fetchEventDetails();
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
