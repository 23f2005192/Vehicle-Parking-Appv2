<template>
  <div class="container mt-5">
    <h1 class="text-center mb-4">{{ message }}</h1>
<nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm">
  <div class="container-fluid">
   
    <div class="d-flex gap-3">
      <button
        class="btn btn-outline-primary"
        :class="{ active: currentView === 'admin' }"
        @click="goToAdmin"
      >
        Admin Page
      </button>
      <button
        class="btn btn-outline-primary"
        :class="{ active: currentView === 'users' }"
        @click="fetchUsers"
      >
        Users
      </button>
      <button
        class="btn btn-outline-primary"
        :class="{ active: currentView === 'summary' }"
        @click="goToSummary"
      >
        Summary
      </button>
    </div>

    <div class="d-flex gap-3 align-items-center">
      <button
        v-if="currentView === 'admin'"
        class="btn btn-primary"
        @click="openAddForm"
      >
        Add Parking Lot
      </button>

      <button
        class="btn btn-outline-danger"
        @click="logout"
      >
        Logout
      </button>
    </div>
  </div>
</nav>


    <div v-if="currentView === 'admin'">
      <div v-if="parkingLots.length === 0" class="d-flex justify-content-center align-items-center flex-column" style="height: 200px;">
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
                  <input v-model="form.name" class="form-control" placeholder="Name" required />
                </div>
                <div class="mb-3">
                  <input v-model.number="form.price" class="form-control" placeholder="Price" type="number" required />
                </div>
                <div class="mb-3">
                  <input v-model="form.address" class="form-control" placeholder="Address" required />
                </div>
                <div class="mb-3">
                  <input v-model.number="form.pincode" class="form-control" placeholder="Pincode" type="number" required />
                </div>
                <div class="mb-3">
                  <input v-model.number="form.spots" class="form-control" placeholder="Spots" type="number" min="1"  required />
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
            <tr v-for="lot in paginatedParkingLots" :key="lot.id">
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

  
        <nav class="mt-3 d-flex justify-content-center" v-if="totalPages > 1">
          <ul class="pagination">
            <li class="page-item" :class="{ disabled: currentPage === 1 }">
              <button class="page-link" @click="currentPage--" :disabled="currentPage === 1">Previous</button>
            </li>
            <li
              v-for="page in totalPages"
              :key="page"
              class="page-item"
              :class="{ active: currentPage === page }"
            >
              <button class="page-link" @click="currentPage = page">{{ page }}</button>
            </li>
            <li class="page-item" :class="{ disabled: currentPage === totalPages }">
              <button class="page-link" @click="currentPage++" :disabled="currentPage === totalPages">Next</button>
            </li>
          </ul>
        </nav>
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
          <tr v-for="user in paginatedUsers" :key="user.id">
            <td>{{ user.id }}</td>
            <td>{{ user.name }}</td>
            <td>{{ user.address }}</td>
            <td>{{ user.phonenumber }}</td>
          </tr>
        </tbody>
      </table>

      <nav class="mt-3 d-flex justify-content-center" v-if="totalUserPages > 1">
        <ul class="pagination">
          <li class="page-item" :class="{ disabled: currentUserPage === 1 }">
            <button class="page-link" @click="currentUserPage--" :disabled="currentUserPage === 1">Previous</button>
          </li>
          <li
            v-for="page in totalUserPages"
            :key="page"
            class="page-item"
            :class="{ active: currentUserPage === page }"
          >
            <button class="page-link" @click="currentUserPage = page">{{ page }}</button>
          </li>
          <li class="page-item" :class="{ disabled: currentUserPage === totalUserPages }">
            <button class="page-link" @click="currentUserPage++" :disabled="currentUserPage === totalUserPages">Next</button>
          </li>
        </ul>
      </nav>
    </div>


    <div v-if="currentView === 'summary'" class="mt-4">
      <h3>Revenue Summary by Parking Lot</h3>
      <canvas id="summaryChart"></canvas>
    </div>
  </div>
</template>
<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import Chart from 'chart.js/auto'

const message = 'Hello, Admin'

const currentView = ref('admin')
const showForm = ref(false)
const isEditMode = ref(false)
const editId = ref(null)
const errorMsg = ref('')

const parkingLots = ref([])
const users = ref([])

const form = ref({
  name: '',
  price: 0,
  address: '',
  pincode: '',
  spots: 1
})

const fetchParkingLots = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:5000/get_parkinglots')
    parkingLots.value = response.data
    currentPage.value = 1
  } catch (error) {
    console.error('Error fetching lots:', error)
  }
}

const fetchUsers = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:5000/get_enrolled_users')
    users.value = response.data
    currentUserPage.value = 1
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
  if (form.value.spots <= 0 ) {
    errorMsg.value = 'Spots must be greater than one'
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

const logout = () => {
  window.location.href = '/'
}

onMounted(fetchParkingLots)


const currentPage = ref(1)
const itemsPerPage = 7
const paginatedParkingLots = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  return parkingLots.value.slice(start, start + itemsPerPage)
})
const totalPages = computed(() => Math.ceil(parkingLots.value.length / itemsPerPage))


const currentUserPage = ref(1)
const usersPerPage = 7
const paginatedUsers = computed(() => {
  const start = (currentUserPage.value - 1) * usersPerPage
  return users.value.slice(start, start + usersPerPage)
})
const totalUserPages = computed(() => Math.ceil(users.value.length / usersPerPage))

// Summary View
const summaryChart = ref(null)
const summaryData = ref([])

const goToSummary = async () => {
  currentView.value = 'summary'
  await fetchSummaryData()
  renderChart()
}

const fetchSummaryData = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:5000/summary')
    summaryData.value = response.data
  } catch (error) {
    console.error('Error fetching summary:', error)
  }
}

const renderChart = () => {
  if (summaryChart.value) {
    summaryChart.value.destroy()
  }

  const ctx = document.getElementById('summaryChart')
  const labels = summaryData.value.map(item => item.name)
  const data = summaryData.value.map(item => item.total_cost)

  summaryChart.value = new Chart(ctx, {
    type: 'bar',
    data: {
      labels,
      datasets: [{
        label: 'Total Revenue (₹)',
        data,
        backgroundColor: 'rgba(54, 162, 235, 0.6)',
        borderColor: 'rgba(54, 162, 235, 1)',
        borderWidth: 0.5,
      
        barThickness: 20 
      }]
    },
    options: {
      responsive: true,
      scales: {
        y: { beginAtZero: true }
      }
    }
  })
}
</script>
