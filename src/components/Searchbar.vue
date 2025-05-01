<template>
  <div class="search-bar">
    <form @submit.prevent="search" class="search-form">
      <div class="search-fields">
        <div class="search-input-group">
          <input
            type="text"
            v-model="searchParams.name"
            placeholder="Name"
            class="search-input"
          />
          <div class="search-icon">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="16"
              height="16"
              fill="currentColor"
              viewBox="0 0 16 16"
            >
              <path
                d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001q.044.06.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1 1 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0z"
              />
            </svg>
          </div>
        </div>
        <div class="search-input-group">
          <input
            type="number"
            v-model="searchParams.birthYear"
            placeholder="Birth Year"
            class="search-input"
            min="1900"
            max="2010"
          />
        </div>
        <div class="search-input-group">
          <select v-model="searchParams.sex" class="search-input">
            <option value="">Select Sex</option>
            <option value="male">Male</option>
            <option value="female">Female</option>
            <option value="other">Other</option>
          </select>
        </div>
        <div class="search-input-group">
          <select v-model="searchParams.race" class="search-input">
            <option value="">Select Race</option>
            <option value="asian">Asian</option>
            <option value="black">Black</option>
            <option value="hispanic">Hispanic</option>
            <option value="white">White</option>
            <option value="other">Other</option>
          </select>
        </div>
      </div>
      <div class="search-buttons">
        <button type="submit" class="search-btn">Search</button>
        <button type="button" @click="resetSearch" class="reset-btn">
          Reset
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
      type: [String, Number, null], // Add null as a valid type
      default: null,
    },
  },
  data() {
    return {
      searchParams: {
        name: "",
        birthYear: "",
        sex: "",
        race: "",
      },
    };
  },
  methods: {
    search() {
      this.$emit("search", this.searchParams);
    },
    resetSearch() {
      this.searchParams = {
        name: "",
        birthYear: "",
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
