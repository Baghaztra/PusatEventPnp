<template>
  <HeaderComponent />
  <div class="container-fluid">
    <div class="row">
      <NavbarComponent />
      <main class="col-md-9 ms-sm-auto col-lg-10 px-md-4">
        <div style="overflow-x: scroll;">
          <slot></slot>
        </div>
      </main>
      <FooterComponent class="col-md-9 ms-sm-auto col-lg-10 px-md-4" />
    </div>
  </div>
</template>

<script>
import FooterComponent from "@/components/admin/FooterComponent.vue";
import HeaderComponent from "@/components/admin/HeaderComponent.vue";
import NavbarComponent from "@/components/admin/NavbarComponent.vue";

export default {
  name: "AdminDashboard",
  components: {
    HeaderComponent,
    NavbarComponent,
    FooterComponent,
  },
  mounted() {
    document.title = "Admin Pusat Event";
  },
};
</script>

<style></style>
