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
    const route = useRoute()
    const lotId = route.params.lotId

    onMounted(async () => {
      try {
        const res = await axios.get(`http://127.0.0.1:5000/parkinglot/${lotId}/spots`)
        lot.value = res.data.lot
      } catch (error) {
        console.error("Error fetching lot:", error)
      }
    })

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

    return {
      lot,
      currentPage,
      totalPages,
      paginatedSpots,
      nextPage,
      prevPage
    }
  }
}
</script>

