<template>
  <div class="container">
    <h1 class="text-center mb-4">Favorites Reports</h1>

    <div v-if="message" class="alert" :class="messageClass" role="alert">
      {{ message }}
    </div>

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
              <h5 class="mb-0">{{ profile.name }}</h5>
              <span class="badge bg-primary"
                >{{ profile.favorite_count }} favorites</span
              >
            </div>
            <div class="card-body">
              <img
                v-if="profile.photo"
                :src="profile.photo"
                class="card-img-top mb-3"
                alt="Profile Photo"
              />
              <p><strong>Parish:</strong> {{ profile.parish }}</p>
              <p>
                <strong>Age:</strong> {{ calculateAge(profile.birth_year) }}
              </p>
              <p><strong>Description:</strong> {{ profile.description }}</p>
              <router-link :to="`/profiles/${profile.id}`" class="btn btn-info"
                >View Details</router-link
              >
            </div>
          </div>
        </div>
      </div>
    </div>

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
              <h5 class="mb-0">{{ profile.name }}</h5>
            </div>
            <div class="card-body">
              <img
                v-if="profile.photo"
                :src="profile.photo"
                class="card-img-top mb-3"
                alt="Profile Photo"
              />
              <p><strong>Parish:</strong> {{ profile.parish }}</p>
              <p>
                <strong>Age:</strong> {{ calculateAge(profile.birth_year) }}
              </p>
              <p><strong>Description:</strong> {{ profile.description }}</p>
              <router-link :to="`/profiles/${profile.id}`" class="btn btn-info"
                >View Details</router-link
              >
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
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
  created() {
    this.fetchTopFavorites();
    this.fetchMyFavorites();
  },
  methods: {
    fetchTopFavorites() {
      const token = localStorage.getItem("token");

      if (!token) {
        this.$router.push("/login");
        return;
      }

      fetch("/api/users/favourites/20", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
        .then((response) => {
          if (response.ok) {
            return response.json();
          }
          throw new Error("Failed to fetch top favorites");
        })
        .then((data) => {
          this.topFavorites = data;
          this.sortTopFavorites(this.sortType);
        })
        .catch((error) => {
          this.message = error.message;
          this.messageClass = "alert-danger";
        });
    },

    fetchMyFavorites() {
      const token = localStorage.getItem("token");

      if (!token) {
        this.$router.push("/login");
        return;
      }

      // We need to get the current user's ID first
      fetch("/api/auth/user", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
        .then((response) => {
          if (response.ok) {
            return response.json();
          }
          throw new Error("Failed to get current user");
        })
        .then((userData) => {
          // Now fetch this user's favorites
          return fetch(`/api/users/${userData.id}/favourites`, {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
        })
        .then((response) => {
          if (response.ok) {
            return response.json();
          }
          throw new Error("Failed to fetch your favorites");
        })
        .then((data) => {
          this.myFavorites = data;
          this.sortMyFavorites(this.myFavSortType);
        })
        .catch((error) => {
          this.message = error.message;
          this.messageClass = "alert-danger";
        });
    },

    calculateAge(birthYear) {
      return this.currentYear - birthYear;
    },

    sortTopFavorites(type) {
      this.sortType = type;

      if (type === "name") {
        this.topFavorites.sort((a, b) => a.name.localeCompare(b.name));
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
        this.myFavorites.sort((a, b) => a.name.localeCompare(b.name));
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
