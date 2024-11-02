<template>
  <div></div>
</template>

<script>
export default {
  name: "AdminStyle",
  mounted() {
    const styles = [
      "https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/cosmo/bootstrap.min.css",
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
