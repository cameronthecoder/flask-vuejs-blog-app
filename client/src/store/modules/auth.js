import Axios from "axios";
import jwt_decode from 'jwt-decode';
import VueCookies from 'vue-cookies';

const state = {
    refresh_token: VueCookies.get('refresh_token') || null,
    access_token: VueCookies.get('access_token') || null,
    user: window.$cookies.get('user') || null,
    loading: false,
    messages: []
};

const getters = {
    isloggedIn: state => state.refresh_token !== null && state.access_token !== null,
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
            VueCookies.set('access_token', response.data.access_token)
            VueCookies.set('refresh_token', response.data.refresh_token)
            commit('setAccessToken', response.data.access_token);
            commit('setRefreshToken', response.data.refresh_token);
            const decoded = jwt_decode(response.data.access_token);
            const user = {
                id: decoded.id,
                username: decoded.username,
                role: decoded.role
            }
            VueCookies.set('user', user)
            commit('setUser', user);
            commit('addMessage', {
                message: 'Login success!',
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
    // TODO: logout
    //logout({commit}) {
    //    //VueCookies.remove("access_token")
    //    //VueCookies.remove("refresh_token")
    //   //VueCookies.remove("user")
    //}
};

const mutations = {
    setAccessToken: (jwt) => (state.access_token = jwt),
    setRefreshToken: (jwt) => (state.refresh_token = jwt),
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