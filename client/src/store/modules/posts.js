import axios from 'axios'

export const API_URL = 'http://localhost:5000';

const state = {
    posts: {},
    loading: false,
};

const getters = {
    loading: state => state.loading,
    getPosts: state => state.posts
};

const actions = {
    async fetchPosts({ commit }) {
        commit('setLoading', true)
        const response = await axios.get(API_URL + '/api/posts/');

        commit('setPosts', response.data.posts);
        commit('setLoading', false);
    }
};

const mutations = {
    setPosts: (state, posts) => (state.posts = posts),
    setLoading: (state, loading) => (state.loading = loading),
};

export default {
    state,
    getters,
    actions,
    mutations
}