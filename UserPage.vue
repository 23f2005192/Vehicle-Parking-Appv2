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

  




    <div class="container mt-5 text-center">
      <h2 class="text-light">Welcome to User Dashboard</h2>
    </div>
  <table v-if="reservations.length" class="table table-striped table-hover shadow-sm">
  <thead class="table-light">
    <tr>
      <th>ID</th>
      <th>Vehicle No</th>
      <th>Start Date</th>
      
      <th>Location</th>
      <th>status</th>
      <th>Action</th>
    </tr>
  </thead>
  <tbody>
    <tr v-for="r in reservations" :key="r.id">
      <td>{{ r.id }}</td>
      <td>{{ r.vehicle_no }}</td>
      <td>{{ r.start_date }}</td>
      
      <td>{{ r.parking_lot_name }}</td>
      <td>{{ r.status }}</td>
      <td>
        
  <button
  v-if="r.status === 'T'"
  class="btn btn-sm btn-outline-danger"
  data-bs-toggle="modal"
  data-bs-target="#releaseModal"
  @click="prepareRelease(r)"
>
  Occupied
</button>
<button
  v-else
  class="btn btn-sm btn-outline-success"
  
>
  Release
</button>

     
</td>
    </tr>
  </tbody>
</table>

<div class="container d-flex justify-content-center align-items-center" style="min-height: 50vh;">
  <div class="w-75">

    <div class="input-group mb-4">
      <input
        type="text"
        class="form-control"
        placeholder="Search by name or pincode..."
        v-model="searchQuery"
      />
      <button class="btn btn-primary" @click="performSearch">Search</button>
    </div>

    
    <div v-if="searchPerformed">
      <div v-if="searchResults.length">
        <table class="table table-bordered table-hover shadow-sm">
          <thead class="table-light">
            <tr>
              <th>Name</th>
              <th>Address</th>
              <th>Price (₹)</th>
              <th>Available Spots</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="lot in searchResults" :key="lot.id">
              <td>{{ lot.name }}</td>
              <td>{{ lot.address }}</td>
              <td>{{ lot.price }}</td>
              <td>{{ lot.spots }}</td>
               <td>
              <button class="btn btn-outline-success btn-sm" @click="openBookingModal(lot)">
                Book
              </button>
              </td>

            </tr>
          </tbody>
        </table>
      </div>
      <p v-else class="text-light mt-3">No results found.</p>
    </div>
  </div>
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
  <div class="modal fade" id="bookModal" tabindex="-1" aria-labelledby="bookModalLabel" aria-hidden="true">
  <div class="modal-dialog modal-dialog-centered">
    <div class="modal-content text-dark">
      <div class="modal-header">
        <h5 class="modal-title" id="bookModalLabel">Book Parking Spot</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <form @submit.prevent="confirmBooking">
        <div class="modal-body">
          <p><strong>Lot:</strong> {{ selectedLot?.name }}</p>
          <div class="mb-3">
            <label for="vehicle" class="form-label">Vehicle Number</label>
            <input v-model="vehicleNo" type="text" class="form-control" id="vehicle" required />
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
          <button type="submit" class="btn btn-success">Confirm Booking</button>
        </div>
      </form>
    </div>
  </div>
</div>
<div class="modal fade" id="releaseModal" tabindex="-1" aria-labelledby="releaseModalLabel" aria-hidden="true">
  <div class="modal-dialog modal-dialog-centered">
    <div class="modal-content text-dark">
      <div class="modal-header">
        <h5 class="modal-title" id="releaseModalLabel">Release Spot</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body" v-if="modalData.id !== null">
        <p><strong>Vehicle No:</strong> {{ modalData.vehicle_no }}</p>
        <p><strong>Start Date:</strong> {{ modalData.start_date }}</p>
        <p><strong>Start Time:</strong> {{ modalData.start_time }}</p>
        <p><strong>Lot:</strong> {{ modalData.parking_lot_name }}</p>
        <p><strong>Spot ID:</strong> {{ modalData.parking_spot_id }}</p>
        <p><strong>Cost:</strong> ₹{{ modalData.cost }}</p>
        <p class="text-danger">Note: These fields are auto-filled and cannot be edited.</p>
       </div>

      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
        <button type="button" class="btn btn-success" @click="releaseReservation">Confirm Release</button>
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
const searchQuery = ref('');
const searchResults = ref([]);

