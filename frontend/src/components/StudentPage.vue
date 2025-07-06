<template>
    <div>
      <div class="header">
        <div class="header-title">Eduplus Campus | STUDENT</div>
        <div class="header-right">
          <button class="profile-btn" @click="toggleDropdown">S</button>
          <div class="dropdown" v-if="dropdownVisible">
            <router-link to="/profile">Profile</router-link>
            <router-link to="/login" @click="logout">Logout</router-link>
          </div>
        </div>
      </div>
  
      <div class="content">
        <!-- Sidebar -->
        <div class="sidebar">
          <a @click="showUploadForm">Upload Resume</a>
          <!-- <a @click="fetchApplicationStatus">View Application Status</a> -->
        </div>
  
        <!-- Main Content Area -->
        <div class="main-content">
          <!-- Upload Resume Section -->
          <div v-if="isUploadVisible">
            <h2>Upload Your Resume</h2>
            <form @submit.prevent="submitResume">
              <div class="form-group">
                <label for="resume">Choose Resume File:</label>
                <input type="file" id="resume" @change="handleFileUpload" />
              </div>
              <button type="submit">Upload</button>
            </form>
          </div>
  
          <!-- Application Status Section -->
          <div v-if="isStatusVisible">
            <h2>Your Application Status</h2>
            <ul>
              <li v-for="application in applications" :key="application.id">
                <p><strong>Job Title:</strong> {{ application.jobTitle }}</p>
                <p><strong>Current Status:</strong> {{ application.status }}</p>
                <p><strong>Last Update:</strong> {{ application.lastUpdated }}</p>
                <hr />
              </li>
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
  import axios from 'axios'; // Import axios for making API calls
  
  export default {
    data() {
      return {
        dropdownVisible: false,
        isUploadVisible: false,
        isStatusVisible: false,
        resumeFile: null,
        applications: [], // Holds application data
      };
    },
    methods: {
      toggleDropdown() {
        this.dropdownVisible = !this.dropdownVisible;
      },
      logout() {
        this.$router.push("/login");
      },
      showUploadForm() {
        this.isUploadVisible = true;
        this.isStatusVisible = false;
      },
      fetchApplicationStatus() {
        // Simulate an API call to fetch application status from the backend
        this.applications = [
          {
            id: 1,
            jobTitle: 'Software Engineer',
            status: 'Shortlisted',
            lastUpdated: '2024-10-05',
          },
          {
            id: 2,
            jobTitle: 'Cloud Engineer',
            status: 'Interview Scheduled',
            lastUpdated: '2024-10-07',
          },
          {
            id: 3,
            jobTitle: 'Data Analyst',
            status: 'Rejected',
            lastUpdated: '2024-10-08',
          },
        ];
  
        this.isStatusVisible = true;
        this.isUploadVisible = false;
      },
      handleFileUpload(event) {
        this.resumeFile = event.target.files[0];
      },
      async submitResume() {
        if (!this.resumeFile) {
          alert("Please select a file.");
          return;
        }
  
        let formData = new FormData();
        formData.append("file", this.resumeFile); // Append file to FormData
  
        try {
          // Replace this URL with your backend API endpoint for handling resume uploads
          const response = await axios.post("http://127.0.0.1:8001/generate-response", formData, {
            headers: { "Content-Type": "multipart/form-data" },
          });
  
          console.log(response.data); // Log the response from the backend
          alert("Resume uploaded successfully!");
          this.isUploadVisible = false; // Hide the upload form after successful submission
        } catch (error) {
          console.error("Error uploading file:", error.response ? error.response.data : error);
          alert("Error uploading resume!");
        }
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
  