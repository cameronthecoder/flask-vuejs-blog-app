<template>
  <div class="nav">
<section class="hero is-medium has-bg-img" v-if="!this.$route.meta.noHeader">
  <div class="hero-body">
    <div class="container has-text-centered">
      <h1 class="title is-size-1 has-text-light">
        Sally's Blog
      </h1>
    </div>
  </div>
</section>      
<nav class="navbar is-spaced has-shadow" role="navigation" aria-label="main navigation" v-if="!this.$route.meta.noNav">
  <div class="navbar-brand">
    <a role="button" class="navbar-burger burger" aria-label="menu" aria-expanded="false" data-target="navbarBasicExample">
      <span aria-hidden="true"></span>
      <span aria-hidden="true"></span>
      <span aria-hidden="true"></span>
    </a>
  </div>
  <div class="container">
  <div class="navbar-menu">
    <div class="navbar-start">
      <a class="navbar-item has-text-primary">
        Home
      </a>

      <a class="navbar-item">
        FAQ
      </a>
      </div>

    <div class="navbar-end">
      <div class="navbar-item">
        <div class="buttons">
          <a class="button is-primary">
            Log in
          </a>
        </div>
      </div>
    </div>
      </div>
  </div>
</nav>
  </div>
</template>

<script>
export default {
    name: 'Navbar'
}
</script>

<style scoped>
.has-bg-img {
    background: url('../assets/dam-5-grey.jpg')top center;
    background-size: cover;

}
</style>