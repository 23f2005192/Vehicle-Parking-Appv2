<template>
  <div>
  
    <nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm">
      <div class="container-fluid">
        <span class="navbar-brand fw-bold text-primary">
          Hello, <span class="text-muted">{{ username }}</span>
        </span>
        <div class="mx-auto d-flex gap-3">
          <button class="btn btn-outline-primary" @click="goHome">Home</button>
          <button class="btn btn-outline-primary">Summary</button>
        </div>
        <div class="d-flex gap-2">
          <button class="btn btn-outline-success" data-bs-toggle="modal" data-bs-target="#editModal">Edit</button>
          <button class="btn btn-outline-danger" data-bs-toggle="modal" data-bs-target="#logoutModal">Logout</button>
        </div>
      </div>
    </nav>
   <div class="container mt-4">
  <input
    type="text"
    class="form-control"
    placeholder="Search Parking Lots..."
    v-model="searchQuery"
    @input="searchParkingLots"
  />
  <ul v-if="searchResults.length" class="list-group mt-2">
    <li
      v-for="lot in searchResults"
      :key="lot.id"
      class="list-group-item list-group-item-action"
      @click="selectParkingLot(lot)"
      style="cursor: pointer;"
    >
      {{ lot.name }} - {{ lot.address }} (₹{{ lot.price }})
    </li>
  </ul>
  <p v-else-if="searchQuery && !searchResults.length" class="mt-2" style="color: white;">
  No results found.
</p>

</div>

   
    


    <div class="container mt-5 text-center">
      <h2 class="text-muted fw-light">Welcome to User Dashboard</h2>
    </div>


    <div class="modal fade" id="editModal" tabindex="-1" aria-labelledby="editModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content text-dark">
          <div class="modal-header text-muted">
            <h5 class="modal-title" id="editModalLabel">Edit User</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <form @submit.prevent="updateUser">
            <div class="modal-body">
              <div class="mb-3">
                <label for="name" class="form-label">Name</label>
                <input v-model="userData.name" type="text" class="form-control" id="name" required />
              </div>
              <div class="mb-3">
                <label for="phonenumber" class="form-label">Phone Number</label>
                <input v-model="userData.phonenumber" type="text" class="form-control" id="phonenumber" />
              </div>
              <div class="mb-3">
                <label for="address" class="form-label">Address</label>
                <input v-model="userData.address" type="text" class="form-control" id="address" />
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
              <button type="submit" class="btn btn-primary">Save Changes</button>
            </div>
          </form>
        </div>
      </div>
    </div>

    
    <div class="modal fade" id="logoutModal" tabindex="-1" aria-labelledby="logoutModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header text-muted">
            <h5 class="modal-title" id="logoutModalLabel">Confirm Logout</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body text-muted">Are you sure you want to logout?</div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">No</button>
            <button type="button" class="btn btn-danger" @click="logout">Yes, Logout</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';

const route = useRoute();
const router = useRouter();

const username = ref('User');
const userData = ref({
  name: '',
  phonenumber: '',
  address: ''
});
const errorMessage = ref(null);

const searchQuery = ref('');
const searchResults = ref([]);


onMounted(async () => {
  const userId = route.params.id;
  try {
    const { data } = await axios.get(`http://127.0.0.1:5000/get_user/${userId}`);
    userData.value = data;
    username.value = data.name || 'User';
  } catch (error) {
    console.error('Failed to fetch user:', error);
    errorMessage.value = 'Failed to load user data. Please check backend.';
  }
});

const updateUser = async () => {
  const userId = route.params.id;
  try {
    await axios.put(`http://127.0.0.1:5000/edit_user/${userId}`, {
      name: userData.value.name,
      phonenumber: userData.value.phonenumber,
      address: userData.value.address
    });
    alert('User updated successfully!');
    username.value = userData.value.name;

    const modalEl = document.getElementById('editModal');
    const modal = bootstrap.Modal.getInstance(modalEl);
    modal?.hide();
  } catch (error) {
    console.error('Failed to update user:', error);
    alert('Failed to update user. Please try again.');
  }
};

const goHome = () => {
  router.push(`/user/${route.params.id}`);
};

const logout = () => {
  router.push('/');
};

let searchTimeout = null;
const searchParkingLots = () => {
  if (searchTimeout) clearTimeout(searchTimeout);

  searchTimeout = setTimeout(async () => {
    if (!searchQuery.value.trim()) {
      searchResults.value = [];
      return;
    }
    try {
      const { data } = await axios.get('http://127.0.0.1:5000/parkinglot/search', {
        params: { q: searchQuery.value.trim() }
      });
      searchResults.value = data;
    } catch (error) {
      console.error('Search failed:', error);
      searchResults.value = [];
    }
  }, 300); 
};

const selectParkingLot = (lot) => {
  alert(`You selected: ${lot.name} at ${lot.address}`);

  searchQuery.value = '';
  searchResults.value = [];
};




</script>
