import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import LoginView from '../views/LoginView.vue';
import RegisterView from '../views/RegisterView.vue';
import NewProfileView from '../views/NewProfileView.vue';
import ProfileDetailsView from '../views/ProfileDetailsView.vue';
import UserProfileView from '../views/UserProfileView.vue';
import FavouritesView from '../views/FavouritesReport.vue';

const routes = [
  { path: '/', name: 'home', component: HomeView },
  { path: '/register', name: 'register', component: RegisterView },
  { path: '/login', name: 'login', component: LoginView },
  {
    path: '/profiles/new',
    name: 'new-profile',
    component: NewProfileView,
    meta: { requiresAuth: true }
  },
  {
    path: '/profiles/:id',
    name: 'profile-details',
    component: ProfileDetailsView,
    props: true
  },
  {
    path: '/users/:id',
    name: 'user-profile',
    component: UserProfileView,
    props: true,
    meta: { requiresAuth: true }
  },
  {
    path: '/profiles/favourites',
    name: 'favourites',
    component: FavouritesView,
    meta: { requiresAuth: true }
  }
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
});


router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('token');
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login');
  } else {
    next();
  }
});

export default router;
