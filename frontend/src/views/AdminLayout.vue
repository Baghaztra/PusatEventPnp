<template>
  <AdminStyle />
  <div class="row">
    <div class="col" style="max-width: 280px">
      <NavbarComponent />
    </div>
    <div class="col">
      <HeaderComponent />
      <main>
        <slot></slot>
      </main>
      <FooterComponent />
    </div>
  </div>
  <AdminScripts />
</template>

<script>
import AdminScripts from "@/components/admin/AdminScripts.vue";
import AdminStyle from "@/components/admin/AdminStyle.vue";
import FooterComponent from "@/components/admin/FooterComponent.vue";
import HeaderComponent from "@/components/admin/HeaderComponent.vue";
import NavbarComponent from "@/components/admin/NavbarComponent.vue";

export default {
  name: "AdminDashboard",
  components: {
    HeaderComponent,
    NavbarComponent,
    FooterComponent,
    AdminStyle,
    AdminScripts,
  },
  mounted() {
    document.title = "Admin Pusat Event";
  },
};
</script>

<style></style>
