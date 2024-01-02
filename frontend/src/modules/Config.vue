<template>
  <modal-user
    :show="showEditNew"
    :selected="user"
    :isConfig="true"
    @save="showEditNew = false"
    @cancel="showEditNew = false"
  ></modal-user>
  <div class="configuracoes ps6xl">
    <div class="flex row l5xl">
      <img src="@/assets/nouser.jpg" v-if="!user.photo" />
      <img :src="user.photo" v-else />
      <div class="name flex column middle l6xl stretch">
        <h1>{{ user.first_name }} {{ user.last_name }}</h1>
        <h4 class="ts">{{ user.type }}</h4>
        <h4 class="ts">
          Criado em: {{ datethis(user.date_joined) }}
        </h4>
        <h4 class="ts">Nome de usuário: {{ user.username }}</h4>
        <h4 class="ts">email: {{ user.email }}</h4>
      </div>
    </div>
    <om-button
      class="t5xl l5xl"
      @click="showEditNew = true"
      >Alterar meus dados</om-button
    >
  </div>
</template>
<script>
import omButton from "@/components/omButton.vue";
import modalUser from "@/components/modalUser.vue";
import { mapState } from "vuex";
import { date, money } from "@/services/filters.js";

export default {
  name: "Config",
  components: {
    omButton,
    modalUser,
  },
  props: [],
  data() {
    return {
      searchTerm: "",
      showEditNew: false,
    };
  },
  mounted() {},
  computed: {
    ...mapState({
      user: (state) => state.user,
    }),
  },
  methods: {
    datethis(value) {
      return date(value);
    },
  },
};
</script>

<style lang="scss" scoped>
img {
  height: 200px;
  border-radius: 50%;
}
.configuracoes {
  height: 100vb;
}
</style>
