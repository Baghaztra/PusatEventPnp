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
      "https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js",
      "https://cdn.startbootstrap.com/sb-forms-latest.js",
      "https://cdn.jsdelivr.net/npm/mdb-ui-kit/js/mdb.min.js",
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
