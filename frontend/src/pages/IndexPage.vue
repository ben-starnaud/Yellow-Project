<template>
  <q-page class="q-pa-md q-pa-sm-xl bg-grey-1">
    <div class="text-center q-mb-xl">
      <h2 class="text-h3 text-weight-bolder text-secondary q-mb-sm">Smartphone Financing</h2>
      <p class="text-subtitle1 text-grey-7">Choose a device and check your daily rate.</p>
    </div>

    <div v-if="loading" class="flex flex-center q-pa-xl">
      <q-spinner-tail color="primary" size="5em" />
    </div>

    <div v-else class="row q-col-gutter-lg justify-center">
      <div v-for="p in products" :key="p.id" class="col-12 col-sm-6 col-md-4">
        <ProductCard :product="p" @apply="openWizard" />
      </div>
    </div>

    <ApplicationWizard 
      v-if="selectedProduct" 
      v-model="showWizard" 
      :product="selectedProduct" 
    />
  </q-page>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { productService } from 'src/services/productService'
import ProductCard from 'src/components/ProductCard.vue'
import ApplicationWizard from 'src/components/ApplicationWizard.vue'

const products = ref([])
const loading = ref(true)
const showWizard = ref(false)
const selectedProduct = ref(null)

const openWizard = (product) => {
  selectedProduct.value = product
  showWizard.value = true
}

onMounted(async () => {
  products.value = await productService.getProducts()
  loading.value = false
})
</script>