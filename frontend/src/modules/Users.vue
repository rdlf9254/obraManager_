<template>
  <modal-user
    :show="showNew"
    @create="createthisUser"
    @cancel="closeModal"
  ></modal-user>
  <modal-user
    :show="showEdit"
    :selected="selected"
    @save="updatethisUser"
    @cancel="closeModal"
  ></modal-user>
  <modal-confirm
    :show="showConfirm"
    confirmtext="Sim"
    description="Tem certeza que deseja excluir este usuário?"
    @accept="deletethisUser"
    @cancel="closeModal"
  ></modal-confirm>
  <om-table
    titulo="Usuários"
    :dados="usuarios"
    :headers="headers"
    :isProject="false"
    nome="usuário"
    @editar="edit"
    @remover="remove"
    @new="showNew = true"
    @clicked="edit"
  ></om-table>
</template>

<script>
import omTable from "@/components/omTable.vue";
import modalConfirm from "@/components/modalConfirm.vue";
import modalUser from "@/components/modalUser.vue";
import {
  updateUser,
  createUser,
  getUsers,
  deleteUser,
} from "@/services/users.js";
export default {
  name: "Users",
  components: {
    omTable,
    modalConfirm,
    modalUser,
  },

  data() {
    return {
      selected: null,
      showConfirm: false,
      showEdit: false,
      showNew: false,
      headers: [
        " ",
        "Nome de usuário",
        "email",
        "Nome",
        "Sobrenome",
        "criado em",
        "Tipo de usuário",
        "Id",
      ],
      usuarios: null,
    };
  },
  computed: {},
  watch: {},
  mounted() {
    this.getThem();
  },
  methods: {
    async getThem() {
      try {
        const response = await getUsers();
        this.usuarios = response.users;
      } catch (error) {
        console.error("Ocorreu um erro ao buscar os usuários:", error);
      }
    },
    async createHim() {
      try {
        const response = await createUser();
      } catch (error) {
        console.error("Ocorreu um erro ao criar os usuários:", error);
      }
    },
    async deletethisUser() {
      try {
        const response = await deleteUser(this.selected.id);
        if (response.success) {
          this.usuarios.splice(this.usuarios.indexOf(this.selected), 1);
        }
      } catch (error) {
        console.error("Erro ao deletar o usuário:", error);
      }
    },
    async updatethisUser(user) {
      try {
        const data = await updateUser(user);
        if (data.success) {
          this.$emit("updated", this.user);
        } 
      } catch (error) {
        console.error("Ocorreu um erro ao atualizar usuario:", error);
      }
    },
    async createthisUser(userData) {
      try {
        const data = await createUser(userData);
        if (data.success) {
          this.$emit("created", this.user);
          this.closeModal()
        }
      } catch (error) {
        console.error("Ocorreu um erro ao criar usuario:", error);
      }
    },
    edit(item) {
      this.selected = item;
      this.showEdit = true;
    },
    remove(item) {
      this.selected = item;
      this.showConfirm = true;
    },
    closeModal() {
      this.selected = null;
      this.showConfirm = false;
      this.showEdit = false;
      this.showNew = false;
    },
  },
};
</script>
