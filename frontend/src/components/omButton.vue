<template>
  <button v-bind="$attrs" class="flex middle" :class="[hierarchy, size, iconPosition]" :disabled="disabled || loading"
    type="button">
    <div v-if="icon" class="icon">
      <i :class="icon"></i>
    </div>
    <span v-if="hasSlotData">
      <slot></slot>
    </span>
  </button>
</template>

<script>
export default {
  name: "om-button",
  props: {
    hierarchy: {
      type: String,
      default: "primary"
    },
    size: {
      default: "medium"
    },
    disabled: {
      default: false
    },
    icon: {
      type: String
    },
    iconPosition: {
      default: "left"
    },
    loading: {
      default: false,
      type: Boolean
    }
  },
  computed: {
    hasSlotData() {
      return this.$slots.default;
    }
  }
};
</script>

<style lang="scss" scoped>
button {

  &:disabled {
    cursor: default;
  }

  &.right {
    flex-direction: row-reverse;
    gap: var(--3sxl);
  }

  gap: var(--ss);
  font-weight: var(--txt-b);
  font-size: var(--p14);
  border-radius: var(--5sxl);
  transition: 0.2s;

  span:empty {
    display: none;
  }

  &.primary {
    background: var(--blue-d);
    color: var(--white);

    &:hover {
      background: var(--blue-d);
    }

    &:disabled {
      background: var(--blue-b);
    }
  }

  &.secondary {
    color: var(--blue-d);
    border: 1px solid;

    &:not(:disabled):hover {
      background: var(--blue-a);
    }

    &:disabled {
      color: var(--blue-b);
    }
  }

  &.terciary {
    color: var(--blue-d);

    &:not(:disabled):hover {
      background: var(--blue-a);
    }

    &:disabled {
      color: var(--blue-b);
    }
  }

  &.small {
    min-height: var(--3sxl);
    min-width: var(--3sxl);
    padding: var(--ss) var(--sm);
    font-size: var(--s12);
  }

  &.medium {
    min-height: var(--5sxl);
    min-width: var(--5sxl);
    padding: var(--sm) var(--sl);
  }

  &.large {
    min-height: var(--6sxl);
    min-width: var(--6sxl);
    padding: var(--sl) var(--sxl);
    font-size: var(--p16);
  }
}</style>
