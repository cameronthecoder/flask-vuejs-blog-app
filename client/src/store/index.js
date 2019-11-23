import Vuex from 'vuex'
import Vue from 'vue'
import auth from './modules/auth'
import posts from './modules/posts'


Vue.use(Vuex);

export default new Vuex.Store({
    modules: {
        auth,
        posts
    }
})