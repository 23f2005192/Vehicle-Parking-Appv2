<template>
  <div class="container">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>Parking Lot: {{ lot?.name || 'Loading...' }}</h2>
      <div v-if="lot && totalPages > 1">
        <button @click="prevPage" :disabled="currentPage === 1" class="btn btn-outline-primary me-2">
          Prev
        </button>
        <button @click="nextPage" :disabled="currentPage === totalPages" class="btn btn-outline-primary">
          Next
        </button>
      </div>
    </div>

    <div v-if="lot">
      <div class="row row-cols-6 row-cols-sm-7 row-cols-md-8 row-cols-lg-9 g-3">
        <div
          v-for="spot in paginatedSpots"
          :key="spot.id"
          class="col"
        >
          <div
            class="card text-center shadow-sm h-100"
            :class="spot.status === 'F' ? 'bg-success text-white' : 'bg-danger text-white'"
            @click="handleSpotClick(spot)"
          >
            <div class="card-body">
              <h5 class="card-title">Spot {{ spot.spot_number }}</h5>
              <p class="card-text">
                {{ spot.status === 'F' ? 'Available' : 'Occupied' }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-else>
      <p>Loading parking lot info...</p>
    </div>

    
    <div class="modal fade" id="spotModal" tabindex="-1" aria-labelledby="spotModalLabel" aria-hidden="true" >
      <div class="modal-dialog">
        <div class="modal-content  text-dark">
          <div class="modal-header">
            <h5 class="modal-title" id="spotModalLabel">
              {{ selectedSpot?.status === 'F' ? `Delete Spot ${selectedSpot?.spot_number}` : 'Reservation Details' }}
            </h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>

          <div class="modal-body">
           
            <template v-if="selectedSpot?.status !== 'F' && selectedSpot?.reservation">
              <p><strong>Reserved by:</strong> {{ selectedSpot.reservation.user_name }}</p>
              <p><strong>Vehicle No:</strong> {{ selectedSpot.reservation.vehicle_no }}</p>
              <p><strong>From:</strong> {{ selectedSpot.reservation.startdate }} {{ selectedSpot.reservation.starttime }}</p>
              <p><strong>To:</strong> {{ selectedSpot.reservation.enddate }} {{ selectedSpot.reservation.endtime }}</p>
              <p><strong>Cost:</strong> ₹{{ selectedSpot.reservation.cost }}</p>
            </template>

   
            <template v-else>
              <p>Are you sure you want to delete <strong>Spot {{ selectedSpot?.spot_number }}</strong>?</p>
            </template>
          </div>

          <div class="modal-footer">
        
            <template v-if="selectedSpot?.status === 'F'">
              <button type="button" class="btn btn-danger" @click="confirmDelete">Delete</button>
            </template>
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

export default {
  name: 'SpotsPage',
  setup() {
    const lot = ref(null)
    const currentPage = ref(1)
    const spotsPerPage = 36
    const selectedSpot = ref(null)
    const modalInstance = ref(null)
    const route = useRoute()
    const lotId = route.params.lotId

    onMounted(async () => {
      await fetchLotData()
    })

    const fetchLotData = async () => {
      try {
        const res = await axios.get(`http://127.0.0.1:5000/parkinglot/${lotId}/spots`)
        lot.value = res.data.lot
      } catch (error) {
        console.error("Error fetching lot:", error)
      }
    }

    const totalPages = computed(() => {
      return lot.value ? Math.ceil(lot.value.spots.length / spotsPerPage) : 1
    })

    const paginatedSpots = computed(() => {
      if (!lot.value) return []
      const start = (currentPage.value - 1) * spotsPerPage
      const end = start + spotsPerPage
      return lot.value.spots.slice(start, end)
    })

    const nextPage = () => {
      if (currentPage.value < totalPages.value) {
        currentPage.value++
      }
    }

    const prevPage = () => {
      if (currentPage.value > 1) {
        currentPage.value--
      }
    }

    const handleSpotClick = (spot) => {
      selectedSpot.value = spot
      if (!modalInstance.value) {
        modalInstance.value = new bootstrap.Modal(document.getElementById('spotModal'))
      }
      modalInstance.value.show()
    }

    const confirmDelete = async () => {
      try {
        await axios.delete(`http://127.0.0.1:5000/spots/${selectedSpot.value.id}`)
        alert(`Spot ${selectedSpot.value.spot_number} deleted.`)
        await fetchLotData()
        modalInstance.value.hide()
      } catch (error) {
        alert("Error deleting spot: " + error)
      }
    }

    return {
      lot,
      currentPage,
      totalPages,
      paginatedSpots,
      nextPage,
      prevPage,
      handleSpotClick,
      confirmDelete,
      selectedSpot
    }
  }
}
</script>
