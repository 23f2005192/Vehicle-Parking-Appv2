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
