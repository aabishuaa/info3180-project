<template>
  <div class="home">
    <!-- Search Section -->
    <section class="search-section py-4">
      <SearchBar v-model="searchQuery" @submit="handleSearch" />
    </section>

    <!-- Hero Section with Sparkles -->
    <section class="hero">
      <div class="sparkle-container">
        <div v-for="n in 50" :key="n" class="sparkle"></div>
      </div>
      <div class="hero-content">
        <h1>Welcome to Jam-Date</h1>
        <p>
          Jam-Date is a dating application that helps users find compatible
          matches based on interests, preferences, and personalities.
        </p>
        <div class="btn-container">
          <template v-if="!isAuthenticated">
            <router-link to="/register" class="btn btn-primary"
              >Sign Up</router-link
            >
            <router-link to="/login" class="btn btn-outline">Login</router-link>
          </template>
          <template v-else>
            <router-link :to="`/users/${userId}`" class="btn btn-primary">
              View Your Profile
            </router-link>
          </template>
        </div>
      </div>
    </section>

    <!-- Profiles Section -->
    <section class="profiles-section" v-if="isAuthenticated">
      <h2 class="section-title" v-if="profilesToShow.length">
        {{ searchQuery ? "Search Results" : "Latest Profiles" }}
      </h2>

      <div class="profiles-grid" v-if="profilesToShow.length">
        <div
          class="profile-card"
          v-for="profile in profilesToShow"
          :key="profile.id"
        >
          <img
            :src="
              profile.photo
                ? `${uploadBase}/api/uploads/${profile.photo}`
                : defaultProfile
            "
            :alt="profile.user?.name || 'Profile'"
            class="profile-img"
          />
          <div class="profile-details">
            <h3 class="profile-name">{{ profile.user?.name || "User" }}</h3>
            <p class="profile-description">{{ profile.description }}</p>
            <router-link :to="`/profiles/${profile.id}`" class="profile-link">
              View Profile
            </router-link>
          </div>
        </div>
      </div>

      <div class="empty-state" v-else>
        <p>No profiles found.</p>
      </div>
    </section>
  </div>
</template>

<script>
import apiClient from "@/api.js";
import SearchBar from "@/components/SearchBar.vue";
import defaultProfile from "@/assets/default-profile.png";

