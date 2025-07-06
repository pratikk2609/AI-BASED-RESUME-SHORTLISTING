import { createApp } from 'vue'; // Import createApp for Vue 3
import App from './App.vue';
import router from './router';

createApp(App)
  .use(router) // Use the router instance
  .mount('#app');
