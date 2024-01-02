<template>
  <div class="tudo">
    <div class="bg flex end bottom ps6xl">
      <h1 class="title">obraManager</h1>
    </div>
    <div class="login-section h100">
      <form class="psxl" @submit.prevent="login">
        <div class="flex column middle">
          <div>
            <label class="flex start" for="username">Email</label>
            <input-text v-model="email" type="text" placeholder="Digite o e-mail"></input-text>
          </div>
          <div>
            <label class="flex left t3xl" for="password">Senha</label>
            <input-text v-model="password" type="password" placeholder="Digite a senha"></input-text>
          </div>
          <om-button class="t3xl" type="submit">Entrar</om-button>
        </div>
      </form>
    </div>
    <p class="error" v-if="error">{{ error }}</p>
  </div>
</template>

<script>
import omButton from "@/components/omButton.vue";
import inputText from "@/components/input/inputText.vue";
import { login } from "@/services/auth.js";

export default {
  components: {
    omButton,
    inputText,
  },
  data() {
    return {
      email: "",
      password: "",
      error: "",
    };
  },

  methods: {
    async login() {
      try {
        const data = await login(this.email, this.password);
        if (data.success) {
          this.$store.dispatch("auth", data);
          localStorage.setItem("access_token", data.access_token);
          this.$router.push({ name: "Projects" });
        } else {
          alert("Credenciais inválidas");
        }
      } catch (error) {
        console.error("Ocorreu um durante o login:", error);
      }
    },
  },
};
</script>

<style scoped>
.tudo {
  display: flex;
  align-items: center;
}

.bg {
  background-image: url("./loginbg.png");

  background-repeat: no-repeat;
  background-position: center;
  background-size: 100%;
  min-height: 100vh;
  width: calc(100vw - 400px);

  .title {
    font-size: var(--6sxl);
    top: var(--5sxl);
    color: white;
  }
}

form {
  width: 400px;
  right: 0;
  position: relative;
}

.error {
  color: red;
  font-weight: bold;
  margin-top: var(--sm);
}

.login-section {
  width: 400px;
  height: 100vh;
  background-color: EFF5FF;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
</style>
