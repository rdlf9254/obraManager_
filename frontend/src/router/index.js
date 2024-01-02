import { createRouter, createWebHistory } from 'vue-router'
import Login from '@/modules/Login.vue'
const Projects = () => import("@/modules/Projects.vue");
const Users = () => import("@/modules/Users.vue");
const Config = () => import("@/modules/Config.vue");
const projectDetail = () => import("@/modules/projectDetail.vue");


const routes = [
  {
    path: '/',
    name: 'Login',
    component: Login
  },
  {
    path: "/projects",
    name: "Projects",
    component: Projects,
  },
  {
    path: "/projects/:id",
    component: projectDetail,
  },
  {
    path: "/users",
    name: "Users",
    component: Users,
  },
  {
    path: "/config",
    name: "Config",
    component: Config,
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router
