import { createRouter, createWebHistory } from 'vue-router'; // Import createRouter and createWebHistory
import Login from '../components/LoginPage.vue';
import Student from '../components/StudentPage.vue';
import HR from '../components/HR.vue';

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: Login },
  { path: '/student', component: Student },
  { path: '/hr', component: HR },
];

const router = createRouter({
  history: createWebHistory(), // Use createWebHistory for Vue 3
  routes,
});

export default router;
