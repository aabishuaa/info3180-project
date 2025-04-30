<!-- src/components/Logout.vue -->
<template>
  <div class="text-center py-5">
    <div class="spinner-border" role="status" v-if="isLoggingOut">
      <span class="visually-hidden">Loading...</span>
    </div>
    <p v-else>You have been logged out successfully.</p>
    <router-link to="/login" class="btn btn-primary mt-3"
      >Login again</router-link
    >
  </div>
</template>

<script>
import apiClient from "@/api.js";

export default {
  name: "Logout",
  data() {
    return {
      isLoggingOut: true,
    };
  },
  created() {
    this.logout();
  },
  methods: {
    logout() {
      const token = localStorage.getItem("token");

      if (token) {
        apiClient
          .post("api/auth/logout")
          .catch((error) => {
            console.error(
              "Error during logout:",
              error.response?.data || error.message
            );
          })
          .finally(() => {
            localStorage.removeItem("token");
            localStorage.removeItem("user_id");
            this.isLoggingOut = false;
          });
      } else {
        this.isLoggingOut = false;
      }
    },
  },
};
</script>
