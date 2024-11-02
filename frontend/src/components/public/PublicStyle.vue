<template>
  <div></div>
</template>

<script>
export default {
  name: "PublicStyle",
  mounted() {
    const styles = [
      "/vendor/bootstrap/css/bootstrap.min.css",
      "/assets/css/fontawesome.css",
      "/assets/css/templatemo-woox-travel.css",
      "/assets/css/owl.css",
      "/assets/css/animate.css",
      "https://unpkg.com/swiper@7/swiper-bundle.min.css",
    ];

    styles.forEach((href) => {
      const link = document.createElement("link");
      link.rel = "stylesheet";
      link.href = href;
      document.head.appendChild(link);
    });
  },
};
</script>
