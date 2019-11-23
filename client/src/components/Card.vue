<template>
    <div class="card">
    <div class="card-content">
      <div class="media">
        <div class="media-content">
          <nav class="level">
            <div class="level-right">
              <p class="title is-2">{{post.title}}</p>
            </div>
            <div class="level-left">
              <div class="tags has-addons">
              <span class="tag">Author</span>
              <span class="tag is-info">Cameron</span>
            </div>
            </div>
          </nav>

        </div>
      </div>

      <div class="content">
        {{post.body}} 
        <br>
        <p>{{ friendlyDate(post.created_at) }}</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
    name: 'Card',
    props: {
        post: Object
    },
    methods: {
        friendlyDate: function(date) {
            let d = new Date(date);
            return d.toLocaleString();
        }
    }
}
</script>

<style>

</style>