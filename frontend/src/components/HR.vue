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
        <div class="sidebar">
          <a @click="showAddJobForm">Add Job Description</a>
          <a @click="toggleShortlistedSection">Shortlist Candidates</a>
        </div>
  
        <div class="main-content">
          <!-- Add Job Description Form -->
          <div v-if="showAddJob">
            <h2>Add Job Description</h2>
            <form @submit.prevent="submitJobDescription">
              <div class="form-group">
                <label for="jobTitle">Job Title:</label>
                <input
                  type="text"
                  id="jobTitle"
                  v-model="jobTitle"
                  placeholder="Enter job title"
                  required
                />
              </div>
              <div class="form-group">
                <label for="jobDescription">Job Description:</label>
                <textarea
                  id="jobDescription"
                  v-model="jobDescription"
                  placeholder="Enter job description"
                  required
                ></textarea>
              </div>
              <button type="submit">Submit</button>
            </form>
          </div>
  
          <!-- Shortlisted Candidates Section -->
          <div v-if="showShortlistedSection" class="shortlisted-candidates-section">
            <h2>Shortlisted Candidates</h2>
  
            <!-- Filter Selection -->
            <div class="filters">
              <h3>Filters:</h3>
              <label>
                <input
                  type="checkbox"
                  value="tenGrade"
                  v-model="selectedFilters"
                />
                10th Grade Percentage
              </label>
              <label>
                <input
                  type="checkbox"
                  value="twelveGrade"
                  v-model="selectedFilters"
                />
                12th Grade Percentage
              </label>
              <label>
                <input
                  type="checkbox"
                  value="cgpa"
                  v-model="selectedFilters"
                />
                CGPA
              </label>
  
              <!-- Input Fields for Selected Filters -->
              <div v-if="selectedFilters.includes('tenGrade')">
                <label for="tenGradeInput">10th Grade Percentage:</label>
                <input
                  type="text"
                  id="tenGradeInput"
                  v-model="filterDetails.tenGrade"
                  placeholder="Enter range (e.g., 85-90)"
                />
              </div>
  
              <div v-if="selectedFilters.includes('twelveGrade')">
                <label for="twelveGradeInput">12th Grade Percentage:</label>
                <input
                  type="text"
                  id="twelveGradeInput"
                  v-model="filterDetails.twelveGrade"
                  placeholder="Enter range (e.g., 80-85)"
                />
              </div>
  
              <div v-if="selectedFilters.includes('cgpa')">
                <label for="cgpaInput">CGPA:</label>
                <input
                  type="text"
                  id="cgpaInput"
                  v-model="filterDetails.cgpa"
                  placeholder="Enter CGPA (e.g., 8.5-9.0)"
                />
              </div>
  
              <button @click="fetchFilteredResumes">Fetch Resumes</button>
            </div>
  
            <!-- Candidates Table -->
            <table v-if="showResumes">
              <thead>
          <tr>
            <th>Rank</th>
            <th>Name</th>
            <th>Similarity Score</th>
            <th>Resume Link</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>1</td>
            <td>Aditi Himpalnerkar</td>
            <td>0.17578607839334617</td>
            <td><a href="https://drive.google.com/file/d/1EHoKjrqGBKj_ZMThIol0bgEpo4hQqPcx/view?usp=drive_link" target="_blank">View Resume</a></td>
          </tr>
          <tr>
            <td>2</td>
            <td>Siddhi Jadhavrao</td>
            <td>0.11904430410598647</td>
            <td><a href="https://drive.google.com/file/d/1-2tOeyjef5r-jshbs6IViCRmaLao7F4W/view?usp=drive_link" target="_blank">View Resume</a></td>
          </tr>
          <tr>
            <td>3</td>
            <td>Nidhi Agrawal</td>
            <td>0.09867961797986956</td>
            <td><a href="https://drive.google.com/file/d/1Ih3cu7flnc8gI3uQUbCri-m36X3Tuz0_/view?usp=drive_link" target="_blank">View Resume</a></td>
          </tr>
          <tr>
            <td>4</td>
            <td>Sanket Patil</td>
            <td>0.04356856122871383</td>
            <td><a href="https://drive.google.com/file/d/1Q9m36Q9LsePz46qKXqd4hTrUqcn1CMdF/view?usp=drive_link" target="_blank">View Resume</a></td>
          </tr>
        </tbody>
  
                <tr v-for="(candidate, index) in filteredCandidates" :key="index">
                  <td>{{ index + 1 }}</td>
                  <td>{{ candidate.name }}</td>
                  <td>{{ candidate.similarity_score }}</td>
                  <td><a :href="candidate.resume_link" target="_blank">View Resume</a></td>
                </tr>
             
            </table>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    data() {
      return {
        jobTitle: "", // Job Title
        jobDescription: "", // Job Description
        skills: [], // Extracted Skills
        candidates: [], // Shortlisted Candidates
        filteredCandidates: [], // Candidates after applying filters
        dropdownVisible: false,
  
        // Flags for section visibility
        showAddJob: true,
        showShortlistedSection: false,
        showResumes: false, // to control when the resumes table should be displayed
  
        // Filters
        selectedFilters: [],
        filterDetails: {
          tenGrade: "",
          twelveGrade: "",
          cgpa: "",
        },
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
        this.showAddJob = true;
        this.showShortlistedSection = false;
      },
      toggleShortlistedSection() {
        this.showAddJob = false;
        this.showShortlistedSection = true;
      },
      async submitJobDescription() {
        const jobData = {
          job_title: this.jobTitle,
          job_description: this.jobDescription,
        };
  
        try {
          const response = await axios.post(
            "http://127.0.0.1:8001/hr-skills",
            jobData,
            { headers: { "Content-Type": "application/json" } }
          );
  
          this.skills = response.data.skills;
          alert("Job description and skills extracted successfully!");
          this.jobTitle = "";
          this.jobDescription = "";
        } catch (error) {
          console.error("Error submitting job description:", error);
          alert("Failed to submit job description. Please try again.");
        }
      },
      async fetchFilteredResumes() {
        this.showResumes = true;
        // Add your logic to fetch filtered resumes here
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
  
  input,
  textarea {
    width: 100%;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
    margin-bottom: 10px;
    box-sizing: border-box;
  }
  
  textarea {
    resize: vertical;
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
    background-color: #303f9f;
  }
  
  .shortlisted-candidates-section table {
    width: 100%;
    border-collapse: collapse;
  }
  
  .shortlisted-candidates-section th,
  .shortlisted-candidates-section td {
    padding: 10px;
    text-align: left;
    border: 1px solid #ddd;
  }
  
  .shortlisted-candidates-section th {
    background-color: #f2f2f2;
  }
  </style>