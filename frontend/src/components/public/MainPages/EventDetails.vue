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
      <div
        id="carouselExampleControls"
        class="carousel slide"
        data-mdb-ride="carousel"
        data-mdb-carousel-init>
        <div class="carousel-inner">
          <div class="carousel-item active">
            <img
              src="https://mdbcdn.b-cdn.net/img/new/slides/041.webp"
              class="d-block w-100"
              alt="Wild Landscape" />
          </div>
          <div class="carousel-item">
            <img
              src="https://mdbcdn.b-cdn.net/img/new/slides/042.webp"
              class="d-block w-100"
              alt="Camera" />
          </div>
          <div class="carousel-item">
            <img
              src="https://mdbcdn.b-cdn.net/img/new/slides/043.webp"
              class="d-block w-100"
              alt="Exotic Fruits" />
          </div>
        </div>
        <button
          class="carousel-control-prev"
          type="button"
          data-mdb-target="#carouselExampleControls"
          data-mdb-slide="prev">
          <span class="carousel-control-prev-icon" aria-hidden="true"></span>
          <span class="visually-hidden">Previous</span>
        </button>
        <button
          class="carousel-control-next"
          type="button"
          data-mdb-target="#carouselExampleControls"
          data-mdb-slide="next">
          <span class="carousel-control-next-icon" aria-hidden="true"></span>
          <span class="visually-hidden">Next</span>
        </button>
      </div>
      <!-- Gallery -->

      <!-- Forum -->
      <h1>Forum</h1>
      <section style="background-color: #e7effd">
        <div class="container my-5 py-5 text-body">
          <div class="row d-flex justify-content-center">
            <div class="col-md-11 col-lg-9 col-xl-7">
              <div class="d-flex flex-start mb-4">
                <img
                  class="rounded-circle shadow-1-strong me-3"
                  src="https://mdbcdn.b-cdn.net/img/Photos/Avatars/img%20(32).webp"
                  alt="avatar"
                  width="65"
                  height="65" />
                <div class="card w-100">
                  <div class="card-body p-4">
                    <div class="">
                      <h5>Johny Cash</h5>
                      <p class="small">3 hours ago</p>
                      <p>
                        Cras sit amet nibh libero, in gravida nulla. Nulla vel metus scelerisque
                        ante sollicitudin. Cras purus odio, vestibulum in vulputate at, tempus
                        viverra turpis. Fusce condimentum nunc ac nisi vulputate fringilla. Donec
                        lacinia congue felis in faucibus ras purus odio, vestibulum in vulputate at,
                        tempus viverra turpis.
                      </p>

                      <div class="d-flex justify-content-between align-items-center">
                        <div class="d-flex align-items-center">
                          <a href="#!" class="link-muted me-2"
                            ><i class="fas fa-thumbs-up me-1"></i>132</a
                          >
                          <a href="#!" class="link-muted"
                            ><i class="fas fa-thumbs-down me-1"></i>15</a
                          >
                        </div>
                        <a href="#!" class="link-muted"><i class="fas fa-reply me-1"></i> Reply</a>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div class="d-flex flex-start">
                <img
                  class="rounded-circle shadow-1-strong me-3"
                  src="https://mdbcdn.b-cdn.net/img/Photos/Avatars/img%20(31).webp"
                  alt="avatar"
                  width="65"
                  height="65" />
                <div class="card w-100">
                  <div class="card-body p-4">
                    <div class="">
                      <h5>Mindy Campbell</h5>
                      <p class="small">5 hours ago</p>
                      <p>
                        Lorem ipsum dolor sit, amet consectetur adipisicing elit. Delectus cumque
                        doloribus dolorum dolor repellat nemo animi at iure autem fuga cupiditate
                        architecto ut quam provident neque, inventore nisi eos quas?
                      </p>

                      <div class="d-flex justify-content-between align-items-center">
                        <div class="d-flex align-items-center">
                          <a href="#!" class="link-muted me-2"
                            ><i class="fas fa-thumbs-up me-1"></i>158</a
                          >
                          <a href="#!" class="link-muted"
                            ><i class="fas fa-thumbs-down me-1"></i>13</a
                          >
                        </div>
                        <a href="#!" class="link-muted"><i class="fas fa-reply me-1"></i> Reply</a>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
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
</style>
