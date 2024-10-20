<template>
  <div class="home" style="height: 100vh">
    <!-- ***** Main Banner Area Start ***** -->
    <section id="section-1">
      <div class="content-slider">
        <input
          type="radio"
          id="banner1"
          class="sec-1-input"
          name="banner"
          checked
        />
        <div class="slider">
          <div id="top-banner-1" class="banner">
            <div class="banner-inner-wrapper header-text">
              <div class="d-flex align-item-center justify-content-center flex-column h-100">
                <h2>Explore any up comming event in State Polytechnic of Padang</h2>
                <h1>Pusat Event Politeknik</h1>
                <div class="d-flex justify-content-center flex-column">
                    <div class="main-button d-flex justify-content-center mb-3">
                      <router-link to="/home">Login!</router-link>
                    </div>
                    <router-link class="text-button" to="/register">dont have any account?</router-link>
                    <span>
                        or <router-link class="text-button" to="/home">enter without login</router-link>
                    </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
    <!-- ***** Main Banner Area End ***** -->
  </div>
</template>

<script>
export default {
  name: "LandingPage",
  components: {},
  methods: {},
  mounted() {
    document.title = 'Pusat Event Politeknik';
  },
};
</script>

<style>
#section-1 .content-slider .slider #top-banner-1 {
  position: relative;
  background: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.75)),
    url("../../public/assets/images/MG_7004-copy-02.jpg") no-repeat center center;
  background-size: cover;
  height: 100vh;
  overflow: hidden;
}

#section-1 .content-slider .slider #top-banner-1::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: inherit;
  filter: blur(5px);
  z-index: -1;
}

#section-1 {
  height: 100vh;
}
</style>
