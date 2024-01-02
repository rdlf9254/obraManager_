<template>
  <modal-confirm
    :show="showConfirm"
    confirmtext="Sim"
    description="Tem certeza que deseja excluir este Projeto?"
    @accept="deletethisProject"
    @cancel="closeModal"
  ></modal-confirm>

  <modal-project
    :show="showNew"
    @create="createthisProject"
    @cancel="closeModal"
  ></modal-project>

  <modal-project
    :show="showEdit"
    :selected="selected"
    @save="updatethisProject"
    @cancel="closeModal"
  ></modal-project>

  <om-table
    titulo="Projetos"
    :dados="dados"
    :headers="headers"
    :isProject="true"
    nome="projeto"
    @editar="editarProj"
    @remover="removerProj"
    @new="showNew = true"
    @clicked="showProject"
  ></om-table>
</template>

<script>
import { mapState } from "vuex";
import omTable from "@/components/omTable.vue";
import {
  getProjectById,
  getAllProjects,
  getMyProjects,
} from "@/services/projects.js";
import modalProject from "@/components/modalProject.vue";
import modalConfirm from "@/components/modalConfirm.vue";

export default {
  name: "projects",
  components: {
    omTable,
    modalProject,
    modalConfirm,
  },
  data() {
    return {
      showNew: false,
      showEdit: false,
      showConfirm: false,
      selected: null,
      headers: [
        " ",
        "Projeto",
        "Estágio",
        "Início",
        "Ultima atualização",
        "Status",
        "Id",
      ],
      dados: [],
    };
  },
  computed: {
    ...mapState({
      user: (state) => state.user,
    }),
  },
  watch: {},
  mounted() {
    this.getData();
  },
  methods: {
    getData() {
      if (this.user.type == "Administrador") {
        this.getAllProjects();
      } else {
        this.getMyProjects(this.user.id);
      }
    },
    async getAllProjects() {
      try {
        const data = await getAllProjects();
        this.dados = this.treatData(data);
      } catch (error) {
        console.error("Ocorreu um erro:", error);
      }
    },
    async getMyProjects() {
      try {
        const data = await getMyProjects(this.user.id);
        this.dados = this.treatData(data);
      } catch (error) {
        console.error("Ocorreu um erro:", error);
      }
    },
    async loadProject(id) {
      try {
        let resposta = await getProjectById(id);
        this.selected = resposta.data;
      } catch (error) {
        console.error("Erro ao carregar o projeto:", error);
      }
    },

    treatData(data) {
      let STAGE_CHOICES = [
        "Anteprojeto",
        "Planejamento",
        "Projeto Básico",
        "Licenciamento",
        "Mobilização",
        "Fundação",
        "Estrutura",
        "Alvenaria",
        "Telhado",
        "Hidráulica",
        "Elétrica",
        "Revestimento Interno",
        "Revestimento Externo",
      ];
      let STATUS_CHOICES = ["No Prazo", "Concluído", "Atrasado", "Em espera"];

      return data.map((data) => ({
        id: data.id,
        name: data.name,
        stage: STAGE_CHOICES[data.stage],
        createdAt: data.createdAt,
        lastUpdate: data.lastUpdate,
        status: STATUS_CHOICES[data.status],
      }));
    },
    showProject(item) {
      this.$router.push({ path: `/projects/${item.id}` });
    },
    editarProj(item) {
      this.loadProject(item.id);
      this.showEdit = true;
    },
    removerProj(item) {
      this.selected = item;
      this.showConfirm = true;
    },
    closeModal() {
      this.showNew = false;
      this.showEdit = false;
      this.showConfirm = false;
      this.selected = null;
    },
  },
};
</script>
