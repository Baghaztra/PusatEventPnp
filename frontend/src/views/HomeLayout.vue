<template>
  <div class="home">
    <PublicStyle />
    <NavbarComponent />
    <main>
      <slot></slot>
    </main>
    <FooterComponent />
    <PublicScripts />
  </div>
</template>

<script>
import FooterComponent from "@/components/public/FooterComponent.vue";
import NavbarComponent from "@/components/public/NavbarComponent.vue";
import PublicScripts from "@/components/public/PublicScripts.vue";
import PublicStyle from "@/components/public/PublicStyle.vue";

export default {
  name: "HomeLayout",
  components: {
    NavbarComponent,
    FooterComponent,
    PublicStyle,
    PublicScripts,
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
