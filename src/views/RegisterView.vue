<template>
  <div class="register-page">
    <!-- Fixed background with gradient -->
    <div class="background"></div>

    <!-- Animated blob background elements -->
    <div class="blob blob-1"></div>
    <div class="blob blob-2"></div>
    <div class="blob blob-3"></div>

    <!-- Main content -->
    <div class="page-content">
      <div class="register-section">
        <div class="register-container">
          <h2 class="text-center mb-4">Find Your Perfect Match</h2>
          <p class="text-center subtitle mb-5">
            Create your Jam-Date account and start connecting
          </p>

          <div class="registration-card">
            <div
              v-if="error"
              class="alert alert-danger animate__animated animate__shakeX"
            >
              {{ error }}
            </div>

            <div
              v-if="successMessage"
              class="alert alert-success animate__animated animate__fadeIn"
            >
              {{ successMessage }}
            </div>

            <form @submit.prevent="register">
              <div class="form-group">
                <label for="username" class="form-label">Username</label>
                <input
                  type="text"
                  class="form-control custom-input"
                  id="username"
                  v-model="user.username"
                  required
                  :class="{ 'is-invalid': errors.username }"
                />
                <div class="invalid-feedback" v-if="errors.username">
                  {{ errors.username }}
                </div>
              </div>

              <div class="form-group">
                <label for="password" class="form-label">Password</label>
                <input
                  type="password"
                  class="form-control custom-input"
                  id="password"
                  v-model="user.password"
                  required
                  minlength="8"
                  :class="{ 'is-invalid': errors.password }"
                />
                <div class="invalid-feedback" v-if="errors.password">
                  {{ errors.password }}
                </div>
                <small class="form-text text-muted"
                  >Password must be at least 8 characters long</small
                >
              </div>

              <div class="form-group">
                <label for="confirmPassword" class="form-label"
                  >Confirm Password</label
                >
                <input
                  type="password"
                  class="form-control custom-input"
                  id="confirmPassword"
                  v-model="confirmPassword"
                  required
                  :class="{ 'is-invalid': errors.confirmPassword }"
                />
                <div class="invalid-feedback" v-if="errors.confirmPassword">
                  {{ errors.confirmPassword }}
                </div>
              </div>

              <div class="form-group">
                <label for="name" class="form-label">Full Name</label>
                <input
                  type="text"
                  class="form-control custom-input"
                  id="name"
                  v-model="user.name"
                  required
                  :class="{ 'is-invalid': errors.name }"
                />
                <div class="invalid-feedback" v-if="errors.name">
                  {{ errors.name }}
                </div>
              </div>

              <div class="form-group">
                <label for="email" class="form-label">Email</label>
                <input
                  type="email"
                  class="form-control custom-input"
                  id="email"
                  v-model="user.email"
                  required
                  :class="{ 'is-invalid': errors.email }"
                />
                <div class="invalid-feedback" v-if="errors.email">
                  {{ errors.email }}
                </div>
              </div>

              <button
                type="submit"
                class="register-btn animate__animated"
                :class="{ animate__pulse: isSubmitting }"
                :disabled="isSubmitting"
              >
                <span v-if="isSubmitting">
                  <span class="spinner"></span>
                  Creating your account...
                </span>
                <span v-else>Create Account</span>
              </button>
            </form>

            <div class="login-link">
              Already have an account?
              <router-link to="/login" class="animate__animated animate__pulse"
                >Login</router-link
              >
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
  name: "Register",
  needsContainer: false,
  data() {
    return {
      user: {
        username: "",
        password: "",
        name: "",
        email: "",
      },
      confirmPassword: "",
      error: null,
      successMessage: null,
      isSubmitting: false,
      errors: {
        username: null,
        password: null,
        confirmPassword: null,
        name: null,
        email: null,
      },
    };
  },
  methods: {
    validateForm() {
      let isValid = true;
      this.errors = {
        username: null,
        password: null,
        confirmPassword: null,
        name: null,
        email: null,
      };

      if (this.user.username.length < 3) {
        this.errors.username = "Username must be at least 3 characters";
        isValid = false;
      }

      if (this.user.password.length < 8) {
        this.errors.password = "Password must be at least 8 characters";
        isValid = false;
      }

      if (this.user.password !== this.confirmPassword) {
        this.errors.confirmPassword = "Passwords do not match";
        isValid = false;
      }

      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(this.user.email)) {
        this.errors.email = "Please enter a valid email address";
        isValid = false;
      }

      return isValid;
    },
    register() {
      if (!this.validateForm()) {
        return;
      }

      this.isSubmitting = true;
      this.error = null;
      this.successMessage = null;

      apiClient
        .post("api/register", this.user)
        .then(() => {
          this.successMessage =
            "Registration successful! Redirecting you to login...";
          setTimeout(() => {
            this.$router.push("/login");
          }, 2000);
        })
        .catch((error) => {
          this.error = error.response?.data?.message || "Registration failed.";
        })
        .finally(() => {
          this.isSubmitting = false;
        });
    },
  },
};
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap");
@import url("https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css");

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.register-page {
  font-family: "Poppins", sans-serif;
  min-height: 100vh;
  position: relative;
  overflow: hidden;
  color: #333;
}

