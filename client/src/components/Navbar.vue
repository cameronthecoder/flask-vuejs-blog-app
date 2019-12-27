<template>
  <div class="nav">    
        <nav class="navbar">
        <div class="container">
            <div class="navbar-brand">
                <a class="navbar-item" href="../">
                        <img src="../assets/bulma.png" alt="Logo">
                    </a>
                <span class="navbar-burger burger" data-target="navbarMenu">
                <span></span>
                <span></span>
                <span></span>
                </span>
            </div>
            <div id="navbarMenu" class="navbar-menu">
                <div class="navbar-end">
                    <a class="navbar-item is-active">
                      Home
                    </a>
                    <div class="navbar-item has-dropdown is-hoverable">
                        <a class="navbar-link">
                            Account
                        </a>
                        <div class="navbar-dropdown">
                          <div v-if="this.$store.getters.isloggedIn">
                            <router-link class="navbar-item" to="dsfhsdfjdsfhj">
                            <a class="navbar-item">
                              Logout
                            </a>
                          </router-link>
                          </div>
                          <div v-else>
                            <router-link class="navbar-item" to="login">
                              <a class="navbar-item">
                                Login
                              </a>
                            </router-link>
                          </div>
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
</style>