<template>
  <div>
    <!-- Komponen template tetap kosong karena pemanggilan <script> dilakukan di JavaScript -->
  </div>
</template>

<script>
export default {
  name: "PublicScripts",
  mounted() {
    // Muat file JavaScript eksternal
    const scripts = [
      "/vendor/jquery/jquery.min.js",
      "/vendor/bootstrap/js/bootstrap.min.js",
      "/assets/js/isotope.min.js",
      "/assets/js/owl-carousel.js",
      "/assets/js/tabs.js",
      "/assets/js/popup.js",
    ];

    scripts.forEach((src) => {
      const script = document.createElement("script");
      script.src = src;
      script.async = true;
      document.body.appendChild(script);
    });
  },
};
</script>