export default {
  name: "HomeView",
  components: { SearchBar },
  data() {
    return {
      allProfiles: [], // ← full list for searching
      latestProfiles: [], // ← first 4
      searchQuery: "",
      searchResults: [],
      userId: null,
    };
  },
  computed: {
    isAuthenticated() {
      return !!localStorage.getItem("token");
    },
    profilesToShow() {
      return this.searchQuery ? this.searchResults : this.latestProfiles;
    },
    uploadBase() {
      return apiClient.defaults.baseURL;
    },
    defaultProfile() {
      return defaultProfile;
    },
  },
  mounted() {
    this.userId = localStorage.getItem("user_id");
    if (this.isAuthenticated) {
      this.fetchProfiles();
    }
    this.createSparkleEffect();
  },
  methods: {
    fetchProfiles() {
      const me = parseInt(this.userId, 10);
      apiClient
        .get("/api/profiles")
        .then((res) => {
          // build the full list excluding current user
          this.allProfiles = (res.data.profiles || res.data).filter(
            (p) => p.user_id_fk !== me
          );

          // show the first 4 by default
          this.latestProfiles = this.allProfiles.slice(0, 4);
          this.searchResults = this.allProfiles;
        })
        .catch(console.error);
    },
    handleSearch() {
      const q = this.searchQuery.trim().toLowerCase();
      if (!q) {
        this.searchResults = this.allProfiles;
        return;
      }
      this.searchResults = this.allProfiles.filter((p) => {
        const desc = p.description.toLowerCase();
        const race = p.race.toLowerCase();
        const sex = p.sex.toLowerCase();
        return (
          desc.includes(q) || race.includes(q) || sex === q // ← exact match on sex
        );
      });
    },
    createSparkleEffect() {
      const container = document.querySelector(".sparkle-container");
      if (!container) return;

      const sparkles = container.querySelectorAll(".sparkle");
      const colors = ["#04acb0", "#fb9623", "#ffbd0f", "#ff7455"];

      sparkles.forEach((sparkle) => {
        sparkle.style.top = `${Math.random() * 100}%`;
        sparkle.style.left = `${Math.random() * 100}%`;
        sparkle.style.width = `${Math.random() * 4 + 1}px`;
        sparkle.style.height = `${Math.random() * 4 + 1}px`;
        sparkle.style.animationDelay = `${Math.random() * 10}s`;
        sparkle.style.animationDuration = `${Math.random() * 10 + 5}s`;

        const randomColor = colors[Math.floor(Math.random() * colors.length)];
        sparkle.style.backgroundColor = randomColor;
        sparkle.style.boxShadow = `0 0 8px 2px ${randomColor}80`;
      });
    },
  },
};
</script>
```

<style scoped>
/* Define color variables */
:root {
  --teal: #04acb0;
  --orange: #fb9623;
  --yellow: #ffbd0f;
  --coral: #ff7455;
}

.home {
  overflow-x: hidden;
}

/* Hero Section Styling */
.hero {
  background: linear-gradient(to bottom, rgb(255, 255, 255), rgb(255, 255, 255)),
    url("/api/placeholder/1800/800") center/cover;
  padding: 6rem 2rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  position: relative;
  overflow: hidden;
  min-height: 500px;
}

.hero-content {
  max-width: 800px;
  z-index: 5;
}

.hero h1 {
  font-size: , 3.5rem;
  margin-bottom: 1.5rem;
  background: linear-gradient(45deg, var(--teal), var(--coral));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-weight: 800;
}

.hero p {
  font-size: 1.2rem;
  margin-bottom: 2rem;
  color: #555;
  line-height: 1.6;
}

.btn-container {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.btn {
  padding: 0.8rem 1.8rem;
  border-radius: 50px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s ease;
  cursor: pointer;
}

.btn-primary {
  background: linear-gradient(45deg, var(--teal), var(--coral));
  color: white;
  box-shadow: 0 4px 15px rgba(4, 172, 176, 0.3);
  border: none;
}

.btn-primary:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(4, 172, 176, 0.4);
}

.btn-outline {
  background: transparent;
  color: var(--teal);
  border: 2px solid var(--teal);
}

.btn-outline:hover {
  background: linear-gradient(45deg, var(--teal), var(--coral));
  color: white;
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(4, 172, 176, 0.4);
}

/* Sparkle effect */
.sparkle-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  overflow: hidden;
  z-index: 1;
}

.sparkle {
  position: absolute;
  width: 3px;
  height: 3px;
  background-color: white;
  border-radius: 50%;
  box-shadow: 0 0 8px 2px rgba(255, 255, 255, 0.8);
  animation: sparkle 8s linear infinite;
  opacity: 0;
}

@keyframes sparkle {
  0% {
    transform: translateX(-100%);
    opacity: 0;
  }
  10% {
    opacity: 1;
  }
  90% {
    opacity: 1;
  }
  100% {
    transform: translateX(100%);
    opacity: 0;
  }
}

/* Profiles Section */
.profiles-section {
  padding: 5rem 2rem;
  background: white;
  position: relative;
  z-index: 5;
}

.section-title {
  text-align: center;
  margin-bottom: 3rem;
  color: var(--teal);
  font-size: 2.2rem;
  position: relative;
  display: inline-block;
  left: 50%;
  transform: translateX(-50%);
}

.section-title::after {
  content: "";
  display: block;
  width: 80px;
  height: 4px;
  background: linear-gradient(45deg, var(--teal), var(--coral));
  margin: 0.5rem auto 0;
  border-radius: 2px;
}

.profiles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.profile-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  position: relative;
}

.profile-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.15);
}

.profile-img {
  width: 100%;
  height: 200px;
  object-fit: contain;
  background: #f8f9fa;
  border-bottom: 1px solid #eee;
}

.profile-details {
  padding: 1.5rem;
}

.profile-name {
  font-size: 1.3rem;
  color: var(--teal);
  margin-bottom: 0.5rem;
}

.profile-description {
  color: #555;
  margin-bottom: 1.5rem;
  line-height: 1.5;
}

.profile-link {
  display: inline-block;
  background: linear-gradient(45deg, var(--teal), var(--coral));
  color: white;
  padding: 0.6rem 1.2rem;
  border-radius: 50px;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
  box-shadow: 0 4px 10px rgba(4, 172, 176, 0.2);
}

.profile-link:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 15px rgba(4, 172, 176, 0.3);
}

.empty-state {
  text-align: center;
  padding: 3rem;
  color: #888;
  font-size: 1.2rem;
}

/* Responsive Styles */
@media (max-width: 768px) {
  .hero h1 {
    font-size: 2.5rem;
  }

  .profiles-grid {
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  }
}

@media (max-width: 576px) {
  .hero h1 {
    font-size: 2rem;
  }

  .btn-container {
    flex-direction: column;
    width: 100%;
  }

  .btn {
    width: 100%;
    text-align: center;
    margin-bottom: 0.5rem;
  }
}
</style>
