<template>
  <header class="site-header navbar navbar-expand-lg">
    <div class="container-fluid">
      <div class="logo-container">
        <svg width="40" height="40" viewBox="0 0 100 100">
          <path
            d="M50,10 C25,10 10,30 10,50 C10,80 40,90 50,90 C60,90 90,80 90,50 C90,30 75,10 50,10 Z"
            fill="none"
            stroke="#ffbd0f"
            stroke-width="4"
          />
          <path
            d="M50,15 C27,15 15,33 15,50 C15,77 42,85 50,85 C58,85 85,77 85,50 C85,33 73,15 50,15 Z"
            fill="none"
            stroke="#ff7455"
            stroke-width="4"
          />
          <path
            d="M50,20 C30,20 20,35 20,50 C20,75 45,80 50,80 C55,80 80,75 80,50 C80,35 70,20 50,20 Z"
            fill="url(#heartGradient)"
          />
          <defs>
            <linearGradient
              id="heartGradient"
              x1="0%"
              y1="0%"
              x2="100%"
              y2="100%"
            >
              <stop offset="0%" stop-color="#04acb0" />
              <stop offset="100%" stop-color="#fb9623" />
            </linearGradient>
          </defs>
        </svg>
        <router-link class="navbar-brand logo-text" to="/"
          >Jam-Date</router-link
        >
      </div>

      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNav"
        aria-controls="navbarNav"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav me-auto nav-links">
          <li class="nav-item">
            <router-link class="nav-link" to="/">Home</router-link>
          </li>
          <li v-if="isAuthenticated" class="nav-item">
            <router-link class="nav-link" :to="`/users/${userId}`"
              >My Profile</router-link
            >
          </li>
          <li v-if="isAuthenticated" class="nav-item">
            <router-link class="nav-link" to="/profiles/favourites"
              >Favourites</router-link
            >
          </li>
        </ul>

        <ul class="navbar-nav nav-links">
          <li v-if="!isAuthenticated" class="nav-item">
            <router-link class="nav-link" to="/login">Login</router-link>
          </li>
          <li v-if="!isAuthenticated" class="nav-item">
            <router-link class="nav-link" to="/register">Register</router-link>
          </li>
          <li v-if="isAuthenticated" class="nav-item">
            <a class="nav-link" style="cursor: pointer" @click="logout"
              >Logout</a
            >
          </li>
        </ul>
      </div>
    </div>
  </header>
</template>

<script>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";

export default {
  name: "AppHeader",
  setup() {
    const router = useRouter();
    const isAuthenticated = ref(false);
    const userId = ref(null);

    const checkAuth = () => {
      isAuthenticated.value = !!localStorage.getItem("token");
      const userInfo = JSON.parse(localStorage.getItem("user") || "{}");
      userId.value = userInfo.id || null;
    };

    const logout = () => {
      localStorage.removeItem("token");
      localStorage.removeItem("user");
      isAuthenticated.value = false;
      router.push("/login");
    };

    onMounted(checkAuth);

    return { isAuthenticated, userId, logout };
  },
};
</script>

<style scoped>
:root {
  --teal: #04acb0;
  --orange: #fb9623;
  --yellow: #ffbd0f;
  --coral: #ff7455;
}

.site-header {
  background: linear-gradient(135deg, #04acb0, #ff7455);
  padding: 1rem 2rem;
  position: relative;
  z-index: 10;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.logo-container {
  display: flex;
  align-items: center;
}

.logo-text {
  font-size: 1.8rem;
  font-weight: 700;
  color: white;
  margin-left: 0.5rem;
  text-decoration: none;
}

.nav-links {
  display: flex;
  gap: 1.5rem;
}

.nav-link {
  color: white;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
}

.nav-link:hover {
  color: #ffbd0f;
}

.navbar-toggler {
  border-color: white;
}

.navbar-toggler-icon {
  background-image: url("data:image/svg+xml;charset=utf8,%3Csvg viewBox='0 0 30 30' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath stroke='rgba%28255, 255, 255, 0.7%29' stroke-width='2' d='M4 7h22M4 15h22M4 23h22'/%3E%3C/svg%3E");
}
</style>
