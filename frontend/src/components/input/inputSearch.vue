<template>
	<div class="input-search">
		<label v-if="label" :for="label">{{ label }}</label>
		<div class="search-field" :class="align">
			<input type="search" :id="label" :align="align" :disabled="disabled" :placeholder="placeholder"
				@input="handleInput($event)">
			<button><i class="uil uil-search"></i></button>
		</div>
	</div>
</template>

<script>
export default {
	name: 'input-search',
	props: {
		align: {
			defaut: 'right'
		},
		placeholder: {
			required: true,
		},
		disabled: {
			default: false,
		},
		label: {
			type: String
		},
		modelValue: {
			default: '',
			type: [Object, String]
		},
	},
	data() {
		return {
			inputText: this.modelValue
		}
	},
	emits: ['update:modelValue', 'change'],
	mounted() { },
	methods: {
		handleInput(e) {
			this.searchTimeout = window.setTimeout(() => {
				this.$emit("update:modelValue", e.target.value);
				this.$emit("change", e);
			}, 1000);
		}
	},
	watch: {
		value() {
			this.inputText = this.modelValue;
		}
	}
}
</script>

<style lang="scss" scoped>
.input-search {
	.search-field {
		position: relative;

		input {
			&:disabled {
				cursor: not-allowed;
			}

			&:disabled+button {
				opacity: .6;
				cursor: not-allowed;
			}
		}

		button {
			position: absolute;
			top: 0;
			height: 100%;
			padding: 0 var(--sl);
			color: grey
		}

		&:not(.left) {
			input {
				padding-right: var(--5sxl);

				&::-webkit-search-cancel-button {
					display: none;
				}
			}

			button {
				right: 0;
			}
		}

		&.left {
			input {
				padding-left: var(--4sxl);
			}

			input::-webkit-search-cancel-button {
				-webkit-appearance: none;
				height: 1em;
				width: 1em;
				border-radius: 50em;
				background: url(https://pro.fontawesome.com/releases/v5.10.0/svgs/solid/times-circle.svg) no-repeat 50% 50%;
				background-size: contain;
				opacity: .3;
			}

			button {
				left: 0;
			}
		}
	}

}
</style>
