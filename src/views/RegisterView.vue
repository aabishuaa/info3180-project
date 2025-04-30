<!-- src/components/Register.vue -->
<template>
  <div class="register">
    <div class="background-blobs">
      <div class="blob blob-1"></div>
      <div class="blob blob-2"></div>
      <div class="blob blob-3"></div>
    </div>

    <div class="container py-5">
      <h2 class="text-center mb-4">Find Your Perfect Match</h2>
      <p class="text-center subtitle mb-5">
        Create your Jam-Date account and start connecting
      </p>

      <div class="row justify-content-center">
        <div class="col-md-8 col-lg-6">
          <div class="card registration-card">
            <div class="card-body p-4">
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
                <div class="mb-3">
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

                <div class="mb-3">
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

                <div class="mb-3">
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

                <div class="mb-3">
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

                <div class="mb-4">
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

                <div class="d-grid">
                  <button
                    type="submit"
                    class="btn btn-primary register-btn animate__animated"
                    :class="{ animate__pulse: isSubmitting }"
                    :disabled="isSubmitting"
                  >
                    <span v-if="isSubmitting">
                      <span
                        class="spinner-border spinner-border-sm me-2"
                        role="status"
                        aria-hidden="true"
                      ></span>
                      Creating your account...
                    </span>
                    <span v-else>Create Account</span>
                  </button>
                </div>
              </form>

              <div class="mt-4 text-center login-link">
                Already have an account?
                <router-link
                  to="/login"
                  class="animate__animated animate__pulse"
                  >Login</router-link
                >
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

.register {
  font-family: "Poppins", sans-serif;
  position: relative;
  min-height: 100vh;
  overflow: hidden;
  padding: 40px 0;
  color: #333;
}

.background-blobs {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  z-index: -1;
  overflow: hidden;
}

.blob {
  position: absolute;
  border-radius: 50%;
  opacity: 0.6;
  filter: blur(60px);
}

.blob-1 {
  width: 500px;
  height: 500px;
  background-color: #04acb0;
  top: -200px;
  right: -100px;
  animation: float 8s ease-in-out infinite;
}

.blob-2 {
  width: 400px;
  height: 400px;
  background-color: #ffbd0f;
  bottom: -150px;
  left: -150px;
  animation: float 10s ease-in-out infinite alternate;
}

.blob-3 {
  width: 300px;
  height: 300px;
  background-color: #ff7455;
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

h2 {
  font-weight: 600;
  color: #04acb0;
  letter-spacing: 0.5px;
}

.subtitle {
  color: #666;
  font-weight: 300;
}

.registration-card {
  border: none;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  transform: translateY(0);
  transition: transform 0.3s ease;
  background-color: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
}

.registration-card:hover {
  transform: translateY(-5px);
}

.custom-input {
  border-radius: 8px;
  padding: 12px;
  border: 1px solid #e0e0e0;
  background-color: #f9f9f9;
  transition: all 0.3s ease;
}

.custom-input:focus {
  box-shadow: 0 0 0 3px rgba(4, 172, 176, 0.2);
  border-color: #04acb0;
}

.form-label {
  font-weight: 500;
  margin-bottom: 8px;
  color: #555;
}

.register-btn {
  padding: 12px;
  border-radius: 8px;
  font-weight: 600;
  letter-spacing: 0.5px;
  background-color: #fb9623;
  border: none;
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px rgba(251, 150, 35, 0.2);
}

.register-btn:hover:not(:disabled) {
  background-color: #ff7455;
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(255, 116, 85, 0.3);
}

.register-btn:active:not(:disabled) {
  transform: translateY(1px);
}

.register-btn:disabled {
  background-color: #fb9623;
  opacity: 0.7;
}

.login-link a {
  color: #04acb0;
  font-weight: 500;
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
  border-radius: 8px;
  padding: 12px 15px;
}

.alert-danger {
  background-color: rgba(255, 116, 85, 0.1);
  border-color: rgba(255, 116, 85, 0.2);
  color: #ff7455;
}

.alert-success {
  background-color: rgba(4, 172, 176, 0.1);
  border-color: rgba(4, 172, 176, 0.2);
  color: #04acb0;
}
</style>
