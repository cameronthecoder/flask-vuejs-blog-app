<template>
  <div id="newpost">
    <form @submit.prevent="newPost">
      <div class="field">
        <label class="label">Token</label>
        <div class="control">
          <input v-model="token" class="input" type="text" placeholder="Text input">
        </div>  
      </div>

      <div class="field">
        <label class="label">Title</label>
        <div class="control">
          <input v-model="title" class="input" type="text" placeholder="Text input">
        </div>
      </div>

      <div class="field">
        <label class="label">Body</label>
        <div class="control">
          <input v-model="body" class="input" type="text" placeholder="Text input">
        </div>
      </div>

      <div class="field">
        <label class="label">Slug</label>
        <div class="control">
          <input v-model="slug" class="input" type="text" placeholder="Text input">
        </div>
      </div>


      <div class="field is-grouped">
        <div class="control">
          <button class="button is-link">Submit</button>
        </div>
        <div class="control">
          <button class="button is-link is-light">Cancel</button>
        </div>
      </div>
    </form> 
  </div>
</template>

<script>
export default {
    name: 'NewPost',
    data () {
        return {
            post: {},
            token: '',
            title: '',
            body: '',
            slug: ''
        }
    },
    methods: {
            newPost: async function () {
                const rawResponse = await fetch('http://192.168.0.173:5000/api/posts/', {
                method: 'POST',
                headers: {
                  'Accept': 'application/json',
                  'Content-Type': 'application/json',
                  'Authorization': 'Bearer ' + this.token
                },
                body: JSON.stringify({"title": this.title, "body": this.body, "slug": this.slug})
              });
              const content = await rawResponse.json();
              console.log(content);
    }
    }
  }
</script>

<style>

</style>