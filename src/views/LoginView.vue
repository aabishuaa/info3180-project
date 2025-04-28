<template>
  <div class="login-page">
    <!-- Background Elements -->
    <div class="background-elements">
      <div class="blob blob-1"></div>
      <div class="blob blob-2"></div>
      <div class="blob blob-3"></div>
      <div class="blob blob-4"></div>
    </div>

    <!-- Login Content -->
    <div class="login-container">
      <div class="login-content">
        <h2 class="welcome-text">Welcome Back</h2>
        <p class="subtitle">Sign in to your Jam-Date account</p>

        <div class="login-form-wrapper">
          <div
            v-if="error"
            class="alert alert-danger animate__animated animate__shakeX"
          >
            {{ error }}
          </div>

          <form @submit.prevent="login" class="login-form">
            <div class="form-group">
              <label for="username">Username</label>
              <input
                type="text"
                id="username"
                v-model="credentials.username"
                required
                placeholder="Enter your username"
              />
            </div>

            <div class="form-group">
              <label for="password">Password</label>
              <input
                type="password"
                id="password"
                v-model="credentials.password"
                required
                placeholder="Enter your password"
              />
            </div>

            <button type="submit" class="sign-in-btn" :disabled="isSubmitting">
              <span v-if="isSubmitting">
                <span class="spinner"></span>
                Signing in...
              </span>
              <span v-else>Sign In</span>
            </button>
          </form>

          <div class="register-prompt">
            Don't have an account?
            <router-link to="/register">Register</router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Login",
  needsContainer: false,
  data() {
    return {
      credentials: {
        username: "",
        password: "",
      },
      error: null,
      isSubmitting: false,
    };
  },
  methods: {
    login() {
      this.isSubmitting = true;
      this.error = null;

      axios
        .post("/api/auth/login", this.credentials)
        .then((response) => {
          // Save token and user info to local storage
          localStorage.setItem("token", response.data.token);
          localStorage.setItem("user", JSON.stringify(response.data.user));

          // Redirect to the user's profile page
          const userInfo = JSON.parse(localStorage.getItem("user"));
          if (userInfo && userInfo.id) {
            this.$router.push(`/users/${userInfo.id}`);
          } else {
            this.$router.push("/");
          }
        })
        .catch((error) => {
          if (error.response && error.response.data) {
            this.error = error.response.data.message || "Login failed";
          } else {
            this.error = "An error occurred. Please try again.";
          }
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

.login-page {
  font-family: "Poppins", sans-serif;
  min-height: 100vh;
  background: linear-gradient(
    135deg,
    rgba(255, 255, 255, 0.95) 0%,
    rgba(240, 240, 240, 0.9) 100%
  );
  position: relative;
  overflow: hidden;
  color: #333;
  display: flex;
  flex-direction: column;
  justify-content: center;
  width: 100%;
}

/* Background Elements */
.background-elements {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  z-index: 1;
  overflow: hidden;
}

.blob {
  position: absolute;
  border-radius: 50%;
  opacity: 0.5;
  filter: blur(60px);
}

.blob-1 {
  width: 500px;
  height: 500px;
  background-color: rgba(4, 172, 176, 0.3);
  top: -200px;
  right: -100px;
  animation: float 15s ease-in-out infinite;
}

.blob-2 {
  width: 600px;
  height: 600px;
  background-color: rgba(255, 189, 15, 0.2);
  bottom: -250px;
  left: -200px;
  animation: float 18s ease-in-out infinite alternate;
}

.blob-3 {
  width: 300px;
  height: 300px;
  background-color: rgba(255, 116, 85, 0.2);
  top: 40%;
  right: 10%;
  animation: float 12s ease-in-out infinite 2s;
}

.blob-4 {
  width: 250px;
  height: 250px;
  background-color: rgba(251, 150, 35, 0.2);
  top: 30%;
  left: 15%;
  animation: float 10s ease-in-out infinite 1s alternate;
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

/* Login Content */
.login-container {
  position: relative;
  z-index: 2;
  width: 100%;
  padding: 0 20px;
  box-sizing: border-box;
  margin-top: -50px; /* Adjust to account for header */
  display: flex;
  justify-content: center;
}

.login-content {
  width: 100%;
  max-width: 450px;
  text-align: center;
}

.welcome-text {
  font-weight: 600;
  font-size: 32px;
  color: #04acb0;
  margin-bottom: 10px;
}

.subtitle {
  color: #666;
  font-weight: 300;
  font-size: 18px;
  margin-bottom: 40px;
}

.login-form-wrapper {
  position: relative;
  z-index: 2;
  background: linear-gradient(
    135deg,
    rgba(255, 255, 255, 0.7) 0%,
    rgba(255, 255, 255, 0.4) 100%
  );
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  padding: 30px;
  border-radius: 20px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.05);
}

.login-form {
  text-align: left;
}

.form-group {
  margin-bottom: 25px;
}

.form-group label {
  display: block;
  font-weight: 500;
  margin-bottom: 8px;
  color: #555;
  font-size: 15px;
}

.form-group input {
  width: 100%;
  padding: 15px;
  border-radius: 10px;
  border: 1px solid rgba(0, 0, 0, 0.1);
  background-color: rgba(255, 255, 255, 0.8);
  font-family: "Poppins", sans-serif;
  font-size: 16px;
  transition: all 0.3s ease;
}

.form-group input:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(4, 172, 176, 0.2);
  border-color: #04acb0;
  background-color: white;
}

.sign-in-btn {
  width: 100%;
  padding: 15px;
  border-radius: 10px;
  background: linear-gradient(135deg, #04acb0 0%, #038e91 100%);
  color: white;
  font-family: "Poppins", sans-serif;
  font-weight: 600;
  font-size: 16px;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 10px rgba(4, 172, 176, 0.3);
  margin-top: 10px;
}

.sign-in-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 15px rgba(4, 172, 176, 0.4);
}

.sign-in-btn:active:not(:disabled) {
  transform: translateY(1px);
  box-shadow: 0 2px 5px rgba(4, 172, 176, 0.3);
}

.sign-in-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.register-prompt {
  margin-top: 30px;
  font-size: 15px;
  color: #666;
}

.register-prompt a {
  color: #fb9623;
  font-weight: 600;
  text-decoration: none;
  position: relative;
  transition: all 0.3s ease;
}

.register-prompt a:hover {
  color: #ff7455;
}

.register-prompt a:after {
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

.register-prompt a:hover:after {
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
  .login-content {
    padding: 0;
  }

  .welcome-text {
    font-size: 28px;
  }

  .subtitle {
    font-size: 16px;
    margin-bottom: 30px;
  }
}
</style>
