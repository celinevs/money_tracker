<template>
    <div id="app">
      <h1>Login</h1>
      <form @submit.prevent="login">
        <input type="text" v-model="username" placeholder="Username" required>
        <input type="password" v-model="password" placeholder="Password" required>
        <button type="submit">Login</button>
      </form>
      <p v-if="message">{{ message }}</p>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        username: '',
        password: '',
        message: ''
      };
    },
    methods: {
      async login() {
        try {
          const response = await fetch('http://localhost:5000/login', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username: this.username, password: this.password })
          });
          if (response.ok) {
            // Redirect to workspace if login is successful
            window.location.href = '/workspace';
          } else {
            const result = await response.json();
            this.message = result.message;
          }
        } catch (error) {
          this.message = 'An error occurred. Please try again later.';
        }
      }
    }
  };
  </script>
  
  <style scoped>
  </style>
  