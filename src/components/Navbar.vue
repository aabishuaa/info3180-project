<template>
  <header class="site-header navbar navbar-expand-lg">
    <div class="container-fluid">
      <div class="logo-container">
        <img :src="logoSrc" alt="Jam-Date Logo" class="logo-img" />
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
          <li v-if="auth.isAuthenticated" class="nav-item">
            <router-link class="nav-link" :to="`/users/${auth.userId}`"
              >My Profile</router-link
            >
          </li>
          <li v-if="auth.isAuthenticated" class="nav-item">
            <router-link class="nav-link" to="/profiles/favourites"
              >Favourites</router-link
            >
          </li>
        </ul>

        <ul class="navbar-nav nav-links">
          <li v-if="!auth.isAuthenticated" class="nav-item">
            <router-link class="nav-link" to="/login">Login</router-link>
          </li>
          <li v-if="!auth.isAuthenticated" class="nav-item">
            <router-link class="nav-link" to="/register">Register</router-link>
          </li>
          <li v-if="auth.isAuthenticated" class="nav-item">
            <a class="nav-link" style="cursor: pointer" @click="logout"
              >Logout</a
            >
          </li>
        </ul>
      </div>
    </div>
  </header>
</template>

<script setup>
import { auth } from "@/auth.js";
import { useRouter } from "vue-router";
import { ref } from "vue";
import jamdateLogo from "@/assets/jamdateLogo.png";

const router = useRouter();
const logoSrc = ref(jamdateLogo);

function logout() {
  localStorage.removeItem("token");
  localStorage.removeItem("user_id");

  auth.isAuthenticated = false;
  auth.userId = null;

  router.push("/login");
}
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;700&display=swap");

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
  font-family: "Poppins", sans-serif;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.logo-container {
  display: flex;
  align-items: center;
}

.logo-img {
  width: 40px;
  height: 40px;
  object-fit: contain;
  display: block; /* Ensure it's displayed as a block element */
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
  background-image: url("data:image/svg+xml;charset=utf8,%3Csvg viewBox='0 0 30 30' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath stroke='rgba(255,255,255,0.7)' stroke-width='2' d='M4 7h22M4 15h22M4 23h22'/%3E%3C/svg%3E");
}
</style>
