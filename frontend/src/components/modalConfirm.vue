<template>
    <modal :title="description" :show="showModal" @close="cancel()">
      <template #action>
        <div class="action">
          <div class="buttons center">
            <a
              @click="accept()"
              class="button primary medium"
              :class="{ unusual: unusual == 'accept' }"
            >
              <span v-if="confirmtext">{{ confirmtext }}</span>
              <span v-else>Sim</span>
            </a>
            <a
              @click="cancel()"
              class="button primary medium"
              :class="{ unusual: unusual == 'cancel' }"
            >
              Não
            </a>
          </div>
        </div>
      </template>
    </modal>
  </template>
  
  <script>
  import Modal from "@/components/Modal.vue";
  
  export default {
    name: "modal-confirm",
    props: {
      confirmtext: String,
      description: {
        required: true
      },
      show: {
        required: true,
        default: false
      },
      unusual: {
        required: false,
        default: "accept"
      }
    },
    components: {
      Modal
    },
    data() {
      return {
        showModal: false
      };
    },
    watch: {
      show(value) {
        this.showModal = value;
      }
    },
    mounted() {
      this.showModal = this.show;
    },
    methods: {
      accept() {
        this.showModal = false;
        this.$emit("accept", true);
      },
      cancel() {
        this.showModal = false;
        this.$emit("cancel", true);
      }
    }
  };
  </script>
  
  <style lang="scss" scoped>
  .action {
    margin-top: var(--2sxl2);
    .button {
      margin-left: var(--sm);
    }
  }
  </style>