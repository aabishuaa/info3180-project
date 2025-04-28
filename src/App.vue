<!-- src/App.vue -->
<template>
  <div id="app">
    <AppHeader />

    <!-- Use container wrapper only when the current route component needs it -->
    <component
      v-if="!$route.meta.needsContainer && !currentComponentNeedsContainer"
      :is="$route.matched[0]?.components?.default"
    />

    <div v-else class="container mt-4">
      <component :is="$route.matched[0]?.components?.default" />
    </div>

    <AppFooter />
  </div>
</template>

<script>
import AppHeader from "./components/AppHeader.vue";
import AppFooter from "./components/AppFooter.vue";

export default {
  name: "App",
  components: {
    AppHeader,
    AppFooter,
  },
  computed: {
    currentComponentNeedsContainer() {
      const currentComponent = this.$route.matched[0]?.components?.default;
      return currentComponent && currentComponent.needsContainer !== false;
    },
  },
};
</script>

<style>
/* Global styles */
:root {
  --teal: #04acb0;
  --orange: #fb9623;
  --yellow: #ffbd0f;
  --coral: #ff7455;
}

body {
  font-family: "Poppins", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
    "Helvetica Neue", Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  background-color: #ffffff;
  margin: 0;
  padding: 0;
  min-height: 100vh;
  overflow-x: hidden;
}

#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.container {
  flex: 1;
}

h1,
h2,
h3,
h4,
h5,
h6 {
  font-weight: 700;
}

/* Override Bootstrap button styles to match our theme */
.btn-primary {
  background: linear-gradient(45deg, var(--teal), var(--coral));
  border: none;
  box-shadow: 0 4px 15px rgba(4, 172, 176, 0.3);
  transition: all 0.3s ease;
}

.btn-primary:hover,
.btn-primary:focus {
  background: linear-gradient(45deg, var(--coral), var(--teal));
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(4, 172, 176, 0.4);
}

.btn-outline-primary {
  color: var(--teal);
  border: 2px solid var(--teal);
  background: transparent;
  transition: all 0.3s ease;
}

.btn-outline-primary:hover,
.btn-outline-primary:focus {
  background: linear-gradient(45deg, var(--teal), var(--coral));
  color: white;
  border-color: transparent;
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(4, 172, 176, 0.4);
}

/* Card styling */
.card {
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  border: none;
}

.card:hover {
  transform: translateY(-10px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.15);
}

.card-title {
  color: var(--teal);
}

/* Form controls */
.form-control:focus {
  border-color: var(--teal);
  box-shadow: 0 0 0 0.25rem rgba(4, 172, 176, 0.25);
}

/* Add animations for page transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter,
.fade-leave-to {
  opacity: 0;
}
</style>
