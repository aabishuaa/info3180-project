<template>
  <div class="container">
    <h1 class="text-center mb-4">Favorites Reports</h1>

    <!-- Error banner -->
    <div v-if="message" class="alert" :class="messageClass" role="alert">
      {{ message }}
    </div>

    <!-- Top Favored Users -->
    <div class="mb-5">
      <h2>Top Favored Users</h2>
      <div class="mb-3">
        <div class="btn-group">
          <button
            class="btn btn-sm"
            :class="sortType === 'name' ? 'btn-primary' : 'btn-outline-primary'"
            @click="sortTopFavorites('name')"
          >
            Sort by Name
          </button>
          <button
            class="btn btn-sm"
            :class="
              sortType === 'parish' ? 'btn-primary' : 'btn-outline-primary'
            "
            @click="sortTopFavorites('parish')"
          >
            Sort by Parish
          </button>
          <button
            class="btn btn-sm"
            :class="sortType === 'age' ? 'btn-primary' : 'btn-outline-primary'"
            @click="sortTopFavorites('age')"
          >
            Sort by Age
          </button>
        </div>
      </div>

      <div v-if="topFavorites.length === 0" class="alert alert-info">
        No data available for top favorites.
      </div>

      <div v-else class="row">
        <div
          v-for="profile in topFavorites"
          :key="profile.id"
          class="col-md-6 col-lg-4 mb-4"
        >
          <div class="card h-100">
            <div
              class="card-header d-flex justify-content-between align-items-center"
            >
              <h5 class="mb-0">{{ profile.description }}</h5>
              <span class="badge bg-primary">
                {{ profile.favorite_count }} favorites
              </span>
            </div>
            <div class="card-body">
              <!-- prepend uploadBase, fallback to defaultProfile -->
              <img
                :src="
                  profile.photo
                    ? `${uploadBase}/api/uploads/${profile.photo}`
                    : defaultProfile
                "
                class="card-img-top mb-3"
                alt="Profile Photo"
              />
              <p><strong>Parish:</strong> {{ profile.parish }}</p>
              <p>
                <strong>Age:</strong> {{ calculateAge(profile.birth_year) }}
              </p>
              <p><strong>Description:</strong> {{ profile.description }}</p>
              <router-link :to="`/profiles/${profile.id}`" class="btn btn-info">
                View Details
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- My Favorites -->
    <div>
      <h2>My Favorites</h2>
      <div class="mb-3">
        <div class="btn-group">
          <button
            class="btn btn-sm"
            :class="
              myFavSortType === 'name' ? 'btn-primary' : 'btn-outline-primary'
            "
            @click="sortMyFavorites('name')"
          >
            Sort by Name
          </button>
          <button
            class="btn btn-sm"
            :class="
              myFavSortType === 'parish' ? 'btn-primary' : 'btn-outline-primary'
            "
            @click="sortMyFavorites('parish')"
          >
            Sort by Parish
          </button>
          <button
            class="btn btn-sm"
            :class="
              myFavSortType === 'age' ? 'btn-primary' : 'btn-outline-primary'
            "
            @click="sortMyFavorites('age')"
          >
            Sort by Age
          </button>
        </div>
      </div>

      <div v-if="myFavorites.length === 0" class="alert alert-info">
        You haven't added any profiles to your favorites yet.
      </div>

      <div v-else class="row">
        <div
          v-for="profile in myFavorites"
          :key="profile.id"
          class="col-md-6 col-lg-4 mb-4"
        >
          <div class="card h-100">
            <div class="card-header">
              <h5 class="mb-0">{{ profile.description }}</h5>
            </div>
            <div class="card-body">
              <img
                :src="
                  profile.photo
                    ? `${uploadBase}/api/uploads/${profile.photo}`
                    : defaultProfile
                "
                class="card-img-top mb-3"
                alt="Profile Photo"
              />
              <p><strong>Parish:</strong> {{ profile.parish }}</p>
              <p>
                <strong>Age:</strong> {{ calculateAge(profile.birth_year) }}
              </p>
              <p><strong>Description:</strong> {{ profile.description }}</p>
              <router-link :to="`/profiles/${profile.id}`" class="btn btn-info">
                View Details
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
import defaultProfile from "@/assets/default-profile.png";

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

    calculateAge(birthYear) {
      return this.currentYear - birthYear;
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
.container {
  padding: 20px;
}
</style>
