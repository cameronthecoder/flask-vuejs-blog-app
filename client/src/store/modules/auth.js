import Axios from "axios";
import Vue from 'vue';
const state = {
    refresh_token: null || Vue.$cookies.get('refreshToken'),
    access_token: null || Vue.$cookies.get('access_token'),
    user: {},
    loading: false,
    messages: {}
};

const getters = {
    getRefreshToken: state => state.refresh_token,
    getAccessToken: state => state.access_token,
    getTokenData: state => state.user,
    loading: state => state.loading,
    getMessages: state => state.messages
};

const actions = {
    async fetchJWT({ commit }, { username, password }) {
        const res = await Axios.post('http://localhost:5000/api/auth/login/', {
            username: username,
            password: password
          })
          .then(function (response) {
              console.log(response);
          })
          .catch(function (error) {
            console.log(error);
          });
          commit('setAccessToken', res.data.access_token);
          commit('setRefreshToken', res.data.refresh_token);
    },
    addMessage({commit}, { type, message }) {
        commit('addMessage', {type, message});
    }
};

const mutations = {
    setAccessToken: (state, jwt) => (this.$cookies.set('access_token', jwt)),
    setRefreshToken: (state, jwt) => (this.$cookies.set('refresh_token', jwt)),
    setLoading: (state, loading) => (state.loading = loading),
    addMessage: (state, message) => state.messages.append(message),
};

export default {
    state,
    getters,
    actions,
    mutations
}