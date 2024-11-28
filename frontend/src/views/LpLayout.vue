<template>
  <div class="home" style=" height: 100vh;">
    <header class="masthead">
      <div class="blur">
        <div class="container d-flex h-100 align-items-center justify-content-center">
          <div class="d-flex justify-content-center">
            <slot></slot>
          </div>
        </div>
      </div>
    </header>
  </div>
</template>

<script>

export default {
  name: "LpLayout",
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
  background: url("../../public/assets/img/bg-pkm.jpg");
  background-position: center;
  background-repeat: no-repeat;
  background-attachment: scroll;
  background-size: cover;
}
.blur {
  backdrop-filter: blur(5px);
  background: linear-gradient(to bottom, rgba(0, 0, 0, 0.5) 0%, rgba(0, 0, 0, 0.7) 75%, #000 100%);
  height: 100%;
  width: 100%;
}
</style>