onMounted(async () => {
  const userId = route.params.id;
  try {
    const { data } = await axios.get(`http://127.0.0.1:5000/get_user/${userId}`);


    userData.value = {
      name: data.name || '',
      phonenumber: data.phonenumber || '',
      address: data.address || ''
    };

    username.value = userData.value.name || 'User';
    userphonenumber.value = userData.value.phonenumber || 'User';
  } catch (error) {
    console.error('Failed to fetch user:', error);
    
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

    username.value = userData.value.name;
    
    alert('User updated successfully!');

   
    const modalEl = document.getElementById('editModal');
    const modal = bootstrap.Modal.getInstance(modalEl);
    modal?.hide();
  } catch (error) {
    console.error('Failed to update user:', error);
    alert('Update failed. Please try again.');
  }
};

const goHome = () => {
  router.push(`/user/${route.params.id}`);
};

const logout = () => {
  router.push('/l');
};

let searchTimeout = null;

const searchPerformed = ref(false); 
const performSearch = async () => {
  searchPerformed.value = false;
  searchResults.value = [];

  const query = searchQuery.value.trim();
  if (!query) return;

  try {
    const { data } = await axios.get('http://127.0.0.1:5000/parkinglot/search', {
      params: { q: query }
    });

    searchResults.value = data;
    searchPerformed.value = true;
  } catch (error) {
    console.error('Search error:', error);
    searchResults.value = [];
    searchPerformed.value = true;
  }
};
const selectedLot = ref(null);
const vehicleNo = ref('');

const openBookingModal = (lot) => {
  selectedLot.value = lot;
  vehicleNo.value = '';
  const modal = new bootstrap.Modal(document.getElementById('bookModal'));
  modal.show();
};

const confirmBooking = async () => {
  const userId = route.params.id;
  try {
    const { data } = await axios.post('http://127.0.0.1:5000/reserve_spot', {
      user_id: userId,
      parking_lot_id: selectedLot.value.id,
      vehicle_no: vehicleNo.value
    });

    alert(data.message);
    bootstrap.Modal.getInstance(document.getElementById('bookModal'))?.hide();
    performSearch(); 
  } catch (error) {
    alert(error.response?.data?.message || 'Booking failed');
  }
};
const reservations = ref([]);


const fetchReservations = async () => {
  const userId = route.params.id;
  try {
    const { data } = await axios.get(`http://127.0.0.1:5000/get_reservations/${userId}`);
    reservations.value = data;
  } catch (error) {
    console.error('Failed to fetch reservations:', error);
    alert('Could not load reservation history.');
  }
};

onMounted(() => {
  fetchReservations();
});


const modalData = ref({
  id: null,
  vehicle_no: '',
  start_date: '',
  start_time: '',
  parking_lot_name: '',
  parking_spot_id: null,
  cost: 0
});
const prepareRelease = async (reservation) => {
  try {
    const { data } = await axios.get(`http://127.0.0.1:5000/api/reservations/${reservation.id}`);
    
    modalData.value = {
      id: data.id,
      vehicle_no: data.vehicle_no,
      start_date: data.start_date,
      start_time: data.start_time || '--:--', 
      parking_lot_name: data.parking_lot_name,
      parking_spot_id: data.parking_spot_id,
      cost: data.cost || 0
    };

    
    const modal = new bootstrap.Modal(document.getElementById('releaseModal'));
    modal.show();
  } catch (error) {
    console.error('Failed to fetch reservation:', error);
    alert('Failed to load reservation info.');
  }
};
const releaseReservation = async () => {
  try {
    const payload = {
      reserve_id: modalData.value.id,
      spot_id: modalData.value.parking_spot_id
    };

    const { data } = await axios.post('http://127.0.0.1:5000/release_spot', payload);

    alert(data.message);
    bootstrap.Modal.getInstance(document.getElementById('releaseModal'))?.hide();

    modalData.value = {}; 
    fetchReservations();  
  } catch (error) {
    console.error('Error releasing spot:', error);
    alert(error.response?.data?.message || 'Failed to release spot.');
  }
};



</script>


