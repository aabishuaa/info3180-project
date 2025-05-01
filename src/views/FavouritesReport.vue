<template>
  <div class="favorites-report">
    <div class="container py-4">
      <h1 class="report-title">
        <i class="bi bi-heart-fill me-2"></i>Favorites Report
      </h1>

      <!-- Error banner -->
      <div
        v-if="message"
        class="alert custom-alert"
        :class="messageClass"
        role="alert"
      >
        {{ message }}
      </div>

      <!-- Top Favored Users Section -->
      <div class="profile-section mb-5">
        <h4 class="section-title">
          <i class="bi bi-trophy me-2"></i>Top 20 Favored Profiles
        </h4>

        <!-- Sort controls -->
        <div class="sort-controls">
          <button
            class="sort-btn"
            :class="sortType === 'name' ? 'active' : ''"
            @click="sortTopFavorites('name')"
          >
            <i class="bi bi-sort-alpha-down me-1"></i>Name
          </button>
          <button
            class="sort-btn"
            :class="sortType === 'parish' ? 'active' : ''"
            @click="sortTopFavorites('parish')"
          >
            <i class="bi bi-geo-alt me-1"></i>Parish
          </button>
          <button
            class="sort-btn"
            :class="sortType === 'age' ? 'active' : ''"
            @click="sortTopFavorites('age')"
          >
            <i class="bi bi-calendar3 me-1"></i>Age
          </button>
        </div>

        <div v-if="topFavorites.length === 0" class="empty-state">
          <i class="bi bi-emoji-neutral"></i>
          <p>No data available for top favorites</p>
        </div>

        <div v-else class="row">
          <div
            v-for="profile in topFavorites"
            :key="profile.id"
            class="col-md-6 col-lg-4 mb-4"
          >
            <div class="favorite-card" @click="goToProfile(profile.id)">
              <div class="card-inner">
                <!-- Profile header with gradient background -->
                <div class="favorite-header">
                  <div class="favorite-cover-gradient"></div>
                  <div class="favorite-count">
                    <i class="bi bi-heart-fill me-1"></i>
                    {{ profile.favorite_count }}
                  </div>
                  <div class="favorite-avatar-container">
                    <img
                      :src="getProfileImage(profile.photo)"
                      class="favorite-avatar"
                      alt="Profile Photo"
                    />
                  </div>
                </div>

                <!-- Profile info -->
                <div class="favorite-content">
                  <h3 class="favorite-name">{{ profile.description }}</h3>

                  <!-- Quick profile details -->
                  <div class="favorite-details">
                    <div class="favorite-detail-item">
                      <i class="bi bi-geo-alt"></i>
                      <span>{{ profile.parish }}</span>
                    </div>
                    <div class="favorite-detail-item">
                      <i class="bi bi-calendar3"></i>
                      <span>{{ calculateAge(profile.birth_year) }}</span>
                    </div>
                  </div>

                  <!-- View button -->
                  <div class="favorite-actions">
                    <button class="btn-view-profile">
                      <i class="bi bi-person-badge"></i>
                      <span>View Profile</span>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- My Favorites Section -->
      <div class="profile-section">
        <h4 class="section-title">
          <i class="bi bi-heart me-2"></i>My Favorites
        </h4>

        <!-- Sort controls -->
        <div class="sort-controls">
          <button
            class="sort-btn"
            :class="myFavSortType === 'name' ? 'active' : ''"
            @click="sortMyFavorites('name')"
          >
            <i class="bi bi-sort-alpha-down me-1"></i>Name
          </button>
          <button
            class="sort-btn"
            :class="myFavSortType === 'parish' ? 'active' : ''"
            @click="sortMyFavorites('parish')"
          >
            <i class="bi bi-geo-alt me-1"></i>Parish
          </button>
          <button
            class="sort-btn"
            :class="myFavSortType === 'age' ? 'active' : ''"
            @click="sortMyFavorites('age')"
          >
            <i class="bi bi-calendar3 me-1"></i>Age
          </button>
        </div>

        <div v-if="myFavorites.length === 0" class="empty-state">
          <i class="bi bi-emoji-smile"></i>
          <p>You haven't added any profiles to your favorites yet</p>
        </div>

        <div v-else class="row">
          <div
            v-for="profile in myFavorites"
            :key="profile.id"
            class="col-md-6 col-lg-4 mb-4"
          >
            <div class="favorite-card" @click="goToProfile(profile.id)">
              <div class="card-inner">
                <!-- Profile header with gradient background -->
                <div class="favorite-header">
                  <div class="favorite-cover-gradient"></div>
                  <div class="favorite-avatar-container">
                    <img
                      :src="getProfileImage(profile.photo)"
                      class="favorite-avatar"
                      alt="Profile Photo"
                    />
                  </div>
                </div>

                <!-- Profile info -->
                <div class="favorite-content">
                  <h3 class="favorite-name">{{ profile.description }}</h3>

                  <!-- Quick profile details -->
                  <div class="favorite-details">
                    <div class="favorite-detail-item">
                      <i class="bi bi-geo-alt"></i>
                      <span>{{ profile.parish }}</span>
                    </div>
                    <div class="favorite-detail-item">
                      <i class="bi bi-calendar3"></i>
                      <span>{{ calculateAge(profile.birth_year) }}</span>
                    </div>
                  </div>

                  <!-- View and remove buttons -->
                  <div class="favorite-actions">
                    <button class="btn-view-profile">
                      <i class="bi bi-person-badge"></i>
                      <span>View Profile</span>
                    </button>
                    <button
                      class="btn-favorite active"
                      @click.stop="removeFavorite(profile.id)"
                    >
                      <i class="bi bi-heart-fill"></i>
                    </button>
                  </div>
                </div>
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
import defaultProfile from "@/assets/defaultProfileImg.png";

