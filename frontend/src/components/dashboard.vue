<template>
  <div class="contain-dash flex">
    <div class="sidebar flex column between">
      <div>
        <h3 class="l5xl">Seja Bem Vindo</h3>
        <div class="flex row l5xl">
          <img src="@/assets/nouser.jpg" v-if="!user.photo" />
          <img :src="user.photo" v-else />
          <div class="name flex column center lxl">
            <h4>{{ user.first_name }} {{ user.last_name }}</h4>
            <h5 class="tm">{{ user.type }}</h5>
          </div>
        </div>
      </div>
      <div class="sidebar-buttons flex column l5xl">
        <button
          type="button"
          class="t2xl"
          @click="routerTo('Projects')"
          :class="{ current: isCurrent('Projects') }"
        >
          <h2>Meus Projetos</h2>
        </button>
        <button
          type="button"
          class="t2xl"
          @click="routerTo('Users')"
          :class="{ current: isCurrent('Users') }"
        >
          <h2 v-if="isAdm">Usuários</h2>
        </button>
        <button
          type="button"
          class="t2xl"
          @click="routerTo('Config')"
          :class="{ current: isCurrent('Config') }"
        >
          <h2>Configurações</h2>
        </button>
      </div>
      <div class="logout flex center l5xl">
        <button @click="logout"><h2>Logout</h2></button>
      </div>
    </div>
    <div class="main-content-dash w100">
      <slot name="content" class="w100"></slot>
    </div>
  </div>
</template>

<script>
import { mapState } from "vuex";
import { details } from "@/services/auth.js";

export default {
  name: "dashboard",
  components: {},
  data() {
    return {
    };
  },
  computed: {
    ...mapState({
      user: (state) => state.user,
    }),
  },

  mounted() {
    this.details(this.user.id);
  },
  methods: {
    async details(id) {
      try {
        const data = await details(id);
        this.$store.dispatch("details", data);
      } catch (error) {
        console.error("Ocorreu um erro:", error);
      }
    },
    isAdm() {
      this.user.type == "Administrador";
    },
    routerTo(route) {
      this.$router.push({ name: route });
    },
    isCurrent(name) {
      return this.$route.name === name;
    },
    logout() {
      localStorage.removeItem('access_token');
      this.$store.dispatch("logout");
      this.$router.push({ name: "Login" });
    },
  },
};
</script>

<style lang="scss" scoped>
.sidebar {
  position: fixed;
  height: 100vh;
  background-color: white;
  width: 256px;
  h3 {
    padding: var(--2sxl2) 0 var(--2sxl2);
    color: var(--blue-c);
  }
  img {
    height: var(--5sxl);
    border-radius: 50%;
  }
  .sidebar-buttons {
    button.current h2 {
      color: var(--blue-c);
    }
    button h2 {
      color: var(--blue-d);
    }
  }
  .logout {
    position: relative; 
    height: var(--5sxl);
    bottom: 0px; 
    button {
      display: flex;
      height: var(--2sxl2);
      position: relative;
      color: grey;
    }
  }
}
.main-content-dash {
  padding-left: 256px;
}
</style>
