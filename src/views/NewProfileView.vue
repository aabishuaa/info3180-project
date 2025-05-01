<template>
  <div class="new-profile-page">
    <div class="container py-4">
      <!-- Back navigation -->
      <router-link :to="`/users/${userId}`" class="back-btn">
        <i class="bi bi-arrow-left"></i> Back to Profile
      </router-link>

      <div class="form-container">
        <div class="form-header">
          <h1 class="form-title">Create Your Profile</h1>
          <p class="form-subtitle">
            Share your details and preferences with the community
          </p>
        </div>

        <div v-if="loading" class="text-center py-5">
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
        </div>

        <div v-else-if="error" class="alert alert-danger">
          {{ error }}
        </div>

        <form v-else @submit.prevent="submitProfile" class="profile-form">
          <!-- Progress indicator -->
          <div class="progress-container">
            <div class="progress">
              <div
                class="progress-bar"
                role="progressbar"
                :style="{ width: `${progressPercentage}%` }"
                :aria-valuenow="progressPercentage"
                aria-valuemin="0"
                aria-valuemax="100"
              >
                {{ progressPercentage }}%
              </div>
            </div>
            <div class="progress-text">{{ currentSection }} of 4</div>
          </div>

          <!-- Personal information section -->
          <div
            v-if="currentSection === 1"
            class="form-section animate__animated animate__fadeIn"
          >
            <h3 class="section-title">
              <i class="bi bi-person-vcard me-2"></i>Personal Information
            </h3>

            <div class="row">
              <div class="col-md-6 mb-3">
                <label for="description" class="form-label">Headline</label>
                <div class="input-group">
                  <span class="input-group-text"
                    ><i class="bi bi-chat-quote"></i
                  ></span>
                  <input
                    type="text"
                    id="description"
                    v-model="profile.description"
                    class="form-control"
                    placeholder="A short headline about yourself"
                    required
                  />
                </div>
                <div class="form-text">This will appear below your name</div>
              </div>

              <div class="col-md-6 mb-3">
                <label for="parish" class="form-label">Parish</label>
                <div class="input-group">
                  <span class="input-group-text"
                    ><i class="bi bi-geo-alt"></i
                  ></span>
                  <select
                    id="parish"
                    v-model="profile.parish"
                    class="form-select"
                    required
                    @change="handleParishChange"
                  >
                    <option value="" disabled>Select your parish</option>
                    <option
                      v-for="parish in parishes"
                      :key="parish"
                      :value="parish"
                    >
                      {{ parish }}
                    </option>
                    <option value="other">Other (specify)</option>
                  </select>
                </div>
                <input
                  v-if="profile.parish === 'other'"
                  type="text"
                  class="form-control mt-2"
                  v-model="profile.customParish"
                  placeholder="Enter your parish"
                  required
                />
              </div>
            </div>

            <div class="row">
              <div class="col-md-6 mb-3">
                <label for="birth_year" class="form-label">Birth Year</label>
                <div class="input-group">
                  <span class="input-group-text"
                    ><i class="bi bi-calendar3"></i
                  ></span>
                  <select
                    id="birth_year"
                    v-model.number="profile.birth_year"
                    class="form-select"
                    required
                  >
                    <option value="" disabled>Select birth year</option>
                    <option
                      v-for="year in birthYears"
                      :key="year"
                      :value="year"
                    >
                      {{ year }}
                    </option>
                  </select>
                </div>
              </div>

              <div class="col-md-6 mb-3">
                <label for="height" class="form-label">Height</label>
                <div class="input-group">
                  <span class="input-group-text"
                    ><i class="bi bi-rulers"></i
                  ></span>
                  <select
                    id="height_feet"
                    v-model.number="heightFeet"
                    class="form-select"
                    required
                    style="border-radius: 0"
                  >
                    <option value="" disabled>Feet</option>
                    <option v-for="n in 8" :key="`feet-${n}`" :value="n">
                      {{ n }}
                    </option>
                  </select>
                  <select
                    id="height_inches"
                    v-model.number="heightInches"
                    class="form-select"
                    required
                    style="border-radius: 0 10px 10px 0"
                  >
                    <option value="" disabled>Inches</option>
                    <option v-for="n in 11" :key="`inch-${n}`" :value="n">
                      {{ n - 1 }}
                    </option>
                  </select>
                  <span class="input-group-text">ft/in</span>
                </div>
              </div>
            </div>

            <div class="row">
              <div class="col-md-6 mb-3">
                <label for="sex" class="form-label">Sex</label>
                <div class="input-group">
                  <span class="input-group-text"
                    ><i class="bi bi-gender-ambiguous"></i
                  ></span>
                  <select
                    id="sex"
                    v-model="profile.sex"
                    class="form-select"
                    required
                  >
                    <option value="" disabled>Select your sex</option>
                    <option value="Male">Male</option>
                    <option value="Female">Female</option>
                    <option value="Other">Other</option>
                  </select>
                </div>
              </div>

              <div class="col-md-6 mb-3">
                <label for="race" class="form-label">Race</label>
                <div class="input-group">
                  <span class="input-group-text"
                    ><i class="bi bi-people"></i
                  ></span>
                  <select
                    id="race"
                    v-model="profile.race"
                    class="form-select"
                    required
                    @change="handleRaceChange"
                  >
                    <option value="" disabled>Select your race</option>
                    <option v-for="race in races" :key="race" :value="race">
                      {{ race }}
                    </option>
                    <option value="other">Other (specify)</option>
                  </select>
                </div>
                <input
                  v-if="profile.race === 'other'"
                  type="text"
                  class="form-control mt-2"
                  v-model="profile.customRace"
                  placeholder="Enter your race"
                  required
                />
              </div>
            </div>

            <div class="form-navigation">
              <button
                type="button"
                class="btn btn-primary btn-next"
                @click="validateAndNextSection"
              >
                Next <i class="bi bi-arrow-right"></i>
              </button>
            </div>
          </div>

          <!-- Biography section -->
          <div
            v-if="currentSection === 2"
            class="form-section animate__animated animate__fadeIn"
          >
            <h3 class="section-title">
              <i class="bi bi-file-person me-2"></i>Biography
            </h3>

            <div class="mb-4">
              <label for="biography" class="form-label"
                >Tell us about yourself</label
              >
              <div class="biography-container">
                <div class="biography-icon">
                  <i class="bi bi-journal-text"></i>
                </div>
                <textarea
                  id="biography"
                  v-model="profile.biography"
                  class="form-control biography-textarea"
                  rows="6"
                  placeholder="Share your story, interests, and what makes you unique..."
                  required
                  maxlength="500"
                ></textarea>
              </div>
              <div
                class="biography-counter"
                :class="{ 'text-danger': bioLength > 500 }"
              >
                {{ bioLength }}/500 characters
              </div>
            </div>

            <div class="form-navigation">
              <button
                type="button"
                class="btn btn-outline btn-prev"
                @click="prevSection"
              >
                <i class="bi bi-arrow-left"></i> Previous
              </button>
              <button
                type="button"
                class="btn btn-primary btn-next"
                @click="validateAndNextSection"
                :disabled="bioLength > 500"
              >
                Next <i class="bi bi-arrow-right"></i>
              </button>
            </div>
          </div>

          <!-- Preferences section -->
          <div
            v-if="currentSection === 3"
            class="form-section animate__animated animate__fadeIn"
          >
            <h3 class="section-title">
              <i class="bi bi-heart me-2"></i>Your Preferences
            </h3>

            <div class="row">
              <div class="col-md-4 mb-3">
                <label for="fav_cuisine" class="form-label"
                  >Favorite Cuisine</label
                >
                <div class="preference-card">
                  <div class="preference-icon">
                    <i class="bi bi-cup-hot"></i>
                  </div>
                  <select
                    id="fav_cuisine"
                    v-model="profile.fav_cuisine"
                    class="form-select"
                    required
                    @change="handleCuisineChange"
                  >
                    <option value="" disabled>Select cuisine</option>
                    <option
                      v-for="cuisine in cuisines"
                      :key="cuisine"
                      :value="cuisine"
                    >
                      {{ cuisine }}
                    </option>
                    <option value="other">Other (specify)</option>
                  </select>
                </div>
                <input
                  v-if="profile.fav_cuisine === 'other'"
                  type="text"
                  class="form-control mt-2"
                  v-model="profile.customCuisine"
                  placeholder="Enter your favorite cuisine"
                  required
                />
              </div>

              <div class="col-md-4 mb-3">
                <label for="fav_colour" class="form-label"
                  >Favorite Color</label
                >
                <div class="preference-card">
                  <div class="preference-icon">
                    <i class="bi bi-palette"></i>
                  </div>
                  <select
                    id="fav_colour"
                    v-model="profile.fav_colour"
                    class="form-select"
                    required
                    @change="handleColorChange"
                  >
                    <option value="" disabled>Select color</option>
                    <option v-for="color in colors" :key="color" :value="color">
                      {{ color }}
                    </option>
                    <option value="other">Other (specify)</option>
                  </select>
                </div>
                <input
                  v-if="profile.fav_colour === 'other'"
                  type="text"
                  class="form-control mt-2"
                  v-model="profile.customColor"
                  placeholder="Enter your favorite color"
                  required
                />
              </div>

              <div class="col-md-4 mb-3">
                <label for="fav_school_subject" class="form-label"
                  >Favorite Subject</label
                >
                <div class="preference-card">
                  <div class="preference-icon">
                    <i class="bi bi-book"></i>
                  </div>
                  <select
                    id="fav_school_subject"
                    v-model="profile.fav_school_subject"
                    class="form-select"
                    required
                    @change="handleSubjectChange"
                  >
                    <option value="" disabled>Select subject</option>
                    <option
                      v-for="subject in subjects"
                      :key="subject"
                      :value="subject"
                    >
                      {{ subject }}
                    </option>
                    <option value="other">Other (specify)</option>
                  </select>
                </div>
                <input
                  v-if="profile.fav_school_subject === 'other'"
                  type="text"
                  class="form-control mt-2"
                  v-model="profile.customSubject"
                  placeholder="Enter your favorite subject"
                  required
                />
              </div>
            </div>

            <div class="form-navigation">
              <button
                type="button"
                class="btn btn-outline btn-prev"
                @click="prevSection"
              >
                <i class="bi bi-arrow-left"></i> Previous
              </button>
              <button
                type="button"
                class="btn btn-primary btn-next"
                @click="validateAndNextSection"
              >
                Next <i class="bi bi-arrow-right"></i>
              </button>
            </div>
          </div>

          <!-- Values section -->
          <div
            v-if="currentSection === 4"
            class="form-section animate__animated animate__fadeIn"
          >
            <h3 class="section-title">
              <i class="bi bi-stars me-2"></i>Your Values
            </h3>

            <div class="values-container">
              <div
                class="value-card"
                :class="{ active: profile.political }"
                @click="profile.political = !profile.political"
              >
                <div class="value-icon">
                  <i class="bi bi-award"></i>
                </div>
                <div class="value-content">
                  <div class="value-title">Political</div>
                  <div class="value-description">
                    Interested in politics and current affairs
                  </div>
                </div>
                <div class="form-check form-switch">
                  <input
                    class="form-check-input"
                    type="checkbox"
                    v-model="profile.political"
                  />
                </div>
              </div>

              <div
                class="value-card"
                :class="{ active: profile.religious }"
                @click="profile.religious = !profile.religious"
              >
                <div class="value-icon">
                  <i class="bi bi-building-fill"></i>
                </div>
                <div class="value-content">
                  <div class="value-title">Religious</div>
                  <div class="value-description">
                    Faith plays an important role in your life
                  </div>
                </div>
                <div class="form-check form-switch">
                  <input
                    class="form-check-input"
                    type="checkbox"
                    v-model="profile.religious"
                  />
                </div>
              </div>

              <div
                class="value-card"
                :class="{ active: profile.family_oriented }"
                @click="profile.family_oriented = !profile.family_oriented"
              >
                <div class="value-icon">
                  <i class="bi bi-people-fill"></i>
                </div>
                <div class="value-content">
                  <div class="value-title">Family Oriented</div>
                  <div class="value-description">
                    Family is a central priority in your life
                  </div>
                </div>
                <div class="form-check form-switch">
                  <input
                    class="form-check-input"
                    type="checkbox"
                    v-model="profile.family_oriented"
                  />
                </div>
              </div>
            </div>

            <div class="form-navigation">
              <button
                type="button"
                class="btn btn-outline btn-prev"
                @click="prevSection"
              >
                <i class="bi bi-arrow-left"></i> Previous
              </button>
              <button
                type="submit"
                class="btn btn-primary"
                :disabled="isSubmitting"
              >
                <i class="bi bi-check-circle me-2"></i
                >{{ isSubmitting ? "Creating..." : "Create Profile" }}
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import apiClient from "@/api.js";
import "animate.css";

