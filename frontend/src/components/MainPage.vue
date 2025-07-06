<template>
    <div>
      <div class="header">
        <div class="header-title">Eduplus Campus | HR MANAGER</div>
        <div class="header-right">
          <button class="profile-btn" @click="toggleDropdown">H</button>
          <div class="dropdown" v-if="dropdownVisible">
            <router-link to="/profile">Profile</router-link>
            <router-link to="/login" @click="logout">Logout</router-link>
          </div>
        </div>
      </div>
  
      <div class="content">
        <!-- Sidebar -->
        <div class="sidebar">
          <a @click="showAddJobForm">Add Job Description</a>
          <a @click="fetchResumes">Fetch Resumes</a>
        </div>
  
        <!-- Main Content Area -->
        <div class="main-content">
          <div v-if="isJobFormVisible">
            <h2>Add Job Description</h2>
            <form @submit.prevent="submitJobDescription">
              <div class="form-group">
                <label for="job-title">Job Title:</label>
                <input type="text" id="job-title" v-model="jobTitle" required />
              </div>
              <div class="form-group">
                <label for="job-description">Job Description:</label>
                <textarea id="job-description" v-model="jobDescription" required></textarea>
              </div>
              <button type="submit">Add Job</button>
            </form>
          </div>
          
          <div v-if="isResumesVisible">
            <h2>Resumes</h2>
            <ul>
              <li v-for="resume in resumes" :key="resume.id">{{ resume.name }}</li>
            </ul>
          </div>
  
          <div v-else>
            <router-view></router-view>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        dropdownVisible: false,
        isJobFormVisible: false,
        isResumesVisible: false,
        jobTitle: '',
        jobDescription: '',
        resumes: [], // Store fetched resumes
      };
    },
    methods: {
      toggleDropdown() {
        this.dropdownVisible = !this.dropdownVisible;
      },
      logout() {
        this.$router.push("/login");
      },
      showAddJobForm() {
        this.isJobFormVisible = true;
        this.isResumesVisible = false;
      },
      fetchResumes() {
        this.resumes = [
          { id: 1, name: 'Resume 1.pdf' },
          { id: 2, name: 'Resume 2.pdf' },
          { id: 3, name: 'Resume 3.pdf' },
        ];
        this.isResumesVisible = true;
        this.isJobFormVisible = false;
      },
      submitJobDescription() {
        alert(`Job "${this.jobTitle}" added successfully!`);
        this.jobTitle = '';
        this.jobDescription = '';
        this.isJobFormVisible = false;
      },
    },
  };
  </script>
  
  <style scoped>
  .header {
    background-color: #3f51b5;
    color: white;
    padding: 15px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .header-title {
    font-size: 20px;
  }
  .header-right {
    position: relative;
    display: inline-block;
  }
  .dropdown {
    position: absolute;
    background-color: #f9f9f9;
    min-width: 100px;
    box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.2);
    z-index: 1;
    right: 0;
  }
  .dropdown a {
    color: black;
    padding: 12px 16px;
    text-decoration: none;
    display: block;
  }
  .dropdown a:hover {
    background-color: #f1f1f1;
  }
  .profile-btn {
    cursor: pointer;
    background-color: #fff;
    border: none;
    padding: 10px;
    border-radius: 50%;
    font-size: 18px;
  }
  
  .content {
    display: flex;
    height: 100vh;
  }
  .sidebar {
    width: 200px;
    background-color: #f4f4f4;
    padding: 20px;
  }
  .sidebar a {
    display: block;
    padding: 10px;
    text-decoration: none;
    color: #333;
    cursor: pointer;
  }
  .sidebar a:hover {
    background-color: #ddd;
  }
  
  .main-content {
    flex-grow: 1;
    padding: 20px;
    background-color: white;
  }
  
  .form-group {
    margin-bottom: 15px;
  }
  
  button {
    padding: 10px 20px;
    background-color: #3f51b5;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #2c3e99;
  }
  </style>
  