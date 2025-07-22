<template>
  <div class="container mt-5">
    <h1 class="text-center mb-4">{{ message }}</h1>

    
    <div class="mb-3 d-flex justify-content-between align-items-center">
      <button
        v-if="currentView === 'admin'"
        class="btn btn-primary"
        @click="openAddForm"
      >
        Add Parking Lot
      </button>

      <div>
        <button
          class="btn btn-secondary me-2"
          :class="{ active: currentView === 'admin' }"
          @click="goToAdmin"
        >
          Admin Page
        </button>
        <button
          class="btn btn-secondary"
          :class="{ active: currentView === 'users' }"
          @click="fetchUsers"
        >
          Users
        </button>
      </div>
    </div>

    
    <div v-if="currentView === 'admin'">
      <div
        v-if="parkingLots.length === 0"
        class="d-flex justify-content-center align-items-center flex-column"
        style="height: 200px;"
      >
        <p class="text-light">No parking lots available yet.</p>
      </div>

      <div class="modal fade show d-block" tabindex="-1" role="dialog" v-if="showForm">
        <div class="modal-dialog" role="document">
          <div class="modal-content">
            <form @submit.prevent="submitForm">
              <div class="modal-header">
                <h5 class="modal-title text-dark">
                  {{ isEditMode ? 'Edit Parking Lot' : 'Add New Parking Lot' }}
                </h5>
                <button type="button" class="btn-close" @click="closeForm"></button>
              </div>
              <div class="modal-body">
                <div class="mb-3">
                  <input
                    v-model="form.name"
                    class="form-control"
                    placeholder="Name"
                    required
                  />
                </div>
                <div class="mb-3">
                  <input
                    v-model.number="form.price"
                    class="form-control"
                    placeholder="Price"
                    type="number"
                    required
                  />
                </div>
                <div class="mb-3">
                  <input
                    v-model="form.address"
                    class="form-control"
                    placeholder="Address"
                    required
                  />
                </div>
                <div class="mb-3">
                  <input
                    v-model.number="form.pincode"
                    class="form-control"
                    placeholder="Pincode"
                    type="number"
                    required
                  />
                </div>
                <div class="mb-3">
                  <input
                    v-model.number="form.spots"
                    class="form-control"
                    placeholder="Spots"
                    type="number"
                    required
                  />
                </div>
                <div v-if="errorMsg" class="alert alert-danger">{{ errorMsg }}</div>
              </div>
              <div class="modal-footer">
                <button type="submit" class="btn btn-success">Submit</button>
                <button type="button" class="btn btn-secondary" @click="closeForm">Cancel</button>
              </div>
            </form>
          </div>
        </div>
      </div>

      
      <div v-if="parkingLots.length > 0" class="table-responsive">
        <h3>Available Parking Lots</h3>
        <table class="table table-striped">
          <thead class="table-dark">
            <tr>
              <th>Name</th>
              <th>Price</th>
              <th>Address</th>
              <th>Pincode</th>
              <th>Spots</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="lot in parkingLots" :key="lot.id">
              <td>{{ lot.name }}</td>
              <td>{{ lot.price }}</td>
              <td>{{ lot.address }}</td>
              <td>{{ lot.pincode }}</td>
              <td>
                <button class="btn btn-outline-info btn-sm" @click="viewSpots(lot.id)">
                  {{ lot.spots }} Spots
                </button>
              </td>
              <td>
                <button class="btn btn-sm btn-warning" @click="openEditForm(lot)">Edit</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    
    <div v-if="currentView === 'users' && users.length > 0" class="table-responsive mt-4">
      <h3>User Details</h3>
      <table class="table table-bordered">
        <thead class="table-dark">
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Address</th>
            <th>Phone Number</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>{{ user.id }}</td>
            <td>{{ user.name }}</td>
            <td>{{ user.address }}</td>
            <td>{{ user.phonenumber }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const message = 'Hello, Admin'

const currentView = ref('admin') 
const showForm = ref(false)
const isEditMode = ref(false)
const editId = ref(null)
const errorMsg = ref('')
const parkingLots = ref([])

const form = ref({
  name: '',
  price: 0,
  address: '',
  pincode: '',
  spots: 1
})

const users = ref([])


const fetchParkingLots = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:5000/get_parkinglots')
    parkingLots.value = response.data
  } catch (error) {
    console.error('Error fetching lots:', error)
  }
}


const fetchUsers = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:5000/get_enrolled_users')
    users.value = response.data
    currentView.value = 'users'
  } catch (error) {
    console.error('Error fetching users:', error)
  }
}


const goToAdmin = async () => {
  await fetchParkingLots()
  currentView.value = 'admin'
}

const openAddForm = () => {
  isEditMode.value = false
  form.value = { name: '', price: 0, address: '', pincode: '', spots: 1 }
  showForm.value = true
}

const openEditForm = (lot) => {
  isEditMode.value = true
  editId.value = lot.id
  form.value = { ...lot }
  showForm.value = true
}

const closeForm = () => {
  showForm.value = false
  errorMsg.value = ''
}

const submitForm = async () => {
  errorMsg.value = ''
  if (form.value.spots <= 0) {
    errorMsg.value = 'There must be at least one spot'
    return
  }

  try {
    if (isEditMode.value) {
      await axios.put(`http://127.0.0.1:5000/parkinglot/${editId.value}`, form.value)
    } else {
      await axios.post('http://127.0.0.1:5000/parkinglot', form.value)
    }

    closeForm()
    await fetchParkingLots()
  } catch (err) {
    errorMsg.value = err.response?.data?.error || 'Failed to save parking lot'
  }
}

const viewSpots = (lotId) => {
  window.location.href = `/spots/${lotId}`
}

onMounted(fetchParkingLots)
</script>


