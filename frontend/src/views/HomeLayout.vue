<template>
  <div class="home">
    <NavbarComponent class="sticky-top"/>
    <main>
      <slot></slot>
    </main>
    <FooterComponent />
  </div>
</template>

<script>
import FooterComponent from "@/components/public/FooterComponent.vue";
import NavbarComponent from "@/components/public/NavbarComponent.vue";

export default {
  name: "HomeLayout",
  components: {
    NavbarComponent,
    FooterComponent,
  },
  watch: {
    $route: "checkToken",
  },
  mounted() {
    document.title = "Pusat Event Politeknik";
    const urlParams = new URLSearchParams(window.location.search);
    const token = urlParams.get("token");
    if (token) {
      localStorage.setItem("token", token);
      this.$router.push("/home");
    }
  },
};
</script>