export default {
  name: "FavoritesReport",
  data() {
    return {
      topFavorites: [],
      myFavorites: [],
      message: "",
      messageClass: "",
      sortType: "name",
      myFavSortType: "name",
      currentYear: new Date().getFullYear(),
      defaultProfile: defaultProfile,
    };
  },
  computed: {
    uploadBase() {
      return apiClient.defaults.baseURL;
    },
  },
  created() {
    this.fetchTopFavorites();
    this.fetchMyFavorites();
  },
  methods: {
    fetchTopFavorites() {
      this.message = "";
      this.messageClass = "";

      apiClient
        .get("/api/users/favourites/20")
        .then((response) => {
          this.topFavorites = response.data.top_favourites || [];
          this.sortTopFavorites(this.sortType);
        })
        .catch((error) => {
          console.error(error.response?.data || error.message);
          this.message =
            error.response?.data?.message || "Failed to fetch top favorites.";
          this.messageClass = "alert-danger";
        });
    },

    fetchMyFavorites() {
      const userId = parseInt(localStorage.getItem("user_id"), 10);
      if (!userId) {
        this.$router.push("/login");
        return;
      }

      this.message = "";
      this.messageClass = "";

      apiClient
        .get(`/api/users/${userId}/favourites`)
        .then((response) => {
          this.myFavorites = (response.data.favourites || []).filter(
            (p) => p.id !== userId
          );
          this.sortMyFavorites(this.myFavSortType);
        })
        .catch((error) => {
          console.error(error.response?.data || error.message);
          this.message =
            error.response?.data?.message || "Failed to fetch your favorites.";
          this.messageClass = "alert-danger";
        });
    },

    getProfileImage(photoName) {
      return photoName
        ? `${this.uploadBase}/api/uploads/${photoName}`
        : this.defaultProfile;
    },

    calculateAge(birthYear) {
      return this.currentYear - birthYear;
    },

    goToProfile(profileId) {
      this.$router.push(`/users/${profileId}/profile`);
    },

    removeFavorite(profileId) {
      // Prevent navigation to profile
      event.stopPropagation();

      apiClient
        .delete(`/api/profiles/${profileId}/favourite`)
        .then(() => {
          // Remove from list
          this.myFavorites = this.myFavorites.filter((p) => p.id !== profileId);

          // Show success message
          this.message = "Profile removed from favorites.";
          this.messageClass = "alert-success";

          // Clear message after a few seconds
          setTimeout(() => {
            this.message = "";
          }, 3000);
        })
        .catch((error) => {
          console.error(error.response?.data || error.message);
          this.message =
            error.response?.data?.message || "Failed to remove favorite.";
          this.messageClass = "alert-danger";
        });
    },

    sortTopFavorites(type) {
      this.sortType = type;
      if (type === "name") {
        this.topFavorites.sort((a, b) =>
          a.description.localeCompare(b.description)
        );
      } else if (type === "parish") {
        this.topFavorites.sort((a, b) => a.parish.localeCompare(b.parish));
      } else if (type === "age") {
        this.topFavorites.sort(
          (a, b) =>
            this.currentYear - b.birth_year - (this.currentYear - a.birth_year)
        );
      }
    },

    sortMyFavorites(type) {
      this.myFavSortType = type;
      if (type === "name") {
        this.myFavorites.sort((a, b) =>
          a.description.localeCompare(b.description)
        );
      } else if (type === "parish") {
        this.myFavorites.sort((a, b) => a.parish.localeCompare(b.parish));
      } else if (type === "age") {
        this.myFavorites.sort(
          (a, b) =>
            this.currentYear - b.birth_year - (this.currentYear - a.birth_year)
        );
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

/* Define color variables matching profile details component */
:root {
  --teal: #04acb0;
  --orange: #fb9623;
  --yellow: #ffbd0f;
  --coral: #ff7455;
  --background: #f9fafb;
  --magenta: #e83e8c;
}

.favorites-report {
  font-family: "Poppins", sans-serif;
  background-color: var(--background);
  min-height: 100vh;
  overflow-x: hidden;
}

.container {
  max-width: 1200px;
  background-color: var(--background);
}

/* Report Title */
.report-title {
  font-size: 2.2rem;
  font-weight: 700;
  background: linear-gradient(45deg, var(--teal), var(--coral));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 25px;
  text-align: center;
  padding-bottom: 15px;
  border-bottom: 2px solid #f0f0f0;
  position: relative;
}

.report-title::after {
  content: "";
  position: absolute;
  bottom: -2px;
  left: 50%;
  transform: translateX(-50%);
  width: 180px;
  height: 3px;
  background: linear-gradient(45deg, var(--teal), var(--coral));
  border-radius: 3px;
}

/* Sections */
.profile-section {
  padding: 25px 30px;
  margin-bottom: 30px;
  background-color: #fff;
  border-radius: 15px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.06);
  transition: all 0.3s ease;
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

/* Sort Controls */
.sort-controls {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 20px;
}

.sort-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 8px 16px;
  border-radius: 50px;
  background-color: #f8f9fa;
  color: #6c757d;
  font-weight: 500;
  border: 2px solid #e9ecef;
  transition: all 0.3s ease;
  cursor: pointer;
}

.sort-btn.active {
  background: linear-gradient(
    45deg,
    rgba(4, 172, 176, 0.1),
    rgba(255, 116, 85, 0.1)
  );
  color: var(--teal);
  border-color: var(--teal);
  box-shadow: 0 5px 10px rgba(4, 172, 176, 0.1);
}

.sort-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
}

/* Empty State */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
  background-color: #f8f9fa;
  border-radius: 10px;
  color: #6c757d;
}

.empty-state i {
  font-size: 3rem;
  margin-bottom: 15px;
  color: var(--teal);
}

/* Alert Styling */
.custom-alert {
  border-radius: 10px;
  border: none;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
  padding: 16px 20px;
  margin-bottom: 25px;
}

.alert-success {
  background-color: rgba(40, 167, 69, 0.15);
  color: #28a745;
}

.alert-danger {
  background-color: rgba(220, 53, 69, 0.15);
  color: #dc3545;
}

/* Favorite Cards */
.favorite-card {
  cursor: pointer;
  transition: all 0.3s ease;
}

.card-inner {
  background-color: white;
  border-radius: 20px;
  overflow: hidden;
  border: none;
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.12);
  transition: all 0.4s ease;
  height: 100%;
}

