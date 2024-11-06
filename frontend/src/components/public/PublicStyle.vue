<template>
  <div></div>
</template>

<script>
export default {
  name: "PublicStyle",
  mounted() {
    const styles = [
      "https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css",
      "https://unpkg.com/swiper@7/swiper-bundle.min.css",
      "https://fonts.googleapis.com/css?family=Varela+Round",
      "https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/united/bootstrap.min.css",
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