export default {
  name: "NewProfileForm",
  data() {
    return {
      currentSection: 1,
      userId: null,
      loading: false,
      error: null,
      isSubmitting: false,
      heightFeet: "",
      heightInches: "",
      profile: {
        description: "",
        biography: "",
        parish: "",
        customParish: "",
        sex: "",
        race: "",
        customRace: "",
        birth_year: "",
        height: "",
        fav_cuisine: "",
        customCuisine: "",
        fav_colour: "",
        customColor: "",
        fav_school_subject: "",
        customSubject: "",
        political: false,
        religious: false,
        family_oriented: false,
      },
      // Form validation
      validationErrors: {},
      // Option lists
      parishes: [
        "St. Andrew",
        "St. Thomas",
        "Portland",
        "St. Mary",
        "St. Ann",
        "Trelawny",
        "St. James",
        "Hanover",
        "Westmoreland",
        "St. Elizabeth",
        "Manchester",
        "Clarendon",
        "St. Catherine",
        "Kingston",
      ],
      races: ["Black", "East Indian", "Chinese", "White", "Mixed", "Other"],
      cuisines: [
        "Jamaican",
        "Italian",
        "Mexican",
        "Chinese",
        "Indian",
        "Japanese",
        "Thai",
        "Mediterranean",
        "French",
        "American",
      ],
      colors: [
        "Red",
        "Blue",
        "Green",
        "Yellow",
        "Purple",
        "Pink",
        "Orange",
        "Black",
        "White",
        "Brown",
        "Teal",
        "Grey",
      ],
      subjects: [
        "Mathematics",
        "Science",
        "History",
        "English",
        "Geography",
        "Art",
        "Music",
        "Physical Education",
        "Computer Science",
        "Economics",
        "Languages",
      ],
    };
  },
  computed: {
    progressPercentage() {
      return Math.round((this.currentSection / 4) * 100);
    },
    birthYears() {
      const currentYear = new Date().getFullYear();
      const years = [];
      for (let year = currentYear - 18; year >= currentYear - 70; year--) {
        years.push(year);
      }
      return years;
    },
    bioLength() {
      return this.profile.biography ? this.profile.biography.length : 0;
    },
  },
  watch: {
    heightFeet() {
      this.updateHeight();
    },
    heightInches() {
      this.updateHeight();
    },
  },
  created() {
    // Get userId from localStorage
    this.userId = localStorage.getItem("user_id");

    // Check if token exists
    const token = localStorage.getItem("token");
    if (!token) {
      this.$router.push("/login");
    }
  },
  methods: {
    updateHeight() {
      if (this.heightFeet !== "" && this.heightInches !== "") {
        this.profile.height =
          parseInt(this.heightFeet, 10) * 12 + parseInt(this.heightInches, 10);
      }
    },
    handleParishChange() {
      if (this.profile.parish !== "other") {
        this.profile.customParish = "";
      }
    },
    handleRaceChange() {
      if (this.profile.race !== "other") {
        this.profile.customRace = "";
      }
    },
    handleCuisineChange() {
      if (this.profile.fav_cuisine !== "other") {
        this.profile.customCuisine = "";
      }
    },
    handleColorChange() {
      if (this.profile.fav_colour !== "other") {
        this.profile.customColor = "";
      }
    },
    handleSubjectChange() {
      if (this.profile.fav_school_subject !== "other") {
        this.profile.customSubject = "";
      }
    },
    nextSection() {
      if (this.currentSection < 4) {
        this.currentSection++;
        this.scrollToTop();
      }
    },
    prevSection() {
      if (this.currentSection > 1) {
        this.currentSection--;
        this.scrollToTop();
      }
    },
    validateAndNextSection() {
      // Validate current section
      let isValid = true;
      this.validationErrors = {};

      // Validate section 1
      if (this.currentSection === 1) {
        if (!this.profile.description) {
          this.validationErrors.description = "Headline is required";
          isValid = false;
        }

        if (!this.profile.parish) {
          this.validationErrors.parish = "Parish is required";
          isValid = false;
        } else if (
          this.profile.parish === "other" &&
          !this.profile.customParish
        ) {
          this.validationErrors.parish = "Please specify your parish";
          isValid = false;
        }

        if (!this.profile.birth_year) {
          this.validationErrors.birth_year = "Birth year is required";
          isValid = false;
        }

        if (this.heightFeet === "" || this.heightInches === "") {
          this.validationErrors.height = "Height is required";
          isValid = false;
        }

        if (!this.profile.sex) {
          this.validationErrors.sex = "Sex is required";
          isValid = false;
        }

        if (!this.profile.race) {
          this.validationErrors.race = "Race is required";
          isValid = false;
        } else if (this.profile.race === "other" && !this.profile.customRace) {
          this.validationErrors.race = "Please specify your race";
          isValid = false;
        }
      }

      // Validate section 2
      else if (this.currentSection === 2) {
        if (!this.profile.biography) {
          this.validationErrors.biography = "Biography is required";
          isValid = false;
        }
        if (this.bioLength > 500) {
          this.validationErrors.biography =
            "Biography must be less than 500 characters";
          isValid = false;
        }
      }

      // Validate section 3
      else if (this.currentSection === 3) {
        if (!this.profile.fav_cuisine) {
          this.validationErrors.fav_cuisine = "Favorite cuisine is required";
          isValid = false;
        } else if (
          this.profile.fav_cuisine === "other" &&
          !this.profile.customCuisine
        ) {
          this.validationErrors.fav_cuisine =
            "Please specify your favorite cuisine";
          isValid = false;
        }

        if (!this.profile.fav_colour) {
          this.validationErrors.fav_colour = "Favorite color is required";
          isValid = false;
        } else if (
          this.profile.fav_colour === "other" &&
          !this.profile.customColor
        ) {
          this.validationErrors.fav_colour =
            "Please specify your favorite color";
          isValid = false;
        }

        if (!this.profile.fav_school_subject) {
          this.validationErrors.fav_school_subject =
            "Favorite subject is required";
          isValid = false;
        } else if (
          this.profile.fav_school_subject === "other" &&
          !this.profile.customSubject
        ) {
          this.validationErrors.fav_school_subject =
            "Please specify your favorite subject";
          isValid = false;
        }
      }

      if (isValid) {
        this.nextSection();
      } else {
        // Display validation errors
        this.error = "Please fill in all required fields";
        setTimeout(() => {
          this.error = null;
        }, 3000);
      }
    },
    scrollToTop() {
      window.scrollTo({ top: 0, behavior: "smooth" });
    },
    triggerFileInput() {
      this.$refs.fileInput.click();
    },
    handleFileUpload(event) {
      const selectedFile = event.target.files[0];
      if (!selectedFile) return;

      // Check file size (max 5MB)
      if (selectedFile.size > 5 * 1024 * 1024) {
        this.error = "File size exceeds 5MB limit";
        setTimeout(() => {
          this.error = null;
        }, 3000);
        return;
      }

      this.file = selectedFile;

      // Create preview
      const reader = new FileReader();
      reader.onload = (e) => {
        this.preview = e.target.result;
      };
      reader.readAsDataURL(selectedFile);
    },
    async submitProfile() {
      const token = localStorage.getItem("token");
      if (!token) {
        this.$router.push("/login");
        return;
      }

      try {
        this.isSubmitting = true;
        this.error = null;

        if (!this.userId) {
          throw new Error("User ID not found. Please log in again.");
        }

        // Process custom fields if needed
        let finalProfile = { ...this.profile };

        if (finalProfile.parish === "other" && finalProfile.customParish) {
          finalProfile.parish = finalProfile.customParish;
        }

        if (finalProfile.race === "other" && finalProfile.customRace) {
          finalProfile.race = finalProfile.customRace;
        }

        if (
          finalProfile.fav_cuisine === "other" &&
          finalProfile.customCuisine
        ) {
          finalProfile.fav_cuisine = finalProfile.customCuisine;
        }

        if (finalProfile.fav_colour === "other" && finalProfile.customColor) {
          finalProfile.fav_colour = finalProfile.customColor;
        }

        if (
          finalProfile.fav_school_subject === "other" &&
          finalProfile.customSubject
        ) {
          finalProfile.fav_school_subject = finalProfile.customSubject;
        }

        // Remove custom fields that aren't needed in the API
        delete finalProfile.customParish;
        delete finalProfile.customRace;
        delete finalProfile.customCuisine;
        delete finalProfile.customColor;
        delete finalProfile.customSubject;

        // First create the profile
        const profileResponse = await apiClient.post("/api/profiles", {
          ...finalProfile,
          user_id_fk: parseInt(this.userId, 10),
        });

        console.log("Full response from /api/profiles:", profileResponse.data);

        const profileData = profileResponse?.data?.profile;
        if (!profileData || !profileData.id) {
          throw new Error("Profile creation failed. No profile ID returned.");
        }
        const profileId = profileData.id;

        // Redirect to the profile page
        this.$router.push(`/profiles/${profileId}`);
      } catch (err) {
        console.error("Profile creation error:", err);
        this.error =
          err.response?.data?.message ||
          err.message ||
          "Failed to create profile. Please try again.";
      } finally {
        this.isSubmitting = false;
      }
    },
  },
};
</script>

