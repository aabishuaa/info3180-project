<template>
  <div class="container mt-5">
    <h2>User Profile</h2>
    <p>Viewing all profiles by user ID: {{ $route.params.id }}</p>
  </div>
</template>

<script>
export default {
  name: "UserProfileView",
};
</script>
