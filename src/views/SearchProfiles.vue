<template>
  <div class="container">
    <h1 class="text-center mb-4">Search Profiles</h1>
    
    <div v-if="message" class="alert" :class="messageClass" role="alert">
      {{ message }}
    </div>
    
    <div class="search-form card mb-4">
      <div class="card-body">
        <form @submit.prevent="searchProfiles">
          <div class="row">
            <div class="col-md-6 mb-3">
              <label for="name" class="form-label">Name</label>
              <input type="text" class="form-control" id="name" v-model="searchCriteria.name">
            </div>
            
            <div class="col-md-6 mb-3">
              <label for="birthYear" class="form-label">Birth Year</label>
              <input type="number" class="form-control" id="birthYear" v-model="searchCriteria.birth_year">
            </div>
          </div>
          
          <div class="row">
            <div class="col-md-6 mb-3">
              <label for="sex" class="form-label">Sex</label>
              <select class="form-control" id="sex" v-model="searchCriteria.sex">
                <option value="">Any</option>
                <option value="Male">Male</option>
                <option value="Female">Female</option>
                <option value="Other">Other</option>
              </select>
            </div>
            
            <div class="col-md-6 mb-3">
              <label for="race" class="form-label">Race</label>
              <select class="form-control" id="race" v-model="searchCriteria.race">
                <option value="">Any</option>
                <option value="Black">Black</option>
                <option value="White">White</option>
                <option value="East Indian">East Indian</option>
                <option value="Chinese">Chinese</option>
                <option value="Mixed">Mixed</option>
                <option value="Other">Other</option>
              </select>
            </div>
          </div>
          
          <div class="text-center mt-3">
            <button type="submit" class="btn btn-primary me-2">Search</button>
            <button type="button" class="btn btn-secondary" @click="resetSearch">Reset</button>
          </div>
        </form>
      </div>
    </div>
    
    <div v-if="loading" class="text-center my-5">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
    
    <div v-else-if="searchPerformed">
      <h2 class="mb-3">Search Results</h2>
      
      <div v-if="searchResults.length === 0" class="alert alert-info">
        No profiles found matching your search criteria.
      </div>
      
      <div v-else class="row">
        <div v-for="profile in searchResults" :key="profile.id" class="col-md-6 col-lg-4