<style scoped>
/* Import Google Fonts - Poppins */
@import url("https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap");
/* Import Bootstrap Icons */
@import url("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css");

/* Define color variables */
:root {
  --teal: #04acb0;
  --orange: #fb9623;
  --yellow: #ffbd0f;
  --coral: #ff7455;
  --background: #f9fafb;
}

.new-profile-page {
  font-family: "Poppins", sans-serif;
  background-color: var(--background);
  min-height: 100vh;
  padding-bottom: 60px;
}

.container {
  max-width: 900px;
  background-color: var(--background);
}

/* Back Button */
.back-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--teal);
  padding: 10px 20px;
  border-radius: 50px;
  background: white;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  text-decoration: none;
  transition: all 0.3s ease;
  margin-bottom: 20px;
  border: 2px solid transparent;
}

.back-btn:hover {
  background: linear-gradient(45deg, var(--teal), var(--coral));
  color: white;
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(4, 172, 176, 0.25);
}

.back-btn i {
  font-size: 1.1rem;
  transition: transform 0.3s ease;
}

.back-btn:hover i {
  transform: translateX(-4px);
}

/* Form Container */
.form-container {
  background-color: white;
  border-radius: 20px;
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1);
  padding: 30px;
  margin-bottom: 40px;
  position: relative;
}

