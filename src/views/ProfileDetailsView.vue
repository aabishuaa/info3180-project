<template>
  <div class="profile-details">
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <div v-else-if="error" class="alert alert-danger">
      {{ error }}
    </div>

    <div v-else class="container py-4">
      <!-- Improved Back navigation -->
      <button @click="goBack" class="back-btn">
        <i class="bi bi-arrow-left"></i> Back
      </button>

      <div class="card profile-card shadow">
        <!-- Profile header -->
        <div class="profile-header">
          <div class="profile-cover-container">
            <div class="profile-cover-gradient"></div>
          </div>
          <div class="profile-avatar-container">
            <img
              :src="profilePhotoUrl"
              class="profile-avatar"
              alt="Profile Photo"
            />
          </div>
          <!-- Profile action buttons - Only show if not viewing own profile -->
          <div
            v-if="!isOwnProfile"
            class="profile-action-buttons"
            :style="{ display: isOwnProfile ? 'none' : 'flex' }"
          >
            <button
              class="btn btn-favorite"
              :class="{ active: isFavorite }"
              @click="toggleFavorite"
              v-show="!isOwnProfile"
            >
              <i
                class="bi"
                :class="isFavorite ? 'bi-heart-fill' : 'bi-heart'"
              ></i>
              <span
                class="favorite-animation"
                :class="{ active: animateFavorite }"
              >
                <i class="bi bi-heart-fill"></i>
              </span>
            </button>
            <button class="btn btn-email" v-show="!isOwnProfile">
              <i class="bi bi-envelope"></i>
            </button>
          </div>
        </div>

        <div class="card-body pb-5">
          <div class="profile-info-section">
            <h2 class="profile-name">{{ profile.user.name }}</h2>
            <div class="profile-headline">{{ profile.description }}</div>
          </div>

          <!-- Biography section -->
          <div class="profile-section">
            <h4 class="section-title">
              <i class="bi bi-file-person me-2"></i>Biography
            </h4>
            <div class="biography-content">
              {{ profile.biography }}
            </div>
          </div>

          <!-- Personal details section -->
          <div class="profile-section">
            <h4 class="section-title">
              <i class="bi bi-person-vcard me-2"></i>Personal Details
            </h4>
            <div class="row profile-details-grid">
              <div class="col-md-4 col-sm-6">
                <div class="detail-card">
                  <div class="detail-icon">
                    <i class="bi bi-geo-alt"></i>
                  </div>
                  <div class="detail-content">
                    <div class="detail-label">Parish</div>
                    <div class="detail-value">{{ profile.parish }}</div>
                  </div>
                </div>
              </div>

              <div class="col-md-4 col-sm-6">
                <div class="detail-card">
                  <div class="detail-icon">
                    <i class="bi bi-gender-ambiguous"></i>
                  </div>
                  <div class="detail-content">
                    <div class="detail-label">Sex</div>
                    <div class="detail-value">{{ profile.sex }}</div>
                  </div>
                </div>
              </div>

              <div class="col-md-4 col-sm-6">
                <div class="detail-card">
                  <div class="detail-icon">
                    <i class="bi bi-people"></i>
                  </div>
                  <div class="detail-content">
                    <div class="detail-label">Race</div>
                    <div class="detail-value">{{ profile.race }}</div>
                  </div>
                </div>
              </div>

              <div class="col-md-4 col-sm-6">
                <div class="detail-card">
                  <div class="detail-icon">
                    <i class="bi bi-calendar3"></i>
                  </div>
                  <div class="detail-content">
                    <div class="detail-label">Age</div>
                    <div class="detail-value">
                      {{ calculateAge(profile.birth_year) }}
                    </div>
                  </div>
                </div>
              </div>

              <div class="col-md-4 col-sm-6">
                <div class="detail-card">
                  <div class="detail-icon">
                    <i class="bi bi-rulers"></i>
                  </div>
                  <div class="detail-content">
                    <div class="detail-label">Height</div>
                    <div class="detail-value">
                      {{ formatHeight(profile.height) }}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Favorites section -->
          <div class="profile-section">
            <h4 class="section-title">
              <i class="bi bi-heart me-2"></i>Preferences
            </h4>
            <div class="row profile-details-grid">
              <div class="col-md-4 col-sm-6">
                <div class="detail-card">
                  <div class="detail-icon">
                    <i class="bi bi-cup-hot"></i>
                  </div>
                  <div class="detail-content">
                    <div class="detail-label">Favorite Cuisine</div>
                    <div class="detail-value">{{ profile.fav_cuisine }}</div>
                  </div>
                </div>
              </div>

              <div class="col-md-4 col-sm-6">
                <div class="detail-card">
                  <div class="detail-icon">
                    <i class="bi bi-palette"></i>
                  </div>
                  <div class="detail-content">
                    <div class="detail-label">Favorite Color</div>
                    <div class="detail-value">{{ profile.fav_colour }}</div>
                  </div>
                </div>
              </div>

              <div class="col-md-4 col-sm-6">
                <div class="detail-card">
                  <div class="detail-icon">
                    <i class="bi bi-book"></i>
                  </div>
                  <div class="detail-content">
                    <div class="detail-label">Favorite Subject</div>
                    <div class="detail-value">
                      {{ profile.fav_school_subject }}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Values section -->
          <div class="profile-section">
            <h4 class="section-title">
              <i class="bi bi-stars me-2"></i>Values
            </h4>
            <div class="values-container">
              <div class="value-pill" :class="{ active: profile.political }">
                <i class="bi bi-award me-2"></i>Political
              </div>
              <div class="value-pill" :class="{ active: profile.religious }">
                <i class="bi bi-building-fill me-2"></i>Religious
              </div>
              <div
                class="value-pill"
                :class="{ active: profile.family_oriented }"
              >
                <i class="bi bi-people-fill me-2"></i>Family Oriented
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import apiClient from "@/api.js";
import defaultProfileImg from "@/assets/defaultProfileImg.png";

