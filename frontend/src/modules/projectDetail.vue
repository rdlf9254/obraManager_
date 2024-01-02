<template>
  <div class="s6xl">
    <div class="flex row middle">
      <h1>
        <span
          @click="routerTo('Projects')"
          style="color: var(--grey-d); cursor: pointer"
          >Projetos ></span
        >
        {{ project.proName }}
      </h1>
      <div class="flex-1"></div>
      <div class="box flex row between pss">
        <span>Status:</span><span>{{ STATUS_CHOICES[project.proStatus] }}</span>
      </div>
    </div>
    <hr />
    <div class="project-info">
      <div class="top-infos flex row tm stretch">
        <div class="box sm psl mh" style="max-width: 100%">
          <h3>Progresso Geral</h3>
          <hr />
          <div class="doughnut-wrapper">
            <doughnut-chart
              v-if="loaded"
              :chartData="chartOneData"
              :chartOptions="chartOneOpt"
            ></doughnut-chart>
            <h1 class="perc" style="position: absolute">
              {{ project.proGeneralProgress }}%
            </h1>
          </div>
        </div>
        <div class="box sm psl mh">
          <h3>Etapas Completas</h3>
          <hr />
          <div class="doughnut-wrapper">
            <doughnut-chart
              v-if="loaded"
              :chartData="chartTwoData"
              :chartOptions="chartOneOpt"
            ></doughnut-chart>
            <h1 class="perc" style="position: absolute">
              {{ project.proDoneTasks }}
            </h1>
          </div>
        </div>
        <div class="box sm psl mh">
          <h3>Orçamento</h3>
          <hr />
          <line-chart
            v-if="loaded"
            :chartData="chartLineData"
            :chartOptions="chartTwoOpt"
            class="h100"
          ></line-chart>
        </div>
      </div>
      <div class="flex row tm">
        <div class="box sm psl">
          <div class="flex row between">
            <div class="info-area">
              <h5>Responsável</h5>
              <p class="ts">{{ responsible }}</p>
            </div>
            <div class="info-area flex row">
              <div class="flex column">
                <h5>Estágio Atual</h5>
                <p class="ts">
                  {{ STAGE_CHOICES[project.proStage] }}
                </p>
              </div>
              <div class="percent h100 flex middle l6xl">
                {{ project.proStageProgress }}%
              </div>
            </div>
            <div class="info-area">
              <h5>Próximo Estágio:</h5>
              <p class="ts">
                {{ STAGE_CHOICES[project.proStage + 1] }}
              </p>
            </div>
          </div>
          <div class="photos tm">
            <h5>Fotos</h5>
            <div
              v-if="!project.photos || project.photos.length === 0"
              class="empty-photos"
            >
              <i class="uil uil-image"></i>
              <h4>Nenhuma foto disponível</h4>
            </div>
            <div v-else class="photo-gallery">
              <div
                class="photo-item"
                v-for="photo in project.photos"
                :key="photo.id"
              >
                <img :src="photo.url" alt="Foto do Projeto" />
              </div>
            </div>
          </div>
          <div class="flex row end">
            <om-button hierarchy="secondary" @click="addPhoto()"
              >Adicionar foto</om-button
            >
            <om-button class="lm" @click="routerTo('Projects')"
              >Voltar</om-button
            >
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { date, money } from "@/services/filters.js";
import {
  getProjectById,
  getNamebyId,
  uploadPhoto,
} from "@/services/projects.js";
import LineChart from "@/components/graficos/linechart.vue";
import DoughnutChart from "@/components/graficos/doughnut.vue";
import omButton from "@/components/omButton.vue";

