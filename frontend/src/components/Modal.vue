<template>
    <section
      v-if="showModal"
      class="modal"
      :class="{
        'can-overflow': overflow,
        'upper-position': upperPosition
      }"
    >
      <div @click="!notClose ? close() : null" class="overlay"></div>
  
      <div
        v-bind:class="{
          'large-box': largebox,
          'modal-box': !largebox,
          'guide-box': guidebox,
          proPlanModal: proPlanModal,
          shareChannel: shareChannel
        }"
      >
        <a v-if="!notClose" @click="close()" class="close">×</a>
        <div v-if="title" class="title">
          <h3>{{ title }}</h3>
        </div>
  
        <div class="modal-content">
          <slot name="content"></slot>
        </div>
  
        <div class="modal-action">
          <slot name="action"></slot>
        </div>
      </div>
    </section>
  </template>
  
  <script>
  export default {
    name: "modal",
    props: {
      show: {
        default: false,
        required: true
      },
      title: {
        default: "",
        required: false
      },
      largebox: {
        default: false
      },
      guidebox: {
        default: false
      },
      proPlanModal: {
        default: false
      },
      shareChannel: {
        default: false
      },
      notClose: {
        default: false
      },
      overflow:{
        default:false
      },
      upperPosition: {
        default: false
      }
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
      close() {
        this.showModal = false;
        this.$emit("close");
      }
    }
  };
  </script>
  
  <style lang="scss" scoped>
  section.modal {
    position: fixed;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 999;
  
    &.can-overflow{
      .modal-box {
        overflow: visible;
      }
      
    }
    
    &.upper-position{
      .modal-box {
        bottom: 150px;
      }
    }
  
    @media only screen and (max-width: 1366px) {
      .button + .button {
        margin-top: 3%;
        margin-left: 0;
      }
    }
    .overlay {
      position: absolute;
      left: 0;
      top: 0;
      width: 100%;
      height: 100%;
      background: radial-gradient(circle, rgba(0, 0, 0, 0.8) 10%, rgba(0, 0, 0, 0.8) 50%, #000 100%);
      z-index: -1;
    }
    .modal-box {
      width: 90%;
      max-width: 650px;
      max-height: 95vh;
      padding: var(--4sxl) var(--5sxl);
      position: relative;
      overflow-y: scroll;
      background: var(--white);
      z-index: 99;
      box-shadow: 0 3px var(--sl) rgba(black, 0.4);
      a.close {
        font-size: var(--2sxl2);
        position: absolute;
        right: var(--sxl);
        top: var(--sm);
        cursor: pointer;
      }
  
      .title {
        text-align: center;
        margin-bottom: var(--4sxl);
        &.less-margin {
          margin-bottom: var(--2sxl2);
        }
        h3 {
          font-size: 2.3rem;
          font-weight: 600;
        }
        p {
          max-width: 500px;
          margin: 5px auto 0;
          font-size: 1.7rem;
          opacity: 0.8;
        }
  
        &.w-icon {
          i[class*="fa-"] {
            font-size: var(--4sxl);
            opacity: 0.5;
            margin-bottom: var(--sxl);
          }
          p {
            margin-top: var(--sm);
          }
        }
      }
  
      .content {
        font-size: 1.6rem;
        padding: 0 var(--sxl) var(--sm);
        text-align: center;
        line-height: 1.5;
        text-align: center;
        p + p {
          margin-top: var(--sl);
        }
        form {
          text-align: left;
        }
      }
    }
  
    .large-box {
      width: 90%;
      max-width: 1080px;
      max-height: 95vh;
      padding: var(--sxl) var(--sm);
      position: relative;
      overflow-y: scroll;
      background: var(--white);
      z-index: 99;
      box-shadow: 0 3px var(--sl) rgba(rgb(0, 0, 0), 0.4);
      a.close {
        font-size: var(--2sxl2);
        position: absolute;
        right: var(--sxl);
        top: var(--sm);
        cursor: pointer;
      }
  
      .title {
        text-align: center;
        margin-bottom: var(--sxl);
        &.less-margin {
          margin-bottom: var(--2sxl2);
        }
        h3 {
          font-size: 2.3rem;
          font-weight: 600;
        }
        p {
          max-width: 500px;
          margin: 5px auto 0;
          font-size: 1.7rem;
          opacity: 0.8;
        }
  
        &.w-icon {
          i[class*="fa-"] {
            font-size: var(--4sxl);
            opacity: 0.5;
            margin-bottom: var(--sxl);
          }
          p {
            margin-top: var(--sm);
          }
        }
      }
  
      .content {
        font-size: 1.6rem;
        padding: 0 var(--sxl) var(--sm);
        text-align: center;
        line-height: 1.5;
        text-align: center;
        p + p {
          margin-top: var(--sl);
        }
        form {
          text-align: left;
        }
      }
    }
  
    .guide-box {
      max-height: 95vh;
      max-width: 860px;
      padding: var(--sxl) var(--2sxl);
      overflow-y: auto;
  
      a.close {
        font-size: var(--2sxl2);
        position: absolute;
        right: var(--sm);
        top: 0px;
        cursor: pointer;
      }
  
      /*responsive video*/
      .video-container {
        position: relative;
        padding-bottom: 56.25%;
        overflow: hidden;
      }
      .video-container iframe,
      .video-container object,
      .video-container embed,
      .video-container .nun-clica,
      .video-container #iframao,
      .video-container .thumb {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: 1;
      }
    }
    .proPlanModal {
      padding: 0px;
    }
  
    .shareChannel {
      max-width: 1200px;
      text-align: left;
      padding: var(--4sxl) var(--5sxl) var(--sxl) var(--5sxl);
  
      .modal-content {
        .content {
          text-align: left;
        }
      }
    }
  }
  </style>