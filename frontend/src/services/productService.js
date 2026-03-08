import { api } from 'boot/axios'

export const productService = {
  async getProducts() {
    const response = await api.get('/products/list-products')
    return response.data
  }
}