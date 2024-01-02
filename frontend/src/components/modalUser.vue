<template>
  <modal :show="showModal" @close="cancel()">
    <template #content>
      <div>
        <div class="title">
          <h3>{{ this.selected ? "Editar Usuário" : "Novo usuário" }}</h3>
        </div>
        <form @submit.prevent="salvar">
          <div class="txl">
            <label for="nome">Nome:</label>
            <input-text
              type="text"
              id="nome"
              placeholder="Digite o nome..."
              v-model="localUser.first_name"
              required
            />
          </div>
          <div class="txl">
            <label for="nome">Sobrenome:</label>
            <input-text
              type="text"
              id="nome"
              placeholder="Digite o email..."
              v-model="localUser.last_name"
              required
            />
          </div>
          <div class="txl">
            <label for="nome">Nome de usuário:</label>
            <input-text
              type="text"
              id="username"
              placeholder="Digite o nome de usuário..."
              v-model="localUser.username"
              required
            />
          </div>
          <div class="txl">
            <label for="nome">Email:</label>
            <input-text
              type="email"
              id="nome"
              placeholder="Digite o email..."
              v-model="localUser.email"
              required
            />
          </div>
          <div class="txl">
            <label for="nome">Senha:</label>
            <input-text
              type="password"
              id="nome"
              placeholder="Digite a senha..."
              v-model="localUser.password"
              required
            />
          </div>

          <div class="txl">
            <label for="nome">Repita a senha:</label>
            <input-text
              type="password"
              id="nome"
              placeholder="Repita a senha..."
              v-model="localUser.password2"
              required
            />
          </div>

          <div class="txl" v-if="!isConfig">
            <label for="tipo">Tipo de Usuário:</label>
            <select id="tipo" v-model="localUser.type" required>
              <option v-for="tipo in typeUsers" :key="tipo.id" :value="tipo">
                {{ tipo.name }}
              </option>
            </select>
          </div>

          <div class="txl">
            <img
              v-if="localUser.photo"
              :src="localUser.photo"
              alt="Foto de usuário"
              width="50"
              height="50"
            />
            <img
              v-else
              src="@/assets/nouser.jpg"
              alt="Default User Photo"
              width="50"
              height="50"
            />
            <canvas id="hiddenCanvas" style="display: none"></canvas>

            <input type="file" id="foto" @change="onFileChange" />
            <label for="foto">Escolher foto</label>
          </div>

          <div class="txl" v-if="!isConfig">
            <label for="projeto">Projetos Relacionados:</label>
            <div v-for="(proj, index) in localUser.projects" :key="index">
              <select
                class="txs"
                :id="index"
                v-model="localUser.projects[index]"
              >
                <option
                  v-for="projeto in allProjects"
                  :key="projeto.id"
                  :value="projeto"
                >
                  {{ projeto.label }}
                </option>
              </select>
            </div>
            <om-button
              class="tl"
              hierarchy="secondary"
              @click="pushNewProject"
            >
              Adicionar projeto
            </om-button>
          </div>

          <div class="flex center t5xl">
            <om-button v-if="this.selected" type="submit">Salvar</om-button>
            <om-button v-else type="submit">Criar</om-button>
          </div>
        </form>
      </div>
    </template>
  </modal>
</template>

<script>
import Modal from "@/components/Modal.vue";
import inputText from "@/components/input/inputText.vue";
import omButton from "../components/omButton.vue";
import { updateUser, createUser } from "@/services/users.js";
import { getAllProjectsNames } from "@/services/projects.js";
import Cropper from "cropperjs";