export default {
  name: "ProfileDetails",
  data() {
    // Get user ID from localStorage
    const userId = localStorage.getItem("user_id");
    const profileId = this.$route ? this.$route.params.id : null;

    // Pre-compute if this is own profile on data initialization
    const isOwnProfile =
      userId && profileId
        ? parseInt(userId, 10) === parseInt(profileId, 10)
        : false;

    console.log("Initial profile comparison:", {
      userId: parseInt(userId, 10),
      profileId: parseInt(profileId, 10),
      isOwnProfile,
    });

    return {
      defaultProfileImg: defaultProfileImg,
      profile: null,
      loading: true,
      error: null,
      isFavorite: false,
      userId: userId,
      animateFavorite: false,
      _favoriteInProgress: false,
      // Store precomputed value
      _isOwnProfile: isOwnProfile,
    };
  },
  computed: {
    // build the image URL from baseURL + uploads path
    uploadBase() {
      return apiClient.defaults.baseURL;
    },
    profilePhotoUrl() {
      const fname = this.profile?.photo || this.profile?.user?.photo;
      return fname
        ? `${this.uploadBase}/api/uploads/${fname}`
        : defaultProfileImg;
    },
    // Check if this is the user's own profile - Use multiple methods to ensure it works
    isOwnProfile() {
      // First use the precomputed value if available
      if (this._isOwnProfile !== undefined) {
        return this._isOwnProfile;
      }

      // Fallback to explicit comparison
      const currentUserId = parseInt(this.userId, 10);
      const profileId = parseInt(this.$route.params.id, 10);

      // Log values for debugging
      console.log("isOwnProfile check:", {
        currentUserId,
        profileId,
        equal: currentUserId === profileId,
      });

      return currentUserId === profileId;
    },
  },
  mounted() {
    // Double check that buttons are hidden on own profile
    this.validateProfileVisibility();
  },
  created() {
    // Check if user is logged in
    const token = localStorage.getItem("token");
    if (!token) {
      this.$router.push("/login");
      return;
    }

    this.fetchProfileDetails();

    // Only check favorites if we have a valid user ID and it's not the user's own profile
    if (this.userId && !this.isOwnProfile) {
      this.checkIfFavorite();
    }
  },
  methods: {
    goBack() {
      this.$router.back();
    },
    fetchProfileDetails() {
      const token = localStorage.getItem("token");
      const profileId = this.$route.params.id;

      if (!profileId) {
        this.error = "Invalid profile ID.";
        this.loading = false;
        return;
      }
      if (!token) {
        this.$router.push("/login");
        return;
      }

      apiClient
        .get(`/api/profiles/${profileId}`)
        .then((response) => {
          // response.data.profile matches your JSON shape
          this.profile = response.data.profile;
          this.loading = false;

          // Check if this is the user's own profile after profile is loaded
          // Force visibility check after DOM update
          this.$nextTick(() => {
            this.validateProfileVisibility();

            // If it's not the user's own profile, only then check if favorite
            if (!this.isOwnProfile) {
              this.checkIfFavorite();
            }
          });
        })
        .catch((err) => {
          this.error =
            err.response?.data?.message || "Failed to load profile details.";
          this.loading = false;
        });
    },

    checkIfFavorite() {
      const token = localStorage.getItem("token");
      const userId = localStorage.getItem("user_id");

      // Only proceed if not viewing own profile
      if (this.isOwnProfile) {
        return;
      }

      if (!token || !userId) {
        this.$router.push("/login");
        return;
      }

      apiClient
        .get(`/api/users/${userId}/favourites`)
        .then((response) => {
          const favs = response.data.favourites || [];
          this.isFavorite = favs.some(
            (fav) => fav.id === parseInt(this.$route.params.id, 10)
          );
        })
        .catch((err) => {
          console.error("favorite check failed", err);
        });
    },

    toggleFavorite() {
      const token = localStorage.getItem("token");
      const profileId = this.$route.params.id;
      const userId = localStorage.getItem("user_id");

      // Only proceed if not viewing own profile
      if (this.isOwnProfile) {
        return;
      }

      if (!token) {
        this.$router.push("/login");
        return;
      }

      // Prevent multiple rapid clicks
      if (this._favoriteInProgress) {
        return;
      }

      this._favoriteInProgress = true;

      // Use the correct API based on current favorite status
      const apiAction = this.isFavorite
        ? apiClient.delete(`/api/profiles/${profileId}/favourite`)
        : apiClient.post(`/api/profiles/${profileId}/favourite`, {
            fav_user_id_fk: parseInt(profileId, 10),
            user_id_fk: parseInt(userId, 10), // Add user ID making the request
          });

      apiAction
        .then(() => {
          // Toggle favorite status
          this.isFavorite = !this.isFavorite;

          // Trigger animation if favoriting
          if (this.isFavorite) {
            this.animateFavorite = true;
            setTimeout(() => {
              this.animateFavorite = false;
            }, 1500);
          }
        })
        .catch((err) => {
          console.error("Toggle favorite failed", err);
          // If we get a 409 conflict, update the favorite status to match server state
          if (err.response && err.response.status === 409) {
            console.log("Favorite status already in desired state");
            // Re-check favorite status to sync with server
            this.checkIfFavorite();
          }
        })
        .finally(() => {
          // Allow future toggle actions after a short delay
          setTimeout(() => {
            this._favoriteInProgress = false;
          }, 500);
        });
    },

    calculateAge(year) {
      return new Date().getFullYear() - year;
    },

    formatHeight(h) {
      // Check if the value is likely in inches (above 12)
      if (h > 12) {
        // Convert from inches to feet and inches
        const ft = Math.floor(h / 12);
        const inch = Math.round(h % 12);
        return `${ft}' ${inch}"`;
      } else {
        // Original logic - assume the value is already in feet
        const ft = Math.floor(h);
        const inch = Math.round((h - ft) * 12);
        return `${ft}' ${inch}"`;
      }
    },

    // Ensure profile action buttons are properly hidden on own profile
    validateProfileVisibility() {
      if (this.isOwnProfile) {
        // Find and hide any action buttons that might be showing
        const actionButtons = document.querySelector(".profile-action-buttons");
        if (actionButtons) {
          actionButtons.style.display = "none";
        }
      }
    },
  },
};
</script>

