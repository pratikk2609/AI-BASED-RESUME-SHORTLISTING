<template>
    <div>
      <h2>Upload Your Resume</h2>
      <form @submit.prevent="submitResume">
        <div class="form-group">
          <label for="resume">Choose Resume File:</label>
          <input type="file" id="resume" @change="handleFileUpload" />
        </div>
        <button type="submit">Upload</button>
      </form>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    data() {
      return {
        resumeFile: null,
      };
    },
    methods: {
      handleFileUpload(event) {
        this.resumeFile = event.target.files[0];
      },
      async submitResume() {
        if (!this.resumeFile) {
          alert("Please select a file.");
          console.log("No file selected.");
          return;
        }
  
        let formData = new FormData();
        formData.append("file", this.resumeFile);
  
        try {
          const response = await axios.post(
            "http://127.0.0.1:8000/generate-response", // Correct endpoint here
            formData,
            {
              headers: {
                "Content-Type": "multipart/form-data",
                body: JSON.stringify(requestData)
              },
            }
          );
  
          console.log("Server Response:", response.data);
          alert("Resume uploaded successfully!");
        } catch (error) {
          console.error("Error uploading resume:", error);
          alert("Failed to upload resume.");
        } finally {
          console.log("submitResume method executed.");
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .form-group {
    margin-bottom: 15px;
  }
  button {
    padding: 10px 20px;
    background-color: #3f51b5;
    color: white;
    border: none;
    border-radius: 5px;
  }
  button:hover {
    background-color: #303f9f;
  }
  </style>