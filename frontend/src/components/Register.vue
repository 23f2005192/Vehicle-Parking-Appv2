<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card shadow">
          <div class="card-body">
            <h1 class="text-center mb-4">Register</h1>
            <form @submit.prevent="handleRegister">
              <div class="mb-3">
                <input v-model="name" placeholder="Full Name" required class="form-control" />
              </div>
              <div class="mb-3">
                <input v-model="username" placeholder="Username" required class="form-control" />
              </div>
              <div class="mb-3">
                <input v-model="password" type="password" placeholder="Password" required class="form-control" />
              </div>
              <div class="mb-3">
                <input v-model="type" placeholder="User Type" required class="form-control" />
              </div>
              <div class="mb-3">
                <input v-model="address" placeholder="Address" class="form-control" />
              </div>
              <div class="mb-3">
                <input v-model="phonenumber" placeholder="Phone Number" required class="form-control" />
              </div>
              <button type="submit" class="btn btn-primary w-100">Register</button>
            </form>

            <div v-if="error" class="alert alert-danger mt-3">{{ error }}</div>
            <div v-if="success" class="alert alert-success mt-3">{{ success }}</div>

            <p class="mt-3 text-center">
              Already have an account?
              <router-link to="/login">Login here</router-link>
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Register',
  data() {
    return {
      name: '',
      username: '',
      password: '',
      type: '',
      address: '',
      phonenumber: '',
      error: null,
      success: null
    };
  },
  methods: {
    async handleRegister() {
      this.error = null;
      this.success = null;

      try {
        const response = await axios.post('http://127.0.0.1:5000/register', {
          name: this.name,
          username: this.username,
          password: this.password,
          type: this.type,
          address: this.address,
          phonenumber: this.phonenumber
        });

        if (response.status === 201) {
          this.success = 'Registration successful! Redirecting to login...';
          setTimeout(() => {
            this.$router.push('/login');
          }, 2000);
        }
      } catch (err) {
        if (err.response && err.response.data && err.response.data.error) {
          this.error = err.response.data.error;
        } else {
          this.error = 'Something went wrong. Please try again.';
        }
      }
    }
  }
};
</script>

