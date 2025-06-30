<template>
  <div class="container mt-4">
    <h2 class="mb-4">Parking Lot: {{ lot?.name || 'Loading...' }}</h2>

    <div v-if="lot">
      <div class="row row-cols-2 row-cols-sm-3 row-cols-md-4 row-cols-lg-5 g-3">
        <div v-for="spot in lot.spots" :key="spot" class="col">
          <div class="card text-center shadow-sm h-100">
            <div class="card-body">
              <h5 class="card-title">Spot {{ spot }}</h5>
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
        const res = await axios.get(`http://localhost:5000/parkinglot/${lotId}/spots`)
        lot.value = res.data.lot
      } catch (error) {
        console.error("Error fetching lot:", error)
      }
    })

    return { lot }
  }
}
</script>