export default {
  name: "modal-user",
  props: {
    selected: {
      default: null,
    },
    show: {
      required: true,
      default: false,
    },
    isConfig: {
      default: false,
    },
  },
  components: {
    Modal,
    inputText,
    omButton,
  },
  data() {
    return {
      showModal: this.show,
      localUser: this.selected
        ? { ...this.selected, projects: [] }
        : {
            first_name: "",
            last_name: "",
            email: "",
            username: "",
            password: "",
            password2: "",
            type: 4,
            projects: [],
            photo: null,
          },
      typeUsers: [
        {
          name: "Administrador",
          id: 1,
        },
        {
          name: "Engenheiro",
          id: 2,
        },
        {
          name: "Mestre de Obras",
          id: 3,
        },
        {
          name: "Cliente",
          id: 4,
        },
      ],
      allProjects: [],
    };
  },
  watch: {
    show(value) {
      this.showModal = value;
      if (!this.showModal) {
        this.resetData();
      } else {
        this.getAllProjects();
      }
    },
    selected: {
      deep: true,
      handler() {
        this.updateUserDataAndTitle();
      },
    },
  },
  mounted() {
    this.updateUserDataAndTitle();
    this.getAllProjects();
  },
  methods: {
    updateUserDataAndTitle() {
      if (this.show) {
        this.localUser = this.selected ? { ...this.selected, projects: [] } : this.localUser;
      }
    },
    cancel() {
      this.showModal = false;
      this.resetData();
      this.$emit("cancel", true);
    },
    onFileChange(e) {
      const file = e.target.files[0];
      const canvas = document.getElementById("hiddenCanvas");
      const ctx = canvas.getContext("2d");
      const img = new Image();

      img.onload = () => {
        let w = img.width;
        let h = img.height;

        const aspectRatio = w / h;

        if (w > h) {
          h = 120;
          w = 120 * aspectRatio;
        } else {
          w = 120;
          h = 120 / aspectRatio;
        }

        canvas.width = w;
        canvas.height = h;

        ctx.drawImage(img, 0, 0, w, h);

        const imageData = ctx.getImageData(
          (w - 120) / 2,
          (h - 120) / 2,
          120,
          120
        );

        ctx.clearRect(0, 0, canvas.width, canvas.height);
        canvas.width = 120;
        canvas.height = 120;

        ctx.putImageData(imageData, 0, 0);

        const base64 = canvas.toDataURL("image/png");

        this.localUser.photo = base64;
      };

      img.src = URL.createObjectURL(file);
    },
    createImage(file) {
      const reader = new FileReader();

      reader.onload = (e) => {
        this.user.Foto = e.target.result;
      };

      reader.readAsDataURL(file);
    },
    salvar() {
      if (this.localUser.password !== this.localUser.password2) {
        alert("As senhas não coincidem.");
        return;
      }
      if (!this.localUser.first_name) {
        alert("Preencha o Primeiro nome.");
        return;
      }
      if (!this.localUser.last_name) {
        alert("Preencha o Sobrenome.");
        return;
      }
      if (!this.localUser.email) {
        alert("Preencha o e-mail.");
        return;
      }
      if (!this.localUser.username) {
        alert("Preencha o nome de usuário.");
        return;
      }
      let userData = {
        first_name: this.localUser.first_name,
        last_name: this.localUser.last_name,
        email: this.localUser.email,
        username: this.localUser.username,
        password: this.localUser.password,
        type: this.localUser.type.id,
        projects: this.localUser.projects,
        photo: this.localUser.photo,
      };
      delete userData.password2;

      if (this.selected) {
        this.updatethisUser();
      } else {
        this.createthisUser(userData);
      }
    },
    async getAllProjects() {
      try {
        const data = await getAllProjectsNames();
        this.allProjects = data;
      } catch (error) {
        console.error("Ocorreu um erro ao pegar obras:", error);
      }
    },
    updatethisUser() {
      this.$emit("save", this.localUser);
    },
    createthisUser() {
      this.$emit("create", this.localUser);
    },
    pushNewProject() {
      if (this.localUser && Array.isArray(this.localUser.projects)) {
        this.localUser.projects.push(this.allProjects[0]);
      } else {
        console.error("localUser.projects não é um array ou está indefinido.");
      }
    },
    resetData() {
      this.localUser = {
        name: "",
        type: "Cliente",
        projects: [],
        photo: null,
      };
    },
  },
};
</script>

<style lang="scss" scoped>
img {
  width: 120px;
  height: 120px;
  border-radius: 50%;
}
#foto {
  display: none;
}

#foto + label {
  background-color: #4caf50;
  color: #fff;
  padding: var(--sm) var(--sl);
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: var(--p16);
  box-shadow: 0px var(--sxs) 6px rgba(0, 0, 0, 0.1);
  transition: background-color 0.3s;
}

#foto + label:hover {
  background-color: #45a049;
}
#image-cropper {
  width: 100%;
  max-width: 300px;
  margin: auto;
}

#image-to-crop {
  max-width: 100%;
}
</style>
