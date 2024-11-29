<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script>
  export default{
    mounted() {
      document.title = "Pusat Event Politeknik";
    },
  }
</script>
