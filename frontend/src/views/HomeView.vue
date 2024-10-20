<template>
  <div class="home">
    <NavbarComponent />
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
              <div class="main-caption">
                <h2>Take a Glimpse Into The Beautiful Country Of:</h2>
                <h1>Caribbean</h1>
                <div class="border-button">
                  <a href="about.html">Go There</a>
                </div>
              </div>
              <div class="container">
                <div class="row">
                  <div class="col-lg-12">
                    <div class="more-info">
                      <div class="row">
                        <div class="col-lg-3 col-sm-6 col-6">
                          <i class="fa fa-user"></i>
                          <h4><span>Population:</span><br />44.48 M</h4>
                        </div>
                        <div class="col-lg-3 col-sm-6 col-6">
                          <i class="fa fa-globe"></i>
                          <h4>
                            <span>Territory:</span><br />275.400 KM<em>2</em>
                          </h4>
                        </div>
                        <div class="col-lg-3 col-sm-6 col-6">
                          <i class="fa fa-home"></i>
                          <h4><span>AVG Price:</span><br />$946.000</h4>
                        </div>
                        <div class="col-lg-3 col-sm-6 col-6">
                          <div class="main-button">
                            <a href="about.html">Explore More</a>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
    <!-- ***** Main Banner Area End ***** -->
     <FooterComponent />
  </div>
</template>

<script>
import FooterComponent from "@/components/public/FooterComponent.vue";
import NavbarComponent from "@/components/public/NavbarComponent.vue";

export default {
  name: "HomeView",
  components: {
    NavbarComponent,
    FooterComponent,
  },
  methods: {
    
  },
  mounted() {
    
  },
};
</script>