<style scoped>
/* Import Google Fonts - Poppins */
@import url("https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap");
/* Import Bootstrap Icons */
@import url("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css");

/* Define color variables */
:root {
  --teal: #04acb0;
  --orange: #fb9623;
  --yellow: #ffbd0f;
  --coral: #ff7455;
  --background: #f9fafb;
  --magenta: #e83e8c;
}

.profile-details {
  font-family: "Poppins", sans-serif;
  background-color: var(--background);
  min-height: 100vh;
  overflow-x: hidden;
}

.container {
  max-width: 1000px;
  background-color: var(--background);
}

.profile-card {
  border-radius: 20px;
  overflow: hidden;
  border: none;
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.12);
  transition: all 0.4s ease;
}

/* Profile header section */
.profile-header {
  position: relative;
  background-color: white;
}

.profile-cover-container {
  height: 200px;
  position: relative;
  overflow: hidden;
}

.profile-cover-gradient {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(45deg, var(--teal), var(--coral));
  opacity: 0.8;
}

.profile-avatar-container {
  position: absolute;
  bottom: -80px;
  left: 50px;
  z-index: 10;
}

.profile-avatar {
  width: 160px;
  height: 160px;
  border-radius: 50%;
  border: 6px solid white;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  object-fit: cover;
}

