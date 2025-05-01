<template>
  <div class="profile-card">
    <div class="profile-card-inner">
      <div class="profile-img-container">
        <img
          :src="photo ? `${uploadBase}/api/uploads/${photo}` : defaultProfile"
          alt="Profile Photo"
          class="profile-img"
        />
      </div>
      <div class="profile-details">
        <h3 class="profile-name">{{ name || "User" }}</h3>
        <p class="profile-description">{{ description }}</p>
        <router-link :to="`/profiles/${id}`" class="profile-link">
          View Profile
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import defaultProfile from "@/assets/defaultProfileImg.png";
import apiClient from "@/api";

export default {
  name: "ProfileCard",
  props: {
    id: Number,
    name: String,
    description: String,
    photo: String,
  },
  computed: {
    uploadBase() {
      return apiClient.defaults.baseURL;
    },
    defaultProfile() {
      return defaultProfile;
    },
  },
};
</script>

<style scoped>
.profile-card {
  background: white;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.12);
  transition: all 0.3s ease;
  position: relative;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.profile-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.18);
}

.profile-card-inner {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.profile-img-container {
  overflow: hidden;
  position: relative;
}

.profile-img {
  width: 100%;
  height: 220px;
  object-fit: cover;
  background: #f8f9fa;
  transition: transform 0.6s ease;
}

.profile-card:hover .profile-img {
  transform: scale(1.05);
}

.profile-details {
  padding: 1.5rem;
  text-align: center;
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  justify-content: space-between;
}

.profile-name {
  font-size: 1.3rem;
  font-weight: 600;
  color: #04acb0;
  margin-bottom: 0.5rem;
}

.profile-description {
  font-size: 1rem;
  color: #555;
  margin-bottom: 1.5rem;
  line-height: 1.5;
  flex-grow: 1;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

.profile-link {
  display: inline-block;
  background: linear-gradient(45deg, #04acb0, #ff7455);
  color: white;
  padding: 0.6rem 1.4rem;
  border-radius: 50px;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
}

.profile-link:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 15px rgba(4, 172, 176, 0.3);
}

@media (max-width: 768px) {
  .profile-img {
    height: 180px;
  }

  .profile-name {
    font-size: 1.2rem;
  }

  .profile-description {
    font-size: 0.9rem;
  }

  .profile-link {
    padding: 0.5rem 1.2rem;
    font-size: 0.9rem;
  }
}
</style>