.form-header {
  text-align: center;
  margin-bottom: 30px;
}

.form-title {
  font-size: 2.2rem;
  font-weight: 700;
  background: linear-gradient(45deg, var(--teal), var(--coral));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 10px;
}

.form-subtitle {
  color: #6c757d;
  font-size: 1.1rem;
}

/* Progress Bar */
.progress-container {
  margin-bottom: 30px;
}

.progress {
  height: 10px;
  border-radius: 10px;
  background-color: #e9ecef;
  margin-bottom: 8px;
}

.progress-bar {
  background: linear-gradient(45deg, var(--teal), var(--coral));
  border-radius: 10px;
  transition: width 0.6s ease;
  font-size: 0;
}

.progress-text {
  text-align: right;
  font-size: 0.9rem;
  color: #6c757d;
}

/* Form Sections */
.form-section {
  margin-bottom: 20px;
}

.section-title {
  color: var(--teal);
  font-weight: 700;
  margin-bottom: 25px;
  display: flex;
  align-items: center;
  position: relative;
  padding-bottom: 10px;
  border-bottom: 2px solid #f0f0f0;
}

.section-title::after {
  content: "";
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 80px;
  height: 3px;
  background: linear-gradient(45deg, var(--teal), var(--coral));
  border-radius: 3px;
}

