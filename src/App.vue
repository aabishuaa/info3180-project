<template>
  <div id="app">
    <Navbar />
    <router-view />
  </div>
</template>

<script>
import Navbar from "./components/Navbar.vue";

export default {
  name: "App",
  components: {
    Navbar,
  },
};
</script>

<style>
/* Optional basic styling */
body {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  background-color: #f8f9fa;
}
</style>
