<template>
  <div class="container mt-5">
    <h2>Profile Details</h2>
    <p>
      This page will show full details for profile ID: {{ $route.params.id }}
    </p>
  </div>
</template>

<script>
export default {
  name: "ProfileDetailsView",
};
</script>
