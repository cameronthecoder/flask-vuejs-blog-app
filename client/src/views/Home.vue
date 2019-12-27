<template>
<div class="home">
    <!-- Bulma template from https://bulmatemplates.github.io/bulma-templates/ -->
    <!-- START NAV -->
    <!-- END NAV -->
    <Navbar />
    <section class="hero is-info is-medium is-bold">
        <div class="hero-body">
            <div class="container has-text-centered">
                <h1 class="title">Cameron's Blog</h1>
            </div>
        </div>
    </section>


    <div class="container">
        <!-- START ARTICLE FEED -->
        <section class="articles">
            <div class="column is-8 is-offset-2">
                <!-- START ARTICLE -->
                <div v-for="post in getPosts" :key="post.id">
                  <div class="card article">
                    <div class="card-content">
                        <div class="media">
                            <div class="media-content has-text-centered">
                                <p class="title article-title">{{post.title}}</p>
                                <div class="tags has-addons level-item">
                                    <span class="tag is-rounded is-info">{{post.username}}</span>
                                    <span :class="{'tag': true, 'is-rounded': true, 'is-danger': post.role == 'Administrator', 'is-warning': post.role == 'Moderator'}" :v-if="post.role">{{post.role}}</span>
                                    <span class="tag is-rounded">{{ friendlyDate(post.created_at) }}</span>
                                </div>
                            </div>
                        </div>
                        <div class="content article-body">
                           <p>{{post.body}}</p>
                        </div>
                    </div>
                </div>
                </div>
              </div>
            </section>
          </div>
        </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';
import Navbar from '../components/Navbar.vue'
export default {
  name: 'Home',
  components: {
    Navbar
  },
  data () {
    return {
      months: ['January', 'Febuary', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    }
  },
  methods: {
    ...mapActions(['fetchPosts']), 
    PMorAM: function (num) {
      return num >= 12 ? 'PM' : 'AM' 
    },
    friendlyDate: function(date) {
      let d = new Date(date);
      return `${this.months[d.getMonth()]} ${d.getDay()}, ${d.getFullYear()}, ${d.getUTCHours()}:${d.getMinutes()} ${this.PMorAM(d.getUTCHours)}`;
    }
  },
  computed: mapGetters(['getPosts', 'loading']),
  created () {
    this.fetchPosts();
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
html,body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen-Sans, Ubuntu, Cantarell, "Helvetica Neue", sans-serif;
  font-size: 14px;
  background: #F0F2F4;
}
.navbar.is-white {
  background: #F0F2F4;
}
.navbar-brand .brand-text {
  font-size: 1.11rem;
  font-weight: bold;
}
.hero-body {
background-image: url(../assets/dam-3-grey.jpg);
background-position: center;
background-size: cover;
background-repeat: no-repeat;
height: 500px;
}
.articles {
  margin: 5rem 0;
  margin-top: -200px;
}
.articles .content p {
    line-height: 1.9;
    margin: 15px 0;
}
.author-image {
    position: absolute;
    top: -30px;
    left: 50%;
    width: 60px;
    height: 60px;
    margin-left: -30px;
    border: 3px solid #ccc;
    border-radius: 50%;
}
.media-center {
  display: block;
  margin-bottom: 1rem;
}
.media-content {
  margin-top: 3rem;
}
.article, .promo-block {
  margin-top: 6rem;
}
div.column.is-8:first-child {
  padding-top: 0;
  margin-top: 0;
}
.article-title {
  font-size: 2rem;
  font-weight: lighter;
  line-height: 2;
}
.article-subtitle {
  color: #909AA0;
  margin-bottom: 3rem;
}
.article-body {
  line-height: 1.4;
  margin: 0 6rem;
}
.promo-block .container {
  margin: 1rem 5rem;
}
</style>
