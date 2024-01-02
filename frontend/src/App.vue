<script>
import { RouterLink, RouterView } from 'vue-router'
import { useRouter } from 'vue-router';
import dashboard from "@/components/dashboard.vue"
  import { mapState } from "vuex";


export default {
  name: 'App',
  components:{dashboard},
  data(){
    return{
    }
  },
  computed: {
    ...mapState({
      user: state => state.user,
    }),
  },
  mounted(){
    let unicons = document.createElement("link");
    unicons.setAttribute('href', 'https://unicons.iconscout.com/release/v2.1.5/css/unicons.css');
    unicons.setAttribute("rel", 'stylesheet');
    document.head.appendChild(unicons);
    if(!this.user.isAuthenticated){
      localStorage.removeItem('access_token');
      this.$store.dispatch("logout");
      this.$router.push({ name: "Login" });
    }
  }
};


</script>

<template>
  <div id="app">
    <div v-if="!user.isAuthenticated">
      <RouterView />
    </div>
    <div v-else>
      <dashboard>
        <template #content>
          <RouterView />
        </template>
      </dashboard>
    </div>
  </div>
</template>
