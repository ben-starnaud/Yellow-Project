<template>
  <q-dialog v-model="internalModel" persistent maximized-xs transition-show="slide-up">
    <q-card :style="$q.screen.gt.xs ? 'min-width: 500px; border-radius: 15px' : ''">
      <q-card-section class="row items-center q-pb-none">
        <div class="text-h6 text-weight-bold">{{ wizardTitle }}</div>
        <q-space />
        <q-btn icon="close" flat round dense v-close-popup @click="resetWizard" />
      </q-card-section>

      <q-card-section class="q-pa-md">
        <q-form v-if="step === 'info'" @submit="handleEligibility" class="q-gutter-y-md">
          <div class="text-subtitle2 text-grey-7 q-mb-sm">
            Please provide your details to calculate your rate.
          </div>
          
          <q-input 
            v-model="form.full_name" 
            label="Full Name" 
            filled 
            color="secondary"
            :rules="[val => !!val || 'Full name is required']" 
          />
          
          <q-input 
            v-model="form.id_number" 
            label="SA ID Number" 
            mask="#############" 
            filled 
            color="secondary"
            hint="Must be 18-65 years old"
            :rules="[validateSAID]" 
          />

          <q-input 
            v-model.number="form.monthly_income" 
            label="Monthly Income (R)" 
            type="number" 
            filled 
            color="secondary"
            :rules="[val => !!val || 'Income is required']" 
          />
          
          <q-file 
            v-model="form.proof_of_income" 
            label="Upload Supporting Proof Document" 
            filled 
            color="secondary"
            :rules="[val => !!val || 'Document is required']"
          >
            <template v-slot:prepend><q-icon name="attach_file" /></template>
          </q-file>

          <div class="row justify-center q-mt-lg">
            <q-btn 
              label="Get My Personalized Rate" 
              type="submit" 
              color="primary" 
              text-color="secondary" 
              class="full-width q-py-md text-weight-bolder rounded-lg"
              unelevated
            />
          </div>
        </q-form>

        <div v-else-if="step === 'quote'" class="text-center">
          <q-icon name="payments" color="primary" size="3rem" class="q-mb-md" />
          <div class="text-subtitle1 text-grey-8">Great news, {{ form.full_name.split(' ')[0] }}!</div>
          <div class="text-h3 text-weight-bolder text-secondary">R{{ quote.daily_payment }}</div>
          <div class="text-caption text-grey-6 q-mb-lg text-weight-bold">Daily payment for 360 days (1 Year)</div>

          <q-list bordered separator class="rounded-borders q-mb-lg text-left">
            <q-item>
              <q-item-section class="text-grey-7">Original Cash Price</q-item-section>
              <q-item-section side class="text-weight-bold">R{{ parseFloat(product.base_cash_price).toFixed(2) }}</q-item-section>
            </q-item>

            <q-item>
              <q-item-section class="text-grey-7">Amount to be Financed</q-item-section>
              <q-item-section side class="text-weight-bold">R{{ parseFloat(quote.loan_principal).toFixed(2) }}</q-item-section>
            </q-item>

            <q-item>
              <q-item-section class="text-grey-7">Annual Interest Rate</q-item-section>
              <q-item-section side class="text-weight-bold text-negative">
                {{ (parseFloat(quote.final_interest_rate) * 100).toFixed(0) }}%
              </q-item-section>
            </q-item>

            <q-item>
              <q-item-section class="text-grey-7">Total Cost of Loan</q-item-section>
              <q-item-section side class="text-weight-bold">
                R{{ (parseFloat(quote.daily_payment) * 360).toFixed(2) }}
              </q-item-section>
            </q-item>

            <q-item class="bg-grey-2">
              <q-item-section class="text-weight-bolder text-secondary">Final Total Cost</q-item-section>
              <q-item-section side class="text-weight-bolder text-primary text-h6">
                R{{ parseFloat(quote.final_cash_price).toFixed(2) }}
              </q-item-section>
            </q-item>
          </q-list>

          <div class="row q-col-gutter-sm">
            <div class="col-6">
              <q-btn outline color="secondary" label="Back" class="full-width q-py-sm rounded-lg" @click="step = 'info'" />
            </div>
            <div class="col-6">
              <q-btn 
                color="primary" 
                text-color="secondary" 
                label="Confirm & Submit" 
                class="full-width q-py-sm text-weight-bolder rounded-lg" 
                :loading="submitting" 
                @click="finalSubmit" 
              />
            </div>
          </div>
        </div>

        <div v-else class="text-center q-pa-xl">
          <q-icon name="check_circle" color="positive" size="5rem" />
          <div class="text-h5 text-weight-bold q-mt-md text-secondary">Application Submitted!</div>
          <p class="text-grey-7 q-mt-sm">Thank you for choosing Yellow. Our team will contact you shortly to finalize your delivery.</p>
          <q-btn label="Back to Shop" color="secondary" class="q-mt-md full-width rounded-lg" v-close-popup @click="resetWizard" />
        </div>
      </q-card-section>
    </q-card>
  </q-dialog>
