<!-- src/components/SearchBar.vue -->
<template>
  <div class="search-bar">
    <form @submit.prevent="search">
      <div class="input-group">
        <input
          type="text"
          v-model="searchInput"
          class="form-control"
          placeholder="Search by Name, Sex, or Race..."
        />
        <button type="submit" class="btn btn-primary">Search</button>
      </div>
    </form>
  </div>
</template>

<script>
export default {
  name: "SearchBar",
  props: {
    modelValue: String,
  },
  emits: ["update:modelValue", "submit"],
  data() {
    return {
      searchInput: this.modelValue,
    };
  },
  watch: {
    searchInput(newVal) {
      this.$emit("update:modelValue", newVal);
    },
  },
  methods: {
    search() {
      this.$emit("submit", this.searchInput);
    },
  },
};
</script>

<style scoped>
.search-bar {
  margin-bottom: 2rem;
  width: 100%;
}
.input-group {
  display: flex;
}
.form-control {
  flex: 1;
  padding: 12px;
  font-size: 1rem;
  border-radius: 30px;
}
.btn-primary {
  margin-left: 10px;
  border-radius: 30px;
}
</style>
