<!-- src/components/UserProfile.vue -->
<template>
  <div class="user-profile">
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <div v-else-if="error" class="alert alert-danger">
      {{ error }}
    </div>

    <div v-else>
      <div class="row mb-4">
        <div class="col-md-4">
          <div class="card">
            <img :src="user.photo" class="card-img-top" alt="Profile Photo" />
            <div class="card-body">
              <h5 class="card-title">{{ user.name }}</h5>
              <p class="card-text">{{ user.email }}</p>
              <p class="card-text">
                <small class="text-muted"
                  >Member since {{ formatDate(user.date_joined) }}</small
                >
              </p>
            </div>
          </div>
        </div>

        <div class="col-md-8">
          <h3>My Profiles</h3>
          <p v-if="profiles.length === 0">
            You haven't created any profiles yet.
            <router-link to="/profiles/new" class="btn btn-primary"
              >Create Profile</router-link
            >
          </p>

          <div v-else>
            <div
              class="card mb-3"
              v-for="profile in profiles"
              :key="profile.id"
            >
              <div class="card-body">
                <h5 class="card-title">{{ profile.description }}</h5>
                <p class="card-text">
                  {{ profile.biography.substring(0, 100) }}...
                </p>
                <div class="d-flex justify-content-between">
                  <router-link
                    :to="`/profiles/${profile.id}`"
                    class="btn btn-info"
                    >View Details</router-link
                  >
                  <button
                    class="btn btn-primary"
                    @click="findMatches(profile.id)"
                  >
                    Match Me
                  </button>
                </div>
              </div>
            </div>

            <div v-if="profiles.length < 3" class="mt-3">
              <router-link to="/profiles/new" class="btn btn-primary"
                >Create New Profile</router-link
              >
            </div>
          </div>
        </div>
      </div>

      <!-- Matches Section (shown when Match Me button is clicked) -->
      <div v-if="showMatches" class="mt-4">
        <h3>Your Matches</h3>
        <div v-if="matches.length > 0" class="row">
          <div class="col-md-3 mb-4" v-for="match in matches" :key="match.id">
            <div class="card">
              <img
                :src="match.user.photo"
                class="card-img-top"
                alt="Profile Photo"
              />
              <div class="card-body">
                <h5 class="card-title">{{ match.user.name }}</h5>
                <p class="card-text">{{ match.description }}</p>
                <router-link
                  :to="`/profiles/${match.id}`"
                  class="btn btn-primary"
                  >View more details</router-link
                >
              </div>
            </div>
          </div>
        </div>
        <div v-else class="alert alert-info">
          No matches found for your profile.
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "UserProfile",
  data() {
    return {
      user: null,
      profiles: [],
      matches: [],
      loading: true,
      error: null,
      showMatches: false,
    };
  },
  created() {
    this.fetchUserData();
  },
  methods: {
    fetchUserData() {
      const token = localStorage.getItem("token");
      const userId = this.$route.params.user_id;

      axios
        .get(`/api/users/${userId}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        .then((response) => {
          this.user = response.data;
          return axios.get(`/api/profiles`, {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
        })
        .then((response) => {
          // Filter profiles for current user
          this.profiles = response.data.filter(
            (profile) =>
              profile.user_id_fk === parseInt(this.$route.params.user_id)
          );
          this.loading = false;
        })
        .catch((error) => {
          this.error = "Failed to load user data";
          this.loading = false;
          console.error("Error fetching user data:", error);
        });
    },
    findMatches(profileId) {
      const token = localStorage.getItem("token");

      this.showMatches = true;

      axios
        .get(`/api/profiles/matches/${profileId}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        .then((response) => {
          this.matches = response.data;
        })
        .catch((error) => {
          console.error("Error fetching matches:", error);
        });
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleDateString();
    },
  },
};
</script>
