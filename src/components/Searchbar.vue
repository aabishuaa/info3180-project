<template>
  <div class="search-bar">
    <form @submit.prevent="search" class="search-form">
      <div class="search-fields">
        <div class="search-input-group">
          <input
            type="text"
            v-model="searchParams.name"
            placeholder="Description"
            class="search-input"
          />
          <div class="search-icon">
            <i class="bi bi-search"></i>
          </div>
        </div>
        <div class="search-input-group">
          <input
            type="number"
            v-model="searchParams.birth_year"
            placeholder="Birth Year"
            class="search-input"
            min="1950"
            max="2007"
          />
        </div>
        <div class="search-input-group">
          <select v-model="searchParams.sex" class="search-input">
            <option value="">Select Sex</option>
            <option value="Male">Male</option>
            <option value="Female">Female</option>
            <option value="Other">Other</option>
          </select>
        </div>
        <div class="search-input-group">
          <select v-model="searchParams.race" class="search-input">
            <option value="">Select Race</option>
            <option value="Asian">Asian</option>
            <option value="Black">Black</option>
            <option value="Hispanic">Hispanic</option>
            <option value="White">White</option>
            <option value="Indian">Indian</option>
            <option value="Mixed">Mixed</option>
            <option value="Other">Other</option>
          </select>
        </div>
      </div>
      <div class="search-buttons">
        <button type="submit" class="search-btn">
          <i class="bi bi-search me-2"></i>Search
        </button>
        <button type="button" @click="resetSearch" class="reset-btn">
          <i class="bi bi-x-circle me-2"></i>Reset
        </button>
      </div>
    </form>
  </div>
</template>

<script>
export default {
  name: "SearchBar",
  props: {
    currentUserId: {
      type: [String, Number, null],
      default: null,
    },
  },
  data() {
    return {
      searchParams: {
        name: "",
        birth_year: "",
        sex: "",
        race: "",
      },
    };
  },
  methods: {
    search() {
      // Create a clean copy of search params, removing empty values
      const params = {};
      Object.keys(this.searchParams).forEach((key) => {
        if (this.searchParams[key]) {
          params[key] = this.searchParams[key];
        }
      });

      this.$emit("search", params);
    },
    resetSearch() {
      this.searchParams = {
        name: "",
        birth_year: "",
        sex: "",
        race: "",
      };
      this.$emit("reset");
    },
  },
};
</script>

<style scoped>
.search-bar {
  background: white;
  border-radius: 20px;
  padding: 1.5rem;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
  margin-bottom: 2rem;
}

.search-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.search-fields {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1rem;
}

.search-input-group {
  position: relative;
}

.search-input {
  width: 100%;
  padding: 0.8rem 1rem;
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 50px;
  font-size: 1rem;
  color: #333;
  transition: all 0.3s ease;
  background: #f8f9fa;
}

.search-input:focus {
  outline: none;
  border-color: #04acb0;
  box-shadow: 0 0 0 2px rgba(4, 172, 176, 0.2);
}

.search-icon {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: #888;
}

.search-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.search-btn,
.reset-btn {
  padding: 0.8rem 2rem;
  border-radius: 50px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 1rem;
  border: none;
}

.search-btn {
  background: linear-gradient(45deg, #04acb0, #ff7455);
  color: white;
  box-shadow: 0 4px 12px rgba(4, 172, 176, 0.3);
}

.search-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 15px rgba(4, 172, 176, 0.4);
}

.reset-btn {
  background: transparent;
  color: #666;
  border: 1px solid #ccc;
}

.reset-btn:hover {
  background: #f5f5f5;
  border-color: #bbb;
}

@media (max-width: 768px) {
  .search-fields {
    grid-template-columns: 1fr;
  }

  .search-buttons {
    flex-direction: column;
    width: 100%;
  }

  .search-btn,
  .reset-btn {
    width: 100%;
  }
}
</style>
