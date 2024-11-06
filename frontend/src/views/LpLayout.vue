<template>
  <PublicStyle />
  <div class="home" style="height: 100vh">
    <header class="masthead">
      <div class="container px-4 px-lg-5 d-flex h-100 align-items-center justify-content-center">
        <div class="d-flex justify-content-center">
          <slot></slot>
        </div>
      </div>
    </header>
    <PublicScripts />
  </div>
</template>

<script>
import PublicScripts from "@/components/public/PublicScripts.vue";
import PublicStyle from "@/components/public/PublicStyle.vue";

export default {
  name: "LpLayout",
  components: {
    PublicStyle,
    PublicScripts,
  },
  methods: {},
  mounted() {
    document.title = "Pusat Event Politeknik";
  },
};
</script>

<style>
.masthead {
  position: relative;
  width: 100%;
  height: 100%;
  background: linear-gradient(to bottom, rgba(0, 0, 0, 0.3) 0%, rgba(0, 0, 0, 0.7) 75%, #000 100%), url("../../public/assets/img/bg-pkm.jpg");
  background-position: center;
  background-repeat: no-repeat;
  background-attachment: scroll;
  background-size: cover;
}
</style>
