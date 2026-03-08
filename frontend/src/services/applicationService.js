import { api } from 'boot/axios'

export const applicationService = {

  async checkIdStatus(idNumber) {
    const response = await api.get(`/applications/check-id/${idNumber}`)
    return response.data // Returns { exists: true/false }
  },
  
  async submitApplication(payload) {
    const formData = new FormData()
    
    // Append text fields
    formData.append('full_name', payload.full_name)
    formData.append('id_number', payload.id_number)
    formData.append('monthly_income', payload.monthly_income)
    formData.append('phone_id', payload.phone_id)
    
    // Append the actual file object
    formData.append('proof_of_income', payload.proof_of_income)

    const response = await api.post('/applications/apply', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    return response.data
  }
}