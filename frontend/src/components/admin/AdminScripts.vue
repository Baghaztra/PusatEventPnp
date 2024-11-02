<template>
  <div>
    <!-- Komponen template tetap kosong karena pemanggilan <script> dilakukan di JavaScript -->
  </div>
</template>

<script>
export default {
  name: "AdminScripts",
  mounted() {
    // Muat file JavaScript eksternal
    const scripts = [];

    scripts.forEach((src) => {
      const script = document.createElement("script");
      script.src = src;
      script.async = true;
      document.body.appendChild(script);
    });
  },
};
</script>
