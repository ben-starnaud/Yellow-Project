<template>
  <q-card class="product-card no-shadow border-primary full-height column">
    <div class="q-pa-md bg-white flex flex-center" style="height: 200px;">
      <q-img 
        :src="product.model_image" 
        fit="contain" 
        class="full-height"
        spinner-color="primary"
      >
        <template v-slot:error>
          <div class="absolute-full flex flex-center bg-grey-3 text-grey-7">
            No Image
          </div>
        </template>
      </q-img>
    </div>
    
    <q-card-section class="col">
      <div class="text-overline text-primary text-weight-bold">
        {{ product.brand }}
      </div>
      <div class="text-h5 text-weight-bold text-secondary q-mb-sm">
        {{ product.model_name }}
      </div>
      
      <div class="bg-secondary text-white q-pa-md rounded-borders">
        <div class="row items-center justify-between">
          <div class="column">
            <span class="text-caption text-grey-5">Starting from</span>
            <span class="text-h6 text-primary text-weight-bolder">
              R{{ lowestPrice }}
            </span>
          </div>
          <div class="text-right">
            <q-badge outline color="primary" label="Daily" />
          </div>
        </div>
      </div>
    </q-card-section>

    <q-card-actions class="q-px-md q-pb-md">
      <q-btn
        unelevated
        color="primary"
        text-color="secondary"
        label="Check Eligibility"
        class="text-weight-bolder full-width q-py-sm rounded-lg"
        @click="$emit('apply', product)"
      />
    </q-card-actions>
  </q-card>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  product: { type: Object, required: true }
})

defineEmits(['apply'])

const lowestPrice = computed(() => {
  if (!props.product || !props.product.pricing_tiers) return '0.00'
  
  // Access key "3" (Risk Group 3) directly from the Object
  const tiers = props.product.pricing_tiers
  const tier3 = tiers["3"] || tiers["1"]
  
  return tier3 ? tier3.daily_payment : '0.00'
})
</script>

<style lang="scss" scoped>
.product-card {
  border-radius: 20px;
  border: 2px solid $primary;
  transition: all 0.3s ease;
  background: white;

  &:hover {
    transform: translateY(-8px);
    box-shadow: 0 12px 20px rgba(0, 0, 0, 0.1);
  }
}
.rounded-lg { border-radius: 12px; }
.rounded-borders { border-radius: 12px; }
</style>