</template>

<script setup>
import { ref, computed } from 'vue'
import { applicationService } from 'src/services/applicationService'

const props = defineProps(['modelValue', 'product'])
const emit = defineEmits(['update:modelValue'])

const internalModel = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val)
})

const step = ref('info')
const submitting = ref(false)
const quote = ref(null)
const form = ref({
  full_name: '',
  id_number: '',
  monthly_income: null,
  proof_of_income: null
})

const wizardTitle = computed(() => {
  if (step.value === 'info') return `Apply for ${props.product?.model_name}`
  if (step.value === 'quote') return 'Your Financing Offer'
  return 'Success'
})

const handleEligibility = () => {
  const yearDigits = parseInt(form.value.id_number.substring(0, 2))
  const currentYear = new Date().getFullYear() % 100
  const fullYear = yearDigits <= currentYear ? 2000 + yearDigits : 1900 + yearDigits
  const age = new Date().getFullYear() - fullYear
  
  let riskKey = "1"
  if (age >= 31 && age <= 50) riskKey = "2"
  else if (age > 50) riskKey = "3"

  if (props.product.pricing_tiers && props.product.pricing_tiers[riskKey]) {
    quote.value = props.product.pricing_tiers[riskKey]
    step.value = 'quote'
  }
}

const finalSubmit = async () => {
  submitting.value = true
  try {
    const payload = { ...form.value, phone_id: props.product.id }
    await applicationService.submitApplication(payload)
    step.value = 'success'
  } catch (err) {
    console.error("Submission error:", err)
  } finally {
    submitting.value = false
  }
}

const resetWizard = () => {
  setTimeout(() => {
    step.value = 'info'
    form.value = { full_name: '', id_number: '', monthly_income: null, proof_of_income: null }
  }, 300)
}


const validateSAID = async (val) => {
  // 1. Basic length check
  if (!val || val.length !== 13) return 'SA ID must be 13 digits'

  // 2. Luhn Algorithm (Mathematical Check)
  let nCheck = 0
  let bEven = false
  for (let n = val.length - 1; n >= 0; n--) {
    let nDigit = parseInt(val.charAt(n), 10)
    if (bEven && (nDigit *= 2) > 9) nDigit -= 9
    nCheck += nDigit
    bEven = !bEven
  }
  if ((nCheck % 10) !== 0) return 'Invalid ID checksum'

  // 3. Age Check 
  const yearDigits = parseInt(val.substring(0, 2))
  const currentYear = new Date().getFullYear() % 100
  const fullYear = yearDigits <= currentYear ? 2000 + yearDigits : 1900 + yearDigits
  const age = new Date().getFullYear() - fullYear
  if (age < 18 || age > 65) return 'Age must be 18-65'

  // 4. Remote Uniqueness Check 
  try {
    const data = await applicationService.checkIdStatus(val)
    if (data.exists) return 'An application with this ID already exists'
  } catch (err) {
    console.error("ID uniqueness check failed", err)
  }

  return true
}
</script>

<style scoped>
.rounded-lg { border-radius: 12px; }
.rounded-borders { border-radius: 12px; }
</style>