/* Profile action buttons */
.profile-action-buttons {
  position: absolute;
  top: 20px;
  right: 20px;
  display: flex;
  gap: 10px;
  z-index: 5;
}

.btn-favorite,
.btn-email {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  border: none;
  transition: all 0.3s ease;
  position: relative;
  overflow: visible;
}

.btn-favorite {
  color: #e83e8c;
}

/* Favorite button color handling */
.btn-favorite i {
  color: #e83e8c;
}

.btn-favorite.active i {
  color: #e83e8c;
}

.btn-favorite:hover {
  background: #e83e8c;
  color: white;
  transform: translateY(-3px);
  box-shadow: 0 8px 15px rgba(232, 62, 140, 0.3);
}

.btn-favorite:hover i {
  color: white;
}

.btn-email {
  color: var(--teal);
}

.btn-email:hover {
  background: var(--teal);
  color: white;
  transform: translateY(-3px);
  box-shadow: 0 8px 15px rgba(4, 172, 176, 0.3);
}

.btn-email:hover i {
  color: white;
}

/* Favorite Animation */
.favorite-animation {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  pointer-events: none;
  z-index: 20;
  opacity: 0;
  transform: scale(0.5);
  transition: all 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.favorite-animation.active {
  animation: favoritePulse 1.5s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
}

.favorite-animation i {
  color: #e83e8c;
  font-size: 1.8rem;
}

@keyframes favoritePulse {
  0% {
    opacity: 0;
    transform: scale(0.5);
  }
  15% {
    opacity: 1;
    transform: scale(1.8);
  }
  30% {
    opacity: 1;
    transform: scale(1.2);
  }
  45% {
    opacity: 1;
    transform: scale(1.8);
  }
  60% {
    opacity: 1;
    transform: scale(1.2);
  }
  70% {
    opacity: 1;
    transform: scale(1.5);
  }
  100% {
    opacity: 0;
    transform: scale(5);
  }
}

/* Floating hearts animation */
.btn-favorite.animate-favorite::before {
  content: "";
  position: absolute;
  animation: floatingHearts 2s ease-out forwards;
}

/* Improved Back Button */
.back-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--teal);
  padding: 10px 20px;
  border-radius: 50px;
  background: white;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  text-decoration: none;
  transition: all 0.3s ease;
  margin-bottom: 20px;
  border: 2px solid transparent;
}

.back-btn:hover {
  background: linear-gradient(45deg, var(--teal), var(--coral));
  color: white;
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(4, 172, 176, 0.25);
}

