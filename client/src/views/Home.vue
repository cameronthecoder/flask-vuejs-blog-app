<template>
<div class="hello">
  <div class="container">
  <div class="columns is-desktop">
    <div class="column is-two-thirds">
      <progress v-if="loading" class="progress is-small is-primary" max="100" />
      <div :v-if="getPosts" v-for="(post, index) in getPosts" :key="index">
        <Card :post="post" />
      </div>
  <nav class="pagination is-centered" role="navigation" aria-label="pagination">
    <a class="pagination-previous">Previous</a>
    <a class="pagination-next">Next page</a>
    <ul class="pagination-list">
      <li><a class="pagination-link" aria-label="Goto page 1">1</a></li>
      <li><span class="pagination-ellipsis">&hellip;</span></li>
      <li><a class="pagination-link" aria-label="Goto page 45">45</a></li>
      <li><a class="pagination-link is-current" aria-label="Page 46" aria-current="page">46</a></li>
      <li><a class="pagination-link" aria-label="Goto page 47">47</a></li>
      <li><span class="pagination-ellipsis">&hellip;</span></li>
      <li><a class="pagination-link" aria-label="Goto page 86">86</a></li>
    </ul>
  </nav>
    </div>
    <div class="column">
      <nav class="panel is-primary">
    <p class="panel-heading">
      Year archive
    </p>
    <a class="panel-block is-active">
      2019
    </a>
    <a class="panel-block">
      2018
    </a>
    <a class="panel-block">
      2017
    </a>
    <a class="panel-block">
      2016
    </a>
    <a class="panel-block">
      2015
    </a>
    <a class="panel-block">
      2014
    </a>
  </nav>
    </div>
  </div>
  </div>
  <footer class="footer">
    <div class="content has-text-centered">
      <p>
        <strong>A random blog</strong> by <a href="https://jgthms.com">Cameron</a>.
      </p>
    </div>
  </footer>
</div>
</template>

<script>
import Card from '../components/Card';
import { mapGetters, mapActions } from 'vuex';

export default {
  name: 'Home',
  components: {
    Card
  },
  methods: {
    ...mapActions(['fetchPosts']),
  },
  computed: mapGetters(['getPosts', 'loading']),
  created () {
    this.fetchPosts();
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.columns {
  margin-top: 10px;
}
.card {
  margin-bottom: 10px;
}
.footer {
  margin-top: 30px;
}
</style>
