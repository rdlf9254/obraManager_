<template>
  <div class="s6xl">
    <h1>{{ titulo }}</h1>
    <hr />
    <input-text type="text" v-model="searchTerm" :placeholder="'Pesquisar ' + nome + '...'" />
    <om-button class="t2xl" @click="this.$emit('new')" v-if="isAdm">
      Novo {{ nome }}
    </om-button>
    <table class="t2xl">
      <thead>
        <tr>
          <th v-for="header in headers" :key="header">{{ header }}</th>
          <th v-if="isAdm">Ação</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="row in filteredRows" :key="row.id" style="cursor: pointer">
          <td v-for="(field, fieldName) in row" :key="fieldName" @click="clicked(row)">
            <div v-if="fieldName === 'usePhoto' && !isProject">
              <img v-if="field" :src="field" alt="User Photo" width="50" height="50" />
              <img v-else src="@/assets/nouser.jpg" alt="Default User Photo" width="50" height="50" />
            </div>

            <div v-else>
              {{ identifyType(fieldName, field) }}
            </div>
          </td>
          <td class="flex w100" v-if="isAdm">
            <om-button hierarchy="terciary" @click="editar(row)" icon="uil uil-edit"></om-button>
            <om-button hierarchy="terciary" @click="remover(row)" icon="uil uil-trash-alt" class="lxl"></om-button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { mapState } from "vuex";
import { date } from "@/services/filters.js";
import omButton from "@/components/omButton.vue";
import inputText from "@/components/input/inputText.vue";

const UserTypeMap = {
  1: "Administrador",
  2: "Engenheiro",
  3: "MestreObras",
  4: "Cliente",
};

export default {
  name: "om-table",
  components: {
    omButton,
    inputText,
  },
  props: ["titulo", "nome", "dados", "headers", "isProject"],
  data() {
    return {
      searchTerm: "",
    };
  },
  mounted() { },
  computed: {
    ...mapState({
      user: (state) => state.user,
    }),

    filteredRows() {
      if (!this.dados) return [];

      let rows = this.searchTerm
        ? this.dados.filter((row) =>
          Object.values(row).some((val) =>
            val
              .toString()
              .toLowerCase()
              .includes(this.searchTerm.toLowerCase())
          )
        )
        : this.dados;

      rows = rows.map((row) => {
        const { id, usePhoto, ...rest } = row;
        return { usePhoto, ...rest, id };
      });

      return rows;
    },
  },

  methods: {
    editar(item) {
      this.$emit("editar", item);
    },
    remover(item) {
      this.$emit("remover", item);
    },
    clicked(item) {
      this.$emit("clicked", item);
    },
    isAdm() {
      this.user.type == "Administrador";
    },
    identifyType(fieldName, fieldValue) {
      const dateFields = [
        "created_at",
        "updated_at",
        "date_joined",
        "createdAt",
        "lastUpdate",
      ];
      if (dateFields.includes(fieldName)) {
        return this.formatDate(fieldValue);
      } else if (fieldName === "useType") {
        return UserTypeMap[fieldValue] || "desconhecido";
      } else if (fieldName === "usePhoto") {
        return "";
      } else {
        return fieldValue;
      }
    },
    formatDate(value) {
      return date(value);
    },
  },
};
</script>

<style lang="scss" scoped>
img {
  border-radius: 50%;
}
</style>
