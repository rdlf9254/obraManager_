<template>
    <div class="input-text" :class="{error : inputText=='xxx'}">
        <div class="flex middle">
            <label v-if="label" class="label" :for="label">{{label}}</label>
        </div>

        <input
            :id="label"
            :type="type"
            :disabled="disabled"
            :readonly="readonly"
            :placeholder="placeholder"
            :value="modelValue"
            @input="handleInput($event)"
            @keypress="checkKeyPath($event)"
          >
        <small class="error">Error message</small>
    </div>
</template>

<script>

export default {
  name: 'input-text',
  components: {
  },
  props: {
    type: {
        defaut: 'text'
    },
    modelValue: {
        default:'',
        type: String
    },
    placeholder: {
        required: true,
    },
    disabled: {
        default: false
    },
    readonly: {
        default: false
    },
    label: {
        type: String
    },
    status: {
        type: String
    },
    help: {
        type: String
    }
  },
  emits: ['update:modelValue', 'change', 'keypress'],
  data() {
    return {
      inputText: this.modelValue
    };
  },

  mounted() {},
  methods: {
    handleInput(event) {
      this.$emit('update:modelValue', event.target.value)
    },
    checkKeyPath(event) {
      this.$emit("keypress", event)
    }
  },
  watch: {
    value(){
      this.inputText = this.value
    }
  }
};
</script>

<style lang="scss" scoped>
.input-text {
  > small {
    display: none;
  }
  &.error > small,
  &.success > small {
    display: block;
  }
}

.label {
  margin-bottom: var(--sm);
}
</style>
