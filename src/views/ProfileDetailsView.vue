<!-- src/components/ProfileDetails.vue -->
<template>
  <div class="profile-details">
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <div v-else-if="error" class="alert alert-danger">
      {{ error }}
    </div>

    <div v-else class="card mb-4">
      <div class="row g-0">
        <div class="col-md-4">
          <img
            :src="profile.user.photo"
            class="img-fluid rounded-start"
            alt="Profile Photo"
          />
        </div>
        <div class="col-md-8">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-center mb-3">
              <h3 class="card-title">{{ profile.user.name }}</h3>
              <button
                class="btn"
                :class="{
                  'btn-outline-danger': !isFavorite,
                  'btn-danger': isFavorite,
                }"
                @click="toggleFavorite"
              >
                <i
                  class="bi"
                  :class="{
                    'bi-heart': !isFavorite,
                    'bi-heart-fill': isFavorite,
                  }"
                ></i>
              </button>
            </div>

            <p class="card-text">{{ profile.description }}</p>

            <div class="row">
              <div class="col-md-6">
                <p><strong>Parish:</strong> {{ profile.parish }}</p>
                <p><strong>Sex:</strong> {{ profile.sex }}</p>
                <p><strong>Race:</strong> {{ profile.race }}</p>
                <p>
                  <strong>Age:</strong> {{ calculateAge(profile.birth_year) }}
                </p>
                <p>
                  <strong>Height:</strong> {{ formatHeight(profile.height) }}
                </p>
              </div>
              <div class="col-md-6">
                <p>
                  <strong>Favorite Cuisine:</strong> {{ profile.fav_cuisine }}
                </p>
                <p><strong>Favorite Color:</strong> {{ profile.fav_colour }}</p>
                <p>
                  <strong>Favorite School Subject:</strong>
                  {{ profile.fav_school_sibject }}
                </p>
                <p>
                  <strong>Political:</strong>
                  {{ profile.political ? "Yes" : "No" }}
                </p>
                <p>
                  <strong>Religious:</strong>
                  {{ profile.religious ? "Yes" : "No" }}
                </p>
                <p>
                  <strong>Family Oriented:</strong>
                  {{ profile.family_oriented ? "Yes" : "No" }}
                </p>
              </div>
            </div>

            <div class="mt-4">
              <h4>Biography</h4>
              <p>{{ profile.biography }}</p>
            </div>

            <div class="mt-4">
              <a :href="`mailto:${profile.user.email}`" class="btn btn-primary"
                >Email Profile</a
              >
              <router-link to="/" class="btn btn-secondary ms-2"
                >Back to Profiles</router-link
              >
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "ProfileDetails",
  data() {
    return {
      profile: null,
      loading: true,
      error: null,
      isFavorite: false,
    };
  },
  created() {
    this.fetchProfileDetails();
    this.checkIfFavorite();
  },
  methods: {
    fetchProfileDetails() {
      const token = localStorage.getItem("token");
      const profileId = this.$route.params.profile_id;

      axios
        .get(`/api/profiles/${profileId}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        .then((response) => {
          this.profile = response.data;
          this.loading = false;
        })
        .catch((error) => {
          this.error = "Failed to load profile details";
          this.loading = false;
          console.error("Error fetching profile details:", error);
        });
    },
    checkIfFavorite() {
      const token = localStorage.getItem("token");
      const userInfo = JSON.parse(localStorage.getItem("user") || "{}");
      const userId = userInfo.id;

      if (!userId) return;

      axios
        .get(`/api/users/${userId}/favourites`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        .then((response) => {
          const favorites = response.data;
          this.isFavorite = favorites.some(
            (fav) => fav.id === parseInt(this.$route.params.profile_id)
          );
        })
        .catch((error) => {
          console.error("Error checking favorites:", error);
        });
    },
    toggleFavorite() {
      const token = localStorage.getItem("token");
      const profileId = this.$route.params.profile_id;

      axios
        .post(
          `/api/profiles/${profileId}/favourite`,
          {},
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        )
        .then(() => {
          this.isFavorite = !this.isFavorite;
        })
        .catch((error) => {
          console.error("Error toggling favorite:", error);
        });
    },
    calculateAge(birthYear) {
      const currentYear = new Date().getFullYear();
      return currentYear - birthYear;
    },
    formatHeight(height) {
      // Convert decimal height to feet and inches
      const feet = Math.floor(height);
      const inches = Math.round((height - feet) * 12);
      return `${feet}' ${inches}"`;
    },
  },
};
</script>

<style scoped>
/* Add custom styles here if needed */
</style>
