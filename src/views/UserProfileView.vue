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
        <!-- Left: User Card and Upload -->
        <div class="col-md-4">
          <div class="card mb-3">
            <img
              :key="photoKey"
              :src="`${uploadBase}/api/uploads/${user.photo}`"
              class="card-img-top"
              alt="Profile"
            />

            <div class="card-body">
              <h5 class="card-title">{{ user.name }}</h5>
              <p class="card-text">{{ user.email }}</p>
              <p class="card-text">
                <small class="text-muted">
                  Member since {{ formatDate(user.date_joined) }}
                </small>
              </p>
            </div>
          </div>

          <!-- Upload Profile Photo -->
          <div class="card">
            <div class="card-body">
              <h6 class="card-title">Update Profile Photo</h6>
              <form @submit.prevent="submitPhoto" enctype="multipart/form-data">
                <input
                  type="file"
                  accept="image/*"
                  @change="handleFileChange"
                  class="form-control mb-2"
                  required
                />
                <button type="submit" class="btn btn-primary btn-sm">
                  Upload
                </button>
                <div v-if="uploadMessage" class="alert alert-success mt-2">
                  {{ uploadMessage }}
                </div>
                <div v-if="uploadError" class="alert alert-danger mt-2">
                  {{ uploadError }}
                </div>
              </form>
            </div>
          </div>
        </div>

        <!-- Right: User Profiles -->
        <div class="col-md-8">
          <h3>My Profiles</h3>
          <p v-if="profiles.length === 0">
            You haven't created any profiles yet.
            <router-link to="/profiles/new" class="btn btn-primary">
              Create Profile
            </router-link>
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
                  {{ (profile.biography || "").substring(0, 100) }}...
                </p>
                <div class="d-flex justify-content-between">
                  <router-link
                    :to="`/profiles/${profile.id}`"
                    class="btn btn-info"
                  >
                    View Details
                  </router-link>
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
              <router-link to="/profiles/new" class="btn btn-primary">
                Create New Profile
              </router-link>
            </div>
          </div>
        </div>
      </div>

      <!-- Matches Section -->
      <div v-if="showMatches" class="mt-4">
        <h3>Your Matches</h3>
        <div v-if="matches.length > 0" class="row">
          <div class="col-md-3 mb-4" v-for="match in matches" :key="match.id">
            <div class="card">
              <div class="card-body">
                <h5 class="card-title">Compatible Match</h5>
                <p class="card-text">{{ match.description }}</p>
                <router-link
                  :to="`/profiles/${match.id}`"
                  class="btn btn-primary"
                >
                  View more details
                </router-link>
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
import apiClient from "@/api.js";

// ensure every request from apiClient sends cookies
apiClient.defaults.withCredentials = true;

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
      csrfToken: "",
      photoFile: null,
      photoKey: Date.now(),
      uploadMessage: null,
      uploadError: null,
    };
  },
  computed: {
    // full backend URL for image src
    uploadBase() {
      return apiClient.defaults.baseURL;
    },
  },
  async created() {
    await this.fetchCsrfToken();
    this.fetchUserData();
  },
  methods: {
    fetchCsrfToken() {
      apiClient
        .get("/api/csrf-token")
        .then((response) => {
          this.csrfToken = response.data.csrf_token;
        })
        .catch((error) => {
          console.error("Failed to get CSRF token", error);
        });
    },

    async fetchUserData() {
      try {
        const userId = localStorage.getItem("user_id");
        // 1) fetch the user object (including its profiles array)
        const resUser = await apiClient.get(`/api/users/${userId}`);
        this.user = resUser.data.user;

        // 2) pull out that user.profiles array directly
        //    (each {id, description, …} comes from your backend)
        this.profiles = resUser.data.user.profiles || [];
      } catch (err) {
        this.error = err.response?.data?.message || "Failed to load user data.";
      } finally {
        this.loading = false;
      }
    },

    handleFileChange(e) {
      this.photoFile = e.target.files[0];
    },
    submitPhoto() {
      const formData = new FormData();
      formData.append("photo", this.photoFile);

      const userId = localStorage.getItem("user_id");
      apiClient
        .post(`/api/users/${userId}/photo`, formData)
        .then((response) => {
          this.uploadMessage = response.data.message;
          this.user.photo = response.data.photo;
          this.photoKey = Date.now();
        })
        .catch((error) => {
          this.uploadError =
            error.response?.data?.errors?.[0] || "Upload failed.";
        });
    },

    async findMatches(id) {
      this.showMatches = true;
      try {
        const res = await apiClient.get(`/api/profiles/matches/${id}`);
        this.matches = res.data.matches;
      } catch (err) {
        console.error(err);
      }
    },

    formatDate(d) {
      return new Date(d).toLocaleDateString();
    },
  },
};
</script>

<style scoped>
.card-img-top {
  width: 100%;
  height: 200px;
  object-fit: contain;
  background: #f8f9fa;
  border-bottom: 1px solid #eee;
}
</style>
