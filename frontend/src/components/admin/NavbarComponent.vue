<template>
  <div>
    <!-- Tombol Toggle Sidebar (hanya muncul di layar kecil) -->
    <button
      class="btn btn-primary d-md-none mb-3"
      @click="toggleSidebar"
      style="position: fixed; top: 10px; left: 10px; z-index: 1050">
      <i class="fas fa-bars"></i>
    </button>

    <!-- Sidebar -->
    <div
      class="d-flex flex-column flex-shrink-0 p-3 bg-body-tertiary sidebar-fixed"
      :class="{ 'sidebar-hidden': !isSidebarVisible && isMobile }">
      <a
        href="/admin"
        class="d-flex align-items-center mb-3 mb-md-0 me-md-auto link-body-emphasis text-decoration-none">
        <!-- <i class="fas fa-bars me-2"></i> -->
        <span class="fs-4">Hi!</span>
      </a>
      <hr />
      <ul class="nav nav-pills flex-column mb-auto">
        <li class="nav-item" v-for="item in navItems" :key="item.text">
          <router-link
            :to="item.link"
            class="nav-link"
            :class="{ 'text-white': isActive(item.link), 'text-primary': !isActive(item.link), active: isActive(item.link) }">
            <i :class="item.icon + ' me-2'"></i>
            {{ item.text }}
          </router-link>
        </li>
      </ul>
      <hr />
      <div class="dropdown">
        <a
          href="#"
          class="d-flex align-items-center link-body-emphasis text-decoration-none dropdown-toggle"
          data-bs-toggle="dropdown"
          aria-expanded="false">
          <img
            src="https://github.com/mdo.png"
            alt=""
            width="32"
            height="32"
            class="rounded-circle me-2" />
          <strong>mdo</strong>
        </a>
        <ul class="dropdown-menu text-small shadow">
          <li><a class="dropdown-item" href="#">Sign out</a></li>
        </ul>
      </div>
    </div>
  </div>
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