.favorite-card:hover .card-inner {
  transform: translateY(-8px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.18);
}

/* Profile header section */
.favorite-header {
  position: relative;
  height: 100px;
  background-color: white;
}

.favorite-cover-gradient {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(45deg, var(--teal), var(--coral));
  opacity: 0.8;
}

.favorite-avatar-container {
  position: absolute;
  bottom: -30px;
  left: 30px;
  z-index: 10;
}

.favorite-avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  border: 4px solid white;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  object-fit: cover;
}

/* Favorite count */
.favorite-count {
  position: absolute;
  top: 15px;
  right: 15px;
  background: white;
  color: var(--magenta);
  border-radius: 50px;
  padding: 5px 12px;
  font-weight: 600;
  font-size: 0.9rem;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 5px;
  z-index: 5;
}

/* Profile content */
.favorite-content {
  padding: 15px 20px 20px 20px;
  padding-top: 40px;
}

.favorite-name {
  font-size: 1.4rem;
  font-weight: 700;
  background: linear-gradient(45deg, var(--teal), var(--coral));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 15px;
}

/* Quick details */
.favorite-details {
  display: flex;
  justify-content: flex-start;
  gap: 15px;
  margin-bottom: 15px;
}

.favorite-detail-item {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 0.85rem;
  color: #6c757d;
}

.favorite-detail-item i {
  color: var(--teal);
}

/* Action buttons */
.favorite-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 15px;
}

.btn-view-profile {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: linear-gradient(45deg, var(--teal), var(--coral));
  color: white;
  border: none;
  border-radius: 50px;
  font-size: 0.9rem;
  font-weight: 600;
  transition: all 0.3s ease;
  cursor: pointer;
  box-shadow: 0 4px 10px rgba(4, 172, 176, 0.25);
}

.btn-view-profile:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 15px rgba(4, 172, 176, 0.3);
}

.btn-favorite {
  width: 40px;
  height: 40px;
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
  color: #e83e8c;
}

/* Favorite button styling */
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

/* Responsive styles */
@media (max-width: 768px) {
  .report-title {
    font-size: 1.8rem;
  }

  .sort-controls {
    justify-content: center;
  }

  .favorite-name {
    font-size: 1.2rem;
  }
}

@media (max-width: 576px) {
  .profile-section {
    padding: 20px 15px;
  }

  .section-title {
    font-size: 1.3rem;
  }

  .report-title {
    font-size: 1.5rem;
  }

  .sort-btn {
    padding: 6px 12px;
    font-size: 0.8rem;
  }
}
</style>
