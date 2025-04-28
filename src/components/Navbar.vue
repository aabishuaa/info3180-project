<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container-fluid">
      <router-link class="navbar-brand" to="/">Jam-Date</router-link>

      <div class="collapse navbar-collapse">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <router-link class="nav-link" to="/">Home</router-link>
          </li>
          <li v-if="!isAuthenticated" class="nav-item">
            <router-link class="nav-link" to="/login">Login</router-link>
          </li>
          <li v-if="!isAuthenticated" class="nav-item">
            <router-link class="nav-link" to="/register">Register</router-link>
          </li>

          <!-- Temporary full access nav -->
          <li class="nav-item">
            <router-link class="nav-link" to="/profiles/new"
              >New Profile</router-link
            >
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/profiles/favourites"
              >Favourites</router-link
            >
          </li>
          <li class="nav-item">
            <router-link class="nav-link" :to="`/users/${testUserId}`"
              >My Profile</router-link
            >
          </li>
        </ul>

        <button
          v-if="isAuthenticated"
          class="btn btn-outline-danger"
          @click="logout"
        >
          Logout
        </button>
      </div>
    </div>
  </nav>
</template>

<script>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";

export default {
  name: "Navbar",
  setup() {
    const isAuthenticated = ref(false);
    const router = useRouter();

    const checkAuth = () => {
      isAuthenticated.value = !!localStorage.getItem("token");
    };

    const logout = () => {
      localStorage.removeItem("token");
      isAuthenticated.value = false;
      router.push("/");
    };

    const testUserId = 1; // Change this if needed to match your logged-in user

    onMounted(checkAuth);

    return { isAuthenticated, logout, testUserId };
  },
};
</script>
