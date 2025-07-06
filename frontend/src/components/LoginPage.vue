<template>
    <div class="login-background">
      <div class="login-container">
        <h2>Login</h2>
        <form @submit.prevent="handleLogin">
          <div class="form-group">
            <label for="username">Username:</label>
            <input type="text" v-model="username" required />
          </div>
          <div class="form-group">
            <label for="password">Password:</label>
            <input type="password" v-model="password" required />
          </div>
          <button type="submit">Login</button>
        </form>
        <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        username: '',
        password: '',
        errorMessage: '',
      };
    },
    methods: {
      handleLogin() {
        //login for demo
        if (this.username === 's' && this.password === 's') {
          this.$router.push('/student');
        } else if (this.username === 'hr' && this.password === 'hr') {
          this.$router.push('/hr');
        } else {
          this.errorMessage = 'Invalid credentials. Please try again.';
        }
      },
    },
  };
  </script>
  
  <style scoped>
  
  .login-background {
    background: linear-gradient(135deg, #667eea, #764ba2); 
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    font-family: 'Arial', sans-serif;
  }
  
  .login-container {
    background-color: rgba(255, 255, 255, 0.9); 
    max-width: 400px;
    margin: 0 auto;
    padding: 40px;
    border-radius: 15px;
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
    text-align: center;
  }
  
  h2 {
    color: #333;
    font-size: 24px;
    margin-bottom: 25px;
  }
  
  .form-group {
    margin-bottom: 20px;
  }
  
  label {
    display: block;
    margin-bottom: 8px;
    font-weight: bold;
    color: #444;
  }
  
  input[type="text"],
  input[type="password"] {
    width: 100%;
    padding: 12px;
    border: 1px solid #ccc;
    border-radius: 10px;
    font-size: 16px;
    box-sizing: border-box;
    transition: border-color 0.3s;
  }
  
  input[type="text"]:focus,
  input[type="password"]:focus {
    border-color: #667eea;
  }
  
  button {
    width: 100%;
    padding: 12px;
    background-color: #667eea;
    color: white;
    border: none;
    border-radius: 10px;
    font-size: 16px;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  button:hover {
    background-color: #764ba2; 
  }
  
  .error {
    color: red;
    margin-top: 15px;
    font-size: 14px;
  }
  </style>
  