export default {
  name: "project-detail",
  components: {
    LineChart,
    DoughnutChart,
    omButton,
  },
  data() {
    return {
      project: {},
      loaded: false,
      chartOneData: {},
      chartTwoData: {},
      chartOneOpt: {
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
          legend: {
            display: false,
          },
        },
        tooltips: {
          enabled: false,
        },
        elements: {
          line: {
            borderWidth: 10,
          },
        },
      },
      chartTwoOpt: {
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
          legend: {
            display: false,
          },
        },
      },

      responsible: "-",
      STAGE_CHOICES: [
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
      ],
      STATUS_CHOICES: ["No Prazo", "Concluído", "Atrasado"],
      chartOneData: {},
    };
  },
  mounted() {
    this.loadProject();
  },
  methods: {
    async loadProject() {
      try {
        const id = this.$route.params.id;
        let resposta = await getProjectById(id);
        this.project = resposta.data;
        this.getName(resposta.data.proResponsible);
        this.chartLineData = this.covertDataForGraph(this.project.graph_data);
        this.chartOneData = {
          labels: ["Progresso", "Restante"],
          datasets: [
            {
              backgroundColor: ["#152C70", "#c9cccf"],
              data: [
                resposta.data.proDoneTasks,
                resposta.data.proTotalTasks - resposta.data.proDoneTasks,
              ],
            },
          ],
        };
        this.chartTwoData = {
          labels: ["Feito", "Restante"],
          datasets: [
            {
              backgroundColor: ["#152C70", "#c9cccf"],
              data: [
                resposta.data.proGeneralProgress,
                100 - resposta.data.proGeneralProgress,
              ],
            },
          ],
        };
        this.loaded = true;
      } catch (error) {
        console.error("Erro ao carregar o projeto:", error);
      }
    },
    async getName(id) {
      try {
        let resposta = await getNamebyId(id);
        this.responsible = resposta.first_name + " " + resposta.last_name;
      } catch (error) {
        console.error("Erro ao carregar o projeto:", error);
      }
    },

    addPhoto() {
      let input = document.createElement("input");
      input.type = "file";
      input.accept = "image/*";
      input.onchange = async (e) => {
        let file = e.target.files[0];
        let reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = async (readerEvent) => {
          let content = readerEvent.target.result;

          let img = new Image();
          img.src = content;
          await new Promise((resolve) => (img.onload = resolve));
          let canvas = document.createElement("canvas");
          let ctx = canvas.getContext("2d");

          let minSize = 300;
          let targetWidth = 400;
          let targetHeight = 300;
          let startX = (img.width - targetWidth) / 2;
          let startY = (img.height - targetHeight) / 2;

          canvas.width = targetWidth;
          canvas.height = targetHeight;
          ctx.drawImage(
            img,
            startX,
            startY,
            targetWidth,
            targetHeight,
            0,
            0,
            targetWidth,
            targetHeight
          );

          let newContent = canvas.toDataURL();

          try {
            let response = await uploadPhoto({
              phoBase: newContent,
              phoProjId: this.$route.params.id,
            });
            if (response.data.status === "success") {
              this.project.photos.push(newContent);
            } else {
              console.error("Erro ao adicionar foto:", response.data.message);
            }
          } catch (error) {
            console.error("Erro ao enviar a foto:", error);
          }
        };
      };
      input.click();
    },
    covertDataForGraph(graph_data) {
      let dates = graph_data.map((item) => {
        let date = new Date(item.graDate);
        let monthNames = [
          "Jan",
          "Fev",
          "Mar",
          "Abr",
          "Mai",
          "Jun",
          "Jul",
          "Ago",
          "Set",
          "Out",
          "Nov",
          "Dez",
        ];
        return monthNames[date.getMonth()];
      });

      let values = graph_data.map((item) => item.graValue);
      let data = {
        labels: dates,
        datasets: [
          {
            borderColor: "rgba(75, 192, 192, 1)",
            data: values,
          },
        ],
      };

      return data;
    },
  },
};
</script>
<style lang="scss" scoped>
.box {
  background-color: white;
  width: 100%;
}
.mh {
  min-height: 310px;
}
.percent {
  font-size: xx-large;
  color: green;
}
.info-area {
  border-bottom: 1px solid var(--grey-d);
  padding-bottom: var(--ss);
}
.photos {
  .empty-photos {
    text-align: center;
    padding: var(--sxl);
    font-size: var(--sl);
    color: grey;

    i::before {
      font-size: var(--5sxl);
      margin-bottom: var(--sl);
    }
  }

  .photo-gallery {
    display: flex;
    overflow-x: auto;

    .photo-item {
      margin-right: var(--sm);

      img {
        width: 120px;
        height: 120px;
        object-fit: cover;
      }
    }
  }
}
.doughnut-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}
.top-infos {
  max-width: 100vb;
}
</style>
