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
            :src="profilePhotoUrl"
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
                  {{ profile.fav_school_subject }}
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
              <a :href="`mailto:${profile.user.email}`" class="btn btn-primary">
                Email Profile
              </a>
              <router-link to="/" class="btn btn-secondary ms-2">
                Back to Profiles
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import apiClient from "@/api.js";

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
  computed: {
    // build the image URL from baseURL + uploads path
    uploadBase() {
      return apiClient.defaults.baseURL;
    },
    profilePhotoUrl() {
      const fname = this.profile.photo || this.profile.user.photo;
      return fname
        ? `${this.uploadBase}/api/uploads/${fname}`
        : "/default-profile.png";
    },
  },
  created() {
    this.fetchProfileDetails();
    this.checkIfFavorite();
  },
  methods: {
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

      if (!token) {
        this.$router.push("/login");
        return;
      }

      apiClient
        .post(`/api/profiles/${profileId}/favourite`, {
          fav_user_id_fk: parseInt(profileId, 10),
        })
        .then(() => {
          this.isFavorite = !this.isFavorite;
        })
        .catch((err) => {
          console.error("toggle favorite failed", err);
        });
    },

    calculateAge(year) {
      return new Date().getFullYear() - year;
    },

    formatHeight(h) {
      const ft = Math.floor(h),
        inch = Math.round((h - ft) * 12);
      return `${ft}' ${inch}"`;
    },
  },
};
</script>

<style scoped>
/* … */
</style>
