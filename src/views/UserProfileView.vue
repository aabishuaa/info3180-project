<template>
  <div class="user-profile">
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <div v-else-if="error" class="alert alert-danger">
      {{ error }}
    </div>

    <div v-else class="container py-4">
      <div class="row mb-4">
        <!-- Left: User Card and Upload -->
        <div class="col-md-4">
          <div class="card profile-card mb-3 shadow-sm">
            <div class="profile-image-container">
              <img
                :key="photoKey"
                :src="profileImageSrc"
                class="card-img-top"
                alt="Profile"
              />
              <div class="profile-image-overlay" @click="triggerFileInput">
                <i class="bi bi-camera-fill"></i>
                <span>Update Photo</span>
              </div>
            </div>

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

          <!-- Hidden Upload Form -->
          <form
            @submit.prevent="submitPhoto"
            enctype="multipart/form-data"
            class="d-none"
          >
            <input
              ref="fileInput"
              type="file"
              accept="image/*"
              @change="handleFileChange"
              class="form-control"
              id="profilePhotoInput"
            />
          </form>
          <div v-if="uploadMessage" class="alert alert-success mt-2">
            {{ uploadMessage }}
          </div>
          <div v-if="uploadError" class="alert alert-danger mt-2">
            {{ uploadError }}
          </div>
        </div>

        <!-- Right: User Profiles -->
        <div class="col-md-8">
          <div class="section-header mb-3">
            <h3 class="section-title">My Profiles</h3>
            <div v-if="profiles.length < 3 && profiles.length > 0">
              <router-link
                to="/profiles/new"
                class="btn btn-primary create-profile-btn"
              >
                <i class="bi bi-plus-circle me-1"></i> Create Profile
              </router-link>
            </div>
          </div>

          <div v-if="profiles.length === 0" class="empty-profiles-container">
            <p class="empty-profiles-message">
              You haven't created any profiles yet.
            </p>
            <router-link
              to="/profiles/new"
              class="btn btn-primary create-profile-btn mt-3"
            >
              <i class="bi bi-plus-circle me-1"></i> Create Profile
            </router-link>
          </div>

          <div v-else>
            <div
              class="card profile-list-card mb-3 shadow-sm"
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
                    class="btn view-details-btn"
                  >
                    <i class="bi bi-eye me-1"></i> View Details
                  </router-link>

                  <router-link
                    :to="`/matches/${profile.id}`"
                    class="btn btn-primary"
                  >
                    <i class="bi bi-heart me-1"></i> Match Me
                  </router-link>
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
import defaultProfileImg from "@/assets/defaultProfileImg.png";

// ensure every request from apiClient sends cookies
apiClient.defaults.withCredentials = true;

export default {
  name: "UserProfile",
  data() {
    return {
      user: null,
      profiles: [],
      loading: true,
      error: null,
      csrfToken: "",
      photoFile: null,
      photoKey: Date.now(),
      uploadMessage: null,
      uploadError: null,
      defaultProfileImg: defaultProfileImg,
    };
  },
  computed: {
    // full backend URL for image src
    uploadBase() {
      return apiClient.defaults.baseURL;
    },
    profileImageSrc() {
      if (this.user && this.user.photo) {
        return `${this.uploadBase}/api/uploads/${this.user.photo}`;
      }
      return this.defaultProfileImg;
    },
  },
  async created() {
    await this.fetchCsrfToken();
    this.fetchUserData();
  },
  methods: {
    triggerFileInput() {
      this.$refs.fileInput.click();
    },

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
      if (this.photoFile) {
        this.submitPhoto();
      }
    },

    submitPhoto() {
      const formData = new FormData();
      formData.append("photo", this.photoFile);

      this.uploadMessage = null;
      this.uploadError = null;

      const userId = localStorage.getItem("user_id");
      apiClient
        .post(`/api/users/${userId}/photo`, formData)
        .then((response) => {
          this.uploadMessage = response.data.message;
          this.user.photo = response.data.photo;
          this.photoKey = Date.now();

          // Hide the message after 3 seconds
          setTimeout(() => {
            this.uploadMessage = null;
          }, 3000);
        })
        .catch((error) => {
          this.uploadError =
            error.response?.data?.errors?.[0] || "Upload failed.";

          // Hide the error after 5 seconds
          setTimeout(() => {
            this.uploadError = null;
          }, 5000);
        });
    },

    formatDate(d) {
      return new Date(d).toLocaleDateString();
    },
  },
};
</script>

<style scoped>
/* Import Google Fonts - Poppins */
@import url("https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap");
/* Import Bootstrap Icons */
@import url("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css");

.user-profile {
  font-family: "Poppins", sans-serif;
}

.card {
  border-radius: 10px;
  overflow: hidden;
  transition: transform 0.2s, box-shadow 0.2s;
}

.card:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1) !important;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.section-title {
  font-weight: 600;
  color: #3a3a3a;
  position: relative;
  padding-bottom: 8px;
  margin-bottom: 0;
}

.section-title:after {
  content: "";
  position: absolute;
  width: 50px;
  height: 3px;
  background-color: #04acb0;
  bottom: 0;
  left: 0;
}

.profile-image-container {
  position: relative;
  overflow: hidden;
}

.card-img-top {
  width: 100%;
  height: 250px;
  object-fit: cover;
  background: #f8f9fa;
  transition: filter 0.3s;
}

.profile-image-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: rgba(0, 0, 0, 0.7);
  color: white;
  text-align: center;
  padding: 12px;
  transform: translateY(100%);
  transition: transform 0.3s ease;
  cursor: pointer;
}

.profile-image-container:hover .profile-image-overlay {
  transform: translateY(0);
}

.profile-image-container:hover .card-img-top {
  filter: brightness(0.8);
}

.profile-image-overlay i {
  font-size: 20px;
  margin-right: 5px;
}

.card-body {
  padding: 1.5rem;
}

.card-title {
  font-weight: 600;
  color: #333;
  margin-bottom: 12px;
}

.btn {
  font-weight: 500;
  padding: 0.5rem 1rem;
  border-radius: 5px;
}

.create-profile-btn {
  background: linear-gradient(45deg, #04acb0, #04acb0);
  color: white;
  font-weight: 500;
  border: none;
  border-radius: 5px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 10px rgba(4, 172, 176, 0.2);
  display: inline-flex;
  align-items: center;
}

.create-profile-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 16px rgba(4, 172, 176, 0.4);
  background: linear-gradient(45deg, #038e91, #04acb0);
}

.view-details-btn {
  background: linear-gradient(45deg, #04acb0, #ff7455);
  color: white;
  font-weight: 500;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 5px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 10px rgba(4, 172, 176, 0.2);
  display: inline-flex;
  align-items: center;
}

.view-details-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 16px rgba(4, 172, 176, 0.4);
  text-decoration: none;
}

.match-card {
  display: flex;
  flex-direction: column;
}

.card-button-container {
  margin-top: auto;
}

.alert {
  border-radius: 8px;
  font-weight: 500;
}

.empty-profiles-container {
  background-color: #f8f9fa;
  border-radius: 10px;
  padding: 2rem;
  text-align: center;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
  margin-bottom: 1.5rem;
}

.empty-profiles-message {
  font-size: 1.1rem;
  color: #555;
  margin-bottom: 0;
}
</style>
