<template>
  <div class="container">
    <h1 class="text-center mt-4 mb-4">Create New Profile</h1>

    <div v-if="message" class="alert" :class="messageClass" role="alert">
      {{ message }}
    </div>

    <form @submit.prevent="submitProfile" class="col-md-8 mx-auto">
      <div class="form-group mb-3">
        <label for="description">Description</label>
        <input
          type="text"
          class="form-control"
          id="description"
          v-model="profile.description"
          required
        />
      </div>

      <div class="form-group mb-3">
        <label for="parish">Parish</label>
        <select
          class="form-control"
          id="parish"
          v-model="profile.parish"
          required
        >
          <option value="">Select a parish</option>
          <option value="Kingston">Kingston</option>
          <option value="St. Andrew">St. Andrew</option>
          <option value="St. Catherine">St. Catherine</option>
          <option value="Clarendon">Clarendon</option>
          <option value="Manchester">Manchester</option>
          <option value="St. Elizabeth">St. Elizabeth</option>
          <option value="Westmoreland">Westmoreland</option>
          <option value="Hanover">Hanover</option>
          <option value="St. James">St. James</option>
          <option value="Trelawny">Trelawny</option>
          <option value="St. Ann">St. Ann</option>
          <option value="St. Mary">St. Mary</option>
          <option value="Portland">Portland</option>
          <option value="St. Thomas">St. Thomas</option>
        </select>
      </div>

      <div class="form-group mb-3">
        <label for="biography">Biography</label>
        <textarea
          class="form-control"
          id="biography"
          rows="4"
          v-model="profile.biography"
          required
        ></textarea>
      </div>

      <div class="form-group mb-3">
        <label for="sex">Sex</label>
        <select class="form-control" id="sex" v-model="profile.sex" required>
          <option value="">Select an option</option>
          <option value="Male">Male</option>
          <option value="Female">Female</option>
          <option value="Other">Other</option>
        </select>
      </div>

      <div class="form-group mb-3">
        <label for="race">Race</label>
        <select class="form-control" id="race" v-model="profile.race" required>
          <option value="">Select an option</option>
          <option value="Black">Black</option>
          <option value="White">White</option>
          <option value="East Indian">East Indian</option>
          <option value="Chinese">Chinese</option>
          <option value="Mixed">Mixed</option>
          <option value="Other">Other</option>
        </select>
      </div>

      <div class="form-group mb-3">
        <label for="birthYear">Birth Year</label>
        <input
          type="number"
          class="form-control"
          id="birthYear"
          v-model="profile.birth_year"
          min="1900"
          :max="currentYear - 18"
          required
        />
      </div>

      <div class="form-group mb-3">
        <label for="height">Height (in inches)</label>
        <input
          type="number"
          step="0.1"
          class="form-control"
          id="height"
          v-model="profile.height"
          required
        />
      </div>

      <div class="form-group mb-3">
        <label for="favCuisine">Favorite Cuisine</label>
        <input
          type="text"
          class="form-control"
          id="favCuisine"
          v-model="profile.fav_cuisine"
          required
        />
      </div>

      <div class="form-group mb-3">
        <label for="favColour">Favorite Colour</label>
        <input
          type="text"
          class="form-control"
          id="favColour"
          v-model="profile.fav_colour"
          required
        />
      </div>

      <div class="form-group mb-3">
        <label for="favSchoolSubject">Favorite School Subject</label>
        <input
          type="text"
          class="form-control"
          id="favSchoolSubject"
          v-model="profile.fav_school_subject"
          required
        />
      </div>

      <div class="form-group mb-3">
        <label>Are you political?</label>
        <div class="form-check">
          <input
            class="form-check-input"
            type="radio"
            id="politicalYes"
            value="true"
            v-model="profile.political"
          />
          <label class="form-check-label" for="politicalYes">Yes</label>
        </div>
        <div class="form-check">
          <input
            class="form-check-input"
            type="radio"
            id="politicalNo"
            value="false"
            v-model="profile.political"
          />
          <label class="form-check-label" for="politicalNo">No</label>
        </div>
      </div>

      <div class="form-group mb-3">
        <label>Are you religious?</label>
        <div class="form-check">
          <input
            class="form-check-input"
            type="radio"
            id="religiousYes"
            value="true"
            v-model="profile.religious"
          />
          <label class="form-check-label" for="religiousYes">Yes</label>
        </div>
        <div class="form-check">
          <input
            class="form-check-input"
            type="radio"
            id="religiousNo"
            value="false"
            v-model="profile.religious"
          />
          <label class="form-check-label" for="religiousNo">No</label>
        </div>
      </div>

      <div class="form-group mb-3">
        <label>Are you family oriented?</label>
        <div class="form-check">
          <input
            class="form-check-input"
            type="radio"
            id="familyYes"
            value="true"
            v-model="profile.family_oriented"
          />
          <label class="form-check-label" for="familyYes">Yes</label>
        </div>
        <div class="form-check">
          <input
            class="form-check-input"
            type="radio"
            id="familyNo"
            value="false"
            v-model="profile.family_oriented"
          />
          <label class="form-check-label" for="familyNo">No</label>
        </div>
      </div>

      <div class="text-center mt-4">
        <button type="submit" class="btn btn-primary">Create Profile</button>
      </div>
    </form>
  </div>
</template>

<script>
export default {
  name: "NewProfile",
  data() {
    return {
      profile: {
        description: "",
        parish: "",
        biography: "",
        sex: "",
        race: "",
        birth_year: null,
        height: null,
        fav_cuisine: "",
        fav_colour: "",
        fav_school_subject: "",
        political: null,
        religious: null,
        family_oriented: null,
      },
      message: "",
      messageClass: "",
      currentYear: new Date().getFullYear(),
    };
  },
  methods: {
    submitProfile() {
      // Convert boolean strings to actual booleans
      this.profile.political = this.profile.political === "true";
      this.profile.religious = this.profile.religious === "true";
      this.profile.family_oriented = this.profile.family_oriented === "true";

      // Get the auth token from local storage
      const token = localStorage.getItem("token");

      if (!token) {
        this.$router.push("/login");
        return;
      }

      fetch("/api/profiles", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(this.profile),
      })
        .then((response) => {
          if (response.ok) {
            return response.json();
          }
          throw new Error("Failed to create profile");
        })
        .then((data) => {
          this.message = "Profile created successfully!";
          this.messageClass = "alert-success";

          // Reset form after successful submission
          this.profile = {
            description: "",
            parish: "",
            biography: "",
            sex: "",
            race: "",
            birth_year: null,
            height: null,
            fav_cuisine: "",
            fav_colour: "",
            fav_school_subject: "",
            political: null,
            religious: null,
            family_oriented: null,
          };

          // Redirect to user profile page after short delay
          setTimeout(() => {
            this.$router.push(`/users/${data.user_id}`);
          }, 2000);
        })
        .catch((error) => {
          this.message = error.message;
          this.messageClass = "alert-danger";
        });
    },
  },
};
</script>

<style scoped>
.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}
</style>
