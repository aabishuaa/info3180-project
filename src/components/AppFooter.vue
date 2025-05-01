<template>
  <footer class="footer">
    <p>&copy; {{ year }} JAM Date. All rights reserved.</p>
  </footer>
</template>

<script setup>
import { ref } from "vue";

const year = new Date().getFullYear();
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;700&display=swap");

:root {
  --teal: #04acb0;
  --orange: #fb9623;
  --yellow: #ffbd0f;
  --coral: #ff7455;
}

.footer {
  background: linear-gradient(135deg, #04acb0, #ff7455);
  color: white;
  padding: 1rem; /* Reduced from 2rem to 1rem */
  text-align: center;
  position: relative;
  z-index: 5;
  box-shadow: 0 -4px 12px rgba(0, 0, 0, 0.1);
  margin-top: 3rem;
  font-family: "Poppins", sans-serif;
  font-size: 0.9rem; /* Added to make the text slightly smaller */
}
</style>
