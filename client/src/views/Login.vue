<template>
  <div id="navbar">
    <section class="hero is-fullheight">
      <div class="hero-body">
        <div class="container">
          <div class="columns is-centered">
            <div class="column is-5-tablet is-4-desktop is-5-widescreen">
              <div class="card">
                <div class="card-content">
                  <p class="title has-text-centered">Log In</p>
                  <hr>
                  <div v-for="(message, index) in getMessages" :key="index">
                    <article :class="{ 'message': true, 'is-danger': message.type == 'error', 'is-success': message.type == 'success' }">
                      <div class="message-body">
                        {{message.message}}
                      </div>
                    </article>

                  </div>
                    <form @submit.prevent="login">
                      <div class="field">
                        <label class="label">Username</label>
                        <div class="control">
                          <input required v-model="username" class="input" type="text" placeholder="Username">
                        </div>
                      </div>

                      <div class="field">
                        <label class="label">Password</label>
                        <div class="control">
                          <input required v-model="password" class="input" type="password" placeholder="Password">
                        </div>
                      </div>

                      <div class="control">
                        <button :class="{'button': true, 'is-primary': 'true', 'is-loading': authLoading}" type="submit">Submit</button>
                      </div>
                    </form>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>
      </div>
</template>

<script>
import { mapGetters } from 'vuex';
export default {
  name: 'login',
  data () {
    return {
      username: '',
      password: '',
    }
  },
  methods: {
   login () {
     this.$store.dispatch('fetchJWT', {
       username: this.username,
       password: this.password
     })
   }
  },
  computed: {
    ...mapGetters(['getMessages', 'authLoading'])
  }
}
</script>

<style>

</style>