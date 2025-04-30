<template>
  <div class="home">
    <!-- Hero Section with Sparkles -->
    <section class="hero">
      <div class="sparkle-container">
        <div v-for="n in 50" :key="n" class="sparkle"></div>
      </div>
      <div class="hero-content">
        <img :src="jamDateLogo" alt="Jam-Date Logo" class="logo" />
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
        Latest Profiles
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
import defaultProfile from "@/assets/defaultProfileImg.png";
import jamDateLogo from "@/assets/jamdateLogo.png";

export default {
  name: "HomeView",
  data() {
    return {
      jamDateLogo,
      allProfiles: [], // full list for searching
      latestProfiles: [], // the 4 most recent
      searchResults: [],
      userId: null,
    };
  },
  computed: {
    isAuthenticated() {
      return !!localStorage.getItem("token");
    },
    profilesToShow() {
      return this.latestProfiles;
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
        .get("/api/profiles", { params: { limit: 4 } })
        .then((res) => {
          this.allProfiles = (res.data.profiles || res.data).filter(
            (p) => p.user_id_fk !== me
          );
          this.latestProfiles = this.allProfiles; // already only 4
        })
        .catch(console.error);
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

<style scoped>
/* Import Poppins font */
@import url("https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap");

/* Define color variables */
:root {
  --teal: #04acb0;
  --orange: #fb9623;
  --yellow: #ffbd0f;
  --coral: #ff7455;
}

/* Apply Poppins font to all elements */
* {
  font-family: "Poppins", sans-serif;
}

.home {
  overflow-x: hidden;
}

/* Logo Styling */
.logo {
  max-width: 220px;
  margin-bottom: 1.5rem;
  filter: drop-shadow(0px 4px 8px rgba(0, 0, 0, 0.2));
}

/* Hero Section Styling - Full Screen */
.hero {
  background: #ffffff, url("/api/placeholder/1800/800") center/cover;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  position: relative;
  overflow: hidden;
  padding: 2rem;
}

.hero-content {
  max-width: 800px;
  z-index: 5;
  animation: fadeIn 1.5s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.hero h1 {
  font-size: 3.8rem;
  margin-bottom: 1.5rem;
  background: linear-gradient(45deg, var(--teal), var(--coral));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-weight: 800;
  letter-spacing: -0.5px;
}

.hero p {
  font-size: 1.3rem;
  margin-bottom: 2.5rem;
  color: #555;
  line-height: 1.7;
  font-weight: 300;
}

.btn-container {
  display: flex;
  gap: 1.5rem;
  justify-content: center;
}

.btn {
  padding: 1rem 2.2rem;
  border-radius: 50px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s ease;
  cursor: pointer;
  font-size: 1.1rem;
  letter-spacing: 0.5px;
}

.btn-primary {
  background: linear-gradient(45deg, var(--teal), var(--coral));
  color: white;
  box-shadow: 0 4px 15px rgba(4, 172, 176, 0.3);
  border: none;
}

.btn-primary:hover {
  transform: translateY(-5px);
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
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(4, 172, 176, 0.4);
  border: 2px solid transparent;
}

.logo {
  max-width: 220px;
  margin-bottom: 2rem;
  display: block;
  margin-left: auto;
  margin-right: auto;
}

/* Enhanced Sparkle effect */
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
  padding: 6rem 2rem;
  background: #f9fafb;
  position: relative;
  z-index: 5;
}

.section-title {
  text-align: center;
  margin-bottom: 3.5rem;
  color: var(--teal);
  font-size: 2.5rem;
  position: relative;
  display: inline-block;
  left: 50%;
  transform: translateX(-50%);
  font-weight: 700;
}

.section-title::after {
  content: "";
  display: block;
  width: 100px;
  height: 5px;
  background: linear-gradient(45deg, var(--teal), var(--coral));
  margin: 0.7rem auto 0;
  border-radius: 3px;
}

.profiles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 2.5rem;
  max-width: 1200px;
  margin: 0 auto;
}

.profile-card {
  background: white;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.12);
  transition: all 0.4s ease;
  position: relative;
}

.profile-card:hover {
  transform: translateY(-12px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.18);
}

.profile-img {
  width: 100%;
  height: 220px;
  object-fit: cover;
  background: #f8f9fa;
  border-bottom: 1px solid #eee;
}

.profile-details {
  padding: 1.8rem;
}

.profile-name {
  font-size: 1.5rem;
  color: var(--teal);
  margin-bottom: 0.7rem;
  font-weight: 600;
}

.profile-description {
  color: #555;
  margin-bottom: 1.8rem;
  line-height: 1.6;
  font-size: 1.05rem;
}

.profile-link {
  display: inline-block;
  background: linear-gradient(45deg, var(--teal), var(--coral));
  color: white;
  padding: 0.7rem 1.5rem;
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
  padding: 4rem;
  color: #888;
  font-size: 1.3rem;
  font-weight: 300;
}

/* Responsive Styles */
@media (max-width: 768px) {
  .hero h1 {
    font-size: 2.8rem;
  }

  .hero p {
    font-size: 1.1rem;
  }

  .profiles-grid {
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  }

  .logo {
    max-width: 180px;
  }
}

@media (max-width: 576px) {
  .hero h1 {
    font-size: 2.2rem;
  }

  .hero p {
    font-size: 1rem;
  }

  .btn-container {
    flex-direction: column;
    width: 100%;
    gap: 1rem;
  }

  .btn {
    width: 100%;
    text-align: center;
    padding: 0.9rem 1rem;
  }

  .logo {
    max-width: 150px;
  }
}
</style>
