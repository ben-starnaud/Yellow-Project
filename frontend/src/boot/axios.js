import { boot } from 'quasar/wrappers'
import axios from 'axios' 

const api = axios.create({ baseURL: process.env.API_URL  || 'http://localhost:8000' })

export default boot(({ app }) => {
  app.config.globalProperties.$api = api
  app.config.globalProperties.$axios = axios
})

export { api }

