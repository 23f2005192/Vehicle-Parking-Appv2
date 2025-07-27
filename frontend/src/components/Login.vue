<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6 col-lg-4">
        <div class="card shadow">
          <div class="card-body">
            <h3 class="card-title text-center mb-4">Login</h3>
            <form @submit.prevent="handleLogin">
             
              <div class="mb-3">
                <label for="username" class="form-label">Username</label>
                <input
                  id="username"
                  v-model.trim="username"
                  type="text"
                  class="form-control"
                  placeholder="Enter your username"
                  required
                />
              </div>

              <div class="mb-3">
                <label for="password" class="form-label">Password</label>
                <div class="input-group">
                  <input
                    :type="showPassword ? 'text' : 'password'"
                    id="password"
                    v-model="password"
                    class="form-control"
                    placeholder="Enter your password"
                    required
                  />
                  <span class="input-group-text  border-start-0" style="color: #000;">
                    <button
                      type="button"
                      class="btn btn-icon " 
                      @click="togglePassword"
                      tabindex="-1"
                      aria-label="Toggle password visibility"
                    >
                       <i :class="showPassword ? 'bi bi-eye-slash' : 'bi bi-eye'" style="color: #000000;"></i>

                    </button>
                  </span>
                </div>
              </div>

          
              <div v-if="errorMessage" class="alert alert-danger" role="alert">
                {{ errorMessage }}
              </div>

              
              <button type="submit" class="btn btn-primary w-100" :disabled="loading">
                {{ loading ? 'Logging in...' : 'Login' }}
              </button>
            </form>

            <p class="mt-3 text-center">
              Don't have an account?
              <router-link to="/register">Register here</router-link>
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

export default {
  setup() {
    const router = useRouter()
    const username = ref('')
    const password = ref('')
    const loading = ref(false)
    const errorMessage = ref('')
    const showPassword = ref(false)

    const togglePassword = () => {
      showPassword.value = !showPassword.value
    }

    const handleLogin = async () => {
      if (!username.value || !password.value) {
        errorMessage.value = 'Please enter both username and password.'
        return
      }

      loading.value = true
      errorMessage.value = ''

      try {
        const response = await fetch('http://127.0.0.1:5000/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            username: username.value,
            password: password.value
          })
        })

        const data = await response.json()

        if (response.ok) {
          alert('Login successful!')
          router.push(data.redirect)
        } else {
          errorMessage.value = data.error || 'Invalid login credentials.'
        }
      } catch (error) {
        errorMessage.value = 'Network error or server is unreachable.'
      } finally {
        loading.value = false
      }
    }

    return {
      username,
      password,
      loading,
      errorMessage,
      handleLogin,
      showPassword,
      togglePassword
    }
  }
}
</script>



