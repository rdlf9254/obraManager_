<template>
  <modal :show="showModal" @close="cancel()">
    <template #content>
      <div>
        <div class="title">
          <h3>{{ this.selected ? "Editar Projeto" : "Novo Projeto" }}</h3>
        </div>
        <form @submit.prevent="salvar">
          <div class="txl">
            <label for="nome">Nome:</label>
            <input-text
              type="text"
              id="nome"
              placeholder="Digite o nome do projeto..."
              v-model="localProject.proName"
              required
            />
          </div>
          <div class="txl">
            <label for="nome">Endereço:</label>
            <input-text
              type="text"
              id="nome"
              placeholder="Digite o endereço do projeto..."
              v-model="localProject.proAddress"
              required
            />
          </div>

          <div class="txl">
            <label for="tipo">Status:</label>
            <select id="tipo" v-model="localProject.proStatus" required>
              <option
                v-for="tipo in STATUS_CHOICES"
                :key="tipo.id"
                :value="tipo.id"
              >
                {{ tipo.label }}
              </option>
            </select>
          </div>

          <div class="txl">
            <label for="tipo">Estágio:</label>
            <select id="tipo" v-model="localProject.proStage" required>
              <option
                v-for="tipo in STAGE_CHOICES"
                :key="tipo.id"
                :value="tipo.id"
              >
                {{ tipo.label }}
              </option>
            </select>
          </div>

          <div class="txl">
            <label for="tipo">Responsável:</label>
            <select id="tipo" v-model="localProject.proResponsible" required>
              <option v-for="tipo in users" :key="tipo.id" :value="tipo.id">
                {{ tipo.label }}
              </option>
            </select>
          </div>

          <div class="txl">
            <label for="nome">Progresso geral (0 - 100):</label>
            <input-text
              type="text"
              id="nome"
              placeholder="Digite o progresso geral do projeto..."
              v-model="localProject.proGeneralProgress"
              required
            />
          </div>

          <div class="txl">
            <label for="nome">Progresso do estágio atual (0 - 100):</label>
            <input-text
              type="text"
              id="nome"
              placeholder="Digite o progresso geral do estágio atual..."
              v-model="localProject.proStageProgress"
              required
            />
          </div>

          <div class="txl">
            <label for="nome">Total de estágios da obra:</label>
            <input-text
              type="text"
              id="nome"
              placeholder="Digite o Total de estágios da obra..."
              v-model="localProject.proTotalTasks"
              required
            />
          </div>

          <div class="txl">
            <label for="nome">Total de estágios concluídos:</label>
            <input-text
              type="text"
              id="nome"
              placeholder="Digite o Total de estágios concluídos..."
              v-model="localProject.proDoneTasks"
              required
            />
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
import { getAllProjectsNames } from "@/services/projects.js";

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
      localProject: this.selected
        ? { ...this.selected, projects: [] }
        : {
            proName: null,
            proAddress: null,
            proStatus: null,
            proCreatedAt: null,
            proLastUpdate: null,
            proStage: null,
            proResponsible: null,
            proGeneralProgress: null,
            proStageProgress: null,
            proNextStageProgress: null,
            proTotalTasks: null,
            proDoneTasks: null,
            proDoingTasks: null,
            proUseCreator: null,
            photos: null,
          },
      STAGE_CHOICES: [
        {
          id: 0,
          label: "Anteprojeto",
        },
        {
          id: 1,
          label: "Planejamento",
        },
        {
          id: 2,
          label: "Projeto Básico",
        },
        {
          id: 3,
          label: "Licenciamento",
        },
        {
          id: 4,
          label: "Mobilização",
        },
        {
          id: 5,
          label: "Fundação",
        },
        {
          id: 6,
          label: "Estrutura",
        },
        {
          id: 7,
          label: "Alvenaria",
        },
        {
          id: 8,
          label: "Telhado",
        },
        {
          id: 9,
          label: "Hidráulica",
        },
        {
          id: 10,
          label: "Elétrica",
        },
        {
          id: 11,
          label: "Revestimento Interno",
        },
        {
          id: 12,
          label: "Revestimento Externo",
        },
      ],
      STATUS_CHOICES: [
        {
          id: 0,
          label: "No Prazo",
        },
        {
          id: 1,
          label: "Concluído",
        },
        {
          id: 2,
          label: "Atrasado",
        },
        {
          id: 3,
          label: "Em espera",
        },
      ],
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
        this.localProject = this.selected
          ? { ...this.selected }
          : this.localProject;
      }
    },
    cancel() {
      this.showModal = false;
      this.resetData();
      this.$emit("cancel", true);
    },
    salvar() {
      if (this.localProject.password !== this.localProject.password2) {
        alert("As senhas não coincidem.");
        return;
      }
      if (!this.localProject.first_name) {
        alert("Preencha o Primeiro nome.");
        return;
      }
      if (!this.localProject.last_name) {
        alert("Preencha o Sobrenome.");
        return;
      }
      if (!this.localProject.email) {
        alert("Preencha o e-mail.");
        return;
      }
      if (!this.localProject.username) {
        alert("Preencha o nome de usuário.");
        return;
      }
      if (this.selected) {
        this.updatethisUser();
      } else {
        this.createthisUser();
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
      this.$emit("save", this.localProject);
    },
    createthisUser() {
      this.$emit("create", this.localProject);
    },
    resetData() {
      this.localProject = {
        proName: null,
        proAddress: null,
        proStatus: null,
        proCreatedAt: null,
        proLastUpdate: null,
        proStage: null,
        proResponsible: null,
        proGeneralProgress: null,
        proStageProgress: null,
        proNextStageProgress: null,
        proTotalTasks: null,
        proDoneTasks: null,
        proDoingTasks: null,
        proUseCreator: null,
        photos: null,
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
