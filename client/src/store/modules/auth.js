import Axios from "axios";
import jwt_decode from 'jwt-decode';

const state = {
    refresh_token: window.$cookies.get('refresh_token') || null,
    access_token: window.$cookies.get('access_token') || null,
    user: {},
    loading: false,
    messages: []
};

const getters = {
    getRefreshToken: state => state.refresh_token,
    getAccessToken: state => state.access_token,
    getTokenData: state => state.user,
    authLoading: state => state.loading,
    getMessages: state => state.messages
};

const actions = {
    async fetchJWT({ commit }, credentials) {
        return new Promise((resolve, reject) => {
        commit('setLoading', true);
        Axios.post('http://localhost:5000/api/auth/login/', {
            username: credentials.username,
            password: credentials.password
          })
          .then(function (response) {
            commit('setLoading', false);
            commit('setAccessToken', response.data.access_token);
            commit('setRefreshToken', response.data.refresh_token);
            const decoded = jwt_decode(response.data.access_token);
            const user = {
                id: decoded.id,
                username: decoded.username
            }
            commit('setUser', user);
            commit('addMessage', {
                message: 'Hello World',
                type: 'success'
            });
            resolve(response);
          })
          .catch(function (error) {
            commit('setLoading', false);
            if (error.response) {
                commit('addMessage', { 
                    message: error.response.data.error, 
                    type: 'error' 
                })
            } else {
                commit('addMessage', { 
                    message: 'Something went wrong. Please try again later.', 
                    type: 'error' 
                })
            }
            reject(error);
          });
        }) 
    },
};

const mutations = {
    setAccessToken: (jwt) => (window.$cookies.set('access_token', jwt)),
    setRefreshToken: (jwt) => (window.$cookies.set('refresh_token', jwt)),
    setUser: (state, user) => (state.user = user),
    setLoading: (state, loading) => (state.loading = loading),
    addMessage: (state, { message, type }) => {
        state.messages = [];
        state.messages.push({message, type});
    }
};

export default {
    state,
    getters,
    actions,
    mutations
}