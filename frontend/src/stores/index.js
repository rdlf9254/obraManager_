import { createStore } from "vuex";

const savedUserState = JSON.parse(sessionStorage.getItem("user-store"));

const UserTypeMap = {
  1: "Administrador",
  2: "Engenheiro",
  3: "MestreObras",
  4: "Cliente",
};

const userModule = {
  state: () => ({
    isAuthenticated: savedUserState?.isAuthenticated || false,
    token: savedUserState?.token || null,
    photo: savedUserState?.photo || null,
    id: savedUserState?.id || null,
    date_joined: savedUserState?.date_joined || null,
    first_name: savedUserState?.first_name || null,
    last_name: savedUserState?.last_name || null,
    username: savedUserState?.username || null,
    type: savedUserState?.type || null,
    email: savedUserState?.email || null,
  }),
  mutations: {
    updateUser(state, data) {
      state.isAuthenticated = true;
      state.token = data.access_token;
      state.id = data.id;
      state.date_joined = data.date_joined;
      state.first_name = data.first_name;
      state.last_name = data.last_name;
      state.username = data.username;
      state.email = data.email;
    },
    detailsUser(state, data) {
      state.photo = data.usePhoto;
      state.token = data.access_token;
      state.id = data.id;
      state.type = UserTypeMap[data.useType || 1];
    },
    clean(state) {
      state.isAuthenticated = false;
      state.token = null;
      state.img = null;
      state.id = null;
      state.date_joined = null;
      state.first_name = null;
      state.last_name = null;
      state.username = null;
      state.email = null;
      state.photo = null;
      state.token = null;
      state.id = null;
      state.type = null;
      sessionStorage.removeItem("user-store");
    },
  },
  actions: {
    logout({ commit }) {
      commit("clean");
    },
    auth({ commit }, val) {
      commit("updateUser", val);
    },
    details({ commit }, val) {
      commit("detailsUser", val);
    },
  },
};

const store = createStore({
  modules: {
    user: userModule,
  },
});

store.subscribe((mutation, state) => {
  sessionStorage.setItem("user-store", JSON.stringify(state.user));
});

export default store;
