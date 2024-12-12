<template>
  <div id="app" class="login-container">
    <h1 class="login-title">Login</h1>
    <form class="login-form" @submit.prevent="login">
      <div class="form-group">
        <input
          type="text"
          v-model="username"
          placeholder="Username"
          required
          class="form-input"
        />
      </div>
      <div class="form-group">
        <input
          type="password"
          v-model="password"
          placeholder="Password"
          required
          class="form-input"
        />
      </div>
      <button type="submit" class="btn-submit">Login</button>
    </form>
    <p v-if="message" class="error-message">{{ message }}</p>
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
.login-container {
max-width: 420px;
margin: 0 auto;
padding: 25px;
border-radius: 15px;
box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
background-color: #fffbf0;
text-align: center;
color: #333;
position: absolute;
top: 50%;
left: 50%;
transform: translate(-50%, -50%);
}

.login-title {
  font-size: 24px;
  margin-bottom: 20px;
  color: #ff7eb9; /* Match primary accent color */
}

.login-form {
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: 15px;
}

.form-input {
  width: 90%;
  padding: 12px;
  border: 2px solid #ffd97d; /* Match transaction card borders */
  border-radius: 12px; /* Rounded corners consistent with cards */
  font-size: 16px;
  background: #ffffff;
  transition: box-shadow 0.3s ease, border-color 0.3s ease;
}

.form-input:focus {
  outline: none;
  border-color: #ff7eb9; /* Highlight matching primary color */
  box-shadow: 0 0 5px #ff7eb9;
}

.btn-submit {
  padding: 12px;
  font-size: 16px;
  color: #fff;
  background-color: #6cdbeb; /* Match "Apply Filters" button color */
  border: none;
  border-radius: 20px; /* Rounded consistent with workspace */
  cursor: pointer;
  transition: transform 0.2s ease, background-color 0.3s ease;
}

.btn-submit:hover {
  background-color: #38a3a5;
  transform: translateY(-3px);
}

.error-message {
  margin-top: 15px;
  color: #e63946;
  font-weight: bold;
}
</style>

