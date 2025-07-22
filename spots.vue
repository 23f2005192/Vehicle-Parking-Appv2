<template>
  <div class="container">
    <h2 class="mb-4">Parking Lot: {{ lot?.name || 'Loading...' }}</h2>

    <div v-if="lot">
      <div class="row row-cols-6 row-cols-sm-7 row-cols-md-8 row-cols-lg-9 g-3">
        <div v-for="spot in lot.spots" :key="spot.id" class="col">
          <div
            class="card text-center shadow-sm h-100 "
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
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

export default {
  name: 'SpotsPage',
  setup() {
    const lot = ref(null)
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

    return { lot }
  }
}
</script>
