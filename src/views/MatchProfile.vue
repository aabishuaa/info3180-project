<template>
  <div class="container main-container">
    <div class="match-header-section mb-4">
      <!-- Added Back to Profiles Button -->
      <a @click="$router.back()" class="back-btn">
        <i class="fa fa-arrow-left"></i> Back
      </a>

      <h1 class="text-center">Your Matches</h1>
      <h3 class="text-center profile-name">{{ profileName }}</h3>

      <div class="match-count-badge" v-if="matches.length > 0">
        <i class="fa fa-fire"></i>
        <span
          >{{ matches.length }} Match{{
            matches.length !== 1 ? "es" : ""
          }}
          Found</span
        >
      </div>
    </div>

    <div v-if="message" class="alert" :class="messageClass" role="alert">
      {{ message }}
    </div>

    <div v-if="loading" class="text-center my-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="mt-2">Finding your matches...</p>
    </div>

    <div v-else>
      <div v-if="matches.length === 0" class="alert alert-info">
        <i class="fa fa-info-circle me-2"></i>
        No matches found for your profile criteria. Try updating your profile to
        find more matches.
      </div>

      <div v-else class="matches-grid">
        <div v-for="profile in matches" :key="profile.id" class="match-card">
          <div class="match-card-image">
            <!-- Fixed profile photo display -->
            <img
              v-if="profile.photo"
              :src="getPhotoUrl(profile.photo)"
              :alt="profile.name || 'Profile'"
            />
            <div v-else class="default-match-image">
              <i class="fa fa-user-circle"></i>
            </div>
            <div class="match-badge">
              <i class="fa fa-fire"></i> {{ profile.matches || 0 }}
            </div>
          </div>

          <div class="match-card-content">
            <h4 class="match-name">
              {{ profile.name || profile.description }}
            </h4>

            <div class="match-highlights">
              <div class="highlight-item">
                <i class="fa fa-birthday-cake"></i>
                <span>{{ calculateAge(profile.birth_year) }} years</span>
              </div>
              <div class="highlight-item">
                <i class="fa fa-map-marker"></i>
                <span>{{ profile.parish || "N/A" }}</span>
              </div>
              <div class="highlight-item">
                <i class="fa fa-ruler-vertical"></i>
                <span>{{ formatHeight(profile.height) }}</span>
              </div>
            </div>

            <p class="match-description">{{ profile.description }}</p>

            <router-link
              :to="`/profiles/${profile.id}`"
              class="btn btn-primary view-btn"
            >
              <i class="fa fa-user"></i> View Profile
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import apiClient from "@/api.js";
import defaultProfile from "@/assets/defaultProfileImg.png"; // Import default profile image

export default {
  name: "MatchProfiles",
  data() {
    return {
      profileId: this.$route.params.profile_id,
      profileName: "",
      myProfile: null,
      matches: [],
      message: "",
      messageClass: "",
      loading: true,
      currentYear: new Date().getFullYear(),
      defaultProfile: defaultProfile, // Add default profile image
    };
  },
  created() {
    this.fetchMatches();
  },
  mounted() {
    const cachedMatches = localStorage.getItem(`matches_${this.profileId}`);
    if (cachedMatches) {
      try {
        this.matches = JSON.parse(cachedMatches);
        this.loading = false;
      } catch (e) {
        console.error("Error parsing cached matches:", e);
      }
    }
  },
  methods: {
    // Improved method to correctly build photo URL
    getPhotoUrl(photoPath) {
      if (!photoPath) {
        return this.defaultProfile; // Return default profile image when no photo
      }

      // Check if the path already contains the full URL
      if (photoPath.startsWith("http")) {
        return photoPath;
      }

      // Handle paths that might start with /api/uploads/
      if (photoPath.startsWith("/api/uploads/")) {
        return `${apiClient.defaults.baseURL}${photoPath}`;
      }

      // Otherwise construct the URL from the base URL
      return `${apiClient.defaults.baseURL}/api/uploads/${photoPath}`;
    },

    fetchMatches() {
      const token = localStorage.getItem("token");
      const userId = localStorage.getItem("user_id");

      if (!token || !userId) {
        this.$router.push("/login");
        return;
      }

      apiClient
        .get(`/api/profiles/${this.profileId}`)
        .then((response) => {
          console.log("My profile data:", response.data);
          this.myProfile = response.data.profile || response.data;
          this.profileName =
            this.myProfile.name ||
            this.myProfile.description ||
            `Profile #${this.profileId}`;

          return apiClient.get(`/api/profiles/matches/${this.profileId}`);
        })
        .then((response) => {
          console.log("Matches response:", response.data);
          this.matches = response.data.matches || response.data || [];

          // Check if matches exist but under different property
          if (
            this.matches.length === 0 &&
            response.data &&
            typeof response.data === "object"
          ) {
            for (const key in response.data) {
              if (Array.isArray(response.data[key])) {
                this.matches = response.data[key];
                break;
              }
            }
          }

          // Cache matches in localStorage
          try {
            localStorage.setItem(
              `matches_${this.profileId}`,
              JSON.stringify(this.matches)
            );
          } catch (e) {
            console.error("Error caching matches:", e);
          }

          this.loading = false;
        })
        .catch((error) => {
          console.error("Error fetching matches:", error);
          this.message =
            error.response?.data?.message ||
            error.message ||
            "Failed to load matches";
          this.messageClass = "alert-danger";
          this.loading = false;
        });
    },

    calculateAge(birthYear) {
      if (!birthYear) return "N/A";
      return this.currentYear - birthYear;
    },

    // Updated formatHeight method to handle inches correctly
    formatHeight(height) {
      if (height === null || height === undefined) {
        return "Not specified";
      }

      // Check if the value is likely in inches (above 12)
      if (height > 12) {
        // Convert from inches to feet and inches
        const ft = Math.floor(height / 12);
        const inch = Math.round(height % 12);
        return `${ft}'${inch}"`;
      } else {
        // Original logic - assume the value is already in feet
        const ft = Math.floor(height);
        const inch = Math.round((height - ft) * 12);
        return `${ft}'${inch}"`;
      }
    },
  },
};
</script>