/* Fixed background with gradient */
.background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    135deg,
    rgba(255, 255, 255, 0.95) 0%,
    rgba(240, 240, 240, 0.9) 100%
  );
  z-index: -2;
}

/* Animated blob background elements */
.blob {
  position: fixed;
  border-radius: 50%;
  opacity: 0.6;
  filter: blur(60px);
  z-index: -1;
}

.blob-1 {
  width: 500px;
  height: 500px;
  background-color: rgba(4, 172, 176, 0.5);
  top: -200px;
  right: -100px;
  animation: float 8s ease-in-out infinite;
}

.blob-2 {
  width: 400px;
  height: 400px;
  background-color: rgba(255, 189, 15, 0.5);
  bottom: -150px;
  left: -150px;
  animation: float 10s ease-in-out infinite alternate;
}

.blob-3 {
  width: 300px;
  height: 300px;
  background-color: rgba(255, 116, 85, 0.5);
  top: 50%;
  right: 10%;
  animation: float 12s ease-in-out infinite 2s;
}

@keyframes float {
  0% {
    transform: translateY(0) scale(1);
  }
  50% {
    transform: translateY(-20px) scale(1.05);
  }
  100% {
    transform: translateY(0) scale(1);
  }
}

/* Main content */
.page-content {
  position: relative;
  z-index: 1;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  width: 100%;
}

/* Register section */
.register-section {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
}

.register-container {
  width: 100%;
  max-width: 550px;
  text-align: center;
}

h2 {
  font-weight: 600;
  font-size: 32px;
  color: #04acb0;
  margin-bottom: 10px;
}

.subtitle {
  color: #666;
  font-weight: 300;
  font-size: 18px;
}

.registration-card {
  background: linear-gradient(
    135deg,
    rgba(255, 255, 255, 0.7) 0%,
    rgba(255, 255, 255, 0.4) 100%
  );
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  padding: 30px;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  text-align: left;
  transition: transform 0.3s ease;
}

.registration-card:hover {
  transform: translateY(-5px);
}

.form-group {
  margin-bottom: 20px;
}

.form-label {
  display: block;
  font-weight: 500;
  margin-bottom: 8px;
  color: #555;
  font-size: 15px;
}

.custom-input {
  width: 100%;
  padding: 12px;
  border-radius: 10px;
  border: 1px solid rgba(0, 0, 0, 0.1);
  background-color: rgba(255, 255, 255, 0.8);
  font-family: "Poppins", sans-serif;
  font-size: 16px;
  transition: all 0.3s ease;
}

.custom-input:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(4, 172, 176, 0.2);
  border-color: #04acb0;
  background-color: white;
}

.is-invalid {
  border-color: #ff7455;
}

.invalid-feedback {
  color: #ff7455;
  font-size: 14px;
  margin-top: 5px;
}

.form-text {
  font-size: 13px;
  margin-top: 5px;
}

.register-btn {
  width: 100%;
  padding: 15px;
  border-radius: 10px;
  background: linear-gradient(135deg, #fb9623 0%, #ff7455 100%);
  color: white;
  font-family: "Poppins", sans-serif;
  font-weight: 600;
  font-size: 16px;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 10px rgba(251, 150, 35, 0.3);
  margin-top: 10px;
  margin-bottom: 20px;
}

.register-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 15px rgba(255, 116, 85, 0.4);
}

.register-btn:active:not(:disabled) {
  transform: translateY(1px);
  box-shadow: 0 2px 5px rgba(251, 150, 35, 0.3);
}

.register-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.login-link {
  margin-top: 20px;
  font-size: 15px;
  color: #666;
  text-align: center;
}

.login-link a {
  color: #04acb0;
  font-weight: 600;
  text-decoration: none;
  position: relative;
  transition: all 0.3s ease;
}

.login-link a:hover {
  color: #ff7455;
}

.login-link a:after {
  content: "";
  position: absolute;
  width: 100%;
  height: 2px;
  bottom: -2px;
  left: 0;
  background-color: #ff7455;
  transform: scaleX(0);
  transform-origin: bottom right;
  transition: transform 0.3s;
}

.login-link a:hover:after {
  transform: scaleX(1);
  transform-origin: bottom left;
}

.alert {
  padding: 15px;
  border-radius: 10px;
  margin-bottom: 25px;
  font-size: 15px;
}

.alert-danger {
  background-color: rgba(255, 116, 85, 0.1);
  border: 1px solid rgba(255, 116, 85, 0.2);
  color: #ff7455;
}

.alert-success {
  background-color: rgba(4, 172, 176, 0.1);
  border: 1px solid rgba(4, 172, 176, 0.2);
  color: #04acb0;
}

.spinner {
  display: inline-block;
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 0.8s linear infinite;
  margin-right: 8px;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Responsive adjustments */
@media (max-width: 768px) {
  h2 {
    font-size: 28px;
  }

  .subtitle {
    font-size: 16px;
    margin-bottom: 30px;
  }

  .registration-card {
    padding: 20px;
  }
}
</style>
