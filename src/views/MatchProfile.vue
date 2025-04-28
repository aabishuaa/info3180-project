<template>
  <div class="container">
    <h1 class="text-center mb-4">Match Results for "{{ profileName }}"</h1>

    <div v-if="message" class="alert" :class="messageClass" role="alert">
      {{ message }}
    </div>

    <div v-if="loading" class="text-center my-5">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="mt-2">Finding your matches...</p>
    </div>

    <div v-else>
      <div v-if="matches.length === 0" class="alert alert-info">
        No matches found for your profile criteria. Try updating your profile to
        find more matches.
      </div>

      <div v-else>
        <p class="lead text-center mb-4">
          We found {{ matches.length }} profile{{
            matches.length !== 1 ? "s" : ""
          }}
          that match your criteria!
        </p>

        <div class="row">
          <div
            v-for="profile in matches"
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
                <p>
                  <strong>Age:</strong> {{ calculateAge(profile.birth_year) }}
                </p>
                <p><strong>Parish:</strong> {{ profile.parish }}</p>
                <p>
                  <strong>Height:</strong> {{ formatHeight(profile.height) }}
                </p>
                <p><strong>Description:</strong> {{ profile.description }}</p>

                <div class="mt-3">
                  <h6>Matching Attributes:</h6>
                  <ul class="list-group list-group-flush">
                    <li
                      v-if="matchesAttribute(profile, 'fav_cuisine')"
                      class="list-group-item"
                    >
                      Favorite Cuisine: {{ profile.fav_cuisine }}
                    </li>
                    <li
                      v-if="matchesAttribute(profile, 'fav_colour')"
                      class="list-group-item"
                    >
                      Favorite Color: {{ profile.fav_colour }}
                    </li>
                    <li
                      v-if="matchesAttribute(profile, 'fav_school_subject')"
                      class="list-group-item"
                    >
                      Favorite School Subject: {{ profile.fav_school_subject }}
                    </li>
                    <li
                      v-if="matchesAttribute(profile, 'political')"
                      class="list-group-item"
                    >
                      Political: {{ profile.political ? "Yes" : "No" }}
                    </li>
                    <li
                      v-if="matchesAttribute(profile, 'religious')"
                      class="list-group-item"
                    >
                      Religious: {{ profile.religious ? "Yes" : "No" }}
                    </li>
                    <li
                      v-if="matchesAttribute(profile, 'family_oriented')"
                      class="list-group-item"
                    >
                      Family Oriented:
                      {{ profile.family_oriented ? "Yes" : "No" }}
                    </li>
                  </ul>
                </div>

                <div class="d-flex justify-content-between mt-3">
                  <router-link
                    :to="`/profiles/${profile.id}`"
                    class="btn btn-info"
                    >View Details</router-link
                  >
                  <button
                    class="btn"
                    :class="
                      profile.isFavorite ? 'btn-danger' : 'btn-outline-danger'
                    "
                    @click="toggleFavorite(profile)"
                  >
                    <i class="fa fa-heart"></i>
                    {{
                      profile.isFavorite
                        ? "Remove from Favorites"
                        : "Add to Favorites"
                    }}
                  </button>
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
    };
  },
  created() {
    this.fetchMatches();
  },
  methods: {
    fetchMatches() {
      const token = localStorage.getItem("token");

      if (!token) {
        this.$router.push("/login");
        return;
      }

      // First get the profile details to use for comparison
      fetch(`/api/profiles/${this.profileId}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
        .then((response) => {
          if (response.ok) {
            return response.json();
          }
          throw new Error("Failed to fetch your profile");
        })
        .then((profileData) => {
          this.myProfile = profileData;
          this.profileName =
            profileData.description || `Profile #${this.profileId}`;

          // Now fetch the matches
          return fetch(`/api/profiles/matches/${this.profileId}`, {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
        })
        .then((response) => {
          if (response.ok) {
            return response.json();
          }
          throw new Error("Failed to fetch matches");
        })
        .then((matchData) => {
          this.matches = matchData;

          // Now check which profiles are already favorites
          return this.checkFavorites();
        })
        .then(() => {
          this.loading = false;
        })
        .catch((error) => {
          this.message = error.message;
          this.messageClass = "alert-danger";
          this.loading = false;
        });
    },

    checkFavorites() {
      const token = localStorage.getItem("token");

      // Get the user's current favorites to mark matched profiles
      return fetch("/api/auth/user", {
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
          throw new Error("Failed to fetch favorites");
        })
        .then((favorites) => {
          // Mark profiles that are already favorites
          const favoriteIds = favorites.map((fav) => fav.id);
          this.matches.forEach((match) => {
            match.isFavorite = favoriteIds.includes(match.id);
          });
        });
    },

    toggleFavorite(profile) {
      const token = localStorage.getItem("token");

      if (!token) {
        this.$router.push("/login");
        return;
      }

      // First get current user id
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
          // Add this profile to favorites
          return fetch(`/api/profiles/${profile.id}/favourite`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify({ user_id: userData.id }),
          });
        })
        .then((response) => {
          if (response.ok) {
            // Toggle the favorite status locally
            profile.isFavorite = !profile.isFavorite;

            this.message = profile.isFavorite
              ? `Added ${profile.name} to your favorites!`
              : `Removed ${profile.name} from your favorites.`;
            this.messageClass = "alert-success";

            // Clear message after 3 seconds
            setTimeout(() => {
              this.message = "";
            }, 3000);
          } else {
            throw new Error("Failed to update favorite status");
          }
        })
        .catch((error) => {
          this.message = error.message;
          this.messageClass = "alert-danger";
        });
    },

    calculateAge(birthYear) {
      return this.currentYear - birthYear;
    },

    formatHeight(inches) {
      const feet = Math.floor(inches / 12);
      const remainingInches = Math.round((inches % 12) * 10) / 10;
      return `${feet}'${remainingInches}"`;
    },

    matchesAttribute(profile, attr) {
      return this.myProfile && this.myProfile[attr] === profile[attr];
    },
  },
};
</script>

<style scoped>
.container {
  padding: 20px;
}
</style>
