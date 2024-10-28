<template>
  <div>
    <header class="header-area header-sticky">
      <div class="container">
        <div class="row">
          <div class="col-12">
            <nav class="main-nav d-flex">
              <!-- ***** Logo Start ***** -->
              <a href="">
                <img src="@/assets/logo.png" alt="" style="height: 4rem; width: auto;"/>
              </a>
              <!-- ***** Logo End ***** -->
              <!-- ***** Menu Start ***** -->
              <ul class="nav">
                <li><router-link to="/home" exact-active-class="active" exact>Home</router-link></li>
                <li><router-link to="/about" exact-active-class="active" exact>About</router-link></li>
                <li><router-link to="/otrher" exact-active-class="active" exact>Apa kek</router-link></li>
                <li><router-link to="/otrher" exact-active-class="active" exact>Yang lain</router-link></li>
              </ul>
              <a class="menu-trigger">
                <span>Menu</span>
              </a>
              <!-- ***** Menu End ***** -->
            </nav>
          </div>
        </div>
      </div>
    </header>
  </div>
</template>

<script>
export default {
  name: "NavbarComponent",
}
</script>