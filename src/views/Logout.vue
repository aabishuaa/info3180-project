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
import axios from "axios";

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
        axios
          .post(
            "/api/auth/logout",
            {},
            {
              headers: {
                Authorization: `Bearer ${token}`,
              },
            }
          )
          .catch((error) => {
            console.error("Error during logout:", error);
          })
          .finally(() => {
            // Clear local storage regardless of API response
            localStorage.removeItem("token");
            localStorage.removeItem("user");
            this.isLoggingOut = false;
          });
      } else {
        // No token found, already logged out
        this.isLoggingOut = false;
      }
    },
  },
};
</script>