<style scoped>
/* Import Poppins font to match home view */
@import url("https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap");

/* Define color variables from home view */
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

.main-container {
  padding: 2rem;
  background-color: #f9fafb;
  min-height: 100vh;
}

/* Added Back Button Styles */
.back-btn {
  position: absolute;
  left: 20px;
  top: 20px;
  background-color: #f8f9fa;
  color: var(--teal);
  border: 2px solid var(--teal);
  padding: 8px 16px;
  border-radius: 30px;
  display: inline-flex;
  align-items: center;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s ease;
}

.back-btn:hover {
  background-color: var(--teal);
  color: white;
  transform: translateX(-3px);
}

.back-btn i {
  margin-right: 8px;
}

.match-header-section {
  text-align: center;
  padding: 20px 0;
  position: relative;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  margin-bottom: 30px;
}

.match-header-section h1 {
  font-size: 2.2rem;
  font-weight: 700;
  margin-bottom: 10px;
  background: linear-gradient(45deg, var(--teal), var(--coral));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.match-header-section .profile-name {
  color: #333;
  font-size: 1.5rem;
  margin-bottom: 20px;
}

.match-count-badge {
  background: linear-gradient(135deg, var(--teal), var(--coral));
  color: white;
  display: inline-flex;
  align-items: center;
  padding: 8px 20px;
  border-radius: 50px;
  font-weight: bold;
  box-shadow: 0 4px 12px rgba(4, 172, 176, 0.3);
}

.match-count-badge i {
  margin-right: 8px;
  font-size: 1.2rem;
  animation: flame 1.5s infinite alternate;
}

@keyframes flame {
  0% {
    transform: scale(1);
    opacity: 0.8;
  }
  100% {
    transform: scale(1.2);
    opacity: 1;
  }
}

.matches-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 2rem;
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.match-card {
  border-radius: 16px;
  overflow: hidden;
  background: white;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
  display: flex;
  flex-direction: column;
}

.match-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
}

.match-card-image {
  height: 180px;
  position: relative;
  overflow: hidden;
}

.match-card-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.6s;
}

.match-card:hover .match-card-image img {
  transform: scale(1.05);
}

.default-match-image {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(145deg, #e6e6e6, #f5f5f5);
}

.default-match-image i {
  font-size: 60px;
  color: #cccccc;
}

.match-badge {
  position: absolute;
  top: 15px;
  right: 15px;
  background: rgba(4, 172, 176, 0.9);
  color: white;
  padding: 5px 12px;
  border-radius: 20px;
  font-weight: bold;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.match-badge i {
  margin-right: 5px;
  animation: flame 1.5s infinite alternate;
}

.match-card-content {
  padding: 20px;
  display: flex;
  flex-direction: column;
  flex: 1;
}

.match-name {
  font-size: 1.3rem;
  font-weight: 600;
  color: var(--teal);
  margin-bottom: 15px;
}

.match-highlights {
  display: flex;
  flex-wrap: wrap;
  margin-bottom: 15px;
  gap: 8px;
}

.highlight-item {
  background-color: #f0f8f1;
  color: #2c3e50;
  padding: 5px 12px;
  border-radius: 20px;
  font-size: 0.85rem;
  display: flex;
  align-items: center;
}

.highlight-item i {
  margin-right: 6px;
  color: var(--teal);
}

.match-description {
  color: #555;
  font-size: 0.95rem;
  margin-bottom: 20px;
  line-height: 1.5;
  max-height: 60px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  flex: 1;
}

.view-btn {
  background: linear-gradient(45deg, var(--teal), var(--coral));
  border: none;
  padding: 10px;
  border-radius: 50px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s ease;
  color: white;
  font-size: 1rem;
  text-align: center;
  box-shadow: 0 4px 15px rgba(4, 172, 176, 0.3);
}

.view-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(4, 172, 176, 0.4);
}

.view-btn i {
  margin-right: 5px;
}

/* Responsive styles */
@media (max-width: 768px) {
  .matches-grid {
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
    padding: 1rem;
  }

  .match-card-image {
    height: 160px;
  }

  .back-btn {
    position: relative;
    left: 0;
    top: 0;
    margin-bottom: 20px;
    display: inline-flex;
  }
}

@media (max-width: 576px) {
  .match-header-section h1 {
    font-size: 1.8rem;
  }

  .match-header-section .profile-name {
    font-size: 1.2rem;
  }

  .highlight-item {
    font-size: 0.8rem;
  }

  .match-badge {
    font-size: 0.8rem;
    padding: 4px 10px;
  }
}
</style>
