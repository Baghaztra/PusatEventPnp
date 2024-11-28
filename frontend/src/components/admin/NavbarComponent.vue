<template>
  <nav id="sidebarMenu" style="height: 82vh; z-index: 1;" class="position-fixed bg-white col-md-3 col-lg-2 d-md-block sidebar collapse">
    <div class="position-sticky pt-3 sidebar-sticky">
      <ul class="nav flex-column">
        <li class="nav-item mb-3" v-for="item in navItems" :key="item">
          <router-link class="nav-link" :class="{ 'bg-primary rounded text-light': $route.path == item.link }" :to="item.link">
            <i :class="item.icon"></i> {{ item.text }}
          </router-link>
        </li>
      </ul>
    </div>
  </nav>
</template>

<script>
export default {
  name: "NavbarAdmin",
  data() {
    return {
      navItems: [
        { text: "Dashboard", icon: "fas fa-dashboard", link: "/admin" },
        { text: "Events", icon: "fas fa-calendar", link: "/admin/events" },
        { text: "Event organizers", icon: "fas fa-users", link: "/admin/eo" },
        { text: "Accounts", icon: "fas fa-user", link: "/admin/accounts" },
      ],
      isSidebarVisible: false,
      isMobile: false,
    };
  },
  methods: {
    isActive(link) {
      return this.$route.path === link;
    },
    toggleSidebar() {
      this.isSidebarVisible = !this.isSidebarVisible;
    },
    handleResize() {
      this.isMobile = window.innerWidth < 768;
      if (!this.isMobile) {
        this.isSidebarVisible = true;
      }
    },
  },

  mounted() {
    this.handleResize();
    window.addEventListener("resize", this.handleResize);
  },
  unmounted() {
    window.removeEventListener("resize", this.handleResize);
  },
};
</script>

<style scoped>
.sidebar-fixed {
  position: fixed;
  top: 0;
  left: 0;
  height: 100vh;
  width: 280px;
  overflow-y: auto;
  transition: transform 0.3s ease;
  z-index: 1000;
}

.sidebar-hidden {
  transform: translateX(-100%);
}

@media (min-width: 768px) {
  .sidebar-hidden {
    transform: translateX(0);
  }
}
</style>
