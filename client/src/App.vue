<template>
  <div id="app">
    <Navbar />
    <router-view/>
  </div>
</template>

<script>
import Navbar from './components/Navbar'
export default {
  el: '#app',
  components: {
    Navbar
  }
}
</script>
<style lang="scss">
</style>