.form-label {
  font-weight: 600;
  color: #495057;
  margin-bottom: 8px;
}

.form-control,
.form-select {
  border-radius: 10px;
  padding: 12px 15px;
  border: 2px solid #e9ecef;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.form-control:focus,
.form-select:focus {
  box-shadow: 0 0 0 4px rgba(4, 172, 176, 0.15);
  border-color: var(--teal);
}

.input-group-text {
  border-radius: 10px 0 0 10px;
  border: 2px solid #e9ecef;
  border-right: none;
  background-color: #f8f9fa;
  color: var(--teal);
}

.input-group .form-control,
.input-group .form-select {
  border-radius: 0 10px 10px 0;
}

.form-text {
  font-size: 0.85rem;
  color: #6c757d;
  margin-top: 5px;
}

/* Biography Section */
.biography-container {
  display: flex;
  gap: 15px;
  margin-bottom: 5px;
}

.biography-icon {
  width: 45px;
  height: 45px;
  border-radius: 50%;
  background: linear-gradient(45deg, var(--teal), var(--coral));
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  box-shadow: 0 5px 10px rgba(4, 172, 176, 0.2);
}

.biography-textarea {
  border-radius: 15px;
  min-height: 150px;
  resize: vertical;
  padding: 15px;
  transition: all 0.3s ease;
}

.biography-counter {
  text-align: right;
  font-size: 0.85rem;
  color: #6c757d;
}

/* Preferences Section */
.preference-card {
  display: flex;
  gap: 15px;
  align-items: center;
  margin-bottom: 15px;
}

.preference-icon {
  width: 45px;
  height: 45px;
  border-radius: 50%;
  background: linear-gradient(45deg, var(--teal), var(--coral));
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  box-shadow: 0 5px 10px rgba(4, 172, 176, 0.2);
  flex-shrink: 0;
}

.preference-card .form-select {
  flex-grow: 1;
}

/* Buttons */
.btn {
  padding: 12px 25px;
  border-radius: 50px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s ease;
}

.btn:hover {
  transform: translateY(-3px);
}

.btn-primary {
  background: linear-gradient(45deg, var(--teal), var(--coral));
  color: white;
  border: none;
  box-shadow: 0 5px 15px rgba(4, 172, 176, 0.3);
}

.btn-success {
  background: linear-gradient(45deg, #28a745, #20c997);
  color: white;
  border: none;
  box-shadow: 0 5px 15px rgba(40, 167, 69, 0.3);
}

.btn-outline {
  background: white;
  color: var(--teal);
  border: 2px solid #e9ecef;
}

.btn-outline:hover {
  border-color: var(--teal);
  background-color: rgba(4, 172, 176, 0.05);
}

/* Mobile adjustments */
@media (max-width: 767px) {
  .form-container {
    padding: 20px 15px;
  }

  .form-navigation {
    flex-direction: column;
    gap: 15px;
  }

  .btn {
    width: 100%;
    justify-content: center;
  }

  .btn-next {
    order: -1;
  }
}

/* Animation overrides */
.animate__animated {
  animation-duration: 0.5s;
}

/* Scrollbar Styling */
::-webkit-scrollbar {
  width: 8px;
}
::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 10px;
}
::-webkit-scrollbar-thumb {
  background: var(--teal);
  border-radius: 10px;
}
::-webkit-scrollbar-thumb:hover {
  background: #038a8d;
}

/* Validation States */
.form-control.is-invalid,
.form-select.is-invalid {
  border-color: #dc3545;
}

.invalid-feedback {
  color: #dc3545;
  font-size: 0.85rem;
  margin-top: 5px;
}
</style>