.back-btn i {
  font-size: 1.1rem;
  transition: transform 0.3s ease;
}

.back-btn:hover i {
  transform: translateX(-4px);
}

.btn {
  padding: 0.9rem 1.8rem;
  border-radius: 50px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s ease;
  cursor: pointer;
  letter-spacing: 0.5px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(4, 172, 176, 0.3);
}

.btn-primary {
  background: linear-gradient(45deg, var(--teal), var(--coral));
  color: white;
  box-shadow: 0 4px 15px rgba(4, 172, 176, 0.3);
  border: none;
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

/* Profile info */
.profile-info-section {
  margin-top: 100px;
  margin-left: 50px;
  margin-bottom: 30px;
}

.profile-name {
  font-size: 2.2rem;
  font-weight: 700;
  background: linear-gradient(45deg, var(--teal), var(--coral));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 5px;
}

.profile-headline {
  font-size: 1.1rem;
  color: #555;
  font-weight: 500;
}

/* Sections */
.profile-section {
  padding: 25px 30px;
  margin-bottom: 20px;
  background-color: #fff;
  border-radius: 15px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.06);
  transition: all 0.3s ease;
}

.profile-section:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1);
}

.section-title {
  font-weight: 700;
  color: var(--teal);
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  padding-bottom: 10px;
  border-bottom: 2px solid #f0f0f0;
  position: relative;
}

.section-title::after {
  content: "";
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 80px;
  height: 3px;
  background: linear-gradient(45deg, var(--teal), var(--coral));
  border-radius: 3px;
}

.biography-content {
  line-height: 1.8;
  color: #555;
  font-size: 1.05rem;
}

/* Details grid */
.profile-details-grid {
  margin-top: 20px;
}

.detail-card {
  display: flex;
  padding: 15px;
  border-radius: 15px;
  margin-bottom: 15px;
  background-color: #f8f9fa;
  transition: all 0.3s ease;
}

.detail-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.08);
}

.detail-icon {
  width: 45px;
  height: 45px;
  border-radius: 50%;
  background: linear-gradient(45deg, var(--teal), var(--coral));
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 15px;
  font-size: 18px;
  box-shadow: 0 5px 10px rgba(4, 172, 176, 0.2);
}

.detail-content {
  flex: 1;
}

.detail-label {
  font-size: 12px;
  color: #6c757d;
  margin-bottom: 3px;
}

.detail-value {
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

/* Values pills */
.values-container {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.value-pill {
  display: flex;
  align-items: center;
  padding: 10px 18px;
  border-radius: 50px;
  background-color: #f8f9fa;
  color: #6c757d;
  font-weight: 500;
  border: 2px solid #e9ecef;
  opacity: 0.6;
  transition: all 0.3s ease;
}

.value-pill.active {
  background: linear-gradient(
    45deg,
    rgba(4, 172, 176, 0.1),
    rgba(255, 116, 85, 0.1)
  );
  color: var(--teal);
  border-color: var(--teal);
  opacity: 1;
  box-shadow: 0 5px 10px rgba(4, 172, 176, 0.1);
}

/* Add some animation when hovering over profile sections */
.profile-section {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.profile-section:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1);
}

/* Responsive styles */
@media (max-width: 768px) {
  .profile-avatar-container {
    left: 50%;
    transform: translateX(-50%);
  }

  .profile-info-section {
    margin-left: 0;
    text-align: center;
  }

  .btn {
    width: 100%;
    justify-content: center;
  }

  .profile-name {
    font-size: 1.8rem;
  }

  .back-btn {
    width: auto;
    display: inline-flex;
    margin-bottom: 15px;
  }

  .profile-action-buttons {
    top: auto;
    right: 20px;
    bottom: -25px;
  }
}

@media (max-width: 576px) {
  .profile-name {
    font-size: 1.5rem;
  }

  .profile-headline {
    font-size: 1rem;
  }

  .btn {
    padding: 0.8rem 1.5rem;
    font-size: 0.9rem;
  }

  .back-btn {
    font-size: 0.9rem;
    padding: 8px 16px;
  }
}
</style>
